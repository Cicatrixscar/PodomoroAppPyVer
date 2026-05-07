# control_buttons.py — Tombol Start / Pause / Reset

import flet as ft
from src.constants.theme import (
    PRIMARY_COLOR,
    TEXT_PRIMARY,
    BG_CARD,
    BORDER_RADIUS_XL,
)


class ControlButtons(ft.UserControl):
    """Tombol kontrol timer: Start/Pause dan Reset."""

    def __init__(self, timer_state, on_start_pause, on_reset, on_skip, color=PRIMARY_COLOR):
        super().__init__()
        self.timer_state = timer_state
        self.on_start_pause = on_start_pause
        self.on_reset = on_reset
        self.on_skip = on_skip
        self.color = color

    def update_color(self, color):
        self.color = color
        self.update()

    def build(self):
        is_running = self.timer_state.is_running

        return ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=16,
            controls=[
                # Reset button
                ft.IconButton(
                    icon=ft.Icons.RESTART_ALT_ROUNDED,
                    icon_color="#A0A0B0",
                    icon_size=28,
                    tooltip="Reset",
                    on_click=self.on_reset,
                    style=ft.ButtonStyle(
                        shape=ft.CircleBorder(),
                        bgcolor="#2A2A3E",
                        padding=16,
                    ),
                ),
                # Start/Pause button (utama, lebih besar)
                ft.ElevatedButton(
                    content=ft.Row(
                        spacing=8,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(
                                name=ft.Icons.PAUSE_ROUNDED if is_running else ft.Icons.PLAY_ARROW_ROUNDED,
                                color=TEXT_PRIMARY,
                                size=24,
                            ),
                            ft.Text(
                                "Pause" if is_running else "Start",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=TEXT_PRIMARY,
                            ),
                        ],
                    ),
                    bgcolor=self.color,
                    on_click=self.on_start_pause,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS_XL),
                        padding=ft.padding.symmetric(horizontal=32, vertical=16),
                        elevation=4,
                        shadow_color=self.color,
                    ),
                ),
                # Skip button
                ft.IconButton(
                    icon=ft.Icons.SKIP_NEXT_ROUNDED,
                    icon_color="#A0A0B0",
                    icon_size=28,
                    tooltip="Skip",
                    on_click=self.on_skip,
                    style=ft.ButtonStyle(
                        shape=ft.CircleBorder(),
                        bgcolor="#2A2A3E",
                        padding=16,
                    ),
                ),
            ],
        )
