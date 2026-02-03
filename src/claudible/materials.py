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
    description: str


MATERIALS = {
    # --- Original materials (upgraded with physics parameters) ---

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
        description="Ultra-soft muffled earth, mossy dampness",
    ),
}


def get_material(name: str) -> Material:
    """Get a material by name."""
    if name not in MATERIALS:
        raise ValueError(f"Unknown material: {name}. Available: {list(MATERIALS.keys())}")
    return MATERIALS[name]


def get_random_material() -> Material:
    """Get a random material."""
    return random.choice(list(MATERIALS.values()))


def list_materials() -> List[str]:
    """List all available material names."""
    return list(MATERIALS.keys())
