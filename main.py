import sys
from PyQt5 import QtGui, QtWidgets, QtCore
from basic_data import *


class HeroLabel(QtWidgets.QLabel):
    def __init__(self, name):
        QtWidgets.QLabel.__init__(self, name)
        self.change_image(name)
        self.setToolTip(HEROS_CN[name])

    clicked = QtCore.pyqtSignal()
    rightClicked = QtCore.pyqtSignal()

    def mousePressEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.rightClicked.emit()
        else:
            self.clicked.emit()

    def change_image(self, name, mode=None):
        '''
        mode: 'normal', 'selected', 'picked', 'banned'
        '''
        if mode == None:
            path = IMAGE_PATH + name + '.png'
        else:
            path = IMAGE_PATH + name + '_' + mode + '.png'

        self.setPixmap(QtGui.QPixmap(path))


class BanPickWindow(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.notes = {}
        self.notes['picked'] = ['blank'] * 10
        self.notes['pendings'] = HEROS
        self.notes['banned'] = []
        self.notes['selected'] = ''

        self.hero_labels = {}
        for anyone in HEROS:
            self.hero_labels[anyone] = HeroLabel(anyone)
            self.hero_labels[anyone].clicked.connect(lambda who=anyone: self.select_hero(who))

        self.pick_labels = {}
        for i in range(10):
            self.pick_labels[i] = HeroLabel('unknown')
            self.pick_labels[i].clicked.connect(lambda n=i: self.unpick_hero(n))

        self.pick_buttons = {}
        self.pick_buttons['radiant'] = QtWidgets.QPushButton('←')
        self.pick_buttons['radiant'].clicked.connect(lambda: self.pick_hero('radiant'))
        self.pick_buttons['dire'] = QtWidgets.QPushButton('→')
        self.pick_buttons['dire'].clicked.connect(lambda: self.pick_hero('dire'))
        self.pick_buttons['ban'] = QtWidgets.QPushButton('╳')
        self.pick_buttons['ban'].clicked.connect(self.ban_hero)

        self.init_ui()

    def init_ui(self):
        top_layout = QtWidgets.QGridLayout()
        for i in range(5):
            top_layout.addWidget(self.pick_labels[i], 0, i)
        for i in range(5,10):
            top_layout.addWidget(self.pick_labels[i], 0, i+1)

        top_layout.addWidget(self.pick_buttons['radiant'], 1, 4)
        top_layout.addWidget(self.pick_buttons['ban'], 1, 5)
        top_layout.addWidget(self.pick_buttons['dire'], 1, 6)

        str_layout = QtWidgets.QGridLayout()
        agi_layout = QtWidgets.QGridLayout()
        int_layout = QtWidgets.QGridLayout()

        for anyone in HEROS:
            if anyone in STR_HEROS:
                j = STR_HEROS.index(anyone)
                str_layout.addWidget(self.hero_labels[anyone], int(j / 15), int(j % 15))
            elif anyone in AGI_HEROS:
                j = AGI_HEROS.index(anyone)
                agi_layout.addWidget(self.hero_labels[anyone], int(j / 15), int(j % 15))
            else:
                j = INT_HEROS.index(anyone)
                int_layout.addWidget(self.hero_labels[anyone], int(j / 15), int(j % 15))


        tmp1 = QtWidgets.QLabel()
        tmp1.setPixmap(QtGui.QPixmap(IMAGE_PATH+'herotypestr.png'))
        tmp2 = QtWidgets.QLabel()
        tmp2.setPixmap(QtGui.QPixmap(IMAGE_PATH+'herotypeagi.png'))
        tmp3 = QtWidgets.QLabel()
        tmp3.setPixmap(QtGui.QPixmap(IMAGE_PATH+'herotypeint.png'))



        mid_layout = QtWidgets.QVBoxLayout()
        mid_layout.addWidget(tmp1)
        mid_layout.addLayout(str_layout)
        mid_layout.addWidget(tmp2)
        mid_layout.addLayout(agi_layout)
        mid_layout.addWidget(tmp3)
        mid_layout.addLayout(int_layout)
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addLayout(mid_layout)

        self.setLayout(layout)

    def select_hero(self, who):
        if who in self.notes['pendings']:
            if who == self.notes['selected']:
                self.notes['selected'] = ''
                self.hero_labels[who].change_image(who)
            else:
                # change notes
                prev_selected = self.notes['selected']
                self.notes['selected'] = who
                # change images
                self.hero_labels[who].change_image(who, 'selected')
                if prev_selected in self.notes['pendings']:
                    self.hero_labels[prev_selected].change_image(prev_selected)

    def pick_hero(self, side):

        who = self.notes['selected']
        if who in self.notes['pendings']:
            if side == 'radiant':
                i = self.notes['picked'].index('blank')
            else:
                tmp = self.notes['picked'][5:]
                i = tmp.index('blank') + 5

            # change notes
            self.notes['picked'][i] = who
            self.notes['pendings'].remove(who)
            self.notes['selected'] = ''
            # change images
            self.pick_labels[i].change_image(who)
            self.pick_labels[i].setToolTip(HEROS_CN[who])
            self.hero_labels[who].change_image(who, 'picked')

            if 'blank' not in self.notes['picked'][:5]:
                self.pick_buttons['radiant'].setDisabled(True)

            if 'blank' not in self.notes['picked'][5:]:
                self.pick_buttons['dire'].setDisabled(True)

    def ban_hero(self):
        who = self.notes['selected']
        if who in self.notes['pendings']:
            # change notes
            self.notes['banned'].append(who)
            self.notes['pendings'].remove(who)
            self.notes['selected'] = ''
            # change images
            self.hero_labels[who].change_image(who, 'banned')
            if len(self.notes['banned']) >= 10:
                self.pick_buttons['ban'].setDisabled(True)

    def unpick_hero(self, i):
        who = self.notes['picked'][i]
        if who != 'blank':
            # change notes
            self.notes['picked'][i] = 'blank'
            self.notes['pendings'].append(who)

            self.hero_labels[who].change_image(who)
            self.pick_labels[i].change_image('unknown')
            self.pick_labels[i].setToolTip('尚未挑选')


def main():
    app = QtWidgets.QApplication(sys.argv)
    bp_window = BanPickWindow()
    bp_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

