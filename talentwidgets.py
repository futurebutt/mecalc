from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget


class TalentPoint(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy1)
        self.setMinimumSize(QSize(19, 25))
        self.setStyleSheet(u"border: 1px solid black;")

    def set_on(self):
        self.setStyleSheet("background-color: rgb(0, 255, 0); border: 1px solid black;")

    def set_off(self):
        self.setStyleSheet("border: 1px solid black;")


class TalentBar(QWidget):

    rankChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        self.rank: int = 0
        self._max_rank: int = 2
        self._update_buttons()

    def setupUi(self):
        self.resize(431, 47)
        self.horizontalLayout = QHBoxLayout(self)
        self.nameLabel = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameLabel.sizePolicy().hasHeightForWidth())
        self.nameLabel.setSizePolicy(sizePolicy)
        self.nameLabel.setMinimumSize(QSize(95, 0))
        font = QFont()
        font.setPointSize(10)
        self.nameLabel.setFont(font)

        self.horizontalLayout.addWidget(self.nameLabel)

        self.tpLayout = QHBoxLayout()
        self.tpLayout.setSpacing(2)
        self.tps = tuple([TalentPoint(self) for _ in range(12)])
        for tp in self.tps:
            self.tpLayout.addWidget(tp)

        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)

        self.horizontalLayout.addLayout(self.tpLayout)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(2)
        self.decrementButton = QPushButton(self)
        sizePolicy1.setHeightForWidth(self.decrementButton.sizePolicy().hasHeightForWidth())
        self.decrementButton.setSizePolicy(sizePolicy1)
        self.decrementButton.setMinimumSize(QSize(0, 27))
        self.decrementButton.setMaximumSize(QSize(25, 27))
        self.decrementButton.setAutoRepeat(True)

        self.buttonLayout.addWidget(self.decrementButton)

        self.incrementButton = QPushButton(self)
        sizePolicy1.setHeightForWidth(self.incrementButton.sizePolicy().hasHeightForWidth())
        self.incrementButton.setSizePolicy(sizePolicy1)
        self.incrementButton.setMinimumSize(QSize(0, 27))
        self.incrementButton.setMaximumSize(QSize(25, 27))
        self.incrementButton.setAutoRepeat(True)

        self.buttonLayout.addWidget(self.incrementButton)

        self.horizontalLayout.addLayout(self.buttonLayout)

        self.nameLabel.setText("<TALENT>")
        for tp in self.tps:
            tp.setText("")
        self.decrementButton.setText("-")
        self.incrementButton.setText("+")

        self.incrementButton.clicked.connect(self.increment_clicked)
        self.decrementButton.clicked.connect(self.decrement_clicked)

    @pyqtSlot()
    def increment_clicked(self):
        self.tps[self.rank].set_on()
        self.rank += 1
        self._update_buttons()
        self.rankChanged.emit()

    @pyqtSlot()
    def decrement_clicked(self):
        self.rank -= 1
        self.tps[self.rank].set_off()
        self._update_buttons()
        self.rankChanged.emit()

    def _update_buttons(self):
        self.decrementButton.setEnabled(self.rank != 0)
        self.incrementButton.setEnabled(self.rank != self._max_rank)

    def set_max_rank(self, rank: int):
        self._max_rank = rank
        self._update_buttons()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication.instance()
    if not app:
        app = QApplication([])
    tb = TalentBar()
    tb.show()
    sys.exit(app.exec())
