from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWebEngineWidgets import QWebEngineView
import sys
import reader

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dictor")
        self.setWindowOpacity(0.4)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.resize(500, 600)
        self.setMouseTracking(True)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover)
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search")
        self.search_input.returnPressed.connect(self.on_search)
        self.webview = QWebEngineView(self)
        layout = QVBoxLayout()
        layout.addWidget(self.search_input)
        layout.addWidget(self.webview)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.old_pos = None
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.position().toPoint()
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = QPoint(event.position().toPoint() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.position().toPoint()
    
    def event(self, event):
        if event.type() == event.Type.HoverEnter:
            self.setWindowOpacity(1)
        elif event.type() == event.Type.HoverLeave:
            self.setWindowOpacity(0.3)
        return super().event(event)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def on_search(self):
        value = self.search_input.text()
        record = reader.query('LDOCE6.mdx', value)
        
        self.webview.setHtml(record)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())