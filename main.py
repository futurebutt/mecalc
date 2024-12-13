import bisect
import itertools

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget

from talentwidgets import TalentBar


# 1-5: 3 points per level
# 6-35: 2 points per level
# 36-60: 1 point per level
point_totals: list[int] = list(itertools.accumulate([3]*5 + [2]*30 + [1]*25))
lvl_to_pts: dict[int, int] = dict(enumerate(point_totals, start=1))
pts_to_lvl: dict[int, int] = {pts: lvl for lvl, pts in lvl_to_pts.items()}


class MainWidget(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)
        uic.loadUi("test.ui", self)

        # ideally use more flexible container for creating/loading talent sets
        self.talent_bars: list[TalentBar] = [self.TalentBar, self.TalentBar_2]

        for tb in self.talent_bars:
            tb.rankChanged.connect(self.talent_bars_rankChanged)

        self.levelSpin.valueChanged.connect(self.levelSpin_valueChanged)

    @property
    def total_points(self) -> int:
        return lvl_to_pts[self.levelSpin.value()]

    @property
    def allocated_points(self) -> int:
        return sum(tb.rank for tb in self.talent_bars)

    @property
    def unallocated_points(self) -> int:
        return self.total_points - self.allocated_points

    def update_total_point_display(self):
        self.totalPointLabel.setText(str(self.total_points))

    def update_unallocated_point_display(self):
        self.unallocatedPointLabel.setText(str(self.unallocated_points))

    def update_TalentBar_max_ranks(self):
        for tb in self.talent_bars:
            # Lowest of: 12, level + 1, talent rank + remaining points
            rank = min((12, self.levelSpin.value() + 1, tb.rank + self.unallocated_points))
            tb.set_max_rank(rank)

    @pyqtSlot(int)
    def levelSpin_valueChanged(self, _):
        self.update_TalentBar_max_ranks()
        self.update_unallocated_point_display()
        self.update_total_point_display()

    @pyqtSlot()
    def talent_bars_rankChanged(self):
        self.update_levelSpin_min()
        self.update_TalentBar_max_ranks()
        self.update_unallocated_point_display()
        self.update_total_point_display()

    def update_totalPointSpin_min(self):
        self.totalPointSpin.setMinimum(self.allocated_points)

    def update_levelSpin_min(self):
        # 1) Make sure there's at least as many total points as allocated
        zero_indexed_level = bisect.bisect_left(point_totals, self.allocated_points)
        min_lvl_by_total = zero_indexed_level + 1
        # 2) Make sure ranks are not greater than level + 1
        highest_rank = max([tb.rank for tb in self.talent_bars])
        min_lvl_by_rank = highest_rank - 1
        # Use high
        min_level = max((min_lvl_by_total, min_lvl_by_rank))
        self.levelSpin.setMinimum(min_level)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication.instance()
    if not app:
        app = QApplication([])
    mw = MainWidget()
    mw.show()
    sys.exit(app.exec())
