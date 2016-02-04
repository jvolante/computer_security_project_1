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
        self.ui.calibrateButton.clicked.connect(self.calibrateButtonHandler)
        self.ui.importButton.clicked.connect(self.importButtonHandler)
        self.ui.exportButton.clicked.connect(self.exportButtonHandler)
        for c in string.lowercase:
            self.ui.edit[c].textEdited.connect(self.editModifiedHandler)

        # disable unavailable functionality
        self.ui.importButton.setDisabled(True)
        self.ui.exportButton.setDisabled(True)
        for c in string.lowercase:
            self.ui.edit[c].setDisabled(True)

        self.decrypter = None

        self.show()

    def calibrateButtonHandler(self):
        # get path to calibration file
        filename = QtGui.QFileDialog.getOpenFileName(self)

        # pass path to new cypher_decriptor object
        self.decrypter = cypher_decriptor(filename)

        # enable import button
        self.ui.importButton.setDisabled(False)

    def importButtonHandler(self):
        # get path to ciphertext
        filename = QtGui.QFileDialog.getOpenFileName(self)

        # pass path to self.decrypter.guess_initial_mappings
        self.decrypter.guess_initial_mappings(filename)

        # display ciphertext in upper pane
        # with open(filename) as f:
        #     ciphertext = f.read()
        self.ui.ciphertext.setPlainText(QtCore.QString(self.decrypter.cypher_text))

        # display mappings
        mappings = self.decrypter.get_mapping()
        for k, v in self.ui.edit.iteritems():
            v.setText(QtCore.QString(mappings[k]))

        # call self.decrypter.decrypt
        plaintext = self.decrypter.decrypt()

        # show results in lower pane
        self.ui.plaintext.setPlainText(QtCore.QString(plaintext))

        # enable export button and editing mappings
        self.ui.exportButton.setDisabled(False)
        for c in string.lowercase:
            self.ui.edit[c].setDisabled(False)

    def exportButtonHandler(self):
        # save plaintext as file
        filename = QtGui.QFileDialog.getSaveFileName(self)
        with open(filename, 'w') as f:
            f.write(self.decrypter.decrypt())

    def editModifiedHandler(self):
        mappings = { c: str(self.ui.edit[c].text()) for c in string.lowercase }
        self.decrypter.set_mapping(mappings)
        plaintext = self.decrypter.decrypt()
        self.ui.plaintext.setPlainText(plaintext)




def main():
    """
    The main method
    """
    app = QtGui.QApplication(sys.argv)
    win = DecrypterWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
