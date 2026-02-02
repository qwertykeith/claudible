# claudible

*An opus for your terminals.*

Ambient audio soundscape feedback for terminal output.

## The Idea

Imagine you are working in a factory. Each Claude Code session is a machine that must be attended to. When it's working, you hear it - crystalline sparkles as text flows, soft chimes when tasks complete. When it goes quiet, you know something needs your attention.

## Installation

```bash
pip install claudible
```

## Usage

```bash
# Run claude with audio feedback (default)
claudible

# Run a different command
claudible "python my_script.py"

# Pipe mode
some-command 2>&1 | claudible --pipe

# Choose a sound character
claudible --character crystal

# Adjust volume
claudible --volume 0.3

# List available characters
claudible --list-characters
```

## Sound Characters

| Character | Description |
|-----------|-------------|
| `ice` | Brittle, very high, fast decay |
| `glass` | Classic wine glass ping |
| `crystal` | Pure with beating from close partials |
| `ceramic` | Duller, muted |
| `bell` | Metallic, longer ring |
| `droplet` | Pitch bend down, liquid |
| `click` | Sharp mechanical click |

## Options

| Flag | Description |
|------|-------------|
| `--pipe` | Read from stdin instead of wrapping |
| `--character`, `-c` | Sound character |
| `--volume`, `-v` | Volume 0.0-1.0 (default: 0.5) |
| `--attention`, `-a` | Silence alert seconds (default: 30) |
| `--list-characters` | Show presets |

## Development

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
```

## License

MIT
