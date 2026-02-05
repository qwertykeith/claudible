# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development commands

```bash
# Run locally without installing
PYTHONPATH=src python3 -m claudible

# Run with a specific mode/character
PYTHONPATH=src python3 -m claudible --pipe          # pipe mode
PYTHONPATH=src python3 -m claudible --character drift
PYTHONPATH=src python3 -m claudible --list-characters
PYTHONPATH=src python3 -m claudible --demo

# Build
pip install build && python -m build

# Install in dev mode
pip install -e .
```

No test suite exists. Verify changes manually with the commands above.

## CI/CD

Push to `main` triggers `.github/workflows/publish.yml`: auto-bumps patch version in `pyproject.toml`, commits with `[skip ci]`, tags, builds, and publishes to PyPI via trusted publishing (OIDC). Avoid manual version bumps.

## Architecture

Four modules in `src/claudible/`:

**cli.py** — Argument parsing and mode dispatch. Two runtime modes:
- **Wrap mode** (default): spawns a PTY around a command, intercepts I/O
- **Pipe mode** (`--pipe`): reads stdin, passes through to stdout

**audio.py** — `SoundEngine`: real-time procedural audio synthesis. 44.1 kHz sounddevice output stream with a lock-protected ring buffer (2 sec). Grains are pre-cached at multiple octave registers on init. Audio callback mixes ring buffer with a background hum (detuned 55 Hz oscillators). DSP uses scipy when available, falls back to numpy-only approximations.

**materials.py** — `Material` dataclass defines physical sound properties (partials, decay rates, reverb, attack noise, etc.). Two sound sets: `ambient` (throbbing textures) and `material` (percussive). Each set has 10–21 named characters.

**monitor.py** — `ActivityMonitor`: tracks output activity in a daemon thread. Triggers `play_grain` per character (throttled to 30/sec), `play_chime` on 3+ consecutive newlines, `play_attention` after configurable silence. Reverse mode inverts the logic (grains during silence).

### Data flow

```
terminal output → ActivityMonitor.process_chunk()
  → on_grain/on_chime/on_attention callbacks
    → SoundEngine.play_*() → ring buffer
      → audio callback → sounddevice → speakers
```

## Cross-platform notes

- **Audio engine native-lib guard:** `sounddevice` (or any replacement) must wrap its import in `try/except (OSError, ImportError)` with platform-specific install instructions and `SystemExit(1)`. See `src/claudible/audio.py`.
- **Unix-only stdlib modules** (`pty`, `select`, `tty`, `termios`): must be lazy-imported inside the functions that use them, never at module top level. This prevents import-time crashes on Windows.

## Style

- Australian English spelling (colour, organisation, behaviour, etc.)
