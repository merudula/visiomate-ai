from datetime import datetime
from visiomate.reminders import parse_time, parse_reminder, ReminderStore


def test_parse_time():
    assert parse_time("at 8:30 pm") == "20:30"
    assert parse_time("at 8 a.m.") == "08:00"
    assert parse_time("at 12 am") == "00:00"
    assert parse_time("at 14:05") == "14:05"
    assert parse_time("no time here") is None


def test_parse_reminder():
    assert parse_reminder("remind me to take bp tablet at 8:30 pm") == ("take bp tablet", "20:30")


def test_due_fires_once_per_day(tmp_path):
    s = ReminderStore(str(tmp_path / "r.db"))
    s.add("take tablet", "09:00")
    now = datetime(2026, 1, 1, 9, 0)
    assert s.due(now) == ["take tablet"]
    assert s.due(now) == []
