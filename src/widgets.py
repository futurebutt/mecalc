import bisect
import itertools

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

import talents as tl


class TalentPoint(QLabel):
    """
    Represents a single talent point on a TalentBar. Turns green for allocated,
    clear for unallocated.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
    
    def setupUi(self):
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy1)
        self.setMinimumSize(QSize(19, 25))
        self.setStyleSheet("border: 1px solid black;")

    def set_on(self):
        self.setStyleSheet("background-color: rgb(0, 255, 0); border: 1px solid black;")

    def set_off(self):
        self.setStyleSheet("border: 1px solid black;")


class TalentBar(QWidget):
    """
    Holds 12 talent points and buttons to increment and decrement points allocated.

    Besides that, houses a raw Talent and provides an interface between it and UI
    functions.
    """

    rankChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        self.talent = tl.Talent(0)
        # Concern for "max rank" is left to the UI. Talents don't care what their rank is as long as it's a number.
        # 2 is the default cap for a level 1 character.
        self._max_rank: int = 2
        self._update_buttons()

    @property
    def rank(self) -> int:
        # Parent/calling objects don't need to care that a TalentBar *houses* a Talent rather than *is* one.
        return self.talent.rank

    @rank.setter
    def rank(self, rank: int):
        self.talent.rank = rank

    def setupUi(self):
        # qt code ripped from Designer output
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
        """Add a talent point."""
        self.rank += 1
        self.display_rank()
        self._update_buttons()
        self.rankChanged.emit()

    @pyqtSlot()
    def decrement_clicked(self):
        """Remove a talent point."""
        self.rank -= 1
        self.display_rank()
        self._update_buttons()
        self.rankChanged.emit()

    def display_rank(self):
        """Update talent point lights from left to right."""
        for i, tp in enumerate(self.tps, start=1):
            if i <= self.rank:
                tp.set_on()
            else:
                tp.set_off()

    def _update_buttons(self):
        """
        Disable the decrement button at minimum rank or enable otherwise. Disable
        the increment button at max rank or enable otherwise.
        """
        self.decrementButton.setEnabled(self.rank != 0)
        self.incrementButton.setEnabled(self.rank != self._max_rank)

    def set_max_rank(self, rank: int):
        self._max_rank = rank
        self._update_buttons()
    
    def set_talent(self, talent: tl.Talent):
        # This hasn't really been implemented except for setup. Later it'll be used in UI class selection.
        assert talent.rank == 0, "I don't care about replacing a talent with points in it yet."
        self.talent = talent
        self.nameLabel.setText(talent.name)


# Classic levels rather than LE.
# 1-5: 3 points per level
# 6-35: 2 points per level
# 36-60: 1 point per level
point_totals: list[int] = list(itertools.accumulate([3]*5 + [2]*30 + [1]*25))
lvl_to_pts: dict[int, int] = dict(enumerate(point_totals, start=1))
pts_to_lvl: dict[int, int] = {pts: lvl for lvl, pts in lvl_to_pts.items()}


class TalentTree(QWidget):

    """
    Holds TalentBars. Tracks and displays values for allocated points, unallocated
    points, total points. Allows level to be set. Later, allow classes to be set.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        if not self.objectName():
            self.setObjectName("Tree")
        self.resize(431, 147)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(431, 0))
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.classStaticLabel = QLabel(self)
        self.classStaticLabel.setObjectName("classStaticLabel")

        self.horizontalLayout_2.addWidget(self.classStaticLabel)

        self.classCombo = QComboBox(self)
        self.classCombo.addItem("")
        self.classCombo.addItem("")
        self.classCombo.addItem("")
        self.classCombo.addItem("")
        self.classCombo.addItem("")
        self.classCombo.addItem("")
        self.classCombo.setObjectName("classCombo")

        self.horizontalLayout_2.addWidget(self.classCombo)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.levelStaticLabel = QLabel(self)
        self.levelStaticLabel.setObjectName("levelStaticLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.levelStaticLabel.sizePolicy().hasHeightForWidth())
        self.levelStaticLabel.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.levelStaticLabel)

        self.levelSpin = QSpinBox(self)
        self.levelSpin.setObjectName("levelSpin")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.levelSpin.sizePolicy().hasHeightForWidth())
        self.levelSpin.setSizePolicy(sizePolicy2)
        self.levelSpin.setReadOnly(False)
        self.levelSpin.setMinimum(1)
        self.levelSpin.setMaximum(60)

        self.horizontalLayout.addWidget(self.levelSpin)

        self.tpStaticLabel = QLabel(self)
        self.tpStaticLabel.setObjectName("tpStaticLabel")
        sizePolicy1.setHeightForWidth(self.tpStaticLabel.sizePolicy().hasHeightForWidth())
        self.tpStaticLabel.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.tpStaticLabel)

        self.totalPointLabel = QLabel(self)
        self.totalPointLabel.setObjectName("totalPointLabel")
        sizePolicy1.setHeightForWidth(self.totalPointLabel.sizePolicy().hasHeightForWidth())
        self.totalPointLabel.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.totalPointLabel)

        self.unallocStaticLabel = QLabel(self)
        self.unallocStaticLabel.setObjectName("unallocStaticLabel")
        sizePolicy1.setHeightForWidth(self.unallocStaticLabel.sizePolicy().hasHeightForWidth())
        self.unallocStaticLabel.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.unallocStaticLabel)

        self.unallocatedPointLabel = QLabel(self)
        self.unallocatedPointLabel.setObjectName("unallocatedPointLabel")
        sizePolicy1.setHeightForWidth(self.unallocatedPointLabel.sizePolicy().hasHeightForWidth())
        self.unallocatedPointLabel.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.unallocatedPointLabel)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.classStaticLabel.setText("Class:")
        self.classCombo.setItemText(0, "Soldier")
        self.classCombo.setItemText(1, "Engineer")
        self.classCombo.setItemText(2, "Adept")
        self.classCombo.setItemText(3, "Infiltrator")
        self.classCombo.setItemText(4, "Vanguard")
        self.classCombo.setItemText(5, "Sentinel")

        self.levelStaticLabel.setText("Level:")
        self.tpStaticLabel.setText("Total Points:")
        self.totalPointLabel.setText("3")
        self.unallocStaticLabel.setText("Unallocated Points:")
        self.unallocatedPointLabel.setText("3")

        self.levelSpin.valueChanged.connect(self.levelSpin_valueChanged)        
    
    @property
    def bars(self) -> list[TalentBar]:
        return self.findChildren(TalentBar)

    def add_talent_bar(self, talent: tl.Talent):
        num_bars = len(self.bars)
        bar = TalentBar(self)
        bar.setObjectName(f"talentbar_{num_bars + 1}")
        bar.set_talent(talent)
        bar.rankChanged.connect(self.talent_bars_rankChanged)
        self.verticalLayout.insertWidget(num_bars + 1, bar)
    
    def reset(self):
        """Blank slate for adding or switching to a new Talent set."""
        # Getting rid of everything is easier to do than changing Talents in-place (I think).
        for bar in self.bars:
            self.verticalLayout.removeWidget(bar)
            bar.deleteLater()
        # Reflect deallocated points.
        self.update_unallocated_point_display()

    @property
    def total_points(self) -> int:
        return lvl_to_pts[self.levelSpin.value()]

    @property
    def allocated_points(self) -> int:
        return sum(bar.rank for bar in self.bars)

    @property
    def unallocated_points(self) -> int:
        return self.total_points - self.allocated_points

    def update_total_point_display(self):
        self.totalPointLabel.setText(str(self.total_points))

    def update_unallocated_point_display(self):
        self.unallocatedPointLabel.setText(str(self.unallocated_points))

    def update_TalentBar_max_ranks(self):
        for bar in self.bars:
            # Lowest of: 12, level + 1, talent rank + remaining points
            rank = min((12, self.levelSpin.value() + 1, bar.rank + self.unallocated_points))
            bar.set_max_rank(rank)

    @pyqtSlot(int)
    def levelSpin_valueChanged(self, _):
        self.update_TalentBar_max_ranks()
        self.update_unallocated_point_display()
        self.update_total_point_display()

    @pyqtSlot()
    def talent_bars_rankChanged(self):
        """Slot for TalentBar.rankChanged for every bar."""
        self.update_levelSpin_min()
        self.update_TalentBar_max_ranks()
        self.update_unallocated_point_display()
        self.update_total_point_display()

    def update_levelSpin_min(self):
        """Prevent Shepard's level from being set below the minimum required for current point allocation."""
        # 1) Make sure there's at least as many total points as allocated
        zero_indexed_level = bisect.bisect_left(point_totals, self.allocated_points)
        min_lvl_by_total = zero_indexed_level + 1
        # 2) Make sure ranks are not greater than level + 1
        highest_rank = max([bar.rank for bar in self.bars])
        min_lvl_by_rank = highest_rank - 1
        # Use high
        min_level = max((min_lvl_by_total, min_lvl_by_rank))
        self.levelSpin.setMinimum(min_level)

    def set_class_soldier(self):
        # Eventually there'll be one of these functions for each class; for now I've just
        # been using it to hard code talents for testing.
        self.reset()
        self.add_talent_bar(tl.Pistols(0))
        self.add_talent_bar(tl.AssaultRifles(0))
        self.add_talent_bar(tl.Shotguns(0))
        self.add_talent_bar(tl.SniperRifles(0))
        self.add_talent_bar(tl.AssaultTraining(0))
        self.add_talent_bar(tl.Fitness(0))
        self.add_talent_bar(tl.CombatArmor(0))
        self.add_talent_bar(tl.FirstAid(0))
        self.add_talent_bar(tl.SpectreTraining(0))
        # self.add_talent_bar(tl.BasicArmor(0))
        # self.add_talent_bar(tl.TacticalArmor(0))
        # self.add_talent_bar(tl.Adept(0))
        # self.add_talent_bar(tl.AdeptBastion(0))
        # self.add_talent_bar(tl.AdeptNemesis(0))
        # self.add_talent_bar(tl.Engineer(0))
        # self.add_talent_bar(tl.EngineerOperative(0))
        # self.add_talent_bar(tl.Infiltrator(0))
        # self.add_talent_bar(tl.InfiltratorCommando(0))
        # self.add_talent_bar(tl.InfiltratorOperative(0))
        # self.add_talent_bar(tl.Sentinel(0))
        # self.add_talent_bar(tl.SentinelBastion(0))
        # self.add_talent_bar(tl.SentinelMedic(0))
        # self.add_talent_bar(tl.Soldier(0))
        # self.add_talent_bar(tl.SoldierCommando(0))
        # self.add_talent_bar(tl.SoldierShockTrooper(0))
        # self.add_talent_bar(tl.Decryption(0))
        # self.add_talent_bar(tl.Electronics(0))
        # self.add_talent_bar(tl.Hacking(0))
        # self.add_talent_bar(tl.Damping(0))
        # self.add_talent_bar(tl.Medicine(0))
        # self.add_talent_bar(tl.Barrier(0))
        # self.add_talent_bar(tl.Lift(0))
        # self.add_talent_bar(tl.Singularity(0))
        # self.add_talent_bar(tl.Stasis(0))
        # self.add_talent_bar(tl.Throw(0))
        # self.add_talent_bar(tl.Warp(0))
        # self.add_talent_bar(tl.Vanguard(0))
        # self.add_talent_bar(tl.VanguardNemesis(0))
        # self.add_talent_bar(tl.VanguardShockTrooper(0))
    
    def get_talents(self):
        return [bar.talent for bar in self.bars]
    

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication.instance()
    if not app:
        app = QApplication([])
    tb = TalentBar()
    tb.show()
    sys.exit(app.exec())
