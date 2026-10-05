"""Emergency SOS: SMS via Twilio and/or Telegram, with a Google Maps location link.

Set secrets as environment variables (never commit them):
  TWILIO_SID, TWILIO_TOKEN, TWILIO_FROM       -> SMS
  TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID        -> Telegram
"""
import requests
from .utils import env
from .navigation import get_location


def send_sos(cfg: dict) -> str:
    loc = get_location(cfg)
    link = f"https://maps.google.com/?q={loc[0]},{loc[1]}" if loc else "location unavailable"
    msg = f"EMERGENCY! A VisioMate user needs help. Location: {link}"
    sent = []

    sid, tok, frm = env("TWILIO_SID"), env("TWILIO_TOKEN"), env("TWILIO_FROM")
    if sid and tok and frm:
        for number in cfg["sos"]["contacts"]:
            try:
                r = requests.post(
                    f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json",
                    auth=(sid, tok), data={"To": number, "From": frm, "Body": msg}, timeout=10)
                if r.ok:
                    sent.append(number)
            except requests.RequestException:
                pass

    bot, chat = env("TELEGRAM_BOT_TOKEN"), env("TELEGRAM_CHAT_ID")
    if bot and chat:
        try:
            r = requests.post(f"https://api.telegram.org/bot{bot}/sendMessage",
                              data={"chat_id": chat, "text": msg}, timeout=10)
            if r.ok:
                sent.append("telegram")
        except requests.RequestException:
            pass

    if sent:
        return "Emergency alert sent to your contacts with your location."
    return "I could not send the alert. Please check internet and SOS settings."
