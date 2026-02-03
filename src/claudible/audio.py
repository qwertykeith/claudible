"""Sound engine for procedural audio generation."""

import numpy as np
import sounddevice as sd
from typing import Optional
import threading

try:
    from scipy.signal import butter, lfilter
    _HAS_SCIPY = True
except ImportError:
    _HAS_SCIPY = False

from .materials import Material, get_random_material


class SoundEngine:
    """Generates and plays procedural sounds based on physical material models."""

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

        # Pre-generate grain variations for efficiency
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

    # --- DSP utilities ---

    def _highpass(self, data: np.ndarray, cutoff: float) -> np.ndarray:
        """High-pass filter. Uses scipy if available, else differentiation."""
        if _HAS_SCIPY:
            nyq = self.SAMPLE_RATE / 2
            norm = min(cutoff / nyq, 0.99)
            if norm <= 0:
                return data
            b, a = butter(2, norm, btype='high')
            return lfilter(b, a, data).astype(np.float32)
        # Fallback: repeated differentiation
        out = np.diff(data, prepend=data[0])
        return np.diff(out, prepend=out[0]).astype(np.float32)

    def _lowpass(self, data: np.ndarray, cutoff: float) -> np.ndarray:
        """Low-pass filter. Uses scipy if available, else moving average."""
        if _HAS_SCIPY:
            nyq = self.SAMPLE_RATE / 2
            norm = min(cutoff / nyq, 0.99)
            if norm <= 0:
                return np.zeros_like(data)
            b, a = butter(2, norm, btype='low')
            return lfilter(b, a, data).astype(np.float32)
        # Fallback: simple moving average
        n = max(int(self.SAMPLE_RATE / cutoff / 2), 1)
        kernel = np.ones(n, dtype=np.float32) / n
        return np.convolve(data, kernel, mode='same').astype(np.float32)

    def _apply_reverb(self, signal: np.ndarray, amount: float,
                      room_size: float = 1.0, damping: float = 0.3) -> np.ndarray:
        """Multi-tap reverb with high-frequency damping on later reflections."""
        if amount <= 0:
            return signal
        base_delays_ms = [23, 37, 53, 79, 113, 149]
        out = signal.copy()
        for i, d in enumerate(base_delays_ms):
            delay_samples = int(d * room_size * self.SAMPLE_RATE / 1000)
            if delay_samples >= len(signal) or delay_samples <= 0:
                continue
            tap = np.zeros_like(signal)
            tap[delay_samples:] = signal[:-delay_samples]
            # Damp high frequencies in later reflections
            if i > 1 and damping > 0:
                cutoff = max(4000 - i * 500 * damping, 500)
                tap = self._lowpass(tap, cutoff)
            out += tap * amount * (0.55 ** i)
        return out / max(1.0 + amount * 1.5, 1.0)

    # --- Audio callback ---

    def _audio_callback(self, outdata, frames, time, status):
        """Audio stream callback - mixes queued sounds with background hum."""
        output = np.zeros(frames, dtype=np.float32)

        # Background hum: multiple detuned oscillators with slow wobble
        t = np.arange(frames) / self.SAMPLE_RATE
        phase_inc = 2 * np.pi * 55.0 / self.SAMPLE_RATE * frames
        wobble = 0.002 * np.sin(2 * np.pi * 0.08 * t + self._hum_phase * 0.01)

        for freq, amp in [(55.0, 0.007), (55.15, 0.006), (54.85, 0.006), (110.05, 0.001)]:
            output += amp * np.sin(
                2 * np.pi * freq * (1 + wobble) * t + self._hum_phase * (freq / 55.0)
            ).astype(np.float32)

        self._hum_phase = (self._hum_phase + phase_inc) % (2 * np.pi)

        # Read from ring buffer
        with self._lock:
            for i in range(frames):
                output[i] += self._buffer[self._read_pos]
                self._buffer[self._read_pos] = 0.0
                self._read_pos = (self._read_pos + 1) % self.BUFFER_SIZE

        outdata[:] = (output * self.volume).reshape(-1, 1)

    def _add_to_buffer(self, samples: np.ndarray):
        """Add samples to the ring buffer (mixes with existing)."""
        with self._lock:
            for i, sample in enumerate(samples):
                pos = (self._read_pos + i) % self.BUFFER_SIZE
                self._buffer[pos] += sample

    # --- Sound generation ---

    def _generate_grain(self) -> np.ndarray:
        """Generate a single grain sound from the material's physical model."""
        m = self.material
        # Vary duration per grain
        duration = m.grain_duration * np.random.uniform(0.85, 1.15)
        n = int(duration * self.SAMPLE_RATE)
        t = np.linspace(0, duration, n, dtype=np.float32)

        grain = np.zeros(n, dtype=np.float32)

        # Randomise base frequency within the material's spread
        base_freq = m.base_freq * (2 ** (np.random.uniform(-m.freq_spread, m.freq_spread) / 12))

        # Generate each partial with its own decay, detuning, and random phase
        for i, (ratio, amp) in enumerate(m.partials):
            detune_cents = np.random.uniform(-m.detune_amount, m.detune_amount)
            freq = base_freq * ratio * (2 ** (detune_cents / 1200))
            # Extra micro-variation per partial
            freq *= np.random.uniform(0.997, 1.003)
            phase = np.random.uniform(0, 2 * np.pi)

            decay_rate = m.decay_rates[i] if i < len(m.decay_rates) else m.decay_rates[-1]
            envelope = np.exp(-decay_rate * t)

            grain += amp * envelope * np.sin(2 * np.pi * freq * t + phase)

        # Noise transient (the "tick" of physical impact)
        if m.attack_noise > 0:
            noise = np.random.randn(n).astype(np.float32)
            noise = self._highpass(noise, m.noise_freq)
            # Shape: fast attack, very fast decay with micro-variation
            noise_env = np.exp(-150 * t)
            noise_env *= np.clip(
                1.0 + 0.3 * np.random.randn(n).astype(np.float32) * np.exp(-200 * t),
                0, 1,
            )
            grain += m.attack_noise * 0.3 * noise * noise_env

        # Attack shaping
        attack_samples = max(int(m.attack_ms / 1000 * self.SAMPLE_RATE), 2)
        if attack_samples < n:
            grain[:attack_samples] *= np.linspace(0, 1, attack_samples, dtype=np.float32)

        # Pitch drop envelope (physical: pitch drops as energy dissipates)
        if m.pitch_drop != 1.0:
            pitch_env = np.linspace(1.0, m.pitch_drop, n)
            phase_mod = np.cumsum(pitch_env) / np.sum(pitch_env) * n
            indices = np.clip(phase_mod.astype(int), 0, n - 1)
            grain = grain[indices]

        # Multi-tap reverb with HF damping
        grain = self._apply_reverb(grain, m.reverb_amount, m.room_size, m.reverb_damping)

        # Truncate reverb tail back to grain length
        grain = grain[:n]

        # Normalise with per-material volume
        peak = np.max(np.abs(grain))
        if peak > 0:
            grain = grain / peak * 0.4 * m.volume

        return grain.astype(np.float32)

    def play_grain(self):
        """Play a grain/sparkle sound."""
        # Pick a random cached grain
        idx = np.random.randint(len(self._grain_cache))
        grain = self._grain_cache[idx].copy()

        # Per-play pitch variation via resampling (±4 semitones)
        pitch_shift = 2 ** (np.random.uniform(-4, 4) / 12)
        if abs(pitch_shift - 1.0) > 0.001:
            new_len = int(len(grain) / pitch_shift)
            if new_len > 0:
                grain = np.interp(
                    np.linspace(0, len(grain) - 1, new_len),
                    np.arange(len(grain)),
                    grain,
                ).astype(np.float32)

        # Random amplitude variation
        grain *= np.random.uniform(0.6, 1.0)

        # Regenerate cached grains aggressively for variety
        if np.random.random() < 0.5:
            self._grain_cache[np.random.randint(len(self._grain_cache))] = self._generate_grain()

        self._add_to_buffer(grain)

    def play_chime(self):
        """Play a soft completion chime using the material's tonal character."""
        m = self.material
        duration = 0.35
        n = int(duration * self.SAMPLE_RATE)
        t = np.linspace(0, duration, n, dtype=np.float32)

        chime = np.zeros(n, dtype=np.float32)

        # Use the material's own partials at a lower register for the chime
        base = m.base_freq * 0.5
        for i, (ratio, amp) in enumerate(m.partials[:4]):
            freq = base * ratio * np.random.uniform(0.998, 1.002)
            phase = np.random.uniform(0, 2 * np.pi)
            decay_rate = m.decay_rates[i] if i < len(m.decay_rates) else m.decay_rates[-1]
            # Slower decay for sustained chime
            envelope = np.exp(-decay_rate * 0.25 * t) * np.sin(np.pi * t / duration)
            chime += amp * 0.3 * np.sin(2 * np.pi * freq * t + phase) * envelope

        # Softer noise transient
        if m.attack_noise > 0:
            noise = np.random.randn(n).astype(np.float32)
            noise = self._highpass(noise, m.noise_freq)
            chime += m.attack_noise * 0.15 * noise * np.exp(-50 * t)

        # More reverb for chimes
        chime = self._apply_reverb(
            chime, m.reverb_amount * 1.3,
            room_size=m.room_size * 1.2,
            damping=m.reverb_damping,
        )
        chime = chime[:n]

        peak = np.max(np.abs(chime))
        if peak > 0:
            chime = chime / peak * 0.35 * m.volume

        self._add_to_buffer(chime.astype(np.float32))

    def play_attention(self):
        """Play a gentle attention signal using the material's tonal character."""
        m = self.material
        duration = 0.8
        n = int(duration * self.SAMPLE_RATE)
        t = np.linspace(0, duration, n, dtype=np.float32)

        signal = np.zeros(n, dtype=np.float32)

        # Two-note rising pattern using material's frequency
        note_samples = n // 2
        for i, pitch_mult in enumerate([1.0, 1.25]):  # Root and major third
            start = i * note_samples
            end = start + note_samples
            nt = t[start:end] - t[start]
            freq = m.base_freq * 0.4 * pitch_mult

            envelope = np.sin(np.pi * nt / (duration / 2)) ** 2
            # Use a couple of the material's partials
            for j, (ratio, amp) in enumerate(m.partials[:2]):
                pfreq = freq * ratio * np.random.uniform(0.998, 1.002)
                signal[start:end] += 0.2 * amp * np.sin(
                    2 * np.pi * pfreq * nt + np.random.uniform(0, 2 * np.pi)
                ) * envelope

        # Gentle reverb
        signal = self._apply_reverb(
            signal, m.reverb_amount * 1.5,
            room_size=m.room_size * 1.3,
            damping=m.reverb_damping,
        )
        signal = signal[:n]

        peak = np.max(np.abs(signal))
        if peak > 0:
            signal = signal / peak * 0.3 * m.volume

        self._add_to_buffer(signal.astype(np.float32))
