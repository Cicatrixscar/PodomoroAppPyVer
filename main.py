# main.py — Entry point Pomodoro App

import flet as ft
import asyncio
import math
import os
import sys
import threading
import time

try:
    import flet_audio
except ImportError:
    flet_audio = None

from src.constants.theme import (
    PRIMARY_COLOR,
    BG_COLOR,
    BG_CARD,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    COLOR_POMODORO,
    COLOR_SHORT_BREAK,
    COLOR_LONG_BREAK,
    TIMER_CIRCLE_SIZE,
    TIMER_CIRCLE_STROKE,
    TIMER_BG_STROKE,
    BORDER_RADIUS_LG,
    BORDER_RADIUS_XL,
    SHADOW_BLUR,
    SHADOW_COLOR,
)
from src.constants.timer import (
    MODE_POMODORO,
    MODE_SHORT_BREAK,
    MODE_LONG_BREAK,
    MODE_LABELS,
    DURATIONS,
)
from src.utils.timer_logic import TimerState
from src.utils.storage import get_today_sessions, increment_sessions

MODE_COLORS = {
    MODE_POMODORO: COLOR_POMODORO,
    MODE_SHORT_BREAK: COLOR_SHORT_BREAK,
    MODE_LONG_BREAK: COLOR_LONG_BREAK,
}


def is_mobile():
    return hasattr(sys, "getandroidapilevel") or sys.platform == "ios"


async def main(page: ft.Page):
    page.title = "🍅 Pomodoro"
    page.bgcolor = BG_COLOR
    page.theme = ft.Theme(color_scheme_seed=PRIMARY_COLOR)
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0  # Padding dipindah ke dalam SafeArea agar bisa scroll penuh
    page.scroll = ft.ScrollMode.AUTO

    # ── State ─────────────────────────────────────────────
    timer = TimerState()
    sessions_today = await get_today_sessions(page)

    # ── Audio ─────────────────────────────────────────────
    stop_alarm_event = threading.Event()
    
    if is_mobile() and flet_audio is not None:
        try:
            audio_ctrl = flet_audio.Audio(
                src="alarm.mp3", 
                autoplay=False, 
                volume=1.0,
                release_mode=flet_audio.ReleaseMode.LOOP
            )
            page.overlay.append(audio_ctrl)
            def play_alarm():
                try:
                    audio_ctrl.play()
                except Exception:
                    pass
            def stop_alarm():
                try:
                    audio_ctrl.pause()
                except Exception:
                    pass
        except ImportError:
            def play_alarm(): pass
            def stop_alarm(): pass
    else:
        alarm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "alarm.mp3")
        def play_alarm():
            stop_alarm_event.clear()
            def _play():
                try:
                    if sys.platform == "win32":
                        import winsound
                        try:
                            # Loop native via SND_LOOP di Windows
                            winsound.PlaySound(alarm_path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
                        except Exception:
                            while not stop_alarm_event.is_set():
                                winsound.Beep(800, 1000)
                                time.sleep(0.5)
                except Exception:
                    pass
            threading.Thread(target=_play, daemon=True).start()
            
        def stop_alarm():
            stop_alarm_event.set()
            try:
                if sys.platform == "win32":
                    import winsound
                    # Hentikan semua suara yang dimainkan secara asinkron
                    winsound.PlaySound(None, winsound.SND_PURGE)
            except Exception:
                pass

    # ── Helper ────────────────────────────────────────────
    def current_color():
        return MODE_COLORS.get(timer.current_mode, COLOR_POMODORO)

    # ══════════════════════════════════════════════════════
    # BUILD UI — menggunakan ProgressRing untuk menghindari bug Canvas Flet di Windows
    # ══════════════════════════════════════════════════════
    timer_size = TIMER_CIRCLE_SIZE

    bg_ring = ft.ProgressRing(
        width=timer_size,
        height=timer_size,
        stroke_width=TIMER_BG_STROKE,
        value=1.0,
        color="#2A2A3E",
    )

    fg_ring = ft.ProgressRing(
        width=timer_size,
        height=timer_size,
        stroke_width=TIMER_CIRCLE_STROKE,
        color=current_color(),
        bgcolor="transparent",
        value=1.0 - timer.progress,  # Berkurang dari 1.0 ke 0.0
        stroke_cap=ft.StrokeCap.ROUND,
    )

    time_text = ft.Text(
        value=timer.display_time,
        size=48,
        weight=ft.FontWeight.BOLD,
        color=TEXT_PRIMARY,
    )
    mode_label_text = ft.Text(
        value=MODE_LABELS[timer.current_mode],
        size=14,
        color=TEXT_SECONDARY,
    )

    timer_display = ft.Stack(
        width=timer_size,
        height=timer_size,
        controls=[
            ft.Container(content=bg_ring, alignment=ft.Alignment.CENTER),
            ft.Container(content=fg_ring, alignment=ft.Alignment.CENTER),
            ft.Container(
                width=timer_size,
                height=timer_size,
                alignment=ft.Alignment.CENTER,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=4,
                    controls=[time_text, mode_label_text],
                ),
            ),
        ],
    )

    # --- Mode Selector ---
    mode_buttons = {}
    mode_texts = {}
    for mode in [MODE_POMODORO, MODE_SHORT_BREAK, MODE_LONG_BREAK]:
        is_sel = mode == timer.current_mode
        color = MODE_COLORS[mode]
        txt = ft.Text(
            MODE_LABELS[mode], size=12,
            weight=ft.FontWeight.W_600 if is_sel else ft.FontWeight.W_400,
            color=TEXT_PRIMARY if is_sel else TEXT_SECONDARY,
        )
        cont = ft.Container(
            content=txt,
            bgcolor=color if is_sel else "transparent",
            border_radius=BORDER_RADIUS_LG,
            padding=ft.Padding.symmetric(horizontal=10, vertical=8),
            on_click=lambda e, m=mode: on_mode_change(m),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            ink=True,
        )
        mode_buttons[mode] = cont
        mode_texts[mode] = txt

    mode_row = ft.Container(
        content=ft.Row(
            controls=[mode_buttons[m] for m in [MODE_POMODORO, MODE_SHORT_BREAK, MODE_LONG_BREAK]],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=4,
        ),
        bgcolor="#1E1E32",
        border_radius=BORDER_RADIUS_LG,
        padding=4,
    )

    # --- Control Buttons (Container-based, NO ElevatedButton/Icon) ---
    start_label = ft.Text(
        "▶  Start", size=16, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY,
    )

    start_btn = ft.Container(
        content=start_label,
        bgcolor=current_color(),
        border_radius=BORDER_RADIUS_XL,
        padding=ft.Padding.symmetric(horizontal=36, vertical=14),
        on_click=lambda e: on_start_pause(),
        ink=True,
        animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
        shadow=ft.BoxShadow(blur_radius=8, color=current_color()),
    )

    reset_label = ft.Text("↺", size=22, color="#A0A0B0")
    reset_btn = ft.Container(
        content=reset_label,
        bgcolor="#2A2A3E",
        border_radius=100,
        width=48, height=48,
        alignment=ft.Alignment.CENTER,
        on_click=lambda e: on_reset(),
        ink=True,
    )

    skip_label = ft.Text("⏭", size=20, color="#A0A0B0")
    skip_btn = ft.Container(
        content=skip_label,
        bgcolor="#2A2A3E",
        border_radius=100,
        width=48, height=48,
        alignment=ft.Alignment.CENTER,
        on_click=lambda e: on_skip(),
        ink=True,
    )

    controls_row = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=16,
        controls=[reset_btn, start_btn, skip_btn],
    )

    # --- Stats Card ---
    sessions_text = ft.Text(str(sessions_today), size=20, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)
    focus_text = ft.Text(f"{sessions_today * 25}m", size=20, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)

    def streak_emoji(s):
        if s >= 8: return "🔥🔥🔥"
        elif s >= 4: return "🔥🔥"
        elif s >= 1: return "🔥"
        return "—"

    streak_text = ft.Text(streak_emoji(sessions_today), size=20, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)

    stats_card = ft.Container(
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text("📊 Statistik Hari Ini", size=16, weight=ft.FontWeight.W_600, color=TEXT_PRIMARY),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    controls=[
                        ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4, controls=[
                            ft.Text("✅", size=22),
                            sessions_text,
                            ft.Text("Sesi Selesai", size=11, color=TEXT_SECONDARY),
                        ]),
                        ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4, controls=[
                            ft.Text("⏱", size=22),
                            focus_text,
                            ft.Text("Waktu Fokus", size=11, color=TEXT_SECONDARY),
                        ]),
                        ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4, controls=[
                            ft.Text("🔥", size=22),
                            streak_text,
                            ft.Text("Streak", size=11, color=TEXT_SECONDARY),
                        ]),
                    ],
                ),
            ],
        ),
        bgcolor=BG_CARD,
        border_radius=BORDER_RADIUS_LG,
        padding=ft.Padding.all(20),
        shadow=ft.BoxShadow(blur_radius=SHADOW_BLUR, color=SHADOW_COLOR),
    )

    # ══════════════════════════════════════════════════════
    # REFRESH UI
    # ══════════════════════════════════════════════════════
    def refresh_ui():
        nonlocal sessions_today
        # 1. Timer
        time_text.value = timer.display_time
        mode_label_text.value = MODE_LABELS[timer.current_mode]

        # 2. Progress Ring
        fg_ring.value = 1.0 - timer.progress
        fg_ring.color = current_color()

        # 3. Start button
        start_label.value = "⏸  Pause" if timer.is_running else "▶  Start"
        start_btn.bgcolor = current_color()

        # 4. Mode buttons
        for mode in [MODE_POMODORO, MODE_SHORT_BREAK, MODE_LONG_BREAK]:
            is_sel = mode == timer.current_mode
            col = MODE_COLORS[mode]
            mode_buttons[mode].bgcolor = col if is_sel else "transparent"
            mode_texts[mode].weight = ft.FontWeight.W_600 if is_sel else ft.FontWeight.W_400
            mode_texts[mode].color = TEXT_PRIMARY if is_sel else TEXT_SECONDARY

        # 5. Stats
        sessions_text.value = str(sessions_today)
        focus_text.value = f"{sessions_today * 25}m"
        streak_text.value = streak_emoji(sessions_today)

        page.update()

    # ══════════════════════════════════════════════════════
    # CALLBACKS
    # ══════════════════════════════════════════════════════
    def on_start_pause():
        stop_alarm()
        if timer.is_running:
            timer.pause()
        else:
            timer.start()
        refresh_ui()

    def on_reset():
        stop_alarm()
        timer.reset()
        refresh_ui()

    def on_mode_change(mode):
        stop_alarm()
        timer.set_mode(mode)
        refresh_ui()

    async def on_timer_complete(completed_mode, completed_sessions_count):
        nonlocal sessions_today
        play_alarm()

        snack = ft.SnackBar(
            content=ft.Text("⏰ Timer selesai!", size=16, color=TEXT_PRIMARY),
            bgcolor=current_color(),
            open=True,
        )
        page.overlay.append(snack)

        if completed_mode == MODE_POMODORO:
            sessions_today = await increment_sessions(page)

        timer.advance_to_next_mode()
        refresh_ui()

    def on_skip():
        stop_alarm()
        timer.advance_to_next_mode()
        refresh_ui()

    timer.set_callbacks(
        on_complete=lambda mode, count: asyncio.ensure_future(on_timer_complete(mode, count)),
    )

    # ══════════════════════════════════════════════════════
    # LAYOUT
    # ══════════════════════════════════════════════════════
    page.add(
        ft.SafeArea(
            content=ft.Container(
                alignment=ft.Alignment.CENTER,
                padding=ft.Padding.symmetric(horizontal=20, vertical=20),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=24,
                    controls=[
                        ft.Text("🍅 Pomodoro", size=28, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                        ft.Container(height=8),
                        mode_row,
                        ft.Container(height=8),
                        timer_display,
                        ft.Container(height=16),
                        controls_row,
                        ft.Container(height=16),
                        stats_card,
                    ],
                )
            )
        )
    )

    # ── Timer Loop ──────────────────────────────────────
    while True:
        await asyncio.sleep(1)
        ticked = timer.tick()
        if ticked:
            refresh_ui()


ft.app(target=main, assets_dir="assets")

