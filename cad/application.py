from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from cad.sketch import Sketch


class Application(QMainWindow):

    def __init__(self, *args):
        super().__init__(*args)

        self.sketch = None

        self.__menu = None
        self.__toolBar = None
        self.__toolBarGroup = None

        self.__initSketch()
        self.__initMenuBar()
        self.__initToolBar()
        self.__initStatusBar()
        self.__initGeometry()

        self.setWindowTitle('Sketch')

    def __initSketch(self):
        self.sketch = Sketch(self)
        self.setCentralWidget(self.sketch)

    def __initMenuBar(self):
        self.__menu = self.menuBar()

        file = self.__menu.addMenu('File')
        file.addAction(self.exitAction())
        file.addAction(self.openAction())
        file.addAction(self.saveAction())

        edit = self.__menu.addMenu('Edit')
        edit.addAction(self.undoAction())
        edit.addAction(self.copyAction())
        edit.addAction(self.pasteAction())

    def undoAction(self):
        action = QAction('Undo', self.__menu)
        action.setShortcut('Ctrl+Z')
        action.setStatusTip('Undo')
        action.setToolTip('Undo')
        return action

    def copyAction(self):
        action = QAction('Copy', self.__menu)
        action.setShortcut('Ctrl+C')
        action.setStatusTip('Copy')
        action.setToolTip('Copy')
        return action

    def pasteAction(self):
        action = QAction('Paste', self.__menu)
        action.setShortcut('Ctrl+V')
        action.setStatusTip('Paste')
        action.setToolTip('Paste')
        return action

    def exitAction(self):
        action = QAction('Exit', self.__menu)
        action.setShortcut('Ctrl+Q')
        action.setToolTip('Close application')
        action.setStatusTip('Close application')
        action.triggered.connect(self.close)
        return action

    def saveAction(self):
        action = QAction('Save As', self.__menu)
        action.setShortcut('Ctrl+S')
        action.setToolTip('Save current application')
        action.setStatusTip('Save current application')
        action.triggered.connect(self.showSaveDialog)
        return action

    def openAction(self):
        action = QAction('Open', self.__menu)
        action.setShortcut('Ctrl+O')
        action.setToolTip('Open file')
        action.setStatusTip('Open file')
        action.triggered.connect(self.showOpenDialog)
        return action

    def __initToolBar(self):
        self.__toolBar = self.addToolBar('Drawing')
        self.__toolBarGroup = QActionGroup(self.__toolBar)

        default = self.disableScopeAction()

        actions = [
            default,
            self.lineAction(),
            self.pointAction(),
            self.angleAction(),
            self.lengthAction(),
            self.parallelAction(),
            self.verticalAction(),
            self.horizontalAction(),
        ]

        for action in actions:
            action.setCheckable(True)
            action.setParent(self.__toolBar)
            self.__toolBar.addAction(action)
            self.__toolBarGroup.addAction(action)

        default.setChecked(True)

    def pointAction(self):
        action = QAction('Point')
        action.setShortcut('Ctrl+P')
        action.setToolTip('Draw point')
        action.setStatusTip('Draw point')
        action.setIcon(QIcon('icons/point.png'))
        action.changed.connect(self.pointActionHandler)
        return action

    def pointActionHandler(self):
        if self.sender().isChecked():
            self.sketch.enableDrawPointMode()

    def lineAction(self):
        action = QAction('Line')
        action.setShortcut('Ctrl+L')
        action.setToolTip('Draw line')
        action.setStatusTip('Draw line')
        action.setIcon(QIcon('icons/line.png'))
        action.changed.connect(self.lineActionHandler)
        return action

    def lineActionHandler(self):
        if self.sender().isChecked():
            self.sketch.enableDrawLineMode()

    def horizontalAction(self):
        action = QAction('Horizontal')
        action.setToolTip('Horizontal constraint')
        action.setStatusTip('Horizontal constraint')
        action.setIcon(QIcon('icons/horizontal.png'))
        action.changed.connect(self.horizontalActionHandler)
        return action

    def horizontalActionHandler(self):
        if self.sender().isChecked():
            self.sketch.enableAngleScope(0)

    def verticalAction(self):
        action = QAction('Vertical')
        action.setToolTip('Vertical constraint')
        action.setStatusTip('Vertical constraint')
        action.setIcon(QIcon('icons/vertical.png'))
        action.changed.connect(self.verticalActionHandler)
        return action

    def verticalActionHandler(self):
        if self.sender().isChecked():
            self.sketch.enableAngleScope(90)

    def angleAction(self):
        action = QAction('Angle')
        action.setToolTip('Angle constraint')
        action.setStatusTip('Angle constraint')
        action.setIcon(QIcon('icons/angle.png'))
        action.changed.connect(self.angleActionHandler)
        return action

    def angleActionHandler(self):
        if self.sender().isChecked():
            angle, ok = self.askAngleValue()
            if ok:
                self.sketch.enableAngleScope(angle)
            else:
                self.disableScopes()

    def askAngleValue(self):
        label = 'Input angle value:'
        title = 'Set angle constraint'
        return QInputDialog.getDouble(self, title, label, 0)

    def lengthAction(self):
        action = QAction('Length')
        action.setToolTip('Length constraint')
        action.setStatusTip('Length constraint')
        action.setIcon(QIcon('icons/length.png'))
        action.changed.connect(self.lengthActionHandler)
        return action

    def lengthActionHandler(self):
        if self.sender().isChecked():
            length, ok = self.askLengthValue()
            if ok:
                self.sketch.enableLengthScope(length)
            else:
                self.disableScopes()

    def askLengthValue(self):
        label = 'Input length value:'
        title = 'Set length constraint'
        return QInputDialog.getDouble(self, title, label, 0, 0)

    def parallelAction(self):
        action = QAction('Parallel')
        action.setToolTip('Parallel constraint')
        action.setStatusTip('Parallel constraint')
        action.setIcon(QIcon('icons/parallel.png'))
        action.changed.connect(self.parallelsActionHandler)
        return action

    def parallelsActionHandler(self):
        if self.sender().isChecked():
            self.sketch.enableParallelsAction()

    def disableScopeAction(self):
        action = QAction('Disable')
        action.setToolTip('Choose action')
        action.setStatusTip('Choose action')
        action.setIcon(QIcon('icons/cursor.png'))
        action.triggered.connect(self.disableScopes)
        return action

    def disableScopes(self):
        for action in self.__toolBarGroup.actions():
            action.setChecked(False)
        self.sketch.disableScope()
        self.__toolBarGroup.actions()[0].setChecked(True)

    def __initStatusBar(self):
        self.statusBar().showMessage('Ready')

    def __initGeometry(self):
        desktop = QDesktopWidget()
        self.setGeometry(desktop.availableGeometry())

    def showOpenDialog(self):
        files = QFileDialog.getOpenFileName(self, 'Open file', '/home', '*.json')

        if files and files[0]:
            with open(files[0], 'r') as fp:
                fp.read()

    def showSaveDialog(self):
        files = QFileDialog.getSaveFileName(self, 'Save As', '/home/cad.json', '*.json')

        if files and files[0]:
            with open(files[0], 'w') as fp:
                fp.write('')

    def keyPressEvent(self, event):
        self.sketch.keyPressEvent(event)

        if event.key() == Qt.Key_Escape:
            return self.disableScopes()

    def closeEvent(self, event):
        title = 'Close application'
        question = 'Are you sure you want to quit?'

        default = QMessageBox.No
        buttons = QMessageBox.No | QMessageBox.Yes

        answer = QMessageBox.question(self, title, question, buttons, default)
        if answer == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
