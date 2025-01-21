
import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
import reader

if __name__ == "__main__":
    app = QApplication([])
    filename = ".dict/data/hwd/ame/2/welcome1.mp3"
    player = QMediaPlayer()
    audio_output = QAudioOutput()
    player.setAudioOutput(audio_output)
    player.setSource(QUrl.fromLocalFile(filename))
    audio_output.setVolume(50)
    player.play()
    
    record = reader.query('.dict/LDOCE6.mdx', "@etymologies_welcome_1")
    print(record)    
    sys.exit(app.exec())