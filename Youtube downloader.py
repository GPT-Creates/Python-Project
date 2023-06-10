import sys
import pytube
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout

class Downloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Input for URL
        self.url_input = QLineEdit()
        # Search button
        search_button = QPushButton('Search')
        search_button.clicked.connect(self.search)
        # Label for available formats
        self.formats_label = QLabel('Available Formats:')
        # ComboBox for available formats
        self.formats_combobox = QComboBox()
        self.formats_combobox.activated[str].connect(self.onActivated)
        # Input for save location
        self.location_input = QLineEdit()
        # Download button
        download_button = QPushButton('Download')
        download_button.clicked.connect(self.download)

        # Create vertical layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.url_input)
        vbox.addWidget(search_button)
        vbox.addWidget(self.formats_label)
        vbox.addWidget(self.formats_combobox)
        vbox.addWidget(self.location_input)
        vbox.addWidget(download_button)

        self.setLayout(vbox)

        self.setWindowTitle('YouTube Video Downloader')
        self.show()

    def search(self):
        url = self.url_input.text()
        video = pytube.YouTube(url)
        self.formats_combobox.clear()
        for stream in video.streams:
            self.formats_combobox.addItem(stream.mime_type + ' (' + str(stream.resolution) + ')')

    def onActivated(self, text):
        self.selected_format = text

    def download(self):
        url = self.url_input.text()
        video = pytube.YouTube(url)
        location = self.location_input.text()
        stream = video.streams.filter(mime_type=self.selected_format.split()[0]).first()
        stream.download(location)
        self.formats_label.setText('Download complete!')

app = QApplication(sys.argv)
downloader = Downloader()
sys.exit(app.exec_())
