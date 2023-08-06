import datetime
from typing import Callable, List

import dominate.tags as T
import dominate.util
import matplotlib.pyplot as plt
import orgpython
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor, QTextDocument
from PyQt5.QtWidgets import (QComboBox, QHBoxLayout, QMainWindow, QSplitter,
                             QStatusBar, QTextEdit, QToolButton, QVBoxLayout,
                             QWidget)

import mento.stats as stats
import mento.viz as viz
from mento.types import Entry


class QJournal(QTextEdit):
    """
    Widget for displaying journal entries.
    """

    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setStyleSheet("QTextEdit { padding:10; border: none; background-color: transparent; }")
        self.font_family = "Lora"

    def format_entry_dt(self, entry: Entry) -> str:
        if entry.time:
            return datetime.datetime.combine(entry.date, entry.time).strftime("%b %d %Y %H:%M:%S")
        else:
            return entry.date.strftime("%b %d %Y")

    def format_entry(self, entry: Entry) -> str:
        div = T.div(style=f"font-family: {self.font_family}")

        div += T.div(self.format_entry_dt(entry), style="color: #999999; font-size: 13px;")
        div += T.br()

        body = dominate.util.raw(orgpython.to_html(entry.body.strip()))
        div += T.div(body, style="color: #555555; font-size: 13px;")

        div += T.br()
        div += T.br()
        div += T.br()

        return div.render()

    def render(self, entries: List[Entry]):
        for entry in entries:
            self.textCursor().insertHtml(self.format_entry(entry))

    def scroll_to_date(self, date: datetime.date):
        """
        Scroll journal to entry on given `date`. If date is not present, don't do
        anything.
        """

        current_position = self.textCursor().position()
        date_str = date.strftime("%b %d %Y")

        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)

        found = False
        while self.find(date_str, QTextDocument.FindFlag.FindBackward):
            found = True

        if found:
            pos = self.textCursor().position()
        else:
            pos = current_position

        cursor = self.textCursor()
        cursor.setPosition(pos)
        self.setTextCursor(cursor)


class QCalendar(FigureCanvasQTAgg):
    """
    Calendar plotted using matplotlib.
    """

    def __init__(self, entries: List[Entry], journal_callback: Callable[[datetime.date], None]):
        self.fig = plt.figure()
        super().__init__(self.fig)
        self.entries = entries
        self.fig.canvas.mpl_connect("pick_event", self.on_pick)
        self.journal_callback = journal_callback

    def on_pick(self, event):
        """
        Function called when a date is selected. We highlight the date and scroll
        the journal to the given position.
        """

        rect = event.artist
        self.journal_callback(rect._data["date"])

    def render(self, year: int, plot_type: str):
        self.fig.clear()

        colors = {}
        if plot_type == "polarity":
            ct = viz.color_transform((-1, 1))
            for dt, v in stats.aggregate_by_date(self.entries, stats.aggregate_mean_polarity).items():
                colors[dt] = ct(v)
            viz.plot_year(self.fig, year, colors)

        elif plot_type == "mood":
            ct = viz.color_transform((-2, 2))
            for dt, v in stats.aggregate_by_date(self.entries, stats.aggregate_mean_mood).items():
                if v is not None:
                    colors[dt] = ct(v)
            viz.plot_year(self.fig, year, colors)

        elif plot_type == "count":
            aggregated = stats.aggregate_by_date(self.entries, len)
            ct = viz.color_transform((0, max(aggregated.values())))
            for dt, v in aggregated.items():
                colors[dt] = ct(v)
            viz.plot_year(self.fig, year, colors)

        elif plot_type == "mentions":
            aggregated = stats.aggregate_by_date(self.entries, stats.aggregate_mentions)
            ct = viz.color_transform((0, max(aggregated.values())))
            for dt, v in aggregated.items():
                colors[dt] = ct(v)
            viz.plot_year(self.fig, year, colors)

        elif plot_type == "mood (hour)":
            viz.plot_year_polar(self.fig, year, self.entries)

        self.fig.canvas.draw_idle()


class QWindow(QMainWindow):
    """
    Main app window
    """

    def __init__(self, entries):
        super().__init__()
        self.setWindowTitle("mento")

        widget = QWidget(self)
        self.setCentralWidget(widget)

        layout = QHBoxLayout()
        min_year = min([e.date for e in entries]).year
        max_year = max([e.date for e in entries]).year

        self.year = max_year
        self.plot_type = "mood"

        self.journal = QJournal()
        self.journal.render(entries)

        self.calendar = QCalendar(entries, self.journal.scroll_to_date)

        side_pane = QWidget()
        side_pane_layout = QVBoxLayout()

        controls = QWidget()
        controls_layout = QHBoxLayout()

        left_button = QToolButton()
        left_button.setArrowType(Qt.LeftArrow)
        left_button.clicked.connect(self.left_click)

        right_button = QToolButton()
        right_button.setArrowType(Qt.RightArrow)
        right_button.clicked.connect(self.right_click)

        years = [str(y) for y in range(min_year, max_year + 1)]
        self.combo_year = QComboBox()
        self.combo_year.addItems(years)
        self.combo_year.activated.connect(self.combo_year_click)
        self.refresh_combo_year()

        self.combo_plot = QComboBox()
        self.combo_plot.addItems(["mood", "mood (hour)", "count", "polarity", "mentions"])
        self.combo_plot.activated.connect(self.combo_plot_click)

        controls_layout.addWidget(left_button)
        controls_layout.addWidget(right_button)
        controls_layout.addWidget(self.combo_year)
        controls_layout.addWidget(self.combo_plot)
        controls.setLayout(controls_layout)

        side_pane_layout.addWidget(controls)
        side_pane_layout.addWidget(self.journal)
        side_pane.setLayout(side_pane_layout)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.calendar)
        splitter.addWidget(side_pane)

        layout.addWidget(splitter)
        widget.setLayout(layout)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.refresh_calendar()

    def refresh_combo_year(self):
        self.combo_year.setCurrentIndex(self.combo_year.findText(str(self.year)))

    def refresh_calendar(self):
        self.calendar.render(self.year, self.plot_type)

    def left_click(self):
        self.year -= 1
        self.refresh_calendar()
        self.refresh_combo_year()

    def right_click(self):
        self.year += 1
        self.refresh_calendar()
        self.refresh_combo_year()

    def combo_year_click(self):
        self.year = int(self.combo_year.currentText())
        self.refresh_calendar()

    def combo_plot_click(self):
        self.plot_type = self.combo_plot.currentText()
        self.refresh_calendar()
