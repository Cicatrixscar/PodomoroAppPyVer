# storage.py — Simpan & baca statistik (page.client_storage)

from datetime import date


def _today_key():
    """Generate storage key untuk hari ini: stats_YYYY-MM-DD."""
    return f"stats_{date.today().isoformat()}"


async def get_today_sessions(page):
    """Baca jumlah sesi selesai hari ini."""
    key = _today_key()
    try:
        value = await page.client_storage.get_async(key)
        if value is not None:
            return int(value)
    except Exception:
        pass
    return 0


async def increment_sessions(page):
    """Tambah 1 sesi selesai hari ini dan return jumlah terbaru."""
    key = _today_key()
    current = await get_today_sessions(page)
    new_count = current + 1
    await page.client_storage.set_async(key, str(new_count))
    return new_count


async def get_volume(page):
    """Baca preferensi volume (0.0 - 1.0)."""
    try:
        value = await page.client_storage.get_async("pref_volume")
        if value is not None:
            return float(value)
    except Exception:
        pass
    return 1.0


async def set_volume(page, volume):
    """Simpan preferensi volume."""
    await page.client_storage.set_async("pref_volume", str(volume))
