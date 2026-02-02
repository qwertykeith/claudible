"""Sound engine for procedural audio generation."""

import numpy as np
import sounddevice as sd
from typing import Optional
import threading

from .materials import Material, get_random_material


class SoundEngine:
    """Generates and plays procedural crystal/glass-like sounds."""

    SAMPLE_RATE = 44100
    BUFFER_SIZE = 44100 * 2  # 2 seconds of audio buffer

    def __init__(self, material: Optional[Material] = None, volume: float = 0.5):
        self.material = material or get_random_material()
        self.volume = volume
        self._stream: Optional[sd.OutputStream] = None
        self._running = False
        self._hum_phase = 0.0
        self._lock = threading.Lock()

        # Ring buffer for mixing audio
        self._buffer = np.zeros(self.BUFFER_SIZE, dtype=np.float32)
        self._write_pos = 0
        self._read_pos = 0

        # Pre-generate some grain variations for efficiency
        self._grain_cache = [self._generate_grain() for _ in range(8)]
        self._cache_index = 0

    def start(self):
        """Start the audio output stream."""
        self._running = True
        self._stream = sd.OutputStream(
            samplerate=self.SAMPLE_RATE,
            channels=1,
            callback=self._audio_callback,
            blocksize=1024,
        )
        self._stream.start()

    def stop(self):
        """Stop the audio output stream."""
        self._running = False
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None

    def _audio_callback(self, outdata, frames, time, status):
        """Audio stream callback - mixes queued sounds with background hum."""
        output = np.zeros(frames, dtype=np.float32)

        # Add subtle background hum with beating
        hum_freq1 = 55.0  # Low A
        hum_freq2 = 55.3  # Slightly detuned for beating
        t = np.arange(frames) / self.SAMPLE_RATE
        phase_inc = 2 * np.pi * hum_freq1 / self.SAMPLE_RATE * frames

        hum = 0.008 * np.sin(2 * np.pi * hum_freq1 * t + self._hum_phase)
        hum += 0.008 * np.sin(2 * np.pi * hum_freq2 * t + self._hum_phase * (hum_freq2 / hum_freq1))
        self._hum_phase = (self._hum_phase + phase_inc) % (2 * np.pi)

        output += hum.astype(np.float32)

        # Read from ring buffer
        with self._lock:
            for i in range(frames):
                output[i] += self._buffer[self._read_pos]
                self._buffer[self._read_pos] = 0.0  # Clear after reading
                self._read_pos = (self._read_pos + 1) % self.BUFFER_SIZE

        outdata[:] = (output * self.volume).reshape(-1, 1)

    def _add_to_buffer(self, samples: np.ndarray):
        """Add samples to the ring buffer (mixes with existing)."""
        with self._lock:
            # Write starting from current read position (play immediately)
            for i, sample in enumerate(samples):
                pos = (self._read_pos + i) % self.BUFFER_SIZE
                self._buffer[pos] += sample

    def _generate_grain(self) -> np.ndarray:
        """Generate a single grain/sparkle sound."""
        m = self.material
        duration = m.grain_duration
        samples = int(duration * self.SAMPLE_RATE)
        t = np.linspace(0, duration, samples, dtype=np.float32)

        grain = np.zeros(samples, dtype=np.float32)

        # Generate each partial with its own decay and random phase
        for i, (ratio, amp) in enumerate(m.partials):
            # Apply micro-detuning
            detune_cents = np.random.uniform(-m.detune_amount, m.detune_amount)
            freq = m.base_freq * ratio * (2 ** (detune_cents / 1200))

            # Apply pitch bend if specified
            if m.pitch_bend != 0:
                bend_env = np.linspace(0, m.pitch_bend, samples)
                freq_array = freq * (2 ** (bend_env / 12))
                phase = np.random.uniform(0, 2 * np.pi)
                partial = amp * np.sin(2 * np.pi * np.cumsum(freq_array) / self.SAMPLE_RATE + phase)
            else:
                phase = np.random.uniform(0, 2 * np.pi)
                partial = amp * np.sin(2 * np.pi * freq * t + phase)

            # Apply per-partial decay
            decay_rate = m.decay_rates[i] if i < len(m.decay_rates) else m.decay_rates[-1]
            envelope = np.exp(-decay_rate * t)
            grain += partial * envelope

        # Add high-frequency noise transient on attack
        if m.attack_noise > 0:
            noise = np.random.randn(samples).astype(np.float32)
            # High-pass filter approximation via differentiation
            noise = np.diff(noise, prepend=noise[0])
            noise_env = np.exp(-80 * t)  # Very fast decay
            grain += m.attack_noise * 0.3 * noise * noise_env

        # Apply overall envelope
        attack_samples = int(0.002 * self.SAMPLE_RATE)  # 2ms attack
        if attack_samples > 0 and attack_samples < samples:
            grain[:attack_samples] *= np.linspace(0, 1, attack_samples)

        # Apply simple reverb (comb filter approximation)
        if m.reverb_amount > 0:
            delay_samples = int(0.03 * self.SAMPLE_RATE)  # 30ms delay
            reverb = np.zeros(samples + delay_samples * 3, dtype=np.float32)
            reverb[:samples] = grain
            for i, decay in enumerate([0.4, 0.25, 0.15]):
                offset = delay_samples * (i + 1)
                reverb[offset:offset + samples] += grain * decay * m.reverb_amount
            grain = reverb[:samples]

        # Normalize
        peak = np.max(np.abs(grain))
        if peak > 0:
            grain = grain / peak * 0.4

        return grain

    def play_grain(self):
        """Play a grain/sparkle sound."""
        # Use cached grain with slight variation
        grain = self._grain_cache[self._cache_index].copy()
        self._cache_index = (self._cache_index + 1) % len(self._grain_cache)

        # Add slight pitch variation - regenerate occasionally
        if np.random.random() < 0.3:
            self._grain_cache[self._cache_index] = self._generate_grain()

        self._add_to_buffer(grain)

    def play_chime(self):
        """Play a soft completion chime (longer, more melodic)."""
        m = self.material
        duration = 0.3
        samples = int(duration * self.SAMPLE_RATE)
        t = np.linspace(0, duration, samples, dtype=np.float32)

        chime = np.zeros(samples, dtype=np.float32)

        # Use a harmonically pleasing chord
        chord_ratios = [1.0, 1.5, 2.0]  # Root, fifth, octave
        for ratio in chord_ratios:
            freq = m.base_freq * 0.5 * ratio  # Lower than grains
            phase = np.random.uniform(0, 2 * np.pi)
            envelope = np.exp(-3 * t) * np.sin(np.pi * t / duration)  # Soft attack/decay
            chime += 0.3 * np.sin(2 * np.pi * freq * t + phase) * envelope

        # More reverb for chimes
        delay_samples = int(0.05 * self.SAMPLE_RATE)
        reverb = np.zeros(samples + delay_samples * 4, dtype=np.float32)
        reverb[:samples] = chime
        for i, decay in enumerate([0.5, 0.35, 0.2, 0.1]):
            offset = delay_samples * (i + 1)
            reverb[offset:offset + samples] += chime * decay
        chime = reverb[:samples]

        peak = np.max(np.abs(chime))
        if peak > 0:
            chime = chime / peak * 0.35

        self._add_to_buffer(chime.astype(np.float32))

    def play_attention(self):
        """Play a gentle attention signal."""
        m = self.material
        duration = 0.8
        samples = int(duration * self.SAMPLE_RATE)
        t = np.linspace(0, duration, samples, dtype=np.float32)

        signal = np.zeros(samples, dtype=np.float32)

        # Two-note pattern (rising)
        note_samples = samples // 2
        for i, pitch_mult in enumerate([1.0, 1.25]):  # Root and major third
            start = i * note_samples
            end = start + note_samples
            nt = t[start:end] - t[start]
            freq = m.base_freq * 0.4 * pitch_mult

            envelope = np.sin(np.pi * nt / (duration / 2)) ** 2
            signal[start:end] += 0.25 * np.sin(2 * np.pi * freq * nt) * envelope

        # Gentle reverb
        delay_samples = int(0.08 * self.SAMPLE_RATE)
        reverb = np.zeros(samples + delay_samples * 3, dtype=np.float32)
        reverb[:samples] = signal
        for i, decay in enumerate([0.4, 0.25, 0.15]):
            offset = delay_samples * (i + 1)
            reverb[offset:offset + samples] += signal * decay
        signal = reverb[:samples]

        peak = np.max(np.abs(signal))
        if peak > 0:
            signal = signal / peak * 0.3

        self._add_to_buffer(signal.astype(np.float32))
