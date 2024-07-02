import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from pydub import AudioSegment
from scipy.fftpack import fft

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class GraphicEqualizer(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Graphic Equalizer')
        self.setGeometry(100, 100, 800, 600)

        self.canvas = MplCanvas(self, width=8, height=6, dpi=100)

        self.load_button = QPushButton('Load Audio File')
        self.load_button.clicked.connect(self.load_audio)

        layout = QVBoxLayout()
        layout.addWidget(self.load_button)
        layout.addWidget(self.canvas)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_audio(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Audio File", "", "Audio Files (*.wav *.mp3 *.flac)", options=options)
        if file_path:
            self.audio = AudioSegment.from_file(file_path)
            self.process_audio()

    def process_audio(self):
        samples = self.audio.get_array_of_samples()
        samples = np.array(samples).astype(np.float32)

        N = len(samples)
        T = 1.0 / self.audio.frame_rate
        yf = fft(samples)
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)

        self.canvas.ax.clear()
        self.canvas.ax.plot(xf, 2.0/N * np.abs(yf[:N//2]))
        self.canvas.ax.set_xlabel('Frequency (Hz)')
        self.canvas.ax.set_ylabel('Amplitude')
        self.canvas.ax.set_title('Frequency Spectrum')

        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = GraphicEqualizer()
    main_win.show()
    sys.exit(app.exec_())
