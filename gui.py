import sys
from PyQt4 import Qt, QtGui, QtCore
from ui import Ui_MainWindow
import string
from monoalphabetic_cypher_tools import cypher_decriptor


class DecrypterWindow(QtGui.QMainWindow):
    def __init__(self):
        """
        Initializes the DecrypterWindow
        """

        super(DecrypterWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # connect event handlers
        self.ui.connectCalibrateButton(self.calibrateButtonHandler)
        self.ui.connectImportButton(self.importButtonHandler)
        self.ui.connectExportButton(self.exportButtonHandler)
        self.ui.connectTextModified(self.editModifiedHandler)

        self.decrypter = None

        self.show()

    def calibrateButtonHandler(self):
        # get path to calibration file
        filename = QtGui.QFileDialog.getOpenFileName(self)

        # pass path to new cypher_decriptor object
        self.decrypter = cypher_decriptor(filename)

    def importButtonHandler(self):
        # get path to ciphertext
        filename = QtGui.QFileDialog.getOpenFileName(self)

        # display ciphertext in upper pane
        with open(filename) as f:
            ciphertext = f.read()
            self.ui.ciphertext.setPlainText(QtCore.QString(ciphertext))

        # pass path to self.decrypter.guess_initial_mappings
        self.decrypter.guess_initial_mappings(filename)

        # display mappings
        mappings = self.decrypter.get_mapping()
        for k, v in self.ui.edit:
            v.setText(QtCore.QString(mappings[k]))

        # call self.decrypter.decrypt
        plaintext = self.decrypter.decrypt()

        # show results in lower pane
        self.ui.plaintext.setPlainText(QtCore.QString(plaintext))

    def exportButtonHandler(self):
        # save plaintext as file
        filename = QtGui.QFileDialog.getSaveFileName(self)
        with open(filename, 'w') as f:
            f.write(self.decrypter.decrypt())

    def editModifiedHandler(self):
        mappings = { c: str(self.ui.edit[c].text()) for c in string.uppercase }
        self.decrypter.set_mapping(mappings)




def main():
    """
    The main method
    """
    app = QtGui.QApplication(sys.argv)
    win = DecrypterWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
