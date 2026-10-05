"""Medicine reminders: SQLite storage + background scheduler."""
import re
import sqlite3
import threading
import time
from datetime import datetime

_TIME = re.compile(r"(\d{1,2})(?:[:.](\d{2}))?\s*([ap])\.?m\.?|(\d{1,2}):(\d{2})", re.I)
_FILLER = re.compile(r"\b(remind me|reminder|set|add|to|at|please|for)\b", re.I)


def parse_time(text: str):
    m = _TIME.search(text)
    if not m:
        return None
    if m.group(1):
        h, mi, ap = int(m.group(1)), int(m.group(2) or 0), m.group(3).lower()
        if ap == "p" and h < 12:
            h += 12
        if ap == "a" and h == 12:
            h = 0
    else:
        h, mi = int(m.group(4)), int(m.group(5))
    if h > 23 or mi > 59:
        return None
    return f"{h:02d}:{mi:02d}"


def parse_reminder(text: str):
    """'remind me to take bp tablet at 8:30 pm' -> ('take bp tablet', '20:30')"""
    t = parse_time(text)
    if not t:
        return None
    label = _TIME.sub("", text)
    label = " ".join(_FILLER.sub(" ", label).split()) or "your medicine"
    return label, t


class ReminderStore:
    def __init__(self, path="reminders.db"):
        self.path = path
        with self._conn() as c:
            c.execute("""CREATE TABLE IF NOT EXISTS reminders(
                id INTEGER PRIMARY KEY AUTOINCREMENT, label TEXT, at TEXT, last_fired TEXT)""")

    def _conn(self):
        return sqlite3.connect(self.path)

    def add(self, label, at):
        with self._conn() as c:
            c.execute("INSERT INTO reminders(label, at) VALUES(?,?)", (label, at))

    def all(self):
        with self._conn() as c:
            return c.execute("SELECT id, label, at FROM reminders ORDER BY at").fetchall()

    def due(self, now: datetime):
        hhmm, today = now.strftime("%H:%M"), now.strftime("%Y-%m-%d")
        with self._conn() as c:
            rows = c.execute("SELECT id, label FROM reminders WHERE at=? AND IFNULL(last_fired,'')<>?",
                             (hhmm, today)).fetchall()
            for rid, _ in rows:
                c.execute("UPDATE reminders SET last_fired=? WHERE id=?", (today, rid))
        return [label for _, label in rows]


class ReminderScheduler(threading.Thread):
    def __init__(self, store: ReminderStore, speak):
        super().__init__(daemon=True)
        self.store, self.speak = store, speak

    def run(self):
        while True:
            for label in self.store.due(datetime.now()):
                for _ in range(2):
                    self.speak(f"Reminder. It is time to {label}.")
            time.sleep(20)
