from collections import OrderedDict


class ObjectDetector:
    def __init__(self, model="yolov8n.pt", confidence=0.45):
        from ultralytics import YOLO
        self.model = YOLO(model)
        self.conf = confidence

    def describe(self, frame) -> str:
        res = self.model(frame, conf=self.conf, verbose=False)[0]
        h, w = frame.shape[:2]
        found = []
        for b in res.boxes:
            name = res.names[int(b.cls)]
            x1, y1, x2, y2 = b.xyxy[0].tolist()
            cx = (x1 + x2) / 2 / w
            area = (x2 - x1) * (y2 - y1) / (w * h)
            side = "on your left" if cx < 0.33 else "on your right" if cx > 0.66 else "in front of you"
            dist = "very close" if area > 0.35 else "nearby" if area > 0.10 else "far away"
            found.append((area, f"{name} {side}, {dist}"))
        if not found:
            return "I cannot see any clear objects."
        found.sort(reverse=True)
        top = list(OrderedDict.fromkeys(s for _, s in found))[:5]
        warn = "Careful! " if any("very close" in s for s in top) else ""
        return warn + "I can see " + "; ".join(top) + "."
