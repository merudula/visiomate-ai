from visiomate.intents import route_intent


def test_basic_intents():
    assert route_intent("what is in front of me") == "detect"
    assert route_intent("read this text") == "ocr"
    assert route_intent("emergency") == "sos"
    assert route_intent("navigate to Gandhipuram bus stand") == "navigate"
    assert route_intent("is this a 500 rupee note") == "currency"
    assert route_intent("what's the time") == "time"
    assert route_intent("my reminders") == "list_reminders"


def test_tanglish():
    assert route_intent("kaapathunga") == "sos"
    assert route_intent("indha text padi") == "ocr"
    assert route_intent("mathirai remind panu") == "add_reminder"


def test_empty_and_unknown():
    assert route_intent("") == "none"
    assert route_intent("banana pancake") == "unknown"
