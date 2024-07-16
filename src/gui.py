import numpy as np
from PyQt5.QtWidgets import QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QSlider, QRadioButton, QButtonGroup, QGridLayout, QFrame
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from src.preprocessing import AudioPreprocessor
from src.filters.parallel import ParallelFilter
from src.filters.CascadeFilter import CascadeFilter
from src.filters.ShelfFilter import ShelfFilter
from src.filters.PeakNotchFilter import PeakNotchFilter

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class GraphicEqualizer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Graphic Equalizer')
        self.setGeometry(100, 100, 1000, 800)

        self.canvas = MplCanvas(self, width=8, height=6, dpi=100)

        self.load_button = QPushButton('Load Audio File')
        self.load_button.clicked.connect(self.load_audio)

        self.apply_button = QPushButton('Apply Filter')
        self.apply_button.clicked.connect(self.apply_filter)

        self.save_button = QPushButton('Save Processed Audio')
        self.save_button.clicked.connect(self.save_audio)

        self.filter_type_group = QButtonGroup(self)
        self.parallel_radio = QRadioButton('Parallel')
        self.cascade_radio = QRadioButton('Cascade')
        self.filter_type_group.addButton(self.parallel_radio)
        self.filter_type_group.addButton(self.cascade_radio)
        self.parallel_radio.setChecked(True)

        filter_type_layout = QHBoxLayout()
        filter_type_layout.addWidget(QLabel('Filter Type:'))
        filter_type_layout.addWidget(self.parallel_radio)
        filter_type_layout.addWidget(self.cascade_radio)

        self.control_frequencies = [50, 100, 200, 400, 800, 1600, 3200, 6400, 12800]
        self.gain_dB_sliders = []

        sliders_layout = QHBoxLayout()
        for control_freq in self.control_frequencies:
            slider_container = QVBoxLayout()

            label = QLabel(f'{control_freq} Hz')
            label.setAlignment(Qt.AlignCenter)

            slider = QSlider(Qt.Vertical)
            slider.setMinimum(-12)
            slider.setMaximum(12)
            slider.setValue(0)
            slider.setTickPosition(QSlider.TicksBothSides)
            slider.setTickInterval(1)
            slider.setFixedWidth(50)

            slider_container.addWidget(label)
            slider_container.addWidget(slider)
            sliders_layout.addLayout(slider_container)

            self.gain_dB_sliders.append(slider)

        layout = QVBoxLayout()
        layout.addWidget(self.load_button)
        layout.addLayout(filter_type_layout)
        layout.addLayout(sliders_layout)
        layout.addWidget(self.apply_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.canvas)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.samples = None
        self.frame_rate = None
        self.filtered_samples = None

    def load_audio(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Audio File", "", "Audio Files (*.wav *.mp3 *.flac)", options=options)
        if file_path:
            self.audio_preprocessor = AudioPreprocessor(file_path)
            self.samples, self.frame_rate = self.audio_preprocessor.process_audio()
            self.plot_spectrum(self.samples, self.frame_rate)

    def plot_spectrum(self, samples, frame_rate):
        N = len(samples)
        T = 1.0 / frame_rate
        yf = np.fft.fft(samples)
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)

        self.canvas.ax.clear()
        self.canvas.ax.plot(xf, 2.0/N * np.abs(yf[:N//2]))
        self.canvas.ax.set_xlabel('Frequency (Hz)')
        self.canvas.ax.set_ylabel('Amplitude')
        self.canvas.ax.set_title('Frequency Spectrum')

        self.canvas.draw()

    def apply_filter(self):
        if self.samples is not None:
            gains_dB = [slider.value() for slider in self.gain_dB_sliders]
            gains_B = [gain_dB / 10 for gain_dB in gains_dB]
            gains = np.pow(10, gains_B)
            if self.parallel_radio.isChecked():
                filter = ParallelFilter(self.control_frequencies, gains)
            else:
                filter = CascadeFilter(self.control_frequencies, gains, 20)

            filtered_samples = filter.apply(self.samples, self.frame_rate)
            self.plot_spectrum(filtered_samples, self.frame_rate)
            self.filtered_samples = filtered_samples

    def save_audio(self):
        if self.filtered_samples is not None:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Processed Audio", "", "WAV Files (*.wav)", options=options)
            if file_path:
                self.audio_preprocessor.save_audio(self.filtered_samples, self.frame_rate * 2, file_path) # Not sure exactly why we need to double the frame rate but we do. -KH
