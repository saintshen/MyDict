from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QDialog
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QUrl

import sys
import os
import reader
from pathlib import Path
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput


class SearchBar(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("MyDict")
        self.resize(120, 32)
        self.setWindowOpacity(0.4)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        central_widget = QWidget()
        # This container holds the window contents, so we can style it.
        central_widget.setObjectName("Container")
        central_widget.setStyleSheet("""#Container {
            background: qlineargradient(x1:0 y1:0, x2:1 y2:1, stop:0 #051c2a stop:1 #44315f);
            border-radius: 10px;
        }""")
        self.search_input = QLineEdit(self)
        self.search_input.returnPressed.connect(self.search)
        
        
        centra_widget_layout = QVBoxLayout()
        centra_widget_layout.setContentsMargins(10,6,10,6)
        centra_widget_layout.addWidget(self.search_input)
        
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
        CURRENT_DIRECTORY = Path(__file__).resolve().parent
        filename = os.fspath(CURRENT_DIRECTORY / ".dict/data/entry.html")
        url = QUrl.fromLocalFile(filename)
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(record)
        
        # self.webview.load(url)
        viewer = DictViewer(self, url)
        viewer.exec()
 
class DictViewer(QDialog):
    def __init__(self, parent=None, url=None):
        super().__init__(parent)
        self.setWindowIcon(QIcon("assets/dictionary.svg"))
        self.setWindowTitle("MyDict")
        self.view = QWebEngineView()
        self.view.setPage(CustomWebEnginePage(self))
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)
        self.resize(800, 600)
        if url:
            self.view.load(url)       

class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def acceptNavigationRequest(self, url, type, isMainFrame):
        print(type)
        if type == QWebEnginePage.NavigationType.NavigationTypeLinkClicked:
            if url.scheme() == "sound":
                print(url.path())
                
                player = self.play_sound(".dict/data/" + url.host() + url.path())
                player.play()
            return False
        return super().acceptNavigationRequest(url, type, isMainFrame)
    
    def play_sound(self, audio_file):
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        print(audio_file)
        self.player.setSource(QUrl.fromLocalFile(audio_file))
        self.audio_output.setVolume(50)
        return self.player
   
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SearchBar()
    window.show()
    app.exec()