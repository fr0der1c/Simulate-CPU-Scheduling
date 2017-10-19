import mainwindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem

app = QApplication(sys.argv)
UI_main_window = mainwindow.Ui_MainWindow()
window = QMainWindow()
UI_main_window.setupUi(window)


def slotStartButton():
    item = QTableWidgetItem("haha")
    UI_main_window.JobPoolTable.setRowCount(2)
    UI_main_window.JobPoolTable.setItem(1, 1, item)
    print("re")


UI_main_window.StartButton.clicked.connect(slotStartButton)

window.show()

exit(app.exec_())
