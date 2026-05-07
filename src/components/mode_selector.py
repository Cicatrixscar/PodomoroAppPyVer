# mode_selector.py — Toggle: Pomodoro / Short Break / Long Break

import flet as ft
from src.constants.timer import MODE_POMODORO, MODE_SHORT_BREAK, MODE_LONG_BREAK, MODE_LABELS
from src.constants.theme import (
    COLOR_POMODORO,
    COLOR_SHORT_BREAK,
    COLOR_LONG_BREAK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BORDER_RADIUS_LG,
)

MODE_COLORS = {
    MODE_POMODORO: COLOR_POMODORO,
    MODE_SHORT_BREAK: COLOR_SHORT_BREAK,
    MODE_LONG_BREAK: COLOR_LONG_BREAK,
}


class ModeSelector(ft.UserControl):
    """Toggle selector untuk memilih mode timer."""

    def __init__(self, current_mode, on_mode_change):
        super().__init__()
        self.current_mode = current_mode
        self.on_mode_change = on_mode_change

    def build(self):
        modes = [MODE_POMODORO, MODE_SHORT_BREAK, MODE_LONG_BREAK]

        buttons = []
        for mode in modes:
            is_selected = mode == self.current_mode
            color = MODE_COLORS[mode]

            buttons.append(
                ft.Container(
                    content=ft.Text(
                        MODE_LABELS[mode],
                        size=13,
                        weight=ft.FontWeight.W_600 if is_selected else ft.FontWeight.W_400,
                        color=TEXT_PRIMARY if is_selected else TEXT_SECONDARY,
                    ),
                    bgcolor=color if is_selected else "transparent",
                    border_radius=BORDER_RADIUS_LG,
                    padding=ft.padding.symmetric(horizontal=16, vertical=8),
                    on_click=lambda e, m=mode: self.on_mode_change(m),
                    animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
                    ink=True,
                )
            )

        return ft.Container(
            content=ft.Row(
                controls=buttons,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=4,
            ),
            bgcolor="#1E1E32",
            border_radius=BORDER_RADIUS_LG,
            padding=4,
        )
