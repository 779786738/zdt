import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import main_widge

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui_main = main_widge.Ui_MainWindow()
    ui_main.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
