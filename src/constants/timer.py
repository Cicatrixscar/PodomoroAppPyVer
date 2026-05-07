# timer.py — Durasi default timer (dalam detik)

# Mode timer
MODE_POMODORO = "pomodoro"
MODE_SHORT_BREAK = "short_break"
MODE_LONG_BREAK = "long_break"

# Durasi dalam detik
DURATIONS = {
    MODE_POMODORO: 25 * 60,      # 25 menit
    MODE_SHORT_BREAK: 5 * 60,    # 5 menit
    MODE_LONG_BREAK: 15 * 60,    # 15 menit
}

# Label untuk UI
MODE_LABELS = {
    MODE_POMODORO: "Pomodoro",
    MODE_SHORT_BREAK: "Short Break",
    MODE_LONG_BREAK: "Long Break",
}

# Jumlah sesi pomodoro sebelum long break
SESSIONS_BEFORE_LONG_BREAK = 4
