from sys import argv, exit as sys_exit

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from mmcp.ui.MainWindow import MainWindow

# pyinstaller --onefile --windowed --icon="media\images\icon.ico" "mmcp\ui\MainWindow.py"
if __name__ == "__main__":
    app = QApplication(argv)
    icon_path = r".\media\images\icon.ico"
    app.setWindowIcon(QIcon(icon_path))
    window = MainWindow()
    window.show()
    sys_exit(app.exec_())
