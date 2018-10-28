from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from cad.sketch import Sketch
from cad.geometry.constraints import *


class Application(QMainWindow):

    def __init__(self, *args):
        super().__init__(*args)

        self.sketch = None

        self.menu = None
        self.toolBar = None
        self.toolBarGroup = None

        self.initSketch()
        self.initMenuBar()
        self.initToolBar()
        self.initStatusBar()
        self.initGeometry()

        self.setWindowTitle('Sketch')

    def initSketch(self):
        self.sketch = Sketch(self)
        self.setCentralWidget(self.sketch)

    def initMenuBar(self):
        self.menu = self.menuBar()

        file = self.menu.addMenu('File')
        file.addAction(self.exitAction())
        file.addAction(self.openAction())
        file.addAction(self.saveAction())

        edit = self.menu.addMenu('Edit')
        edit.addAction(self.undoAction())
        edit.addAction(self.copyAction())
        edit.addAction(self.pasteAction())
        edit.addAction(self.deleteAction())

    def undoAction(self):
        action = QAction('Undo', self.menu)
        action.setShortcut('Ctrl+Z')
        action.setStatusTip('Undo')
        action.setToolTip('Undo')
        return action

    def copyAction(self):
        action = QAction('Copy', self.menu)
        action.setShortcut('Ctrl+C')
        action.setStatusTip('Copy')
        action.setToolTip('Copy')
        return action

    def pasteAction(self):
        action = QAction('Paste', self.menu)
        action.setShortcut('Ctrl+V')
        action.setStatusTip('Paste')
        action.setToolTip('Paste')
        return action

    def deleteAction(self):
        action = QAction('Delete', self.menu)
        action.setShortcut('Delete')
        action.setStatusTip('Delete')
        action.setToolTip('Delete')
        return action

    def exitAction(self):
        action = QAction('Exit', self.menu)
        action.setShortcut('Ctrl+Q')
        action.setToolTip('Close application')
        action.setStatusTip('Close application')
        action.triggered.connect(self.close)
        return action

    def saveAction(self):
        action = QAction('Save As', self.menu)
        action.setShortcut('Ctrl+S')
        action.setToolTip('Save current application')
        action.setStatusTip('Save current application')
        action.triggered.connect(self.showSaveDialog)
        return action

    def openAction(self):
        action = QAction('Open', self.menu)
        action.setShortcut('Ctrl+O')
        action.setToolTip('Open file')
        action.setStatusTip('Open file')
        action.triggered.connect(self.showOpenDialog)
        return action

    def initToolBar(self):
        self.toolBar = self.addToolBar('Drawing')
        self.toolBarGroup = QActionGroup(self.toolBar)

        default = self.disableAction()

        actions = [
            default,
            self.lineAction(),
            # self.pointAction(),
            self.angleAction(),
            self.lengthAction(),
            self.parallelAction(),
            self.perpendicularAction(),
            self.verticalAction(),
            self.horizontalAction(),
            # self.coincidentAction(),
        ]

        for action in actions:
            action.setCheckable(True)
            action.setParent(self.toolBar)
            self.toolBar.addAction(action)
            self.toolBarGroup.addAction(action)

        default.setChecked(True)

    def pointAction(self):
        action = QAction('Point')
        action.setShortcut('Ctrl+P')
        action.setToolTip('Draw point')
        action.setStatusTip('Draw point')
        action.setIcon(QIcon('icons/point.png'))
        action.triggered.connect(self.pointActionHandler)
        return action

    def pointActionHandler(self):
        mode = DrawPoint(self.sketch)
        self.sketch.setMode(mode)

    def lineAction(self):
        action = QAction('Line')
        action.setShortcut('Ctrl+L')
        action.setToolTip('Draw line')
        action.setStatusTip('Draw line')
        action.setIcon(QIcon('icons/line.png'))
        action.triggered.connect(self.lineActionHandler)
        return action

    def lineActionHandler(self):
        mode = DrawSegment(self.sketch)
        self.sketch.setMode(mode)

    def horizontalAction(self):
        action = QAction('Horizontal')
        action.setToolTip('Horizontal constraint')
        action.setStatusTip('Horizontal constraint')
        action.setIcon(QIcon('icons/horizontal.png'))
        action.triggered.connect(self.horizontalActionHandler)
        return action

    def horizontalActionHandler(self):
        mode = Horizontal(self.sketch)
        self.sketch.setMode(mode)

    def verticalAction(self):
        action = QAction('Vertical')
        action.setToolTip('Vertical constraint')
        action.setStatusTip('Vertical constraint')
        action.setIcon(QIcon('icons/vertical.png'))
        action.triggered.connect(self.verticalActionHandler)
        return action

    def verticalActionHandler(self):
        mode = Vertical(self.sketch)
        self.sketch.setMode(mode)

    def angleAction(self):
        action = QAction('Angle')
        action.setToolTip('Angle constraint')
        action.setStatusTip('Angle constraint')
        action.setIcon(QIcon('icons/angle.png'))
        action.triggered.connect(self.angleActionHandler)
        return action

    def angleActionHandler(self):
        mode = Angle(self.sketch)
        self.sketch.setMode(mode)

    def lengthAction(self):
        action = QAction('Length')
        action.setToolTip('Length constraint')
        action.setStatusTip('Length constraint')
        action.setIcon(QIcon('icons/length.png'))
        action.triggered.connect(self.lengthActionHandler)
        return action

    def lengthActionHandler(self):
        mode = Length(self.sketch)
        self.sketch.setMode(mode)

    def parallelAction(self):
        action = QAction('Parallel')
        action.setToolTip('Parallel constraint')
        action.setStatusTip('Parallel constraint')
        action.setIcon(QIcon('icons/parallel.png'))
        action.triggered.connect(self.parallelsActionHandler)
        return action

    def parallelsActionHandler(self):
        mode = Parallel(self.sketch)
        self.sketch.setMode(mode)

    def perpendicularAction(self):
        action = QAction('Perpendicular')
        action.setToolTip('Perpendicular constraint')
        action.setStatusTip('Perpendicular constraint')
        action.setIcon(QIcon('icons/perpendicular.png'))
        action.triggered.connect(self.perpendicularActionHandler)
        return action

    def perpendicularActionHandler(self):
        mode = Perpendicular(self.sketch)
        self.sketch.setMode(mode)

    def coincidentAction(self):
        action = QAction('Coincident')
        action.setToolTip('Coincident constraint')
        action.setStatusTip('Coincident constraint')
        action.setIcon(QIcon('icons/coincident.png'))
        action.triggered.connect(self.coincidentActionHandler)
        return action

    def coincidentActionHandler(self):
        mode = Coincident(self.sketch)
        self.sketch.setMode(mode)

    def disableAction(self):
        action = QAction('Disable')
        action.setToolTip('Choose action')
        action.setStatusTip('Choose action')
        action.setIcon(QIcon('icons/cursor.png'))
        action.triggered.connect(self.disableActionHandler)
        return action

    def disableActionHandler(self):
        for action in self.toolBarGroup.actions():
            action.setChecked(False)

        self.sketch.setMode(SketchMode(self.sketch))
        self.toolBarGroup.actions()[0].setChecked(True)

    def initStatusBar(self):
        self.statusBar().showMessage('Ready')

    def initGeometry(self):
        desktop = QDesktopWidget()
        self.setGeometry(desktop.availableGeometry())

    def showOpenDialog(self):
        ext = '*.json'
        title = 'Open from'
        default = '/home/cad.json'
        files = QFileDialog.getOpenFileName(self, title, default, ext)

        if files and files[0]:
            with open(files[0], 'r') as fp:
                fp.read()

    def showSaveDialog(self):
        ext = '*.json'
        title = 'Save as'
        default = '/home/cad.json'
        files = QFileDialog.getSaveFileName(self, title, default, ext)

        if files and files[0]:
            with open(files[0], 'w') as fp:
                fp.write('')

    def keyPressEvent(self, event):
        self.sketch.keyPressEvent(event)

        if event.key() == Qt.Key_Escape:
            return self.disableActionHandler()

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
