import sys
import os
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QPoint, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QFont, QMovie, QColor, QPainter, QBrush, QPen

class FadingLabel(QLabel):
    """Custom QLabel with opacity animation."""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._opacity = 1.0
        self.setStyleSheet("color: #AEE6FF;")
        self.setWordWrap(True)

    def setOpacity(self, opacity):
        self._opacity = opacity
        self.repaint()

    def getOpacity(self):
        return self._opacity

    opacity = pyqtProperty(float, fget=getOpacity, fset=setOpacity)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(self._opacity)
        super().paintEvent(event)


class AssistantUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(400, 500)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignCenter)

        self.luna_gif = QLabel(self)
        gif_path = "Luna AI.gif"
        if os.path.exists(gif_path):
            self.movie = QMovie(gif_path)
            self.luna_gif.setMovie(self.movie)
            self.luna_gif.setScaledContents(True)
            self.luna_gif.setFixedSize(250, 250)
            self.movie.start()
        else:
            self.luna_gif.setText("GIF not found")
            self.luna_gif.setStyleSheet("color: red; font-size: 14px;")
        layout.addWidget(self.luna_gif, alignment=Qt.AlignCenter)

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.label = FadingLabel("Listening...", self)
        self.label.setFont(QFont("Poppins", 14, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)

        self.dots = QLabel("● ○ ○", self)
        self.dots.setFont(QFont("Arial", 18))
        self.dots.setAlignment(Qt.AlignCenter)
        self.dots.setStyleSheet("color: #AEE6FF;")
        layout.addWidget(self.dots, alignment=Qt.AlignCenter)

        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(1200)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.start()

        self.float_animation = QPropertyAnimation(self, b"pos")
        self.float_animation.setDuration(3000)
        self.float_animation.setStartValue(QPoint(self.x(), self.y()))
        self.float_animation.setEndValue(QPoint(self.x(), self.y() - 10))
        self.float_animation.setEasingCurve(QEasingCurve.InOutSine)
        self.float_animation.setLoopCount(-1)
        self.float_animation.start()

        self.start_dot_animation()
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        brush = QBrush(QColor(25, 25, 25, 240))
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 30, 30)
        pen = QPen(QColor(0, 180, 255, 180), 3)
        painter.setPen(pen)
        painter.drawRoundedRect(rect.adjusted(2, 2, -2, -2), 30, 30)

    def start_dot_animation(self):
        self.dots_texts = ["● ○ ○", "● ● ○", "● ● ●", "○ ● ●", "○ ○ ●"]
        self.current_index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_dots)
        self.timer.start(400)

    def update_dots(self):
        self.dots.setText(self.dots_texts[self.current_index])
        self.current_index = (self.current_index + 1) % len(self.dots_texts)

    def update_text(self, new_text):
        fade_out = QPropertyAnimation(self.label, b"opacity")
        fade_out.setDuration(400)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.InOutSine)

        fade_in = QPropertyAnimation(self.label, b"opacity")
        fade_in.setDuration(400)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.InOutSine)

        def change_text():
            self.label.setText(new_text)

        fade_out.finished.connect(change_text)
        fade_out.finished.connect(fade_in.start)
        fade_out.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    assistant = AssistantUI()
    sys.exit(app.exec_())
