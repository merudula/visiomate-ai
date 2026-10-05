import argparse
from visiomate.utils import load_config
from visiomate.voice import Voice
from visiomate.assistant import Assistant


def main():
    ap = argparse.ArgumentParser(description="VisioMate AI - voice assistant for the visually impaired")
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--text", action="store_true", help="keyboard mode (no microphone/speaker)")
    args = ap.parse_args()

    cfg = load_config(args.config)
    voice = Voice(cfg["language"], cfg["speech_rate"], text_mode=args.text)
    bot = Assistant(cfg, voice)
    wake = cfg.get("wake_word", "visiomate").lower()

    voice.speak("VisioMate is ready. Say help to hear what I can do.")
    while True:
        heard = voice.listen()
        if cfg.get("require_wake_word"):
            if wake not in heard:
                continue
            heard = heard.replace(wake, "").strip()
        if not bot.handle(heard):
            break


if __name__ == "__main__":
    main()
