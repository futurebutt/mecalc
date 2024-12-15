from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

import summarize as sm


class MainWidget(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)
        uic.loadUi(Path(__file__).with_name("test.ui"), self)

        self.talentTree.set_class_soldier()
        
        self.summaryButton.clicked.connect(self.summarizeButton_clicked)

    def summarizeButton_clicked(self):
        self.summaryTextEdit.clear()
        talents = self.talentTree.get_talents()
        for summarize in (
            sm.summarize_Shepard,
            sm.summarize_Adrenaline_Burst,
            sm.summarize_Immunity,
            sm.summarize_Pistol,
            sm.summarize_Marksman,
        ):
            summary = summarize(talents)
            if summary:
                self.summaryTextEdit.append(summary)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication.instance()
    if not app:
        app = QApplication([])
    mw = MainWidget()
    mw.show()
    sys.exit(app.exec())
