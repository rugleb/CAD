from PyQt5 import QtCore, QtGui, QtWidgets

from cad.drawing import Line, Point, Pen


class Sketch(QtWidgets.QWidget):
    _segments = None
    _point = None

    def __init__(self, *args):
        super().__init__(*args)

        self._segments = []
        self._point = None

        self.setMouseTracking(True)
        self.setWindowTitle('Sketch')

    def isMousePressed(self):
        return self._point is not None

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Delete:
            self._segments = [s for s in self._segments if not s.hasPoint(self._p2)]
        self.update()

    def mousePressEvent(self, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.LeftButton:
                self._point = Point(event.localPos())

    def mouseReleaseEvent(self, event):
        if event.type() == QtCore.QEvent.MouseButtonRelease:
            if event.button() == QtCore.Qt.LeftButton:
                point = Point(event.localPos())
                line = Line(self._point, point)
                self._point = None
                self.draw(line)

    def mouseMoveEvent(self, event):
        point = Point(event.localPos())
        self._p2 = point
        if self.isMousePressed():
            if self._segments:
                self._segments.pop(-1)
            line = Line(self._point, point)
            self._segments.append(line)
        for line in self._segments:
            if line.hasPoint(point):
                line.setPen(Pen.active())
            else:
                line.setPen(Pen.stable())
        self.update()

    def draw(self, line):
        self._segments.append(line)
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self._drawLines(painter)
        painter.end()

    def _drawLines(self, painter):
        for line in self._segments:
            pen = line.getPen()
            painter.setPen(pen)
            painter.drawLine(line)
            width = pen.widthF()
            pen.setWidthF(width * 2)
            painter.setPen(pen)
            painter.drawPoints(line.p1(), line.p2())
            pen.setWidthF(width)