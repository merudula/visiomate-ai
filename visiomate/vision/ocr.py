class TextReader:
    def __init__(self, lang="eng+tam"):
        self.lang = lang

    def read(self, frame) -> str:
        import cv2
        import pytesseract
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 9, 75, 75)
        thr = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY, 31, 15)
        text = pytesseract.image_to_string(thr, lang=self.lang).strip()
        text = " ".join(text.split())
        return text if text else "I could not find any readable text. Please hold the page steady and well lit."
