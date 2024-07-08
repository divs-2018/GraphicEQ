import sys
from PyQt5.QtWidgets import QApplication
from src.gui import GraphicEqualizer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = GraphicEqualizer()
    main_win.show()
    sys.exit(app.exec_())
