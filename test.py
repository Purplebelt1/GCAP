import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap, QPainter

class ComponentButtonClass(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QPixmap("image1.svg")  # Load the SVG image

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.image.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 App")
        self.setMinimumSize(QSize(400, 300))
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        component_button = ComponentButtonClass()
        layout.addWidget(component_button)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
