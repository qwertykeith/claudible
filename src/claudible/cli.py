"""Command-line interface for claudible."""

import argparse
import os
import subprocess
import sys
import time
from typing import Optional

from .audio import SoundEngine
from .materials import (
    get_material, get_random_material, list_materials, list_sound_sets,
    get_sound_set, SOUND_SETS, DEFAULT_SOUND_SET,
)
from .monitor import ActivityMonitor


def run_demo(volume: float, sound_set: str = DEFAULT_SOUND_SET):
    """Play a short demo of every sound character in a set."""
    materials = get_sound_set(sound_set)
    print(f"Claudible character demo [{sound_set}]\n", file=sys.stderr)
    for name, mat in materials.items():
        print(f"  {name:10} - {mat.description}", file=sys.stderr)
        engine = SoundEngine(material=mat, volume=volume)
        engine.start()
        # Play a burst of grains then a chime
        for i in range(8):
            engine.play_grain(chr(ord('a') + i))
            time.sleep(0.06)
        time.sleep(0.15)
        engine.play_chime()
        time.sleep(0.6)
        engine.stop()
    print("\nDone.", file=sys.stderr)


def run_pipe_mode(engine: SoundEngine, monitor: ActivityMonitor):
    """Run in pipe mode, reading from stdin."""
    engine.start()
    monitor.start()

    try:
        while True:
            data = sys.stdin.buffer.read(1024)
            if not data:
                break
            monitor.process_chunk(data)
            sys.stdout.buffer.write(data)
            sys.stdout.buffer.flush()
        # Let audio buffer drain
        time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        monitor.stop()
        engine.stop()


def run_wrap_mode(command: str, engine: SoundEngine, monitor: ActivityMonitor):
    """Run in wrap mode, spawning a PTY for the command."""
    import pty
    import select
    import shlex
    import termios
    import tty

    engine.start()
    monitor.start()

    if ' ' in command:
        args = shlex.split(command)
    else:
        args = [command]

    master_fd, slave_fd = pty.openpty()

    try:
        process = subprocess.Popen(
            args,
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            preexec_fn=os.setsid,
        )
        os.close(slave_fd)

        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setraw(sys.stdin.fileno())

            while process.poll() is None:
                rlist, _, _ = select.select([sys.stdin, master_fd], [], [], 0.1)

                for fd in rlist:
                    if fd == sys.stdin:
                        data = os.read(sys.stdin.fileno(), 1024)
                        if data:
                            os.write(master_fd, data)
                    elif fd == master_fd:
                        try:
                            data = os.read(master_fd, 1024)
                            if data:
                                monitor.process_chunk(data)
                                sys.stdout.buffer.write(data)
                                sys.stdout.buffer.flush()
                        except OSError:
                            break
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    except KeyboardInterrupt:
        pass
    finally:
        os.close(master_fd)
        monitor.stop()
        engine.stop()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog='claudible',
        description='Ambient audio soundscape feedback for terminal output',
    )
    parser.add_argument(
        'command',
        nargs='?',
        default='claude',
        help='Command to wrap (default: claude)',
    )
    parser.add_argument(
        '--pipe',
        action='store_true',
        help='Pipe mode: read from stdin instead of wrapping a command',
    )
    parser.add_argument(
        '--set', '-s',
        choices=list_sound_sets(),
        default=DEFAULT_SOUND_SET,
        help=f'Sound set (default: {DEFAULT_SOUND_SET})',
    )
    parser.add_argument(
        '--character', '-c',
        help='Sound character (default: random). Use --list-characters to see options.',
    )
    parser.add_argument(
        '--volume', '-v',
        type=float,
        default=0.5,
        help='Volume 0.0-1.0 (default: 0.5)',
    )
    parser.add_argument(
        '--attention', '-a',
        type=float,
        default=30.0,
        help='Seconds of silence before attention signal (default: 30)',
    )
    parser.add_argument(
        '--reverse', '-r',
        action='store_true',
        help='Reverse mode: sound plays during silence, not during output',
    )
    parser.add_argument(
        '--list-characters',
        action='store_true',
        help='List available sound characters',
    )
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Play a short demo of each sound character',
    )

    args = parser.parse_args()

    sound_set = args.set

    if args.list_characters:
        for set_name, materials in SOUND_SETS.items():
            default_tag = " (default)" if set_name == DEFAULT_SOUND_SET else ""
            print(f"\n  [{set_name}]{default_tag}\n")
            for name, mat in materials.items():
                print(f"    {name:10} - {mat.description}")
        print()
        return

    if args.demo:
        volume = max(0.0, min(1.0, args.volume))
        run_demo(volume, sound_set)
        return

    # Validate character against the chosen set
    if args.character:
        available = list_materials(sound_set)
        if args.character not in available:
            parser.error(
                f"character '{args.character}' not in set '{sound_set}'. "
                f"Available: {', '.join(available)}"
            )
        material = get_material(args.character, sound_set)
    else:
        material = get_random_material(sound_set)

    volume = max(0.0, min(1.0, args.volume))

    engine = SoundEngine(material=material, volume=volume)
    monitor = ActivityMonitor(
        on_grain=engine.play_grain,
        on_chime=engine.play_chime,
        on_attention=engine.play_attention,
        attention_seconds=args.attention,
        reverse=args.reverse,
    )

    mode_label = " (reverse)" if args.reverse else ""
    print(f"[claudible] {material.name}{mode_label} - {material.description}", file=sys.stderr)

    if args.pipe:
        run_pipe_mode(engine, monitor)
    else:
        run_wrap_mode(args.command, engine, monitor)


if __name__ == '__main__':
    main()
