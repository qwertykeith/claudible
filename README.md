```
        ♪ ♫ ♪
      ┌─────────┐
      │ ╭─────╮ │ ♩
      │ │ ▓▓▓ │ │
      │ │ ▓▓▓ │ │  ♬    ┈┈┈╮
      │ ╰─────╯ │     ♪    │
      │  claude  │ ♫       │
      └────┬────┘    ♩    ≋≋≋
     ══════╧══════       ≋≋≋≋≋
      ♪  audible  ♫       ≋≋≋
```

# 🎵 claudible

*An opus for your terminals.*

Possibly the most annoying Claude utility ever made but here it is anyway.

Ambient audio soundscape feedback for terminal output. It really shines with a lot of busy busy Claude Code terminals running at the same time.

## 🎼 The Idea

Imagine you are working in a factory. Each Claude Code session is a machine that must be attended to. When it's working, you hear it — crystalline sparkles as text flows, soft chimes when tasks complete. When it goes quiet, you know something needs your attention.

## 🎶 Installation

```bash
# Recommended (handles PATH automatically)
brew install pipx && pipx ensurepath  # macOS
# or: pip install --user pipx && pipx ensurepath

pipx install claudible

# Or with pip
pip install claudible
```

> **`claudible` command not found?** If you used `pip install --user`, the script directory may not be on your PATH. Use `python3 -m claudible` instead, or switch to `pipx`.

## 🎹 Usage

```bash
# Run claude with audio feedback (default: ambient sound set)
claudible

# Run a different command
claudible "python my_script.py"

# Pipe mode
some-command 2>&1 | claudible --pipe

# Choose a sound character
claudible --character drift

# Use the percussive material sound set
claudible --set material -c bell

# Adjust volume
claudible --volume 0.3

# List available characters across all sets
claudible --list-characters

# Demo all sound characters in a set
claudible --demo
claudible --demo --set material
```

### 🔇 Reverse Mode

In reverse mode, claudible is silent while output is flowing and plays ambient sound during silence. Useful when you want to know a task is *waiting* rather than *working*.

```bash
# Ambient grains play when Claude is idle/waiting for you
claudible --reverse

# Combine with a character
claudible --reverse -c shell
```

## 🎧 Works With Any CLI

Built for Claude Code, but claudible works with anything that produces terminal output.

```bash
# Aider
claudible "aider"

# Watch a dev server
npm run dev 2>&1 | claudible --pipe

# Monitor logs
tail -f /var/log/app.log | claudible --pipe -c droplet
```

## 🎻 Sound Sets

Claudible ships with two sound sets. The **ambient** set (default) produces soft, throbbing textures with rich overtones. The **material** set has crisp, percussive sounds modelled on physical materials.

### Ambient (default) `--set ambient`

| Character | | Description |
|-----------|---|-------------|
| `drift` | 🌊 | Slow undulating low throb, gentle beating pairs |
| `tide` | 🌀 | Oceanic wash, phase interference, wide and enveloping |
| `breath` | 💨 | Soft exhale texture, breathy warmth with filtered noise |
| `haze` | 🌫️ | Dense foggy overtones, warm and thick with close partial clusters |
| `pulse` | 💗 | Gentle rhythmic throbbing from detuned pairs, hypnotic |
| `glow` | 🕯️ | Warm radiant harmonics, rich natural overtone series |
| `cloud` | ☁️ | Diffuse and soft, massive reverb space, floating |
| `murmur` | 🫧 | Low gentle rumble, warm harmonic murmur with subtle throb |
| `shimmer` | ✨ | High ethereal overtones, floating and luminous |
| `deep` | 🎚️ | Sub-bass throb, felt more than heard, very deep and slow |

### Material `--set material`

| Character | | Description |
|-----------|---|-------------|
| `ice` | 🧊 | Brittle, very high, fast decay with pitch drop |
| `glass` | 🍷 | Classic wine glass ping |
| `crystal` | 💎 | Pure lead crystal with beating from close partial pairs |
| `ceramic` | 🏺 | Duller muted earthenware tap |
| `bell` | 🔔 | Small metallic bell, classic ratios, long ring |
| `droplet` | 💧 | Water droplet, pitch bend down, liquid |
| `click` | ⌨️ | Sharp mechanical click, keyboard-like |
| `wood` | 🪵 | Hollow wooden tap, warm marimba-like resonance |
| `stone` | 🪨 | Dense slate tap, heavy and earthy |
| `bamboo` | 🎋 | Hollow tube resonance, odd harmonics, breathy and airy |
| `ember` | 🔥 | Warm crackling ember, fire-like with wide pitch scatter |
| `silk` | 🪶 | Soft breathy whisper, delicate airy texture |
| `shell` | 🐚 | Swirly ocean interference, dense phase beating |
| `moss` | 🌿 | Ultra-soft muffled earth, mossy dampness |

## 🎛️ Options

| Flag | Description |
|------|-------------|
| `--pipe` | 📥 Read from stdin instead of wrapping |
| `--set`, `-s` | 🎼 Sound set: `ambient` (default), `material` |
| `--character`, `-c` | 🎵 Sound character within the set |
| `--volume`, `-v` | 🔊 Volume 0.0–1.0 (default: 0.5) |
| `--attention`, `-a` | ⏰ Silence alert seconds (default: 30) |
| `--reverse`, `-r` | 🔄 Reverse mode: sound during silence, quiet during output |
| `--list-characters` | 📋 Show all characters across all sets |
| `--demo` | 🔊 Demo characters in the selected set |

## 🛠️ Development

Test locally without installing:

```bash
cd claudible

# Run wrapping claude (Ctrl+C to stop)
PYTHONPATH=src python3 -m claudible

# Wrap a different command
PYTHONPATH=src python3 -m claudible "ls -la"

# Pipe mode
echo "test" | PYTHONPATH=src python3 -m claudible --pipe -c glass

# List characters
PYTHONPATH=src python3 -m claudible --list-characters

# Demo all characters
PYTHONPATH=src python3 -m claudible --demo
```

## 📜 License

MIT
