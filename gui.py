import sys
from PyQt4 import Qt, QtGui, QtCore
from ui import Ui_MainWindow


class DecrypterWindow(QtGui.QMainWindow):
    def __init__(self):
        super(DecrypterWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()


def main():
    app = QtGui.QApplication(sys.argv)
    win = DecrypterWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
