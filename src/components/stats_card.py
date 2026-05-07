# stats_card.py — Kartu statistik sesi harian

import flet as ft
from src.constants.theme import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BG_CARD,
    BG_CARD_LIGHT,
    BORDER_RADIUS_LG,
    SHADOW_BLUR,
    SHADOW_COLOR,
)


class StatsCard(ft.UserControl):
    """Kartu yang menampilkan statistik sesi Pomodoro hari ini."""

    def __init__(self, sessions_today=0):
        super().__init__()
        self.sessions_today = sessions_today

    def set_sessions(self, count):
        self.sessions_today = count
        self.update()

    def build(self):
        # Estimasi fokus time
        focus_minutes = self.sessions_today * 25

        return ft.Container(
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Text(
                        "📊 Statistik Hari Ini",
                        size=16,
                        weight=ft.FontWeight.W_600,
                        color=TEXT_PRIMARY,
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[
                            self._stat_item(
                                icon=ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED,
                                value=str(self.sessions_today),
                                label="Sesi Selesai",
                                color="#4CAF50",
                            ),
                            self._stat_item(
                                icon=ft.Icons.TIMER_OUTLINED,
                                value=f"{focus_minutes}m",
                                label="Waktu Fokus",
                                color="#2196F3",
                            ),
                            self._stat_item(
                                icon=ft.Icons.LOCAL_FIRE_DEPARTMENT_ROUNDED,
                                value=self._get_streak_emoji(),
                                label="Streak",
                                color="#FF9800",
                            ),
                        ],
                    ),
                ],
            ),
            bgcolor=BG_CARD,
            border_radius=BORDER_RADIUS_LG,
            padding=ft.padding.all(20),
            shadow=ft.BoxShadow(
                blur_radius=SHADOW_BLUR,
                color=SHADOW_COLOR,
            ),
        )

    def _stat_item(self, icon, value, label, color):
        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
            controls=[
                ft.Icon(icon, color=color, size=24),
                ft.Text(
                    value,
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_PRIMARY,
                ),
                ft.Text(
                    label,
                    size=11,
                    color=TEXT_SECONDARY,
                ),
            ],
        )

    def _get_streak_emoji(self):
        s = self.sessions_today
        if s >= 8:
            return "🔥🔥🔥"
        elif s >= 4:
            return "🔥🔥"
        elif s >= 1:
            return "🔥"
        return "—"
