"""I/O activity tracking and event detection."""

import time
from typing import Callable, Optional
import threading


class ActivityMonitor:
    """Monitors text output and triggers audio events."""

    MAX_GRAINS_PER_SEC = 30
    NEWLINE_THRESHOLD = 3  # Consecutive newlines to trigger completion chime

    def __init__(
        self,
        on_grain: Callable[[], None],
        on_chime: Callable[[], None],
        on_attention: Callable[[], None],
        attention_seconds: float = 30.0,
    ):
        self.on_grain = on_grain
        self.on_chime = on_chime
        self.on_attention = on_attention
        self.attention_seconds = attention_seconds

        self._last_grain_time = 0.0
        self._min_grain_interval = 1.0 / self.MAX_GRAINS_PER_SEC
        self._consecutive_newlines = 0
        self._last_activity_time = time.time()
        self._attention_triggered = False
        self._running = False
        self._attention_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

    def start(self):
        """Start monitoring for silence."""
        self._running = True
        self._last_activity_time = time.time()
        self._attention_thread = threading.Thread(target=self._attention_loop, daemon=True)
        self._attention_thread.start()

    def stop(self):
        """Stop monitoring."""
        self._running = False
        if self._attention_thread:
            self._attention_thread.join(timeout=1.0)

    def _attention_loop(self):
        """Background thread to check for extended silence."""
        while self._running:
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

        # Decode safely
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
