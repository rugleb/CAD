from PyQt5.QtWidgets import *

from cad.sketch import Sketch


class Application(QMainWindow):

    def __init__(self, *args):
        super().__init__(*args)

        self.sketch = None

        self.initMenuBar()
        self.initStatusBar()
        self.initDrawingBar()
        self.initRestrictionsBar()
        self.initSketch()
        self.initGeometry()

        self.setWindowTitle('Sketch')
        self.show()

    def initSketch(self):
        self.sketch = Sketch(self)
        self.setCentralWidget(self.sketch)

    def initMenuBar(self):
        file = self.menuBar().addMenu('File')
        file.addAction(self.exitAction())
        file.addAction(self.openAction())
        file.addAction(self.saveAction())

    def exitAction(self):
        action = QAction('Exit', self)
        action.setShortcut('Ctrl+Q')
        action.setStatusTip('Exit application')
        action.triggered.connect(self.close)
        return action

    def saveAction(self):
        action = QAction('Save As', self)
        action.setShortcut('Ctrl+S')
        action.setStatusTip('Saving')
        action.triggered.connect(self.showSaveDialog)
        return action

    def openAction(self):
        action = QAction('Open', self)
        action.setShortcut('Ctrl+O')
        action.setStatusTip('Open file')
        action.triggered.connect(self.showOpenDialog)
        return action

    def initDrawingBar(self):
        toolbar = self.addToolBar('Drawing')

        self.pointButton = QPushButton('Point', toolbar)
        self.segmentButton = QPushButton('Segment', toolbar)

        self.pointButton.clicked.connect(self._handlePointClick)
        self.segmentButton.clicked.connect(self._handleSegmentClick)

        toolbar.addWidget(QLabel('Drawing ', toolbar))
        toolbar.addWidget(self.pointButton)
        toolbar.addWidget(self.segmentButton)

    def initRestrictionsBar(self):
        self._restrictionBar = self.addToolBar('Restrictions')

        self._restrictionBar.addWidget(QLabel('Restrictions: '))
        self._setAngleRestriction()
        self._setLengthRestriction()
        self._setParallelsRestriction()

    def _setParallelsRestriction(self):
        self._parallelsButton = QPushButton('Parallels')
        self._parallelsButton.clicked.connect(self._parallelsClickHandler)

        self._parallelsButton.setParent(self._restrictionBar)
        self._restrictionBar.addWidget(self._parallelsButton)

    def _parallelsClickHandler(self):
        self.setStatusTip('Select line')

    def _setLengthRestriction(self):
        self._lengthButton = QPushButton('Length')
        self._lengthButton.clicked.connect(self._lengthClickHandler)

        self._lengthButton.setParent(self._restrictionBar)
        self._restrictionBar.addWidget(self._lengthButton)

    def _lengthClickHandler(self):
        length, pressed = QInputDialog.getDouble(self, 'Length restriction', 'Value: ', min=0.)
        if pressed and length:
            print(length)

    def _setAngleRestriction(self):
        self._angleButton = QPushButton('Angle')
        self._angleButton.clicked.connect(self._angleClickHandler)

        self._angleButton.setParent(self._restrictionBar)
        self._restrictionBar.addWidget(self._angleButton)

    def _angleClickHandler(self):
        angle, pressed = QInputDialog.getInt(self, 'Angle restriction', 'Value: ', min=-360, max=360)
        if pressed and angle:
            print(angle)

    def _handlePointClick(self):
        self.segmentButton.setDown(False)
        self.pointButton.setDown(not self.pointButton.isDown())

    def _handleSegmentClick(self):
        self.pointButton.setDown(False)
        self.segmentButton.setDown(not self.segmentButton.isDown())

    def initStatusBar(self):
        self.statusBar().showMessage('Ready')

    def initGeometry(self):
        desktop = QDesktopWidget()
        self.setGeometry(desktop.availableGeometry())

    def showOpenDialog(self):
        files = QFileDialog.getOpenFileName(self, 'Open file', '/home', '*.json')

        if files and files[0]:
            with open(files[0], 'r') as fp:
                data = fp.read()

    def showSaveDialog(self):
        files = QFileDialog.getSaveFileName(self, 'Save As', '/home/cad.json', '*.json')

        if files and files[0]:
            with open(files[0], 'w') as fp:
                fp.write('')

    def keyPressEvent(self, QKeyEvent):
        self.sketch.keyPressEvent(QKeyEvent)

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
