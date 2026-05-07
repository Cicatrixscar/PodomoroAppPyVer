# timer_logic.py — State mesin timer (countdown, mode cycling)

import time
from src.constants.timer import (
    MODE_POMODORO,
    MODE_SHORT_BREAK,
    MODE_LONG_BREAK,
    DURATIONS,
    SESSIONS_BEFORE_LONG_BREAK,
)


class TimerState:
    """State terpusat untuk timer Pomodoro."""

    def __init__(self):
        self.current_mode = MODE_POMODORO
        self.time_remaining = DURATIONS[MODE_POMODORO]
        self.is_running = False
        self.completed_sessions = 0
        self._on_tick = None
        self._on_complete = None
        self._on_mode_change = None

    @property
    def total_duration(self):
        """Durasi total untuk mode saat ini."""
        return DURATIONS[self.current_mode]

    @property
    def progress(self):
        """Progress 0.0 - 1.0, dimana 1.0 = selesai."""
        total = self.total_duration
        if total == 0:
            return 0.0
        return 1.0 - (self.time_remaining / total)

    @property
    def minutes(self):
        return self.time_remaining // 60

    @property
    def seconds(self):
        return self.time_remaining % 60

    @property
    def display_time(self):
        """Format waktu MM:SS."""
        return f"{self.minutes:02d}:{self.seconds:02d}"

    def set_callbacks(self, on_tick=None, on_complete=None, on_mode_change=None):
        """Set callback functions."""
        self._on_tick = on_tick
        self._on_complete = on_complete
        self._on_mode_change = on_mode_change

    def start(self):
        """Mulai / resume timer."""
        self.is_running = True

    def pause(self):
        """Pause timer."""
        self.is_running = False

    def reset(self):
        """Reset timer ke durasi awal mode saat ini."""
        self.is_running = False
        self.time_remaining = DURATIONS[self.current_mode]
        if self._on_tick:
            self._on_tick()

    def set_mode(self, mode):
        """Ganti mode timer."""
        self.current_mode = mode
        self.time_remaining = DURATIONS[mode]
        self.is_running = False
        if self._on_mode_change:
            self._on_mode_change(mode)
        if self._on_tick:
            self._on_tick()

    def tick(self):
        """Dipanggil setiap detik oleh timer loop.
        Return True jika timer sedang berjalan (agar UI bisa di-refresh).
        """
        if not self.is_running:
            return False

        if self.time_remaining > 0:
            self.time_remaining -= 1

        if self.time_remaining <= 0:
            self.is_running = False
            self._handle_completion()

        return True

    def _handle_completion(self):
        """Handle saat timer selesai."""
        if self.current_mode == MODE_POMODORO:
            self.completed_sessions += 1

        if self._on_complete:
            self._on_complete(self.current_mode, self.completed_sessions)

    def get_next_mode(self):
        """Tentukan mode selanjutnya setelah timer selesai."""
        if self.current_mode == MODE_POMODORO:
            if self.completed_sessions % SESSIONS_BEFORE_LONG_BREAK == 0:
                return MODE_LONG_BREAK
            return MODE_SHORT_BREAK
        else:
            return MODE_POMODORO

    def advance_to_next_mode(self):
        """Pindah ke mode selanjutnya secara otomatis."""
        next_mode = self.get_next_mode()
        self.set_mode(next_mode)
