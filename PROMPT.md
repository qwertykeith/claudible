Build a pip-installable Python package called `claudible` - ambient audio soundscape feedback for terminal output.

## The idea

You wrap Claude Code (or any command) to play ambient sounds as it outputs text. Crystalline sparkles for activity, chimes for completion, alerts for silence. Like machines humming in a factory.

## Sound design

Generate all sounds procedurally with numpy (no audio files):

- Crystal/glass-like with inharmonic partials (ratios like 1.0, 2.4, 4.2, 6.8)
- Very short grains (~35-50ms)
- High frequency noise transient on attack
- Per-partial decay rates (higher partials die faster)
- Subtle reverb, micro-detuning, random phase

Material presets: ice, glass, crystal, ceramic, bell, droplet, click

## Features

- Wrap mode: `claudible` (wraps "claude" by default)
- Pipe mode: `some-command | claudible --pipe`
- Grains on text output (throttled ~30/sec)
- Chime on task completion (multiple newlines)
- Attention signal after N seconds silence
- Background hum with beating
- `--character`, `--volume`, `--attention`, `--list-characters`

## Dependencies

numpy, sounddevice

## Structure

```
claudible/
├── pyproject.toml
├── README.md
└── src/claudible/
    ├── __init__.py
    ├── __main__.py
    ├── cli.py
    ├── audio.py
    ├── materials.py
    └── monitor.py
```
