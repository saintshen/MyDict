from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWebEngineWidgets import QWebEngineView
import sys
import reader


class MyDict(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("MyDict")
        self.resize(500, 500)
        self.setWindowOpacity(0.4)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        central_widget = QWidget()
        # This container holds the window contents, so we can style it.
        central_widget.setObjectName("Container")
        central_widget.setStyleSheet("""#Container {
            background: qlineargradient(x1:0 y1:0, x2:1 y2:1, stop:0 #051c2a stop:1 #44315f);
            border-radius: 20px;
        }""")
        self.search_input = QLineEdit(self)
        self.search_input.returnPressed.connect(self.search)
        self.webview = QWebEngineView()
        
        work_space_layout = QVBoxLayout()
        # work_space_layout.setContentsMargins(11, 11, 11, 11)
        work_space_layout.addWidget(self.webview)
        
        centra_widget_layout = QVBoxLayout()
        centra_widget_layout.setContentsMargins(10,10,10,10)
        # centra_widget_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        centra_widget_layout.addWidget(self.search_input)
        centra_widget_layout.addLayout(work_space_layout)
        
        central_widget.setLayout(centra_widget_layout)
        self.setCentralWidget(central_widget)
       
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.initial_pos = event.position().toPoint()
        super().mousePressEvent(event)
        event.accept()        
            
    def mouseMoveEvent(self, event):
        if self.initial_pos is not None:
            delta = event.position().toPoint() - self.initial_pos
            self.window().move(
                self.window().x() + delta.x(),
                self.window().y() + delta.y(),
            )
        super().mouseMoveEvent(event)
        event.accept()     
    
    def mouseReleaseEvent(self, event):
        self.initial_pos = None
        super().mouseReleaseEvent(event)
        event.accept()         
    
    def event(self, event):
        if event.type() == event.Type.HoverEnter:
            self.setWindowOpacity(1)
        elif event.type() == event.Type.HoverLeave:
            self.setWindowOpacity(0.4)
        return super().event(event)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def search(self):
        value = self.search_input.text()
        record = reader.query('.dict/LDOCE6.mdx', value)
        self.webview.setHtml(record)
        self.webview.show()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyDict()
    window.show()
    app.exec()