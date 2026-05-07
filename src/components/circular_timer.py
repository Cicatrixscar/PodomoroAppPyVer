# circular_timer.py — Widget timer lingkaran (Canvas arc)

import math
import flet as ft
from flet.canvas import Canvas, Arc, Circle
from src.constants.theme import (
    TIMER_CIRCLE_SIZE,
    TIMER_CIRCLE_STROKE,
    TIMER_BG_STROKE,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BG_CARD,
)


class CircularTimer(ft.UserControl):
    """Timer lingkaran yang menampilkan countdown dengan Canvas arc."""

    def __init__(self, timer_state, color="#E05A4E"):
        super().__init__()
        self.timer_state = timer_state
        self.color = color
        self._size = TIMER_CIRCLE_SIZE

    def update_color(self, color):
        self.color = color
        self.update()

    def build(self):
        return ft.Container(
            width=self._size,
            height=self._size,
            content=ft.Stack(
                controls=[
                    # Canvas untuk lingkaran timer
                    self._build_canvas(),
                    # Teks timer di tengah
                    ft.Container(
                        width=self._size,
                        height=self._size,
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=4,
                            controls=[
                                ft.Text(
                                    value=self.timer_state.display_time,
                                    size=48,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXT_PRIMARY,
                                ),
                                ft.Text(
                                    value=self._get_mode_label(),
                                    size=14,
                                    color=TEXT_SECONDARY,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

    def _build_canvas(self):
        progress = self.timer_state.progress
        center = self._size / 2
        radius = (self._size - TIMER_CIRCLE_STROKE * 2) / 2

        # Background circle
        bg_paint = ft.Paint(
            color="#2A2A3E",
            stroke_width=TIMER_BG_STROKE,
            style=ft.PaintingStyle.STROKE,
            stroke_cap=ft.StrokeCap.ROUND,
        )

        # Progress arc
        progress_paint = ft.Paint(
            color=self.color,
            stroke_width=TIMER_CIRCLE_STROKE,
            style=ft.PaintingStyle.STROKE,
            stroke_cap=ft.StrokeCap.ROUND,
        )

        # Glow paint
        glow_paint = ft.Paint(
            color=self.color,
            stroke_width=TIMER_CIRCLE_STROKE + 4,
            style=ft.PaintingStyle.STROKE,
            stroke_cap=ft.StrokeCap.ROUND,
            mask_filter=ft.MaskFilter.blur(ft.BlurType.NORMAL, 8),
        )

        sweep_angle = progress * 2 * math.pi
        start_angle = -math.pi / 2  # Mulai dari atas (12 o'clock)

        shapes = [
            # Background circle
            Circle(center, center, radius, bg_paint),
        ]

        if sweep_angle > 0:
            # Glow arc
            shapes.append(
                Arc(
                    center - radius,
                    center - radius,
                    radius * 2,
                    radius * 2,
                    start_angle,
                    sweep_angle,
                    glow_paint,
                )
            )
            # Progress arc
            shapes.append(
                Arc(
                    center - radius,
                    center - radius,
                    radius * 2,
                    radius * 2,
                    start_angle,
                    sweep_angle,
                    progress_paint,
                )
            )

        return Canvas(
            shapes=shapes,
            width=self._size,
            height=self._size,
        )

    def _get_mode_label(self):
        from src.constants.timer import MODE_LABELS
        return MODE_LABELS.get(self.timer_state.current_mode, "")
