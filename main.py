import sys
from PyQt5 import QtGui, QtWidgets, QtCore
from basic_data import *


class ClickableQLabel(QtWidgets.QLabel):
    def __init__(self):
        QtWidgets.QLabel.__init__(self)

    clicked = QtCore.pyqtSignal()
    rightClicked = QtCore.pyqtSignal()

    def mousePressEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.rightClicked.emit()
        else:
            self.clicked.emit()


class BanPickWindow(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)

        self.notes = {}
        self.notes['picks'] = ['blank'] * 10
        self.notes['pendings'] = HEROS
        self.notes['bans'] = []
        self.notes['choose'] = ''

        self.hero_buttons = {}
        for anyone in HEROS:
            self.hero_buttons[anyone] = ClickableQLabel()
            self.hero_buttons[anyone].setPixmap(QtGui.QPixmap(IMAGES[anyone]))
            self.hero_buttons[anyone].clicked.connect(lambda who=anyone: self.choose_hero(who))

        self.pick_labels = {}
        for i in range(11):
            self.pick_labels[i] = ClickableQLabel()
            self.pick_labels[i].setPixmap(QtGui.QPixmap(IMAGES['unknown']))
            self.pick_labels[i].clicked.connect(lambda n=i:self.unpick_hero(n))
        self.pick_labels[-1] = QtWidgets.QLabel()
        self.pick_labels[-1].setPixmap(QtGui.QPixmap(IMAGES['unknown']))
 
        self.pick_buttons = {}
        self.pick_buttons['radiant'] = QtWidgets.QPushButton('←')
        self.pick_buttons['radiant'].clicked.connect(lambda: self.pick_hero('radiant'))
        self.pick_buttons['dire'] = QtWidgets.QPushButton('→')
        self.pick_buttons['dire'].clicked.connect(lambda: self.pick_hero('dire'))
        self.pick_buttons['ban'] = QtWidgets.QPushButton('╳')

        self.init_ui()


    def init_ui(self):
        top_layout = QtWidgets.QHBoxLayout()
        for i in range(5):
            top_layout.addWidget(self.pick_labels[i])
        top_layout.addWidget(self.pick_labels[-1])
        for i in range(5,10):
            top_layout.addWidget(self.pick_labels[i])

        button_layout = QtWidgets.QHBoxLayout()
        for btn in ['radiant', 'ban', 'dire']:
            button_layout.addWidget(self.pick_buttons[btn])

        str_layout = QtWidgets.QGridLayout()
        agi_layout = QtWidgets.QGridLayout()
        int_layout = QtWidgets.QGridLayout()

        for anyone in HEROS:
            if anyone in STR_HEROS:
                j = STR_HEROS.index(anyone)
                str_layout.addWidget(self.hero_buttons[anyone], int(j / 15), int(j % 15))
            elif anyone in AGI_HEROS:
                j = AGI_HEROS.index(anyone)
                agi_layout.addWidget(self.hero_buttons[anyone], int(j / 15), int(j % 15))
            else:
                j = INT_HEROS.index(anyone)
                int_layout.addWidget(self.hero_buttons[anyone], int(j / 15), int(j % 15))

        mid_layout = QtWidgets.QVBoxLayout()
        mid_layout.addLayout(str_layout)
        mid_layout.addLayout(agi_layout)
        mid_layout.addLayout(int_layout)
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addLayout(button_layout)
        layout.addLayout(mid_layout)

        self.setLayout(layout)


    def choose_hero(self, who):
        if who in self.notes['pendings']:
            self.notes['choose'] = who
            self.pick_labels[-1].setPixmap(QtGui.QPixmap(IMAGES[who]))

    def pick_hero(self, side):
        if self.notes['choose'] in self.notes['pendings']:
            if side == 'radiant':
                i = self.notes['picks'].index('blank')
            else:
                tmp = self.notes['picks'][5:]
                i = tmp.index('blank')+5

            self.notes['picks'][i] = self.notes['choose']
            self.notes['pendings'].remove(self.notes['choose'])

            self.pick_labels[i].setPixmap(QtGui.QPixmap(IMAGES[self.notes['choose']]))
            self.pick_labels[-1].setPixmap(QtGui.QPixmap(IMAGES['unknown']))

            if 'blank' not in self.notes['picks'][:5]:
                self.pick_buttons['radiant'].setDisabled(True)

            if 'blank' not in self.notes['picks'][5:]:
                self.pick_buttons['dire'].setDisabled(True)

    def unpick_hero(self, i):
        hero = self.notes['picks'][i]
        self.notes['picks'][i] = 'blank'
        self.notes['pendings'].append(hero)
        self.pick_labels[i].setPixmap(QtGui.QPixmap(IMAGES['unknown']))





def main():
    app = QtWidgets.QApplication(sys.argv)
    bp_window = BanPickWindow()
    bp_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()




def get_best_choises(picks, )




















