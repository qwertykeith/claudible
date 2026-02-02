"""Material character presets for sound generation."""

from dataclasses import dataclass
from typing import List, Tuple
import random


@dataclass
class Material:
    """Defines the sonic character of a material."""

    name: str
    base_freq: float  # Hz
    partials: List[Tuple[float, float]]  # (ratio, amplitude) pairs
    grain_duration: float  # seconds
    attack_noise: float  # 0-1, amount of high-freq noise on attack
    decay_rates: List[float]  # decay multiplier per partial (higher = faster decay)
    detune_amount: float  # cents of random detuning
    reverb_amount: float  # 0-1
    pitch_bend: float  # semitones to bend (negative = down)
    description: str


MATERIALS = {
    "ice": Material(
        name="ice",
        base_freq=2800,
        partials=[(1.0, 1.0), (2.3, 0.6), (4.1, 0.3), (7.2, 0.15)],
        grain_duration=0.035,
        attack_noise=0.4,
        decay_rates=[12, 18, 25, 35],
        detune_amount=8,
        reverb_amount=0.3,
        pitch_bend=0,
        description="Brittle, very high, fast decay",
    ),
    "glass": Material(
        name="glass",
        base_freq=1200,
        partials=[(1.0, 1.0), (2.4, 0.7), (4.2, 0.4), (6.8, 0.2)],
        grain_duration=0.045,
        attack_noise=0.25,
        decay_rates=[8, 12, 18, 25],
        detune_amount=5,
        reverb_amount=0.4,
        pitch_bend=0,
        description="Classic wine glass ping",
    ),
    "crystal": Material(
        name="crystal",
        base_freq=1800,
        partials=[(1.0, 1.0), (2.01, 0.8), (4.0, 0.5), (4.03, 0.45), (6.5, 0.2)],
        grain_duration=0.050,
        attack_noise=0.15,
        decay_rates=[6, 7, 10, 11, 16],
        detune_amount=3,
        reverb_amount=0.5,
        pitch_bend=0,
        description="Pure with beating from close partial pairs",
    ),
    "ceramic": Material(
        name="ceramic",
        base_freq=600,
        partials=[(1.0, 1.0), (2.8, 0.4), (5.1, 0.15)],
        grain_duration=0.040,
        attack_noise=0.35,
        decay_rates=[15, 22, 30],
        detune_amount=12,
        reverb_amount=0.25,
        pitch_bend=0,
        description="Duller, muted",
    ),
    "bell": Material(
        name="bell",
        base_freq=900,
        partials=[(1.0, 1.0), (2.0, 0.8), (3.6, 0.6), (5.4, 0.4), (8.2, 0.2)],
        grain_duration=0.055,
        attack_noise=0.3,
        decay_rates=[4, 5, 7, 10, 14],
        detune_amount=6,
        reverb_amount=0.6,
        pitch_bend=0,
        description="Metallic, longer ring",
    ),
    "droplet": Material(
        name="droplet",
        base_freq=1400,
        partials=[(1.0, 1.0), (2.2, 0.5), (3.8, 0.2)],
        grain_duration=0.045,
        attack_noise=0.5,
        decay_rates=[10, 15, 22],
        detune_amount=4,
        reverb_amount=0.45,
        pitch_bend=-4,
        description="Pitch bend down, liquid",
    ),
    "click": Material(
        name="click",
        base_freq=3500,
        partials=[(1.0, 1.0), (2.5, 0.3)],  # Minimal partials, mostly transient
        grain_duration=0.020,  # Very short
        attack_noise=0.7,  # Heavy noise transient = the click
        decay_rates=[40, 60],  # Super fast decay, no ring
        detune_amount=15,  # More randomness for organic feel
        reverb_amount=0.1,  # Basically dry
        pitch_bend=0,
        description="Sharp mechanical click, keyboard-like",
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
