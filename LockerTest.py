import sys

import oschmod
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QListWidget, QPushButton, QMessageBox, \
    QTabWidget, QComboBox
import MyCalenderWidget


class DropLabel(QLabel):
    def __init__(self, text):
        self.text = text
        super().__init__()
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setText(self.text)


class Buttons(QPushButton):
    def __init__(self, name):
        self.name = name
        super().__init__()
        self.setText(name)
        self.resize(50, 50)

        self.setStyleSheet(
            '''
                QPushButton{
                    background-color: rgb(169,169,169);
                    border: 1px solid black;
                    border-radius: 5px;
                    padding: 5px;
                    
                }
                QPushButton:pressed {
                    background-color: rgb(128,128,128);
                    border-style: inset;
                }
            '''
        )


def set_permissions(url, reset_clicked=False):
    '''
    Change permissions of the file or folder to prevent access from its abuser.
    NB. I should probably check what permissions the file has before it can be given full access.
    :param url: Path to file or folder. Inserted by dropEvent()
    :param reset_clicked: Self-explanatory
    :return: returns None
    '''
    if reset_clicked:
        oschmod.set_mode(url, 777) #777 gives full access (read, write, execute) to file or folder
    else:
        oschmod.set_mode(url, 000) #000 removes all rights to the file or folder
    return None


def menu_items():
    '''
    List of deterrent numbers. The selected value is the number of times
    the deterrent dialog will appear.
    :return: Dropdown of deterrent number options
    '''
    dropdown_list = QComboBox()
    dropdown_list.addItem("1")
    dropdown_list.addItem("3")
    dropdown_list.addItem("4")
    dropdown_list.addItem("200")
    dropdown_list.addItem("300")
    dropdown_list.addItem("400")
    dropdown_list.addItem("500")
    return dropdown_list


def settings():
    '''
    Settings tab
    :return:
    '''
    settings_tab = QWidget()
    info_label = QLabel()
    info_label.setText("Choose the number of times you want to be deterred.")
    settings_layout = QVBoxLayout()

    settings_layout.setAlignment(Qt.AlignTop)
    settings_layout.addWidget(info_label)
    settings_layout.addWidget(menu_items())
    settings_tab.setLayout(settings_layout)
    return settings_tab


def calender_window():
    '''Calender Tab'''
    calender_tab = QWidget()
    cal = MyCalenderWidget.MyCalender()

    vlayout = QVBoxLayout()

    label = QLabel("Select lockdown days")
    label.setAlignment(Qt.AlignCenter)
    label.setFont(QFont("Sanserif", 15))
    label.setStyleSheet('color:gray')

    vlayout.addWidget(cal)
    vlayout.addWidget(label)
    calender_tab.setLayout(vlayout)
    return calender_tab


class Home(QWidget):
    def __init__(self):
        super().__init__()

        self.drop_list = ListWidget()
        self.setWindowTitle("Lock Addiction")
        self.resize(300, 300)
        self.setAcceptDrops(True)
        self.setWindowIcon(QtGui.QIcon("locker.jpg"))

        self.vertical_layout = QVBoxLayout()
        self.Tabs = QTabWidget()
        self.Tabs.addTab(self.dump_window(), "Dump")
        self.Tabs.addTab(settings(), "Settings")
        self.Tabs.addTab(calender_window(), "Calender")
        self.vertical_layout.addWidget(self.Tabs)
        self.setLayout(self.vertical_layout)

    def dump_window(self):
        '''Drag and drop tab'''
        dump_tab = QWidget()
        vertical_layout = QVBoxLayout()
        title_label = DropLabel("Addiction Dump")

        reset_button = Buttons("Reset")

        reset_button.clicked.connect(lambda: self.deterrent_dialog())

        vertical_layout.addWidget(title_label)
        vertical_layout.addWidget(self.drop_list)
        vertical_layout.addWidget(reset_button)

        dump_tab.setLayout(vertical_layout)
        return dump_tab

    def deterrent_dialog(self):
        """
        Diolog box that should annoy the user.
        The number of times the deterrent Dialog appears should be in settings. Default:1000
        """
        if len(self.drop_list) == 0:
            return None
        msg = QMessageBox()
        deterrent_number = int(menu_items().currentText())
        print(deterrent_number)
        for i in range(deterrent_number):
            annoying_message = msg.question(self, "Wussying Out?", "I am going to make things very difficult for you. :)",
                               QMessageBox.Retry | QMessageBox.Cancel)

            if annoying_message == QMessageBox.Cancel:
                break
            elif i == deterrent_number - 1:
                msg_box = QMessageBox()
                msg_box.setText("You actually did it xD")
                msg_box.setWindowTitle("End of Deterrent")
                msg_box.setIcon(QMessageBox.Information)
                reset_button = msg_box.addButton(self.tr("Reset"), QMessageBox.ActionRole)
                msg_box.exec_()
                if msg_box.clickedButton() == reset_button:
                    self.reset()
        return None

    def reset(self):
        '''Reset permissions, more like just give full permissions. Bad idea i will fix soon....probably'''
        for index in range(self.drop_list.count()):
            link = self.drop_list.item(index).text()
            set_permissions(link, reset_clicked=True)
        self.drop_list.clear()
        return None

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        event.accept()
        return None

    def dragLeaveEvent(self, event: QtGui.QDragLeaveEvent):
        event.accept()
        return None

    def dragMoveEvent(self, event: QtGui.QDragMoveEvent):
        event.accept()
        return None

    def dropEvent(self, event: QtGui.QDropEvent):
        link = event.mimeData().urls()[0].toLocalFile()
        set_permissions(link)
        self.drop_list.addItem(link)
        event.accept()
        return None


class ListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
            '''
                QListWidget{
                    border: 4px dashed #aaa;
                }
                QListView::item{
                    padding-bottom: 5px;
                }
            '''
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Home()
    window.show()
    sys.exit(app.exec_())
