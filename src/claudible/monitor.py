"""I/O activity tracking and event detection."""

import time
from typing import Callable, Optional
import threading


class ActivityMonitor:
    """Monitors text output and triggers audio events."""

    MAX_GRAINS_PER_SEC = 30
    NEWLINE_THRESHOLD = 3  # Consecutive newlines to trigger completion chime

    # Reverse mode: ambient grain rate when idle
    REVERSE_GRAINS_PER_SEC = 12
    REVERSE_IDLE_DELAY = 3.0  # Seconds of silence before ambient grains start

    def __init__(
        self,
        on_grain: Callable[[], None],
        on_chime: Callable[[], None],
        on_attention: Callable[[], None],
        attention_seconds: float = 30.0,
        reverse: bool = False,
    ):
        self.on_grain = on_grain
        self.on_chime = on_chime
        self.on_attention = on_attention
        self.attention_seconds = attention_seconds
        self.reverse = reverse

        self._last_grain_time = 0.0
        self._min_grain_interval = 1.0 / self.MAX_GRAINS_PER_SEC
        self._consecutive_newlines = 0
        self._last_activity_time = time.time()
        self._attention_triggered = False
        self._running = False
        self._bg_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

        # Reverse mode state
        self._reverse_playing = False
        self._was_active = False

    def start(self):
        """Start monitoring."""
        self._running = True
        self._last_activity_time = time.time()
        self._bg_thread = threading.Thread(target=self._background_loop, daemon=True)
        self._bg_thread.start()

    def stop(self):
        """Stop monitoring."""
        self._running = False
        if self._bg_thread:
            self._bg_thread.join(timeout=1.0)

    def _background_loop(self):
        """Background thread for attention signals and reverse-mode ambient grains."""
        reverse_interval = 1.0 / self.REVERSE_GRAINS_PER_SEC

        while self._running:
            if self.reverse:
                with self._lock:
                    elapsed = time.time() - self._last_activity_time

                if elapsed >= self.REVERSE_IDLE_DELAY:
                    if not self._reverse_playing:
                        self._reverse_playing = True
                        self.on_chime()
                    self.on_grain()
                    time.sleep(reverse_interval)
                else:
                    if self._reverse_playing:
                        self._reverse_playing = False
                    time.sleep(0.1)
            else:
                time.sleep(1.0)
                with self._lock:
                    elapsed = time.time() - self._last_activity_time
                    if elapsed >= self.attention_seconds and not self._attention_triggered:
                        self._attention_triggered = True
                        self.on_attention()

    def process_chunk(self, data: bytes):
        """Process a chunk of output data."""
        if not data:
            return

        with self._lock:
            self._last_activity_time = time.time()
            self._attention_triggered = False

        if self.reverse:
            # In reverse mode, activity = silence. Just update the timestamp.
            return

        # Normal mode: trigger sounds on output
        try:
            text = data.decode('utf-8', errors='replace')
        except Exception:
            text = str(data)

        for char in text:
            if char == '\n':
                self._consecutive_newlines += 1
                if self._consecutive_newlines >= self.NEWLINE_THRESHOLD:
                    self.on_chime()
                    self._consecutive_newlines = 0
            else:
                self._consecutive_newlines = 0
                self._maybe_trigger_grain()

    def _maybe_trigger_grain(self):
        """Trigger a grain if enough time has passed (throttling)."""
        now = time.time()
        if now - self._last_grain_time >= self._min_grain_interval:
            self._last_grain_time = now
            self.on_grain()
