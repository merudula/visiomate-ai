import os


class CurrencyRecognizer:
    """Indian currency note recognition using a custom YOLOv8 model.

    Train a model on INR note images (classes like '10','20','50','100','200','500','2000')
    and put the weights at models/inr_currency.pt. See README -> Training.
    """

    def __init__(self, model="models/inr_currency.pt", confidence=0.6):
        self.available = os.path.exists(model)
        self.conf = confidence
        if self.available:
            from ultralytics import YOLO
            self.model = YOLO(model)

    def describe(self, frame) -> str:
        if not self.available:
            return "Currency model is not installed yet. Please add the trained weights file."
        res = self.model(frame, conf=self.conf, verbose=False)[0]
        values = []
        for b in res.boxes:
            label = res.names[int(b.cls)]
            digits = "".join(c for c in label if c.isdigit())
            if digits:
                values.append(int(digits))
        if not values:
            return "I could not recognise a note. Hold it flat, closer to the camera."
        notes = ", ".join(f"{v} rupees" for v in values)
        return f"I see {notes}. Total is {sum(values)} rupees."
