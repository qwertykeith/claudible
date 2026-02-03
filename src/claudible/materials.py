"""Material character presets for sound generation."""

from dataclasses import dataclass, field
from typing import List, Tuple
import random


@dataclass
class Material:
    """Defines the sonic character of a material.

    Based on physical vibration properties of real materials.
    """

    name: str
    base_freq: float  # centre frequency in Hz
    partials: List[Tuple[float, float]]  # (ratio, amplitude) pairs
    decay_rates: List[float]  # per-partial exponential decay (higher = faster)
    grain_duration: float  # base grain duration in seconds
    attack_noise: float  # 0-1, amount of noise transient on attack
    noise_freq: float  # high-pass cutoff for noise transient in Hz
    detune_amount: float  # cents of random micro-detuning per partial
    reverb_amount: float  # 0-1 reverb wet amount
    reverb_damping: float  # 0-1 high-frequency damping in reverb tails
    room_size: float  # reverb room size multiplier
    pitch_drop: float  # pitch envelope multiplier (<1 = drops, >1 = rises, 1 = flat)
    attack_ms: float  # attack ramp time in milliseconds
    freq_spread: float  # semitones of random base freq variation per grain
    volume: float  # per-material volume scaling (0-1)
    octave_range: Tuple[int, int]  # (min, max) octave shifts for grain cache
    description: str


DEFAULT_SOUND_SET = "ambient"

# --- Ambient sound set (default) ---
# Throbbing, textured, overtone-rich with percussive attack.
# Close partial pairs create beating/throbbing. High attack noise for punch.
# Kept low — nothing shrill. Dense, gritty texture.

AMBIENT_MATERIALS = {
    "drift": Material(
        name="drift",
        base_freq=95,
        partials=[
            (1.0, 1.0), (1.005, 0.95),  # beating pair ~0.48Hz throb
            (2.0, 0.5), (2.008, 0.45),   # octave beating pair
            (3.01, 0.2), (4.02, 0.1),
        ],
        decay_rates=[3, 3.2, 5, 5.3, 8, 11],
        grain_duration=0.16,
        attack_noise=0.35,
        noise_freq=600,
        detune_amount=12,
        reverb_amount=0.6,
        reverb_damping=0.55,
        room_size=1.8,
        pitch_drop=0.997,
        attack_ms=1.5,
        freq_spread=3.0,
        volume=0.7,
        octave_range=(-3, 0),
        description="Low undulating throb, punchy attack into beating pairs",
    ),

    "tide": Material(
        name="tide",
        base_freq=120,
        partials=[
            (1.0, 1.0), (1.003, 0.92),   # slow beat
            (1.498, 0.55), (1.502, 0.52), # fifth beating pair
            (2.0, 0.35), (3.0, 0.12),
        ],
        decay_rates=[4, 4.1, 6, 6.2, 8, 12],
        grain_duration=0.18,
        attack_noise=0.3,
        noise_freq=500,
        detune_amount=14,
        reverb_amount=0.7,
        reverb_damping=0.5,
        room_size=2.0,
        pitch_drop=0.996,
        attack_ms=1.0,
        freq_spread=4.0,
        volume=0.65,
        octave_range=(-3, 0),
        description="Oceanic wash with percussive bite, wide phase interference",
    ),

    "breath": Material(
        name="breath",
        base_freq=160,
        partials=[
            (1.0, 1.0), (1.006, 0.85),   # beating pair
            (2.01, 0.4), (3.02, 0.15),
        ],
        decay_rates=[5, 5.2, 8, 12],
        grain_duration=0.14,
        attack_noise=0.4,
        noise_freq=900,
        detune_amount=18,
        reverb_amount=0.55,
        reverb_damping=0.6,
        room_size=1.6,
        pitch_drop=0.998,
        attack_ms=1.2,
        freq_spread=5.0,
        volume=0.6,
        octave_range=(-3, 0),
        description="Gritty exhale, noisy attack decaying into warm throb",
    ),

    "haze": Material(
        name="haze",
        base_freq=110,
        partials=[
            (1.0, 1.0), (1.004, 0.9),    # tight beating
            (2.003, 0.6), (2.007, 0.55),  # octave beating
            (3.005, 0.3), (4.01, 0.15),
            (5.02, 0.06),
        ],
        decay_rates=[3.5, 3.7, 5, 5.2, 7, 10, 14],
        grain_duration=0.15,
        attack_noise=0.32,
        noise_freq=550,
        detune_amount=10,
        reverb_amount=0.65,
        reverb_damping=0.6,
        room_size=1.9,
        pitch_drop=0.997,
        attack_ms=1.0,
        freq_spread=3.5,
        volume=0.65,
        octave_range=(-3, 0),
        description="Dense foggy cluster, percussive onset into thick overtone haze",
    ),

    "pulse": Material(
        name="pulse",
        base_freq=80,
        partials=[
            (1.0, 1.0), (1.008, 0.9),    # ~0.64Hz beating = pulsing
            (2.0, 0.55), (2.012, 0.5),    # faster beat in octave
            (3.0, 0.25),
        ],
        decay_rates=[2.5, 2.6, 4, 4.2, 7],
        grain_duration=0.2,
        attack_noise=0.38,
        noise_freq=400,
        detune_amount=8,
        reverb_amount=0.5,
        reverb_damping=0.65,
        room_size=1.5,
        pitch_drop=0.995,
        attack_ms=0.8,
        freq_spread=2.5,
        volume=0.7,
        octave_range=(-3, 0),
        description="Thumpy rhythmic throb, hard attack into hypnotic beating",
    ),

    "glow": Material(
        name="glow",
        base_freq=145,
        partials=[
            (1.0, 1.0), (1.003, 0.88),   # beating pair
            (2.0, 0.6), (3.0, 0.35),
            (4.0, 0.2), (5.0, 0.1),
        ],
        decay_rates=[4, 4.2, 5, 6.5, 8, 11],
        grain_duration=0.13,
        attack_noise=0.28,
        noise_freq=700,
        detune_amount=15,
        reverb_amount=0.55,
        reverb_damping=0.45,
        room_size=1.7,
        pitch_drop=0.998,
        attack_ms=1.5,
        freq_spread=4.0,
        volume=0.65,
        octave_range=(-3, 0),
        description="Warm radiant harmonics, punchy onset with rich overtone bloom",
    ),

    "cloud": Material(
        name="cloud",
        base_freq=190,
        partials=[
            (1.0, 1.0), (1.002, 0.85),
            (1.5, 0.4), (2.0, 0.25),
            (2.5, 0.1),
        ],
        decay_rates=[5, 5.2, 7, 9, 13],
        grain_duration=0.14,
        attack_noise=0.3,
        noise_freq=800,
        detune_amount=16,
        reverb_amount=0.75,
        reverb_damping=0.4,
        room_size=2.2,
        pitch_drop=0.998,
        attack_ms=1.2,
        freq_spread=5.0,
        volume=0.55,
        octave_range=(-3, 0),
        description="Percussive puff into massive diffuse reverb, textured",
    ),

    "murmur": Material(
        name="murmur",
        base_freq=70,
        partials=[
            (1.0, 1.0), (1.006, 0.88),   # low beating
            (2.0, 0.5), (3.0, 0.25),
            (4.01, 0.1),
        ],
        decay_rates=[3, 3.2, 5, 8, 12],
        grain_duration=0.17,
        attack_noise=0.35,
        noise_freq=350,
        detune_amount=12,
        reverb_amount=0.5,
        reverb_damping=0.7,
        room_size=1.4,
        pitch_drop=0.994,
        attack_ms=0.8,
        freq_spread=3.0,
        volume=0.7,
        octave_range=(-3, 0),
        description="Deep rumble thump, heavy attack into warm beating murmur",
    ),

    "shimmer": Material(
        name="shimmer",
        base_freq=260,
        partials=[
            (1.0, 1.0), (1.002, 0.9),    # slow beating
            (2.001, 0.55), (2.003, 0.52), # octave beating
            (3.0, 0.25), (4.0, 0.1),
        ],
        decay_rates=[5, 5.1, 7, 7.2, 10, 14],
        grain_duration=0.11,
        attack_noise=0.25,
        noise_freq=1200,
        detune_amount=10,
        reverb_amount=0.65,
        reverb_damping=0.3,
        room_size=2.0,
        pitch_drop=0.999,
        attack_ms=1.0,
        freq_spread=4.0,
        volume=0.55,
        octave_range=(-3, 0),
        description="Bright-ish tap into shimmering beating overtones",
    ),

    "deep": Material(
        name="deep",
        base_freq=50,
        partials=[
            (1.0, 1.0), (1.01, 0.85),    # ~0.5Hz beating
            (2.0, 0.55), (2.015, 0.5),   # wider octave beat
            (3.0, 0.2),
        ],
        decay_rates=[2, 2.2, 3.5, 3.8, 6],
        grain_duration=0.22,
        attack_noise=0.4,
        noise_freq=250,
        detune_amount=8,
        reverb_amount=0.45,
        reverb_damping=0.8,
        room_size=1.3,
        pitch_drop=0.992,
        attack_ms=0.6,
        freq_spread=2.5,
        volume=0.75,
        octave_range=(-3, 0),
        description="Sub-bass thump, hard hit into very deep slow throb",
    ),

    # --- High register whispers (very quiet, above 3kHz) ---

    "wisp": Material(
        name="wisp",
        base_freq=3200,
        partials=[
            (1.0, 1.0), (1.002, 0.9),    # tight beating
            (2.0, 0.2), (3.01, 0.05),
        ],
        decay_rates=[12, 12.5, 20, 30],
        grain_duration=0.06,
        attack_noise=0.15,
        noise_freq=5000,
        detune_amount=4,
        reverb_amount=0.7,
        reverb_damping=0.2,
        room_size=2.0,
        pitch_drop=1.0,
        attack_ms=2.0,
        freq_spread=2.0,
        volume=0.18,
        octave_range=(-1, 1),
        description="Faint crystalline wisp, barely there",
    ),

    "glint": Material(
        name="glint",
        base_freq=3800,
        partials=[
            (1.0, 1.0), (1.5, 0.4), (2.01, 0.15),
        ],
        decay_rates=[18, 25, 35],
        grain_duration=0.04,
        attack_noise=0.25,
        noise_freq=6000,
        detune_amount=6,
        reverb_amount=0.65,
        reverb_damping=0.15,
        room_size=1.8,
        pitch_drop=0.998,
        attack_ms=0.8,
        freq_spread=3.0,
        volume=0.15,
        octave_range=(-1, 0),
        description="Tiny metallic glint, quiet and sharp",
    ),

    "arc": Material(
        name="arc",
        base_freq=4200,
        partials=[
            (1.0, 1.0), (1.003, 0.85),   # slow beating at high freq
            (1.5, 0.3), (2.0, 0.1),
        ],
        decay_rates=[10, 10.5, 16, 24],
        grain_duration=0.07,
        attack_noise=0.1,
        noise_freq=7000,
        detune_amount=3,
        reverb_amount=0.75,
        reverb_damping=0.1,
        room_size=2.2,
        pitch_drop=1.0,
        attack_ms=3.0,
        freq_spread=1.5,
        volume=0.14,
        octave_range=(-1, 0),
        description="High glass arc, delicate beating shimmer",
    ),

    "spark": Material(
        name="spark",
        base_freq=5000,
        partials=[
            (1.0, 1.0), (1.41, 0.35), (2.0, 0.08),
        ],
        decay_rates=[22, 30, 45],
        grain_duration=0.03,
        attack_noise=0.3,
        noise_freq=8000,
        detune_amount=8,
        reverb_amount=0.6,
        reverb_damping=0.15,
        room_size=1.6,
        pitch_drop=0.996,
        attack_ms=0.5,
        freq_spread=4.0,
        volume=0.12,
        octave_range=(-1, 0),
        description="Tiny electric spark, fast and faint",
    ),

    "dust": Material(
        name="dust",
        base_freq=3500,
        partials=[
            (1.0, 1.0), (1.001, 0.95),   # very tight beating
            (2.003, 0.3), (2.006, 0.28),  # octave beating pair
            (3.0, 0.08),
        ],
        decay_rates=[8, 8.2, 14, 14.5, 22],
        grain_duration=0.08,
        attack_noise=0.12,
        noise_freq=5500,
        detune_amount=5,
        reverb_amount=0.8,
        reverb_damping=0.1,
        room_size=2.4,
        pitch_drop=1.0,
        attack_ms=4.0,
        freq_spread=2.0,
        volume=0.16,
        octave_range=(-1, 0),
        description="Soft high dust motes, floating reverb texture",
    ),
}


# --- Material sound set (percussive, physical) ---
# The original set: crisp, percussive sounds modelled on physical materials.

MATERIAL_MATERIALS = {
    "ice": Material(
        name="ice",
        base_freq=2800,
        partials=[(1.0, 1.0), (2.71, 0.7), (5.13, 0.5), (8.41, 0.3), (12.7, 0.15)],
        decay_rates=[25, 40, 60, 80, 100],
        grain_duration=0.035,
        attack_noise=0.4,
        noise_freq=5000,
        detune_amount=8,
        reverb_amount=0.2,
        reverb_damping=0.3,
        room_size=1.0,
        pitch_drop=0.995,
        attack_ms=0.5,
        freq_spread=4.0,
        volume=0.85,
        octave_range=(-3, 3),
        description="Brittle, very high, fast decay with pitch drop",
    ),

    "glass": Material(
        name="glass",
        base_freq=1200,
        partials=[(1.0, 1.0), (2.32, 0.6), (4.17, 0.35), (6.85, 0.15)],
        decay_rates=[18, 28, 45, 65],
        grain_duration=0.05,
        attack_noise=0.35,
        noise_freq=4000,
        detune_amount=5,
        reverb_amount=0.28,
        reverb_damping=0.3,
        room_size=1.0,
        pitch_drop=1.0,
        attack_ms=0.8,
        freq_spread=3.0,
        volume=0.9,
        octave_range=(-3, 3),
        description="Classic wine glass ping",
    ),

    "crystal": Material(
        name="crystal",
        base_freq=1800,
        partials=[(1.0, 1.0), (1.003, 0.9), (2.41, 0.5), (2.43, 0.45), (4.2, 0.2)],
        decay_rates=[12, 13, 22, 24, 40],
        grain_duration=0.07,
        attack_noise=0.25,
        noise_freq=3500,
        detune_amount=3,
        reverb_amount=0.35,
        reverb_damping=0.25,
        room_size=1.2,
        pitch_drop=1.0,
        attack_ms=1.0,
        freq_spread=2.5,
        volume=0.85,
        octave_range=(-3, 3),
        description="Pure lead crystal with beating from close partial pairs",
    ),

    "ceramic": Material(
        name="ceramic",
        base_freq=600,
        partials=[(1.0, 1.0), (2.15, 0.5), (3.87, 0.35), (5.21, 0.2), (7.43, 0.1)],
        decay_rates=[30, 45, 60, 75, 90],
        grain_duration=0.04,
        attack_noise=0.5,
        noise_freq=2500,
        detune_amount=12,
        reverb_amount=0.22,
        reverb_damping=0.4,
        room_size=0.9,
        pitch_drop=0.998,
        attack_ms=1.2,
        freq_spread=3.5,
        volume=1.0,
        octave_range=(-3, 3),
        description="Duller muted earthenware tap",
    ),

    "bell": Material(
        name="bell",
        base_freq=900,
        partials=[
            (1.0, 1.0), (1.183, 0.8), (1.506, 0.6),
            (2.0, 0.7), (2.514, 0.4), (3.011, 0.25),
        ],
        decay_rates=[10, 12, 15, 14, 20, 28],
        grain_duration=0.08,
        attack_noise=0.2,
        noise_freq=3000,
        detune_amount=6,
        reverb_amount=0.4,
        reverb_damping=0.2,
        room_size=1.3,
        pitch_drop=1.0,
        attack_ms=0.3,
        freq_spread=2.5,
        volume=0.8,
        octave_range=(-3, 3),
        description="Small metallic bell, classic ratios, long ring",
    ),

    "droplet": Material(
        name="droplet",
        base_freq=1400,
        partials=[(1.0, 1.0), (2.8, 0.3), (5.2, 0.1)],
        decay_rates=[35, 50, 70],
        grain_duration=0.03,
        attack_noise=0.15,
        noise_freq=6000,
        detune_amount=4,
        reverb_amount=0.45,
        reverb_damping=0.2,
        room_size=1.0,
        pitch_drop=0.92,
        attack_ms=0.3,
        freq_spread=4.0,
        volume=0.8,
        octave_range=(-3, 3),
        description="Water droplet, pitch bend down, liquid",
    ),

    "click": Material(
        name="click",
        base_freq=3500,
        partials=[(1.0, 1.0), (2.5, 0.3)],
        decay_rates=[40, 60],
        grain_duration=0.02,
        attack_noise=0.7,
        noise_freq=7000,
        detune_amount=15,
        reverb_amount=0.1,
        reverb_damping=0.5,
        room_size=0.5,
        pitch_drop=1.0,
        attack_ms=0.2,
        freq_spread=6.0,
        volume=0.95,
        octave_range=(-3, 3),
        description="Sharp mechanical click, keyboard-like",
    ),

    # --- New materials with distinct textures ---

    "wood": Material(
        name="wood",
        base_freq=420,
        partials=[
            (1.0, 1.0), (2.0, 0.55), (3.0, 0.28),
            (4.01, 0.12), (5.02, 0.05),
        ],
        decay_rates=[22, 32, 45, 55, 70],
        grain_duration=0.04,
        attack_noise=0.45,
        noise_freq=2000,
        detune_amount=8,
        reverb_amount=0.18,
        reverb_damping=0.55,
        room_size=0.8,
        pitch_drop=0.997,
        attack_ms=0.6,
        freq_spread=4.0,
        volume=1.0,
        octave_range=(-3, 3),
        description="Hollow wooden tap, warm marimba-like resonance",
    ),

    "stone": Material(
        name="stone",
        base_freq=280,
        partials=[
            (1.0, 1.0), (2.37, 0.5), (4.73, 0.25),
            (7.11, 0.12), (9.89, 0.06),
        ],
        decay_rates=[35, 48, 60, 72, 85],
        grain_duration=0.03,
        attack_noise=0.6,
        noise_freq=1800,
        detune_amount=15,
        reverb_amount=0.15,
        reverb_damping=0.6,
        room_size=0.7,
        pitch_drop=0.994,
        attack_ms=0.4,
        freq_spread=5.0,
        volume=1.0,
        octave_range=(-3, 3),
        description="Dense slate tap, heavy and earthy",
    ),

    "bamboo": Material(
        name="bamboo",
        base_freq=680,
        partials=[
            (1.0, 1.0), (3.01, 0.5), (5.03, 0.25), (7.02, 0.1),
        ],
        decay_rates=[15, 24, 34, 45],
        grain_duration=0.05,
        attack_noise=0.3,
        noise_freq=5000,
        detune_amount=6,
        reverb_amount=0.35,
        reverb_damping=0.25,
        room_size=1.1,
        pitch_drop=1.0,
        attack_ms=1.0,
        freq_spread=3.5,
        volume=0.85,
        octave_range=(-3, 3),
        description="Hollow tube resonance, odd harmonics, breathy and airy",
    ),

    "ember": Material(
        name="ember",
        base_freq=350,
        partials=[
            (1.0, 1.0), (1.73, 0.6), (2.91, 0.35), (4.37, 0.15),
        ],
        decay_rates=[42, 55, 68, 80],
        grain_duration=0.025,
        attack_noise=0.7,
        noise_freq=1500,
        detune_amount=22,
        reverb_amount=0.2,
        reverb_damping=0.7,
        room_size=0.6,
        pitch_drop=0.98,
        attack_ms=0.3,
        freq_spread=8.0,
        volume=0.9,
        octave_range=(-3, 3),
        description="Warm crackling ember, fire-like with wide pitch scatter",
    ),

    "silk": Material(
        name="silk",
        base_freq=1800,
        partials=[(1.0, 1.0), (2.01, 0.4), (3.5, 0.1)],
        decay_rates=[22, 35, 50],
        grain_duration=0.045,
        attack_noise=0.55,
        noise_freq=6500,
        detune_amount=10,
        reverb_amount=0.5,
        reverb_damping=0.15,
        room_size=1.4,
        pitch_drop=1.0,
        attack_ms=2.5,
        freq_spread=5.0,
        volume=0.6,
        octave_range=(-3, 3),
        description="Soft breathy whisper, delicate airy texture",
    ),

    "shell": Material(
        name="shell",
        base_freq=750,
        partials=[
            (1.0, 1.0), (1.003, 0.9), (2.01, 0.6),
            (2.016, 0.55), (3.02, 0.3), (3.028, 0.28),
        ],
        decay_rates=[8, 9, 14, 15, 22, 23],
        grain_duration=0.07,
        attack_noise=0.2,
        noise_freq=3000,
        detune_amount=4,
        reverb_amount=0.6,
        reverb_damping=0.2,
        room_size=1.5,
        pitch_drop=1.0,
        attack_ms=1.5,
        freq_spread=2.0,
        volume=0.75,
        octave_range=(-3, 3),
        description="Swirly ocean interference, dense phase beating",
    ),

    "moss": Material(
        name="moss",
        base_freq=220,
        partials=[(1.0, 1.0), (2.1, 0.25), (3.3, 0.08)],
        decay_rates=[28, 42, 58],
        grain_duration=0.035,
        attack_noise=0.15,
        noise_freq=1200,
        detune_amount=12,
        reverb_amount=0.3,
        reverb_damping=0.8,
        room_size=0.5,
        pitch_drop=0.996,
        attack_ms=3.0,
        freq_spread=4.0,
        volume=0.7,
        octave_range=(-3, 3),
        description="Ultra-soft muffled earth, mossy dampness",
    ),
}


SOUND_SETS = {
    "ambient": AMBIENT_MATERIALS,
    "material": MATERIAL_MATERIALS,
}

# Default MATERIALS points to the default set for backwards compat
MATERIALS = SOUND_SETS[DEFAULT_SOUND_SET]


def list_sound_sets() -> List[str]:
    """List all available sound set names."""
    return list(SOUND_SETS.keys())


def get_sound_set(name: str) -> dict:
    """Get a sound set by name."""
    if name not in SOUND_SETS:
        raise ValueError(f"Unknown sound set: {name}. Available: {list(SOUND_SETS.keys())}")
    return SOUND_SETS[name]


def get_material(name: str, sound_set: str = DEFAULT_SOUND_SET) -> Material:
    """Get a material by name from a given sound set."""
    materials = get_sound_set(sound_set)
    if name not in materials:
        raise ValueError(f"Unknown character: {name}. Available: {list(materials.keys())}")
    return materials[name]


def get_random_material(sound_set: str = DEFAULT_SOUND_SET) -> Material:
    """Get a random material from a given sound set."""
    materials = get_sound_set(sound_set)
    return random.choice(list(materials.values()))


def list_materials(sound_set: str = DEFAULT_SOUND_SET) -> List[str]:
    """List all available material names in a sound set."""
    return list(get_sound_set(sound_set).keys())
