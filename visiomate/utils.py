import os
import yaml


def load_config(path: str = "config.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def capture_frame(camera_index: int = 0):
    """Grab a single frame from the camera. Returns a BGR numpy array or None."""
    import cv2
    cap = cv2.VideoCapture(camera_index)
    try:
        for _ in range(5):  # let auto-exposure settle
            cap.read()
        ok, frame = cap.read()
        return frame if ok else None
    finally:
        cap.release()


def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)
