from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QCalendarWidget


class MyCalender(QCalendarWidget):
    def __init__(self):
        super().__init__()
        self.setGridVisible(True)
        # self.selectionChanged.connect(self.calendar_date)
        self.clicked.connect(self.calendar_date)
        self.days = []

    def paintCell(self, painter, rect, date):
        '''
        This function is called internally.
        Paints the date i click on.
        I am trying to get the color to appear when i first click it and disappear when
        i click it again.
        Right now, another date must be clicked first before a second click makes
        the color disappear.
        '''
        QCalendarWidget.paintCell(self, painter, rect, date)
        if date.toString() in self.days:
            painter.save()
            painter.fillRect(rect, QtGui.QColor("#3c72cf"))
            painter.drawText(rect, QtCore.Qt.AlignCenter, str(date.day()))
            painter.restore()
        else:
            painter.save()
            painter.fillRect(rect, QtGui.QColor("#ffffff"))
            painter.drawText(rect, QtCore.Qt.AlignCenter, str(date.day()))
            painter.restore()

    def calendar_date(self):
        '''
        Days the user wants to lock up an app.
        Probably have to put a DONE button.
        The user might not want to lock something for a whole day.
        i have to add time (hours). Sigh. This seems more like a bad idea.
        :return:
        '''
        print("Clicked")
        date_selected = self.selectedDate()

        if date_selected.toString() in self.days:
            self.days.remove(date_selected.toString())
        else:
            self.days.append(date_selected.toString())

        print(self.days)
        return None
