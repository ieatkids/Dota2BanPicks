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

        self.picks = ['blank'] * 10
        self.bans = []
        self.pendings = HEROS
        self.selected_hero = None

        # GUI
        self.pick_labels = {}
        for i in range(10):
            self.pick_labels[i] = ClickableQLabel()
            self.pick_labels[i].setPixmap(QtGui.QPixmap(IMAGES['unknown']))
        self.hero_labels = {}
        for hero in HEROS:
            self.hero_labels[hero] = ClickableQLabel()
            self.hero_labels[hero].setPixmap(QtGui.QPixmap(IMAGES[hero]))
            self.hero_labels[hero].clicked.connect(lambda who = hero: self.select_hero(who))
            self.hero_labels[hero].rightClicked.connect(self.unselect_hero)

        self.toradiant_btn = QtWidgets.QPushButton('←')
        self.toradiant_btn.clicked.connect(lambda: self.pick_hero('radiant'))

        self.todire_btn = QtWidgets.QPushButton('→')
        self.todire_btn.clicked.connect(lambda: self.pick_hero('dire'))

        self.ban_btn = QtWidgets.QPushButton('╳')
        self.ban_btn.clicked.connect(self.ban_hero)

        self.init_ui()

    def init_ui(self):
        pick_layout = QtWidgets.QHBoxLayout()
        for i in range(10):
            pick_layout.addWidget(self.pick_labels[i])

        btns_layout = QtWidgets.QHBoxLayout()
        btns_layout.addWidget(self.toradiant_btn)
        btns_layout.addWidget(self.ban_btn)
        btns_layout.addWidget(self.todire_btn)

        str_layout = QtWidgets.QGridLayout()
        agi_layout = QtWidgets.QGridLayout()
        int_layout = QtWidgets.QGridLayout()

        for hero in HEROS:
            if hero in STR_HEROS:
                j = STR_HEROS.index(hero)
                str_layout.addWidget(self.hero_labels[hero], int(j/15), int(j%15))
            elif hero in AGI_HEROS:
                j = AGI_HEROS.index(hero)
                agi_layout.addWidget(self.hero_labels[hero], int(j/15), int(j%15))
            else:
                j = INT_HEROS.index(hero)
                int_layout.addWidget(self.hero_labels[hero], int(j/15), int(j%15))
        hero_layout = QtWidgets.QVBoxLayout()
        hero_layout.addLayout(str_layout)
        hero_layout.addLayout(agi_layout)
        hero_layout.addLayout(int_layout)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(pick_layout)
        layout.addLayout(btns_layout)
        layout.addLayout(hero_layout)
        self.setLayout(layout)

    def select_hero(self, hero):
        self.selected_hero = hero

    def unselect_hero(self):
        self.selected_hero = None

    def pick_hero(self, side):
        if self.selected_hero in self.pendings:
            if side == 'radiant' and 'blank' in self.picks[:5]:
                i = self.picks[:5].index('blank')
                self.picks[i] = self.selected_hero
                self.pendings.remove(self.selected_hero)
                self.pick_labels[i].setPixmap(QtGui.QPixmap(IMAGES[self.selected_hero]))
            elif side == 'dire' and 'blank' in self.picks[5:]:
                i = self.picks[:5].index('blank') + 5
                self.picks[i] = self.selected_hero
                self.pendings.remove(self.selected_hero)
                self.pick_labels[i].setPixmap(QtGui.QPixmap(IMAGES[self.selected_hero]))

    def ban_hero(self):
        if self.selected_hero in self.pendings and len(self.bans) < 5:
            self.pendings.remove(self.selected_hero)
            self.bans.append(self.selected_hero)
            self.hero_labels[self.selected_hero].setPixmap(QtGui.QPixmap(IMAGES_GRAY[self.selected_hero]))
        print(self.bans)





# class BanPickWindow(QtWidgets.QDialog):
#     def __init__(self):
#         QtWidgets.QDialog.__init__(self)
#         self.setGeometry(100, 100, 800, 600)
#
#         self.picks = ['blank'] * 10
#         self.pending_heros = HEROS
#         self.selected_hero = None
#         self.selected_hero_label = QtWidgets.QLabel()
#         self.selected_hero_label.setPixmap(QtGui.QPixmap(IMAGES['unknown']))
#
#         # set pick bar
#         for i in range(10):
#             self.__setattr__('picked_hero_' + str(i), ClickableQLabel())
#             self.__dict__['picked_hero_' + str(i)].setPixmap(QtGui.QPixmap(IMAGES['unknown']))
#             self.__dict__['picked_hero_' + str(i)].rightClicked.connect(lambda n=i: self.unpickHero(n))
#
#         # set search bars
#         search_comleter = QtWidgets.QCompleter(list(CN_HEROS.keys()))
#         for side in ['radiant', 'dire']:
#             self.__setattr__(side + '_searchbar', QtWidgets.QLineEdit())
#             self.__dict__[side + '_searchbar'].setCompleter(search_comleter)
#             self.__dict__[side + '_searchbar'].editingFinished.connect(
#                 lambda direction=side: self.pickHeroFromSearchbar(direction))
#
#         # set pick buttons
#         self.toradiant_btn = QtWidgets.QPushButton('←')
#         self.toradiant_btn.clicked.connect(lambda: self.pickHero('radiant'))
#         self.todire_btn = QtWidgets.QPushButton('→')
#         self.todire_btn.clicked.connect(lambda: self.pickHero('dire'))
#         self.ban_btn = QtWidgets.QPushButton('╳')
#
#         self.initUI()
#
#     def initUI(self):
#         # set hero buttons
#         hero_labels = {}
#         for name in HEROS:
#             hero_labels[name] = ClickableQLabel()
#             hero_labels[name].setPixmap(QtGui.QPixmap(IMAGES[name]))
#             hero_labels[name].setToolTip(name)
#             hero_labels[name].clicked.connect(lambda who=name: self.selectHero(who))
#
#         top_layout = QtWidgets.QGridLayout()
#         top_layout.addWidget(self.selected_hero_label, 0, 5)
#         for i in range(10):
#             if i < 5:
#                 top_layout.addWidget(self.__dict__['picked_hero_' + str(i)], 0, i)
#             else:
#                 top_layout.addWidget(self.__dict__['picked_hero_' + str(i)], 0, i + 1)
#
#         pick_layout = QtWidgets.QHBoxLayout()
#         pick_layout.addWidget(self.radiant_searchbar)
#         pick_layout.addWidget(self.toradiant_btn)
#         pick_layout.addWidget(self.ban_btn)
#         pick_layout.addWidget(self.todire_btn)
#         pick_layout.addWidget(self.dire_searchbar)
#
#         str_layout = QtWidgets.QGridLayout()
#         for str_hero in STR_HEROS:
#             j = STR_HEROS.index(str_hero)
#             str_layout.addWidget(hero_labels[str_hero], int(j / 15), int(j % 15))
#
#         agi_layout = QtWidgets.QGridLayout()
#         for agi_hero in AGI_HEROS:
#             k = AGI_HEROS.index(agi_hero)
#             agi_layout.addWidget(hero_labels[agi_hero], int(k / 15), int(k % 15))
#
#         int_layout = QtWidgets.QGridLayout()
#         for int_hero in INT_HEROS:
#             l = INT_HEROS.index(int_hero)
#             int_layout.addWidget(hero_labels[int_hero], int(l / 15), int(l % 15))
#
#         layout = QtWidgets.QVBoxLayout()
#         layout.addLayout(top_layout)
#         layout.addLayout(pick_layout)
#         layout.addLayout(str_layout)
#         layout.addLayout(agi_layout)
#         layout.addLayout(int_layout)
#
#         self.setLayout(layout)
#
#     def selectHero(self, hero):
#         self.selected_hero = hero
#         self.selected_hero_label.setPixmap(QtGui.QPixmap(IMAGES[hero]))
#         print(self.picks)
#
#     def pickHero(self, side):
#         if self.selected_hero in self.pending_heros:
#             if side == 'radiant' and 'blank' in self.picks[:5]:
#                 n = self.picks.index('blank')
#             elif side == 'dire' and 'blank' in self.picks[5:]:
#                 n = self.picks[5:].index('blank') + 5
#
#             self.picks[n] = self.selected_hero
#             self.__dict__['picked_hero_' + str(n)].setPixmap(QtGui.QPixmap(IMAGES['unknown']))
#
#     def unpickHero(self, n):
#         pass
#
#     def debugfunc(self):
#         print('bug here')

def main():
    app = QtWidgets.QApplication(sys.argv)
    bp_window = BanPickWindow()
    bp_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
