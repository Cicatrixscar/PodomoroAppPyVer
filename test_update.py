# test_update.py — Minimal test: apakah page.update() + Canvas bekerja?

import flet as ft
import asyncio
import math
from flet.canvas import Canvas, Arc, Circle


async def main(page: ft.Page):
    page.bgcolor = "#1A1A2E"
    count = 0
    running = False

    size = 250
    center = size / 2
    radius = 110

    def make_shapes():
        progress = count / 60  # 0..1
        sweep = progress * 2 * math.pi
        start = -math.pi / 2

        bg = ft.Paint(color="#2A2A3E", stroke_width=4,
                      style=ft.PaintingStyle.STROKE, stroke_cap=ft.StrokeCap.ROUND)
        fg = ft.Paint(color="#E05A4E", stroke_width=8,
                      style=ft.PaintingStyle.STROKE, stroke_cap=ft.StrokeCap.ROUND)

        shapes = [Circle(center, center, radius, bg)]
        if sweep > 0:
            shapes.append(Arc(center - radius, center - radius,
                              radius * 2, radius * 2, start, sweep, fg))
        return shapes

    canvas = Canvas(shapes=make_shapes(), width=size, height=size)
    timer_text = ft.Text(f"{count}", size=48, color="white", weight=ft.FontWeight.BOLD)
    status_text = ft.Text("Stopped", size=16, color="#A0A0B0")

    def refresh():
        timer_text.value = f"{count}"
        status_text.value = "Running" if running else "Stopped"
        canvas.shapes = make_shapes()
        page.update()

    def toggle(e):
        nonlocal running
        running = not running
        refresh()

    def reset(e):
        nonlocal count, running
        count = 0
        running = False
        refresh()

    page.add(
        ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Stack(
                    controls=[
                        canvas,
                        ft.Container(
                            width=size, height=size,
                            alignment=ft.Alignment.CENTER,
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[timer_text, status_text],
                            ),
                        ),
                    ],
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.ElevatedButton("Start/Pause", on_click=toggle),
                        ft.ElevatedButton("Reset", on_click=reset),
                    ],
                ),
            ],
        )
    )

    while True:
        await asyncio.sleep(1)
        if running:
            count = (count + 1) % 61
            refresh()


ft.app(target=main)
