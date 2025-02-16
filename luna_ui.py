import sys
import os
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt5.QtGui import QFont, QPainter, QBrush, QColor, QMovie


class AssistantUI(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(500,300,400,500)
        
        self.label = QLabel("Listening....", self)
        self.label.setFont(QFont("Arial", 12, QFont.Bold))
        self.label.setGeometry(100, 350, 150, 40)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("Color:lightblue;")
        
        self.dots = QLabel("● ● ●", self)
        self.dots.setFont(QFont("Arial",18))
        self.dots.setGeometry(190, 350, 150, 40)
        self.dots.setAlignment(Qt.AlignCenter)
        self.dots.setStyleSheet("color:lightblue;")
        
        
        self.luna_gif = QLabel(self)
        gif_path = "talking.gif"
        
        if os.path.exists(gif_path):
            self.movie = QMovie(gif_path)
            self.luna_gif.setMovie(self.movie)
            self.luna_gif.setScaledContents(True)
            self.luna_gif.setGeometry(50,50,300,300)
            self.movie.start()
        
        else:
            self.luna_gif.setText("gif not found")
            self.luna_gif.setGeometry(100,100,200, 200)
            self.luna_gif.setAlignment(Qt.AlignCenter)
            self.luna_gif.setStyleSheet("color: red;")
            
            
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(1000)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.start()
        
        self.start_dot_animation()
        self.show()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        brush = QBrush(QColor(30, 30, 30, 220))  # Dark translucent background
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 30, 30)
        
    
    def start_dot_animation(self):
        self.dots_texts =  ["● ○ ○", "● ● ○", "● ● ●", "○ ● ●", "○ ○ ●", "○ ○ ○"]
        self.current_index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_dots)
        self.timer.start(300)

    
    def update_dots(self):
        self.dots.setText(self.dots_texts[self.current_index])
        self.current_index = (self.current_index + 1 ) % len(self.dots_texts)
        

    def update_text(self, text):
        self.label.setText(text)
        
    def close_after(self, seconds):
        QTimer.singleShot(seconds * 1000, self.close)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    assistant = AssistantUI()
    sys.exit(app.exec_())
            
        
        
