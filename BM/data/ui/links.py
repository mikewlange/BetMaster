# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'links.ui'
#
# Created: Sat Feb  1 00:10:33 2014
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Links(object):
    def setupUi(self, Links):
        Links.setObjectName("Links")
        Links.resize(594, 577)
        self.verticalLayout_4 = QtGui.QVBoxLayout(Links)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabWidget = QtGui.QTabWidget(Links)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.West)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.button_betradar = QtGui.QPushButton(self.tab)
        self.button_betradar.setObjectName("button_betradar")
        self.horizontalLayout_4.addWidget(self.button_betradar)
        self.button_betexplorer = QtGui.QPushButton(self.tab)
        self.button_betexplorer.setObjectName("button_betexplorer")
        self.horizontalLayout_4.addWidget(self.button_betexplorer)
        self.button_previous = QtGui.QPushButton(self.tab)
        self.button_previous.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/actions/actions/agt_back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_previous.setIcon(icon)
        self.button_previous.setObjectName("button_previous")
        self.horizontalLayout_4.addWidget(self.button_previous)
        self.button_next = QtGui.QPushButton(self.tab)
        self.button_next.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/actions/actions/agt_forward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_next.setIcon(icon1)
        self.button_next.setFlat(False)
        self.button_next.setObjectName("button_next")
        self.horizontalLayout_4.addWidget(self.button_next)
        self.button_add = QtGui.QPushButton(self.tab)
        self.button_add.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/actions/actions/edit_add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_add.setIcon(icon2)
        self.button_add.setObjectName("button_add")
        self.horizontalLayout_4.addWidget(self.button_add)
        self.line_name = QtGui.QLineEdit(self.tab)
        self.line_name.setMaximumSize(QtCore.QSize(150, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(243, 237, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(243, 237, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(247, 247, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.line_name.setPalette(palette)
        self.line_name.setObjectName("line_name")
        self.horizontalLayout_4.addWidget(self.line_name)
        self.line_url = QtGui.QLineEdit(self.tab)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(243, 237, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(243, 237, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(247, 247, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.line_url.setPalette(palette)
        self.line_url.setObjectName("line_url")
        self.horizontalLayout_4.addWidget(self.line_url)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.label = QtGui.QLabel(self.tab)
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label)
        self.webView = QtWebKit.QWebView(self.tab)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(243, 237, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(243, 237, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(247, 247, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.webView.setPalette(palette)
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")
        self.verticalLayout_5.addWidget(self.webView)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tree_link_bases = QtGui.QTreeWidget(self.tab)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(243, 237, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(243, 237, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(247, 247, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.tree_link_bases.setPalette(palette)
        self.tree_link_bases.setObjectName("tree_link_bases")
        self.tree_link_bases.headerItem().setText(0, "1")
        self.verticalLayout.addWidget(self.tree_link_bases)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_save = QtGui.QPushButton(self.tab)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/actions/actions/filesaveas.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_save.setIcon(icon3)
        self.button_save.setObjectName("button_save")
        self.horizontalLayout_2.addWidget(self.button_save)
        self.line_save = QtGui.QLineEdit(self.tab)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(243, 237, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(243, 237, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(247, 247, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.line_save.setPalette(palette)
        self.line_save.setInputMask("")
        self.line_save.setObjectName("line_save")
        self.horizontalLayout_2.addWidget(self.line_save)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_delete = QtGui.QPushButton(self.tab)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/actions/actions/editdelete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_delete.setIcon(icon4)
        self.button_delete.setObjectName("button_delete")
        self.horizontalLayout.addWidget(self.button_delete)
        self.button_load = QtGui.QPushButton(self.tab)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/actions/actions/fileopen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_load.setIcon(icon5)
        self.button_load.setObjectName("button_load")
        self.horizontalLayout.addWidget(self.button_load)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tree_url = QtGui.QTreeWidget(self.tab)
        self.tree_url.setMinimumSize(QtCore.QSize(0, 200))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(243, 237, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(243, 237, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(247, 247, 247))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.tree_url.setPalette(palette)
        self.tree_url.setObjectName("tree_url")
        self.tree_url.headerItem().setText(0, "1")
        self.verticalLayout_2.addWidget(self.tree_url)
        self.button_check = QtGui.QPushButton(self.tab)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/actions/actions/reload.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_check.setIcon(icon6)
        self.button_check.setObjectName("button_check")
        self.verticalLayout_2.addWidget(self.button_check)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.button_remove = QtGui.QPushButton(self.tab)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/actions/actions/edit_remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_remove.setIcon(icon7)
        self.button_remove.setObjectName("button_remove")
        self.horizontalLayout_3.addWidget(self.button_remove)
        self.button_clear = QtGui.QPushButton(self.tab)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/actions/actions/editclear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_clear.setIcon(icon8)
        self.button_clear.setObjectName("button_clear")
        self.horizontalLayout_3.addWidget(self.button_clear)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.tabWidget.addTab(self.tab, "")
        self.verticalLayout_4.addWidget(self.tabWidget)

        self.retranslateUi(Links)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Links)

    def retranslateUi(self, Links):
        Links.setWindowTitle(QtGui.QApplication.translate("Links", "Links creator", None, QtGui.QApplication.UnicodeUTF8))
        self.button_betradar.setText(QtGui.QApplication.translate("Links", "Betradar", None, QtGui.QApplication.UnicodeUTF8))
        self.button_betexplorer.setText(QtGui.QApplication.translate("Links", "Betexplorer", None, QtGui.QApplication.UnicodeUTF8))
        self.line_name.setText(QtGui.QApplication.translate("Links", "league_name", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Links", "<html><head/><body><p><span style=\" font-weight:600;\">Betradar</span> : choose league, go to fixtures, select \'full listing\' and \'week by week\'.</p><p><span style=\" font-weight:600;\">Betexplorer: </span>example link : http://www.betexplorer.com/soccer/netherlands/eredivisie/</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.button_save.setText(QtGui.QApplication.translate("Links", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.line_save.setText(QtGui.QApplication.translate("Links", "name", None, QtGui.QApplication.UnicodeUTF8))
        self.button_delete.setText(QtGui.QApplication.translate("Links", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.button_load.setText(QtGui.QApplication.translate("Links", "Load", None, QtGui.QApplication.UnicodeUTF8))
        self.button_check.setText(QtGui.QApplication.translate("Links", "Check", None, QtGui.QApplication.UnicodeUTF8))
        self.button_remove.setText(QtGui.QApplication.translate("Links", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.button_clear.setText(QtGui.QApplication.translate("Links", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("Links", "Scrape website", None, QtGui.QApplication.UnicodeUTF8))

from PySide import QtWebKit
import icons_rc
