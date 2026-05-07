# test_button.py — Test: apakah update Icon di dalam Button crash?

import flet as ft
import asyncio
import math
from flet.canvas import Canvas, Arc, Circle


async def main(page: ft.Page):
    page.bgcolor = "#1A1A2E"

    running = False
    count = 0
    size = 250
    center = size / 2
    radius = 110

    def make_shapes():
        progress = count / 60
        sweep = progress * 2 * math.pi
        start_angle = -math.pi / 2

        bg = ft.Paint(color="#2A2A3E", stroke_width=4,
                      style=ft.PaintingStyle.STROKE, stroke_cap=ft.StrokeCap.ROUND)
        fg = ft.Paint(color="#E05A4E", stroke_width=8,
                      style=ft.PaintingStyle.STROKE, stroke_cap=ft.StrokeCap.ROUND)
        # Glow with ARGB alpha
        glow = ft.Paint(color="#40E05A4E", stroke_width=12,
                        style=ft.PaintingStyle.STROKE, stroke_cap=ft.StrokeCap.ROUND)

        shapes = [Circle(center, center, radius, bg)]
        if sweep > 0:
            shapes.append(Arc(center - radius, center - radius, radius * 2, radius * 2,
                              start_angle, sweep, glow))
            shapes.append(Arc(center - radius, center - radius, radius * 2, radius * 2,
                              start_angle, sweep, fg))
        return shapes

    canvas = Canvas(shapes=make_shapes(), width=size, height=size)
    timer_text = ft.Text(f"00:{count:02d}", size=48, color="white", weight=ft.FontWeight.BOLD)

    # Test: Icon inside ElevatedButton — same as main.py
    btn_icon = ft.Icon(ft.Icons.PLAY_ARROW_ROUNDED, color="white", size=24)
    btn_label = ft.Text("Start", size=16, weight=ft.FontWeight.BOLD, color="white")

    start_btn = ft.ElevatedButton(
        content=ft.Row(spacing=8, alignment=ft.MainAxisAlignment.CENTER,
                       controls=[btn_icon, btn_label]),
        bgcolor="#E05A4E",
        on_click=lambda e: toggle(),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=24),
            padding=ft.Padding.symmetric(horizontal=32, vertical=16),
        ),
    )

    stats = ft.Text("Sessions: 0", size=14, color="#A0A0B0")

    def refresh():
        timer_text.value = f"00:{count:02d}"
        canvas.shapes = make_shapes()
        btn_icon.icon = ft.Icons.PAUSE_ROUNDED if running else ft.Icons.PLAY_ARROW_ROUNDED
        btn_label.value = "Pause" if running else "Start"
        page.update()

    def toggle():
        nonlocal running
        running = not running
        print(f"Toggle: running={running}")
        refresh()

    page.add(
        ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Stack(
                    width=size, height=size,
                    controls=[
                        canvas,
                        ft.Container(
                            width=size, height=size,
                            alignment=ft.Alignment.CENTER,
                            content=timer_text,
                        ),
                    ],
                ),
                ft.Container(height=16),
                start_btn,
                ft.Container(height=8),
                stats,
            ],
        )
    )

    while True:
        await asyncio.sleep(1)
        if running:
            count = (count + 1) % 61
            refresh()


ft.app(target=main)
