# notifications.py — Notifikasi & alarm (flet Audio + vibrate)

import flet as ft


class NotificationManager:
    """Mengelola notifikasi suara dan haptic feedback."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.audio = ft.Audio(
            src="alarm.mp3",
            autoplay=False,
            volume=1.0,
        )
        self.page.overlay.append(self.audio)

    def set_volume(self, volume: float):
        """Set volume audio (0.0 - 1.0)."""
        self.audio.volume = volume
        self.audio.update()

    def play_alarm(self):
        """Mainkan suara alarm."""
        try:
            self.audio.play()
        except Exception:
            self._fallback_notification()

    def stop_alarm(self):
        """Hentikan suara alarm."""
        try:
            self.audio.pause()
        except Exception:
            pass

    def _fallback_notification(self):
        """Fallback jika audio gagal: snackbar + haptic."""
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("⏰ Timer selesai!", size=16),
                bgcolor="#E05A4E",
            )
        )
        try:
            self.page.haptic_feedback(ft.HapticFeedbackType.HEAVY_IMPACT)
        except Exception:
            pass

    def notify_completion(self, mode: str):
        """Notifikasi saat timer selesai."""
        self.play_alarm()
        self._fallback_notification()
