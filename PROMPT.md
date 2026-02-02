Here's your Claude Code prompt:

---

Build a pip-installable Python package called `claudible` - ambient audio soundscape feedback for terminal output.

## The idea

You host a terminal with Claude Code in it and monitor the I/O to play sound. Not music, but use the activity to make it sound like a machine that's working. Use very soothing sounds like sparkles as text is returned. The idea is you have multiple separate terminals humming away in the background like machines. You know to attend to them if things go quiet.

in the readme, describe this starting with "Imagine you are working in a factory.  Each Claude Code is a machine that must be attended to... etc etc"

## Sound design

Generate all sounds procedurally with numpy (no audio files). The sounds should be:

- Crystal/glass-like with inharmonic partials (ratios like 1.0, 2.4, 4.2, 6.8 - not integer harmonics)
- Very short grains (~35-50ms) - tight sparkles, not long sustains
- High frequency noise transient on attack for realism
- Each partial decays at different rates (higher partials die faster)
- Subtle reverb for space
- Micro-detuning and random phase for organic feel

Include multiple "material" character presets that are randomly chosen at startup, one sound for each process that is running:

- ice (brittle, very high, fast decay)
- glass (classic wine glass ping)
- crystal (pure with beating from close partial pairs)
- ceramic (duller, muted)
- bell (metallic, longer ring)
- droplet (pitch bend down, liquid)

## Features

- Pipe mode: `some-command 2>&1 | claudible --pipe`
- Wrap mode: `claudible` (defaults to wrapping "claude", or `claudible "other-command"`)
- Grains trigger on text output (throttled to ~30/sec max)
- Soft chime on task completion (multiple newlines)
- Gentle attention signal after N seconds of silence
- Very subtle background hum with beating
- `--character` flag to choose specific material, otherwise random
- `--volume` master volume control
- `--attention` seconds before silence alert
- `--list-characters` show available presets
- Cross-platform: Mac, Windows, Linux

## Dependencies

Only numpy and sounddevice (keeps install small, ~20MB)

## README

Include the opus pun - describe the package as "an opus for your terminals" or similar. Mention it's designed for running multiple Claude Code sessions as background "machines" that you can hear.

## Structure

```
claudible/
├── pyproject.toml
├── README.md
├── src/
│   └── claudible/
│       ├── __init__.py
│       ├── cli.py
│       ├── audio.py (sound engine)
│       ├── materials.py (character presets)
│       └── monitor.py (I/O activity tracking)
```
