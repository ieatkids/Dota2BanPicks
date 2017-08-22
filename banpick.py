import sys
from PyQt5 import QtGui, QtWidgets
from pandas import DataFrame
from basic_data import *


class BanPickWindow(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setGeometry(100, 100, 800, 600)

        self.radiant_picks = ['blank'] * 5
        self.dire_picks = ['blank'] * 5
        self.heros = dict(zip(HEROS, ['pending'] * len(HEROS)))

        # set pick bar
        for i in range(5):
            self.__setattr__('radiantpick' + str(i), QtWidgets.QLabel())
            self.__setattr__('direpick' + str(i), QtWidgets.QLabel())
            self.__dict__['radiantpick' + str(i)].setPixmap(QtGui.QPixmap(IMAGES['unknown']))
            self.__dict__['direpick' + str(i)].setPixmap(QtGui.QPixmap(IMAGES['unknown']))

        # set hero buttons
        for name in HEROS:
            self.__setattr__(name + '_btn', QtWidgets.QLabel())
            self.__dict__[name + '_btn'].setPixmap(QtGui.QPixmap(IMAGES[name]))
            self.__dict__[name + '_btn'].setToolTip(name)

        # set search bars
        search_comleter = QtWidgets.QCompleter(list(CN_HEROS.keys()))
        self.radiant_searchbar = QtWidgets.QLineEdit()
        self.radiant_searchbar.setCompleter(search_comleter)
        self.radiant_searchbar.editingFinished.connect(self.radiantPickFromSearchBar)
        self.dire_searchbar = QtWidgets.QLineEdit()
        self.dire_searchbar.setCompleter(search_comleter)
        self.dire_searchbar.editingFinished.connect(self.direPickFromSearchBar)

        #set pick buttons
        self.toradiant_btn = QtWidgets.QPushButton('←')
        self.todire_btn = QtWidgets.QPushButton('→')
        self.ban_btn = QtWidgets.QPushButton('╳')


        self.initUI()

    def initUI(self):
        top_layout = QtWidgets.QGridLayout()
        for i in range(5):
            top_layout.addWidget(self.__dict__['radiantpick' + str(i)], 0, i)
            top_layout.addWidget(self.__dict__['direpick' + str(i)], 0, 6 + i)

        pick_layout = QtWidgets.QHBoxLayout()
        pick_layout.addWidget(self.radiant_searchbar)
        pick_layout.addWidget(self.toradiant_btn)
        pick_layout.addWidget(self.ban_btn)
        pick_layout.addWidget(self.todire_btn)
        pick_layout.addWidget(self.dire_searchbar)

        str_layout = QtWidgets.QGridLayout()
        for str_hero in STR_HEROS:
            j = STR_HEROS.index(str_hero)
            str_layout.addWidget(self.__dict__[str_hero + '_btn'], int(j / 15), int(j % 15))

        agi_layout = QtWidgets.QGridLayout()
        for agi_hero in AGI_HEROS:
            k = AGI_HEROS.index(agi_hero)
            agi_layout.addWidget(self.__dict__[agi_hero + '_btn'], int(k / 15), int(k % 15))

        int_layout = QtWidgets.QGridLayout()
        for int_hero in INT_HEROS:
            l = INT_HEROS.index(int_hero)
            int_layout.addWidget(self.__dict__[int_hero + '_btn'], int(l / 15), int(l % 15))

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addLayout(pick_layout)
        layout.addLayout(str_layout)
        layout.addLayout(agi_layout)
        layout.addLayout(int_layout)

        self.setLayout(layout)

    def radiantPickFromSearchBar(self):
        if str(self.radiant_searchbar.text()) in CN_HEROS.keys() and 'blank' in self.radiant_picks:
            hero = CN_HEROS[str(self.radiant_searchbar.text())]
            if self.heros[hero] == 'pending':
                ind = self.radiant_picks.index('blank')
                self.radiant_picks[ind] = hero
                self.heros[hero] = 'radiant'
                self.__dict__['radiantpick' + str(ind)].setPixmap(QtGui.QPixmap(IMAGES[hero]))
        self.radiant_searchbar.setText('')

    def direPickFromSearchBar(self):
        if str(self.dire_searchbar.text()) in CN_HEROS.keys() and 'blank' in self.dire_picks:
            hero = CN_HEROS[str(self.dire_searchbar.text())]
            if self.heros[hero] == 'pending':
                ind = self.dire_picks.index('blank')
                self.dire_picks[ind] = hero
                self.heros[hero] = 'dire'
                self.__dict__['direpick' + str(ind)].setPixmap(QtGui.QPixmap(IMAGES[hero]))
        self.dire_searchbar.setText('')


def main():
    app = QtWidgets.QApplication(sys.argv)
    bp_window = BanPickWindow()
    bp_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
