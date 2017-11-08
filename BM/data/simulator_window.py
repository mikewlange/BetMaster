# -*- coding: utf-8 -*-
"""
Copyright 2013 Jacek Markowski, jacek87markowski@gmail.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import sys
import csv
import os
import shutil
from csv import reader
import locale

from PySide import QtCore, QtGui
from ui.simulator import Ui_Simulator
from bb_engine import Database
from bb_shared import Shared

class SimulatorApp(QtGui.QWidget, Database, Shared):
    '''Creates gui and events  '''
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        Database.__init__(self, parent)
        Shared.__init__(self)
        self.app = 'simulator'
        self.gui = Ui_Simulator()
        self.gui.setupUi(self)
        self.gui.tree_leagues.headerItem().setText(0, ('Leagues'))
        self.gui.tree_nets.headerItem().setText(0, ('Nets'))
        self.gui.tree_ranges.headerItem().setText(0, ('Net ranges'))
        self.gui.tree_ranges_profile.headerItem().setText(0, ('Net ranges'))
        self.gui.tree_bets.headerItem().setText(0, ('Selection filters'))
        self.gui.tree_profiles.headerItem().setText(0, ('Profiles'))
        self.gui.tree_filters.headerItem().setText(0, ('Simulation filters'))
        labels = ['Path',
                        'League',
                        'Net',
                        'Simulation filter',
                        'Net ranges',
                        'Bet filters',
                        'R_min',
                        'R_max',
                        'Odds level']
        for i in range(0, len(labels)):
            self.gui.tree_batch.headerItem().setText(i,
                                                   (labels[i]))
        labels = [
        'Results',
        'Path',
        'League',
        'Net',
        'Filter',
        'Ranges',
        'Bet_selector',
        'R_min',
        'R_max',
        'Odds level']
        for i in range(0, len(labels)):
            self.gui.tree_hits.headerItem().setText(i,
                                                  (labels[i]))
        self.gui.tree_hits.setColumnWidth(0, 200)
        labels = ['Selected bets']
        for i in range(0, 1):
            self.gui.tree_bets_selected.headerItem().setText(i,
                                                   (labels[i]))

        # try to show files in folders profile
        trees = (
        self.leagues_tree,
        self.nets_tree,
        self.ranges_tree,
        self.bets_tree,
        self.batch_profiles_tree,
        self.filters_tree)
        for i in trees:
            try:
                i()
            except:
                pass
        self.filter_combos_spins()
        # load filters at startup
        profiles = (self.bets_load, self.ranges_load, self.filters_load)
        for i in profiles:
            try:
                i()
            except:
                pass

        # size of columns
        labels = ['Date','Home','Away','Result','Bet','Odd','Net','Status']
        self.gui.table_preview.setColumnCount(len(labels))
        self.gui.table_preview.setHorizontalHeaderLabels(labels)
        self.gui.table_preview.setRowCount(0)
        self.gui.table_filtered.setColumnCount(len(labels))
        self.gui.table_filtered.setHorizontalHeaderLabels(labels)
        self.gui.table_filtered.setRowCount(0)
        self.gui.table_preview.setItem(0, 1, QtGui.QTableWidgetItem('test'))
        self.gui.table_filtered.setItem(0, 1, QtGui.QTableWidgetItem('test'))
        self.gui.table_preview.clear()
        self.gui.table_filtered.clear()
        self.gui.table_filtered.setColumnWidth(0, 90)
        self.gui.table_filtered.setColumnWidth(1, 90)
        self.gui.table_filtered.setColumnWidth(2, 90)
        self.gui.table_filtered.setColumnWidth(3, 60)
        self.gui.table_filtered.setColumnWidth(4, 60)
        self.gui.table_filtered.setColumnWidth(5, 60)
        self.gui.table_filtered.setColumnWidth(6, 100)
        self.gui.table_preview.setColumnWidth(0, 100)
        self.gui.table_preview.setColumnWidth(1, 100)
        self.gui.table_preview.setColumnWidth(2, 100)
        self.gui.table_preview.setColumnWidth(3, 50)
        self.gui.table_preview.setColumnWidth(4, 80)
        labels = ['Date','Home','Away','Result','Goals','Bet','Odd','Net','Status']
        self.gui.table_preview.setColumnCount(len(labels))
        self.gui.table_preview.setHorizontalHeaderLabels(labels)
        self.gui.table_preview.setRowCount(0)
        self.gui.table_filtered.setColumnCount(len(labels))
        self.gui.table_filtered.setHorizontalHeaderLabels(labels)
        self.gui.table_filtered.setRowCount(0)
        try:
            self.auto_load()
        except:
            print 'restore settings problem'
        self.bindings()

    def closeEvent(self, event):
        self.stop_action = 1
        event.accept()


    def bindings(self):
        ''' Widgets bindings'''
        self.gui.spin_1_max.valueChanged.connect(self.spins_manage)
        self.gui.spin_1x_max.valueChanged.connect(self.spins_manage)
        self.gui.spin_x_max.valueChanged.connect(self.spins_manage)
        self.gui.spin_x2_max.valueChanged.connect(self.spins_manage)
        self.gui.spin_2_max.valueChanged.connect(self.spins_manage)
        self.gui.spin_1_min.valueChanged.connect(self.spins_manage)
        self.gui.spin_1x_min.valueChanged.connect(self.spins_manage)
        self.gui.spin_x_min.valueChanged.connect(self.spins_manage)
        self.gui.spin_x2_min.valueChanged.connect(self.spins_manage)
        self.gui.spin_2_min.valueChanged.connect(self.spins_manage)
        self.gui.button_ranges_save.clicked.connect(self.ranges_save)
        self.gui.button_ranges_load.clicked.connect(self.ranges_load)
        self.gui.tree_ranges_profile.clicked.connect(self.ranges_name)
        self.gui.button_ranges_delete.clicked.connect(self.ranges_delete)
        self.gui.button_add.clicked.connect(self.batch_add)
        self.gui.button_batch_remove.clicked.connect(self.batch_remove)
        self.gui.button_batch_clear.clicked.connect(self.batch_clear)
        self.gui.button_batch_save.clicked.connect(self.batch_save)
        self.gui.button_batch_load.clicked.connect(self.batch_load)
        self.gui.tree_profiles.clicked.connect(self.batch_name)
        self.gui.button_batch_delete.clicked.connect(self.batch_delete)
        self.gui.button_bets_load.clicked.connect(self.bets_load)
        self.gui.tree_bets_profile.clicked.connect(self.bets_name)
        self.gui.button_bets_save.clicked.connect(self.bets_save)
        self.gui.button_bets_delete.clicked.connect(self.bets_delete)
        self.gui.button_filters_save.clicked.connect(self.filters_save)
        self.gui.button_filters_load.clicked.connect(self.filters_load)
        self.gui.tree_filters_profile.clicked.connect(self.filters_name)
        self.gui.button_filters_delete.clicked.connect(self.filters_delete)
        self.gui.button_batch_run.clicked.connect(self.simulation_batch)
        self.gui.button_preview_show.clicked.connect(self.simulation_show)
        self.gui.button_save_reports.clicked.connect(self.simulation_reports_save)
        self.gui.button_preview_save.clicked.connect(self.batch_preview_save)
        self.gui.button_bets_final_save.clicked.connect(self.bets_final_save)
        self.gui.combo_points.currentIndexChanged.connect(self.filter_combos_spins)
        self.gui.combo_points_ha.currentIndexChanged.connect(self.filter_combos_spins)
        self.gui.combo_form.currentIndexChanged.connect(self.filter_combos_spins)
        self.gui.combo_form_ha.currentIndexChanged.connect(self.filter_combos_spins)
        self.gui.spin_points.valueChanged.connect(self.filter_combos_spins)
        self.gui.spin_points_ha.valueChanged.connect(self.filter_combos_spins)
        self.gui.spin_form.valueChanged.connect(self.filter_combos_spins)
        self.gui.spin_form_ha.valueChanged.connect(self.filter_combos_spins)
        self.gui.spin_rounds_min.valueChanged.connect(self.combos_rounds)
        self.gui.spin_rounds_max.valueChanged.connect(self.combos_rounds)
        self.gui.button_stop.clicked.connect(self.simulation_stop)
        # double click
        self.gui.tree_leagues.doubleClicked.connect(self.batch_add)
        # mark
        self.gui.button_mark.clicked.connect(self.mark_color)
        # auto save bindings
        self.gui.spin_rounds_max.valueChanged.connect(self.auto_save)
        self.gui.spin_rounds_min.valueChanged.connect(self.auto_save)
        self.gui.spin_odds_level.valueChanged.connect(self.auto_save)
        self.gui.tree_nets.itemClicked.connect(self.auto_save)
        self.gui.tree_filters.itemClicked.connect(self.auto_save)
        self.gui.tree_ranges.itemClicked.connect(self.auto_save)
        self.gui.tree_bets.itemClicked.connect(self.auto_save)
    def combos_rounds(self):
        ''' Prevents spins to have conflicting values'''
        val = [
        self.gui.spin_rounds_min,
        self.gui.spin_rounds_max,
        ]

        if val[0].value() >= val[1].value():
            number = val[0].value()
            val[1].setValue(number)

    def filter_combos_spins(self):
        ''' Changes values of combos and spins for away team'''
        combos = [
        (self.gui.combo_points,self.gui.combo_points_2),
        (self.gui.combo_points_ha,self.gui.combo_points_ha_2),
        (self.gui.combo_form,self.gui.combo_form_2),
        (self.gui.combo_form_ha,self.gui.combo_form_ha_2)]
        spins = [
        (self.gui.spin_points,self.gui.spin_points_2),
        (self.gui.spin_points_ha,self.gui.spin_points_ha_2),
        (self.gui.spin_form,self.gui.spin_form_2),
        (self.gui.spin_form_ha,self.gui.spin_form_ha_2)]

        for i in combos:
            if i[0].currentText() == '>=':
                i[1].setItemText(0,'<=')
            elif  i[0].currentText() == '<=':
                i[1].setItemText(0,'>=')

        for i in spins:
            val1 = i[0].value()
            val2 = 100 - i[0].value()
            i[0].setValue(val1)
            i[1].setValue(val2)


    def spins_manage(self):
        ''' Prevents spins to have conflicting values'''
        val = [
        self.gui.spin_1_min,
        self.gui.spin_1_max,
        self.gui.spin_1x_min,
        self.gui.spin_1x_max,
        self.gui.spin_x_min,
        self.gui.spin_x_max,
        self.gui.spin_x2_min,
        self.gui.spin_x2_max,
        self.gui.spin_2_min,
        self.gui.spin_2_max
        ]

        for i in range(1, len(val)):
            if val[i].value() <= val[i-1].value():
                number = val[i-1].value()
                val[i].setValue(number)

    def leagues_tree(self):
        ''' Fills tree with available csv files'''
        self.gui.tree_leagues.sortItems(0, QtCore.Qt.SortOrder(0))
        paths = []
        for i in os.walk("leagues/"):
            paths.append(i[0])
        paths.pop(0)
        paths.reverse()
        for i in paths:
            name = os.path.split(i)
            name = name[1]
            item = QtGui.QTreeWidgetItem(self.gui.tree_leagues)
            item.setText(0, (name))
            files = os.listdir(i)
            for f in files:
                QtGui.QTreeWidgetItem(item).setText(0, f)
        self.gui.tree_leagues.setSortingEnabled(0)
        item.setExpanded(1)
        self.gui.tree_leagues.setCurrentItem(item.child(0))
        self.gui.tree_leagues.setSortingEnabled(1)

    def nets_tree(self):
        ''' Fills tree with available csv files'''
        self.gui.tree_nets.clear()
        self.gui.tree_nets.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_nets.setSortingEnabled(1)
        dir_exports = os.listdir(os.path.join('net'))
        for i in dir_exports:
            item_exp = QtGui.QTreeWidgetItem(self.gui.tree_nets)
            item_exp.setText(0, (i))
        self.gui.tree_nets.setCurrentItem(item_exp)
        self.gui.tree_nets.setSortingEnabled(1)

    def batch_profiles_tree(self):
        self.gui.tree_profiles.clear()
        self.gui.tree_profiles.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_profiles.setSortingEnabled(1)
        dir_exports = os.listdir(os.path.join('profiles','simulation'))
        for i in dir_exports:
            item_exp = QtGui.QTreeWidgetItem(self.gui.tree_profiles)
            item_exp.setText(0, (i))

    def ranges_tree(self):
        ''' Fills tree with available files'''
        self.gui.tree_ranges.clear()
        self.gui.tree_ranges.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_ranges.setSortingEnabled(1)
        dir_exports = os.listdir(os.path.join('profiles','ranges'))
        for i in dir_exports:
            item_exp = QtGui.QTreeWidgetItem(self.gui.tree_ranges)
            item_exp.setText(0, (i))
        self.gui.tree_ranges.setCurrentItem(item_exp)
        self.gui.tree_ranges.setSortingEnabled(1)
        self.gui.tree_ranges_profile.clear()
        self.gui.tree_ranges_profile.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_ranges_profile.setSortingEnabled(1)
        dir_exports = os.listdir(os.path.join('profiles','ranges'))
        for i in dir_exports:
            item_exp = QtGui.QTreeWidgetItem(self.gui.tree_ranges_profile)
            item_exp.setText(0, (i))
        self.gui.tree_ranges_profile.setCurrentItem(item_exp)

    def ranges_save(self):
        ''' Saves ranges profiles'''
        self.min_1=self.gui.spin_1_min.value()
        self.min_1x=self.gui.spin_1x_min.value()
        self.min_x=self.gui.spin_x_min.value()
        self.min_x2=self.gui.spin_x2_min.value()
        self.min_2=self.gui.spin_2_min.value()
        self.max_1=self.gui.spin_1_max.value()
        self.max_1x=self.gui.spin_1x_max.value()
        self.max_x=self.gui.spin_x_max.value()
        self.max_x2=self.gui.spin_x2_max.value()
        self.max_2=self.gui.spin_2_max.value()
        val = [
        self.min_1,
        self.max_1,
        self.min_1x,
        self.max_1x,
        self.min_x,
        self.max_x,
        self.min_x2,
        self.max_x2,
        self.min_2,
        self.max_2
        ]
        file_name = self.gui.line_ranges.text()
        with open(os.path.join('profiles','ranges',file_name),'w') as save:
            for i in val:
                save.write(str(i)+self.nl)
        self.ranges_tree()

    def ranges_delete(self):
        ''' Delete ranges profile'''
        path = os.path.join('profiles','ranges','')
        item = self.gui.tree_ranges_profile.currentItem()
        file_delete = item.text(0)
        self.delete_file(file_delete,path)
        self.ranges_tree()

    def ranges_name(self):
        item = self.gui.tree_ranges_profile.currentItem()
        file_name = item.text(0)
        self.gui.line_ranges.setText(file_name)
    def ranges_load(self):
        ''' Load ranges profiles'''
        val = [
        self.gui.spin_1_min,
        self.gui.spin_1_max,
        self.gui.spin_1x_min,
        self.gui.spin_1x_max,
        self.gui.spin_x_min,
        self.gui.spin_x_max,
        self.gui.spin_x2_min,
        self.gui.spin_x2_max,
        self.gui.spin_2_min,
        self.gui.spin_2_max
        ]
        item = self.gui.tree_ranges_profile.currentItem()
        file_name = item.text(0)
        with open(os.path.join('profiles','ranges',file_name),'r') as f:
            load = list(f)
        for i in range(0,len(val)):
            item =self.rm_lines(load[i])
            val[i].setValue(float(item))

    def batch_remove(self):
        ''' Delete batch profile'''
        item = self.gui.tree_batch.currentItem()
        index = self.gui.tree_batch.indexOfTopLevelItem(item)
        self.gui.tree_batch.takeTopLevelItem(index)

    def batch_clear(self):
        ''' Clears batch tree'''
        self.gui.tree_batch.clear()

    def batch_add(self):
        ''' Add item to batch tree'''
        #Wtry:
        item = self.gui.tree_nets.currentItem()
        net = item.text(0)
        item = self.gui.tree_leagues.currentItem()
        league = item.text(0)
        path =item.parent()
        path = path.text(0)
        item = self.gui.tree_filters.currentItem()
        filters = item.text(0)
        item = self.gui.tree_ranges.currentItem()
        ranges = item.text(0)
        item = self.gui.tree_bets.currentItem()
        bets = item.text(0)
        r_min = self.gui.spin_rounds_min.value()
        r_max = self.gui.spin_rounds_max.value()
        odds = self.gui.spin_odds_level.value()
        if path != None:
            val = [path,
                   league,
                   net,
                   filters,
                   ranges,
                   bets,
                   r_min,
                   r_max,
                   odds]
            
            item = QtGui.QTreeWidgetItem(self.gui.tree_batch)
            for i in range(0,len(val)):
                item.setText(i,(str(val[i])))
        #except:
        #    print 'Cant adds some error in batch_add'

    def batch_save(self):
        ''' Save items in bath tree'''
        file_name = self.gui.line_batch.text()
        with open(os.path.join('profiles','simulation',str(file_name))\
            , 'w') as file_save:
            count = self.gui.tree_batch.topLevelItemCount()
            for i in range(0,count):
                item = self.gui.tree_batch.topLevelItem(i)
                path = item.text(0)
                league = item.text(1)
                net = item.text(2)
                filters = item.text(3)
                ranges = item.text(4)
                bets = item.text(5)
                r_min = item.text(6)
                r_max = item.text(7)
                odds = item.text(8)
                val = [path,
                        league,
                        net,
                        filters,
                        ranges,
                        bets,
                        r_min,
                        r_max,
                        odds]
                line = ''
                for i in val:
                    line+=i+','
                line = line +self.nl
                file_save.write(line)
        self.batch_profiles_tree()

    def batch_delete(self):
        ''' Deletes batch profile'''
        path = os.path.join('profiles','simulation','')
        item = self.gui.tree_profiles.currentItem()
        file_delete = item.text(0)
        self.delete_file(file_delete,path)
        self.batch_profiles_tree()

    def batch_name(self):
        item = self.gui.tree_profiles.currentItem()
        file_name = item.text(0)
        self.gui.line_batch.setText(file_name)

    def batch_load(self):
        ''' Loads batch profile'''
        self.gui.tree_batch.clear()
        item = self.gui.tree_profiles.currentItem()
        file_name = item.text(0)
        with open(os.path.join('profiles','simulation',file_name),'r') as f:
            load = reader(f)
            for i in load:
                item = QtGui.QTreeWidgetItem(self.gui.tree_batch)
                for n in range(0,9):
                    item.setText(n,(i[n]))

    def bets_tree(self):
        ''' Filss tree in both tabs with saved bets filters'''
        self.gui.tree_bets.clear()
        self.gui.tree_bets.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_bets.setSortingEnabled(1)
        dir_exports = os.listdir(os.path.join('profiles','bets'))
        for i in dir_exports:
            item_exp = QtGui.QTreeWidgetItem(self.gui.tree_bets)
            item_exp.setText(0, (i))
        self.gui.tree_bets.setCurrentItem(item_exp)
        self.gui.tree_bets.setSortingEnabled(1)
        self.gui.tree_bets_profile.clear()
        self.gui.tree_bets_profile.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_bets_profile.setSortingEnabled(1)
        self.gui.tree_bets_profile.headerItem().setText(0, ('Bet filters'))
        dir_exports = os.listdir(os.path.join('profiles','bets'))
        for i in dir_exports:
            item_exp = QtGui.QTreeWidgetItem(self.gui.tree_bets_profile)
            item_exp.setText(0, (i))
        self.gui.tree_bets_profile.setCurrentItem(item_exp)

    def bets_name(self):
        item = self.gui.tree_bets_profile.currentItem()
        file_name = item.text(0)
        self.gui.line_bets_save.setText(file_name)

    def bets_load(self):
        ''' Load bets profiles'''
        val = [
        self.gui.spin_acc_1,
        self.gui.spin_acc_x,
        self.gui.spin_acc_2,
        self.gui.spin_acc_1x,
        self.gui.spin_acc_x2,
        self.gui.spin_bet_odd_1_min,
        self.gui.spin_bet_odd_x_min,
        self.gui.spin_bet_odd_2_min,
        self.gui.spin_bet_odd_1x_min,
        self.gui.spin_bet_odd_x2_min,
        self.gui.spin_bet_odd_1_max,
        self.gui.spin_bet_odd_x_max,
        self.gui.spin_bet_odd_2_max,
        self.gui.spin_bet_odd_1x_max,
        self.gui.spin_bet_odd_x2_max
        ]
        item = self.gui.tree_bets_profile.currentItem()
        file_name = item.text(0)
        with open(os.path.join('profiles','bets',file_name),'r') as f:
            load = list(f)
        for i in range(0,len(val)):
            item =self.rm_lines(load[i])
            val[i].setValue(float(item))



    def bets_delete(self):
        ''' Deletes bets profile'''
        path = os.path.join('profiles','bets','')
        item = self.gui.tree_bets_profile.currentItem()
        file_delete = item.text(0)
        self.delete_file(file_delete,path)
        self.bets_tree()

    def bets_final_save(self):
        ''' Save selected bets'''
        file_name = QtGui.QFileDialog.getSaveFileName(self, 'Save selected bets', 'saves/')
        with open(file_name[0],'w') as file_save:
            count = self.gui.tree_bets_selected.topLevelItemCount()
            for i in range(0,count):
                item = self.gui.tree_bets_selected.topLevelItem(i)
                simulation = item.text(0)
                line = simulation+self.nl
                file_save.write(line)
                child_num = item.childCount()
                for i in range(0,child_num):
                    name = item.child(i)
                    name = name.text(0)
                    line = name+self.nl
                    file_save.write('.........'+line)

    def bets_save(self):
        ''' Saves bets profiles'''
        acc_1=self.gui.spin_acc_1.value()
        acc_x=self.gui.spin_acc_x.value()
        acc_2=self.gui.spin_acc_2.value()
        acc_1x=self.gui.spin_acc_1x.value()
        acc_x2=self.gui.spin_acc_x2.value()
        odd_1_min=self.gui.spin_bet_odd_1_min.value()
        odd_x_min=self.gui.spin_bet_odd_x_min.value()
        odd_2_min=self.gui.spin_bet_odd_2_min.value()
        odd_1x_min=self.gui.spin_bet_odd_1x_min.value()
        odd_x2_min=self.gui.spin_bet_odd_x2_min.value()

        odd_1_max=self.gui.spin_bet_odd_1_max.value()
        odd_x_max=self.gui.spin_bet_odd_x_max.value()
        odd_2_max=self.gui.spin_bet_odd_2_max.value()
        odd_1x_max=self.gui.spin_bet_odd_1x_max.value()
        odd_x2_max=self.gui.spin_bet_odd_x2_max.value()

        val = [
        acc_1,
        acc_x,
        acc_2,
        acc_1x,
        acc_x2,
        odd_1_min,
        odd_x_min,
        odd_2_min,
        odd_1x_min,
        odd_x2_min,
        odd_1_max,
        odd_x_max,
        odd_2_max,
        odd_1x_max,
        odd_x2_max
        ]
        file_name = self.gui.line_bets_save.text()
        with open(os.path.join('profiles','bets',file_name),'w') as save:
            for i in val:
                save.write(str(i)+self.nl)
        self.bets_tree()

    def batch_preview_save(self):
        ''' Saves batch profile'''
        file_name = self.gui.line_preview_save.text()
        green = QtGui.QColor('#11BD00')
        with open(os.path.join('profiles','simulation',str(file_name))\
        , 'w') as file_save:
            count = self.gui.tree_hits.topLevelItemCount()
            for i in range(0,count):
                item = self.gui.tree_hits.topLevelItem(i)
                path = item.text(1)
                league = item.text(2)
                net = item.text(3)
                filters = item.text(4)
                ranges = item.text(5)
                bets = item.text(6)
                r_min = item.text(7)
                r_max = item.text(8)
                odds = item.text(9)

                val = [path,
                        league,
                        net,
                        filters,
                        ranges,
                        bets,
                        r_min,
                        r_max,
                        odds]
                line = ''
                if item.background(0) == green:
                    for i in val:
                        line+=i+','
                    line = line +self.nl
                    file_save.write(line)
        self.batch_profiles_tree()

    def simulation_batch(self):
        self.simulation_run(mode=0)

    def simulation_show(self):
        #self.simulation_run(mode=1)
        self.gui.table_filtered.setSortingEnabled(False)
        self.gui.table_preview.setSortingEnabled(False)
        self.gui.table_preview.setRowCount(0)
        self.gui.table_filtered.setRowCount(0)

        selected = self.gui.tree_hits.currentIndex().row()
        green = QtGui.QColor('#11BD00')
        red = QtGui.QColor('#C40202')
        with open(os.path.join('tmp','simulations',(str(selected)+'full')), 'r') as stream:
            table = csv.reader(stream)
            table = list(table)
        for i in range(0, len(table)):
            rows_all = self.gui.table_preview.rowCount()
            index = 0
            if table[i][8] == 'Miss':
                color = red
            else:
                color = green
            for j in table[i]:
                item = QtGui.QTableWidgetItem()
                if table[i].index(j) == 7 or table[i].index(j) == 6:
                    item.setData(QtCore.Qt.EditRole,float(j))
                else:
                    item.setData(QtCore.Qt.EditRole,j)
                self.gui.table_preview.setRowCount(rows_all+1)
                self.gui.table_preview.setItem(rows_all, index, item)
                self.gui.table_preview.item(rows_all, index).\
                        setBackground(QtGui.QColor(color))
                index +=1
        with open(os.path.join('tmp','simulations',(str(selected)+'filter')), 'r') as stream:
            table = csv.reader(stream)
            table = list(table)
        for i in range(0, len(table)):
            rows_all = self.gui.table_filtered.rowCount()
            index = 0
            if table[i][8] == 'Miss':
                color = red
            else:
                color = green

            for j in table[i]:
                item = QtGui.QTableWidgetItem()
                if table[i].index(j) == 7 or table[i].index(j) == 6:
                    item.setData(QtCore.Qt.EditRole,float(j))
                else:
                    item.setData(QtCore.Qt.EditRole,j)
                self.gui.table_filtered.setRowCount(rows_all+1)
                self.gui.table_filtered.setItem(rows_all, index, item)
                self.gui.table_filtered.item(rows_all, index).\
                    setBackground(QtGui.QColor(color))
                index +=1

        self.gui.table_filtered.setSortingEnabled(True)
        self.gui.table_preview.setSortingEnabled(True)
    def simulation_stop(self):
        ''' Stops simulation'''
        self.stop_action = 1
    def simulation_run(self,mode=0):
        ''' Runs all selected simulations
        mode 0 - batch simulation
        mode 1 - restart selected simulation (after batch simulation)'''
        self.stop_action = 0
        self.id_simulation = -1 # simulation id used as name for temp save file of simulation
        self.gui.table_filtered.setSortingEnabled(False)
        self.gui.table_preview.setSortingEnabled(False)
        if mode == 0:
            self.gui.tree_hits.clear()
            self.gui.tree_bets_selected.clear()
            count = self.gui.tree_batch.topLevelItemCount()
            self.gui.tabWidget.setCurrentIndex(1)
        elif mode == 1:
            count = 1

        for i in range(0,count):
            if mode == 0:
                sim = self.gui.tree_batch.topLevelItem(i)
            elif mode ==1:
                item = self.gui.tree_hits.currentItem()
                sim = item
            self.sim_stats = {
            'Path':'-',
            'League':'-',
            'Net':'-',
            'Filter':'-',
            'Ranges':'-',
            'Bet_selector':'-',
            'R_min':'-',
            'R_max':'-',
            'matches_filter':0.0,
            'matches_odds':0.0,
            'bets':0.0,
            'Overall':0.0,
            '1x,x2':0.0,
            '1,x,2':0.0,
            '1':0.0,
            '1 hit':0.0,
            '1x':0.0,
            '1x hit':0.0,
            'x':0.0,
            'x hit':0.0,
            'x2':0.0,
            'x2 hit':0.0,
            '2':0.0,
            '2 hit':0.0,
            'Overall yield':0.0,
            '1x,x2 yield':0.0,
            '1,x,2 yield':0.0,
            '1 yield':0.0,
            'x yield':0.0,
            '2 yield':0.0,
            '1x yield':0.0,
            'x2 yield':0.0,
            '1 balance':0.0,
            'x balance':0.0,
            '2 balance':0.0,
            '1x balance':0.0,
            'x2 balance':0.0,
            'Overall odd_avg':0.0,
            '1,x,2 odd_avg':0.0,
            '1x,x2 odd_avg':0.0,
            '1 odd_avg':0.0,
            'x odd_avg':0.0,
            '2 odd_avg':0.0,
            '1x odd_avg':0.0,
            'x2 odd_avg':0.0,
            '1 odd_balance':0.0,
            'x odd_balance':0.0,
            '2 odd_balance':0.0,
            '1x odd_balance':0.0,
            'x2 odd_balance':0.0,
            'T-odd_1':0.0,
            'T-odd_x':0.0,
            'T-odd_2':0.0,
            'T-odd_1x':0.0,
            'T-odd_x2':0.0,
            'T-points':0.0,
            'T-pointsH/A':0.0,
            'T-form':0.0,
            'T-formH/A':0.0,
            'T1-wins':0.0,
            'T1-wins_home':0.0,
            'T1-draws':0.0,
            'T1-draws_home':0.0,
            'T1-loses':0.0,
            'T1-loses_home':0.0,
            'T1-nowins':0.0,
            'T1-nowins_home':0.0,
            'T1-nodraws':0.0,
            'T1-nodraws_home':0.0,
            'T1-noloses':0.0,
            'T1-noloses_home':0.0,
            'T1-bts':0.0,
            'T1-bts_home':0.0,
            'T1-over':0.0,
            'T1-over_home':0.0,
            'T1-under':0.0,
            'T1-under_home':0.0,
            'T2-wins':0.0,
            'T2-wins_away':0.0,
            'T2-draws':0.0,
            'T2-draws_away':0.0,
            'T2-loses':0.0,
            'T2-loses_away':0.0,
            'T2-nowins':0.0,
            'T2-nowin_saway':0.0,
            'T2-nodraws':0.0,
            'T2-nodraws_away':0.0,
            'T2-noloses':0.0,
            'T2-noloses_away':0.0,
            'T2-bts':0.0,
            'T2-bts_away':0.0,
            'T2-over':0.0,
            'T2-over_away':0.0,
            'T2-under':0.0,
            'T2-under_away':0.0}

            if mode == 0:
                self.sim_stats['Path']= str(sim.text(0))
                self.sim_stats['League']= str(sim.text(1))
                self.sim_stats['Net']= str(sim.text(2))

                self.sim_stats['Filter']= str(sim.text(3))
                self.sim_stats['Ranges']= str(sim.text(4))
                self.sim_stats['Bet_selector']= str(sim.text(5))
                self.sim_stats['R_min']= str(sim.text(6))
                self.sim_stats['R_max']= str(sim.text(7))
                self.odds_level = float(sim.text(8))
            elif mode == 1:
                self.sim_stats['Path']= str(sim.text(1))
                self.sim_stats['League']= str(sim.text(2))
                self.sim_stats['Net']= str(sim.text(3))
                self.sim_stats['Filter']= str(sim.text(4))
                self.sim_stats['Ranges']= str(sim.text(5))
                self.sim_stats['Bet_selector']= str(sim.text(6))
                self.sim_stats['R_min']= str(sim.text(7))
                self.sim_stats['R_max']= str(sim.text(8))
                self.odds_level = float(sim.text(9))
            rounds_min = int(self.sim_stats['R_min'])
            rounds_max = int(self.sim_stats['R_max'])
            self.gui.table_preview.clear()
            self.gui.table_filtered.clear()
            labels = ['Date','Home','Away','Result','Goals','Bet','Odd','Net','Status']
            self.gui.table_preview.setColumnCount(len(labels))
            self.gui.table_preview.setHorizontalHeaderLabels(labels)
            self.gui.table_preview.setRowCount(0)
            self.gui.table_filtered.setColumnCount(len(labels))
            self.gui.table_filtered.setHorizontalHeaderLabels(labels)
            self.gui.table_filtered.setRowCount(0)
            # ranges
            with open(os.path.join('profiles','ranges',self.sim_stats['Ranges'])\
            ,'r') as ranges:
                load = list(ranges)
            val = []
            for i in range(0,len(load)):
                item = self.rm_lines(load[i])
                item = float(item)
                val.append(item)
            self.min_1 = val[0]
            self.max_1 = val[1]
            self.min_1x = val[2]
            self.max_1x = val[3]
            self.min_x = val[4]
            self.max_x = val[5]
            self.min_x2 = val[6]
            self.max_x2 = val[7]
            self.min_2 = val[8]
            self.max_2 = val[9]
            # filters
            self.filters_load(self.sim_stats['Filter'])
            locale.setlocale(locale.LC_ALL, "C")
            if self.stop_action == 0:

                self.load_csv(os.path.join('leagues',
                            self.sim_stats['Path'],''),
                            self.sim_stats['League'],
                            r_min=rounds_min,
                            r_max=rounds_max,
                            mode=2,
                            net=self.sim_stats['Net'])
            if mode == 0:
                self.id_simulation += 1
                self.simulation_stats() # stats for simulation
                self.simulation_save_temp() # save results to text file
        if mode == 0 and self.stop_action == 0:
            pass
            #self.gui.tabWidget.setCurrentIndex(2)  #change tab
        self.gui.table_filtered.setSortingEnabled(True)
        self.gui.table_preview.setSortingEnabled(True)

    def simulation_save_temp(self):
        """Saves results of every simulation in batch for loading after clicking"""
        with open(os.path.join('tmp','simulations',(str(self.id_simulation)+'full')), 'w') as stream:
            writer = csv.writer(stream)
            for row in range(self.gui.table_preview.rowCount()):
                rowdata = []
                for column in range(self.gui.table_preview.columnCount()):
                    item = self.gui.table_preview.item(row, column)
                    if item is not None:
                        rowdata.append(
                                unicode(item.text()).encode('utf8'))
                    else:
                        rowdata.append('')
                writer.writerow(rowdata)
        with open(os.path.join('tmp','simulations',(str(self.id_simulation)+'filter')), 'w') as stream:
            writer = csv.writer(stream)
            for row in range(self.gui.table_filtered.rowCount()):
                rowdata = []
                for column in range(self.gui.table_filtered.columnCount()):
                    item = self.gui.table_filtered.item(row, column)
                    if item is not None:
                        rowdata.append(
                                unicode(item.text()).encode('utf8'))
                    else:
                        rowdata.append('')
                writer.writerow(rowdata)
        with open(os.path.join('tmp','simulations',(str(self.id_simulation)+'stats')), 'w') as file_save:
            item = self.gui.tree_hits.topLevelItem(self.id_simulation)
            simulation = item.text(1) + ',' + item.text(2) + ',' +\
                item.text(3) + ',' +item.text(4) + ',' +\
                item.text(5) + ',' +item.text(6) + ',' +item.text(7) + ',' +\
                item.text(8) + ',' +item.text(9)
            line = simulation+self.nl
            file_save.write(line)
            child_num = item.childCount()
            for i in range(0,child_num):
                name = item.child(i)
                name = name.text(0)
                line = name+self.nl
                file_save.write('.........'+line)
    def simulation_stats(self):
        ''' Adds simulation stats to tree preview'''

        item = QtGui.QTreeWidgetItem(self.gui.tree_hits)
        self.simulation_yield()
        item.setText(0,str(round(self.sim_stats['Overall yield'],1))+'%')
        item.setText(1,(self.sim_stats['Path']))
        item.setText(2,(self.sim_stats['League']))
        item.setText(3,(self.sim_stats['Net']))
        item.setText(4,(self.sim_stats['Filter']))
        item.setText(5,(self.sim_stats['Ranges']))
        item.setText(6,(self.sim_stats['Bet_selector']))
        item.setText(7,(self.sim_stats['R_min']))
        item.setText(8,(self.sim_stats['R_max']))
        item.setText(9,str(self.odds_level))

        ### profit/loss - yield
        QtGui.QTreeWidgetItem(item).setText(0, '*Yield*')
        #self.simulation_yield()
        val = ['Overall yield','1,x,2 yield','1x,x2 yield','1 yield','x yield','2 yield','1x yield','x2 yield']
        for i in range(0,len(val)):
            profit = str(round(self.sim_stats[val[i]],2))
            line = val[i]+': '+profit+' %'
            QtGui.QTreeWidgetItem(item).setText(0, line)

        self.simulation_overall_accuracy()
        QtGui.QTreeWidgetItem(item).setText(0, '*Accuracy*')
        val = ['Overall','1,x,2','1x,x2']
        overall = round(self.sim_stats['1']+self.sim_stats['x']+self.sim_stats['2']+\
                    self.sim_stats['1x']+self.sim_stats['x2'],0)
        overall_hit = round(self.sim_stats['1 hit']+self.sim_stats['x hit']+self.sim_stats['2 hit']+\
                    self.sim_stats['1x hit']+self.sim_stats['x2 hit'],0)
        single = round(self.sim_stats['1']+self.sim_stats['x']+self.sim_stats['2'],0)
        single_hit = round(self.sim_stats['1 hit']+self.sim_stats['x hit']+self.sim_stats['2 hit'],0)
        double = round(self.sim_stats['1x']+self.sim_stats['x2'],0)
        double_hit = round(self.sim_stats['1x hit']+self.sim_stats['x2 hit'],0)

        # overall acc
        acc = str(round(self.sim_stats['Overall'],2))
        line_acc = str(overall_hit)+'/'+str(overall)
        line = 'Overall'+': '+line_acc+', '+acc+'%'
        QtGui.QTreeWidgetItem(item).setText(0, line)
        # 1,x,2 acc
        acc = str(round(self.sim_stats['1,x,2'],2))
        line_acc = str(single_hit)+'/'+str(single)
        line = '1,x,2'+': '+line_acc+', '+acc+'%'
        QtGui.QTreeWidgetItem(item).setText(0, line)
        # 1x,x2 acc
        acc = str(round(self.sim_stats['1x,x2'],2))
        line_acc = str(double_hit)+'/'+str(double)
        line = '1x,x2'+': '+line_acc+', '+acc+'%'
        QtGui.QTreeWidgetItem(item).setText(0, line)
        ### bets
        val = ['1','1x','x','x2','2']
        for i in range(0,len(val)):
            a = int(self.sim_stats[val[i]])
            b = int(self.sim_stats[val[i]+' hit'])
            count = str(b)+'/'+str(a)
            try:
                percent = self.sim_stats[val[i]+' hit']/self.sim_stats[val[i]]*100
            except:
                percent = 0
            line = val[i]+' hits: '+count+', '+str(round(percent,2))+'%'
            QtGui.QTreeWidgetItem(item).setText(0, line)

        ### avg_odds
        QtGui.QTreeWidgetItem(item).setText(0, '*Average hit odds*')
        self.simulation_avg_odds()
        val = ['Overall odd_avg','1,x,2 odd_avg','1x,x2 odd_avg','1 odd_avg','x odd_avg','2 odd_avg','1x odd_avg','x2 odd_avg']
        for i in range(0,len(val)):
            odds = str(round(self.sim_stats[val[i]],2))
            line = val[i]+': '+odds
            QtGui.QTreeWidgetItem(item).setText(0, line)
        ### filter series report
        matches_sum = int(self.sim_stats['matches_filter']+self.sim_stats['matches_odds'])
        QtGui.QTreeWidgetItem(item).setText(0, '*Matches removed* %d'%matches_sum)
        QtGui.QTreeWidgetItem(item).setText(0, '**By points/series**')
        self.simulation_avg_odds()
        val = (
        'T-points',
        'T-pointsH/A',
        'T-form',
        'T-formH/A',
        'T1-wins',
        'T1-wins_home',
        'T1-draws',
        'T1-draws_home',
        'T1-loses',
        'T1-loses_home',
        'T1-nowins',
        'T1-nowins_home',
        'T1-nodraws',
        'T1-nodraws_home',
        'T1-noloses',
        'T1-noloses_home',
        'T1-bts',
        'T1-bts_home',
        'T1-over',
        'T1-over_home',
        'T1-under',
        'T1-under_home',
        'T2-wins',
        'T2-wins_away',
        'T2-draws',
        'T2-draws_away',
        'T2-loses',
        'T2-loses_away',
        'T2-nowins',
        'T2-nowin_saway',
        'T2-nodraws',
        'T2-nodraws_away',
        'T2-noloses',
        'T2-noloses_away',
        'T2-bts',
        'T2-bts_away',
        'T2-over',
        'T2-over_away',
        'T2-under',
        'T2-under_away')
        matches = self.sim_stats['matches_filter']
        line = 'Count: '+str(matches)
        QtGui.QTreeWidgetItem(item).setText(0, line)
        for i in range(0,len(val)):
            filter_item = self.sim_stats[val[i]]
            if matches>0:
                report = str(round(filter_item/matches*100.0, 2))
            else:
                report = 0
            if filter_item > 0:
                line = val[i]+': '+str(filter_item)+', '+str(report)+' %'
                QtGui.QTreeWidgetItem(item).setText(0, line)
        ### filter odds report
        QtGui.QTreeWidgetItem(item).setText(0, '**By odds**')
        self.simulation_avg_odds()
        val = (
        'T-odd_1',
        'T-odd_x',
        'T-odd_2',
        'T-odd_1x',
        'T-odd_x2')
        matches = self.sim_stats['matches_odds']
        line = 'Count: '+str(matches)+', 100%'
        QtGui.QTreeWidgetItem(item).setText(0, line)
        for i in range(0,len(val)):
            filter_item = self.sim_stats[val[i]]
            if matches>0:
                report = str(round(filter_item/matches*100.0, 2))
            else:
                report = 0
            if filter_item > 0:
                line = val[i]+': '+str(filter_item)+', '+str(report)+' %'
                QtGui.QTreeWidgetItem(item).setText(0, line)


        
        if self.stop_action == 0:
            self.batch_bets()
            
        else:print 'no bets'
    def simulation_reports_save(self):
        ''' Save simulation to a file'''
        file_name = QtGui.QFileDialog.getSaveFileName(self)
        selected = self.gui.tree_hits.currentIndex().row()
        ext = ('full','filter','stats')
        for i in ext:
            src = os.path.join('tmp','simulations',(str(selected)+i))
            dst = file_name[0]+i
            shutil.copy(src,dst)

    def batch_bets(self):
        ''' Gives bets'''
         # bets filter
        with open(os.path.join('profiles','bets',self.sim_stats['Bet_selector'])\
        ,'r') as bets:
            load = list(bets)
        val = []
        for i in range(0,len(load)):
            item = self.rm_lines(load[i])
            item = float(item)
            val.append(item)
        self.acc_1 = val[0]
        self.acc_x = val[1]
        self.acc_2 = val[2]
        self.acc_1x = val[3]
        self.acc_x2 = val[4]
        self.spin_odds_1_min=val[5]
        self.spin_odds_x_min=val[6]
        self.spin_odds_2_min=val[7]
        self.spin_odds_1x_min=val[8]
        self.spin_odds_x2_min=val[9]
        self.spin_odds_1_max=val[10]
        self.spin_odds_x_max=val[11]
        self.spin_odds_2_max=val[12]
        self.spin_odds_1x_max=val[13]
        self.spin_odds_x2_max=val[14]


        min_date = self.relations_base.execute('''SELECT min(date_num)
                                    From Results WHERE
                                    gHomeEnd == "NULL"''')
        min_date = min_date.fetchone()
        min_date = min_date[0]
        if min_date:
            matches = self.relations_base.execute('''SELECT date_txt,home,away
                        From Results WHERE
                        gHomeEnd == "NULL" and date_num=%f'''%min_date)

            matches = matches.fetchall()
        else:
            matches = []
        print matches[:]
        if len(matches)>0:
            self.item_sim = QtGui.QTreeWidgetItem(self.gui.tree_bets_selected)
            line = str(
            str(round(self.sim_stats['Overall yield'],1))+'% ,'+\
            self.sim_stats['Path']+','+\
            self.sim_stats['League']+','+\
            self.sim_stats['Net']+','+\
            self.sim_stats['Filter']+','+\
            self.sim_stats['Ranges']+','+\
            self.sim_stats['Bet_selector']+','+\
            self.sim_stats['R_min']+','+\
            self.sim_stats['R_max']+','+\
            str(self.odds_level))
            self.item_sim.setText(0,(line))
            for i in matches:
                date,home,away = i
                self.date = date
                ## predict result using odds from file  or predicted odds
                odds = self.relations_base.execute('''SELECT odd_1,odd_x,odd_2,date_txt
                FROM results WHERE (home="%s" AND away="%s" AND gHomeEnd = "NULL")'''%(home,away))
                try: #match in database
                    odds = odds.fetchone()
                    odd_1,odd_x,odd_2,dt = odds
                except: # didn't match
                    odd_1 = 0
                if odd_1>0:
                    self.simulation_prediction(home,away,self.sim_stats['Net'],date = date, mode=2)
                else:
                    self.simulation_prediction(home,away,self.sim_stats['Net'])
                self.filter_status = ''
                self.simulation_filters(home,away)
                self.simulation_match_filters()
                self.simulation_colors()
                if self.filter_status == 'yes':
                    odd_filter =self.odds_filter(self.bet)
                    if odd_filter[0] == 'yes':
                        self.select_bet(home,away,date)

    def select_bet(self,home,away,date):
        ''' Bet filters for selecting bets'''
        try:
            c_acc_1 = self.sim_stats['1 hit']/self.sim_stats['1']*100
        except:
            c_acc_1 = 0
        try:
            c_acc_x = self.sim_stats['x hit']/self.sim_stats['x']*100
        except:
            c_acc_x = 0
        try:
            c_acc_2 = self.sim_stats['2 hit']/self.sim_stats['2']*100
        except:
            c_acc_2 = 0
        try:
            c_acc_1x = self.sim_stats['1x hit']/self.sim_stats['1x']*100
        except:
            c_acc_1x = 0
        try:
            c_acc_x2 = self.sim_stats['x2 hit']/self.sim_stats['x2']*100
        except:
            c_acc_x2 = 0
        ###########
        if self.bet == '1' and c_acc_1>=self.acc_1:
            line = date+' '+home+' - '+away+' :'+self.bet+'  odd: '+\
                                                        str(round(self.odd_1,2))
            #item = QtGui.QTreeWidgetItem(self.gui.tree_bets_selected)
            QtGui.QTreeWidgetItem(self.item_sim).setText(0, (line))
        if self.bet == 'x' and c_acc_x>=self.acc_x:
            line = date+' '+home+' - '+away+' :'+self.bet+'  odd: '+\
                                                        str(round(self.odd_x,2))
            #item = QtGui.QTreeWidgetItem(self.gui.tree_bets_selected)
            QtGui.QTreeWidgetItem(self.item_sim).setText(0, (line))
        if self.bet == '2' and c_acc_2>=self.acc_2:
            line = date+' '+home+' - '+away+' :'+self.bet+'  odd: '+\
                                                        str(round(self.odd_2,2))
            #item = QtGui.QTreeWidgetItem(self.gui.tree_bets_selected)
            QtGui.QTreeWidgetItem(self.item_sim).setText(0, (line))
        if self.bet == '1x' and c_acc_1x>=self.acc_1x:
            line = date+' '+home+' - '+away+' :'+self.bet+'  odd: '+\
                                                        str(round(self.odd_1x,2))
            #item = QtGui.QTreeWidgetItem(self.gui.tree_bets_selected)
            QtGui.QTreeWidgetItem(self.item_sim).setText(0, (line))
        if self.bet == 'x2' and c_acc_x2>=self.acc_x2:
            line = date+' '+home+' - '+away+' :'+self.bet+'  odd: '+\
                                                        str(round(self.odd_x2,2))
            #item = QtGui.QTreeWidgetItem(self.gui.tree_bets_selected)
            QtGui.QTreeWidgetItem(self.item_sim).setText(0, (line))

    def batch_print(self):
        ''' Adds matches to all matches and filtered matches'''
        rows_all = self.gui.table_preview.rowCount()
        rows_filtered = self.gui.table_filtered.rowCount()
        self.filter_status = '' # when 'yes' then adds match to filtered
        self.simulation_match_filters() # filter matches
        self.simulation_colors() # count accuracy give colors (green-win etc.)


        table =['self.date','self.home','self.away','self.result',"str(self.fth)+':'+\
            str(self.fta)",'self.bet','odd_filter[1]','self.prediction','self.color']
        # all matches
        odd_filter =self.odds_filter(self.bet)
        for i in range(0,len(table)):
            if i == 7:
                item = QtGui.QTableWidgetItem()
                item.setData(QtCore.Qt.EditRole,(eval(table[i])))
            else:
                item = QtGui.QTableWidgetItem(str(eval(table[i])))
            #item = QtGui.QTableWidgetItem(str(eval(table[i])))
            self.gui.table_preview.setRowCount(rows_all+1)
            self.gui.table_preview.setItem(rows_all, i, item)
            self.gui.table_preview.item(rows_all, i).\
                setBackground(self.prediction_color)
        # filtered list table
        if self.filter_status == 'no':
            # counts removed matches by filters
            self.sim_stats['matches_filter'] = self.sim_stats['matches_filter'] + 1
        if odd_filter[0] == 'no':
            #counts removed matches by odd
            bets = ['1','x','2','1x','x2']
            if self.bet in bets:
                for i in bets:
                    if self.bet == i:
                        self.sim_stats['T-odd_'+i] = self.sim_stats['T-odd_'+i] +1
                self.sim_stats['matches_odds'] = self.sim_stats['matches_odds'] + 1
        if self.filter_status == 'yes':
            for i in range(0,len(table)):
                ####
                # Odds filter
                ####
                if odd_filter[0] == 'yes':
                    if i == 7:
                        item = QtGui.QTableWidgetItem()
                        item.setData(QtCore.Qt.EditRole,(eval(table[i])))
                    else:
                        item = QtGui.QTableWidgetItem(str(eval(table[i])))
                    self.gui.table_filtered.setRowCount(rows_filtered+1)
                    self.gui.table_filtered.setItem(rows_filtered, i, item)
                    self.gui.table_filtered.item(rows_filtered, i).\
                        setBackground(self.prediction_color)



        self.gui.table_preview.setCurrentCell(rows_all,0)
        self.gui.table_filtered.setCurrentCell(rows_filtered,0)
        QtGui.QApplication.processEvents()
    def odds_filter(self,bet):
        ''' Filters matches by min odds'''
        if bet == '1' and float(self.spin_odd_1_max)>=self.odd_1 >=float(self.spin_odd_1_min):
            status = ('yes',self.odd_1)
        elif bet == 'x' and float(self.spin_odd_x_max)>=self.odd_x >=float(self.spin_odd_x_min):
            status = ('yes',self.odd_x)
        elif bet == '2' and float(self.spin_odd_2_max)>=self.odd_2 >=float(self.spin_odd_2_min):
            status = ('yes',self.odd_2)
        elif bet == '1x' and float(self.spin_odd_1x_max)>=self.odd_1x >=float(self.spin_odd_1x_min):
            status = ('yes',self.odd_1x)
        elif bet == 'x2' and float(self.spin_odd_x2_max)>=self.odd_x2 >=float(self.spin_odd_x2_min):
            status = ('yes',self.odd_x2)
        else:
            status = ('no',0)

        return status



    def simulation_stats_balance(self,bet,mode):
        '''Counts balance win - lost money( for yield calculations)
        mode = 0 lost coupon
        mode = 1 won coupon'''

        if bet == '1':
            profit = 100*self.odd_1*mode
            self.sim_stats['1 balance'] = self.sim_stats['1 balance'] + profit
            self.sim_stats['1 odd_balance'] = self.sim_stats['1 odd_balance'] + self.odd_1
        if bet == 'x':
            profit = 100*self.odd_x*mode
            self.sim_stats['x balance'] = self.sim_stats['x balance'] + profit
            self.sim_stats['x odd_balance'] = self.sim_stats['x odd_balance'] + self.odd_x
        if bet == '2':
            profit = 100*self.odd_2*mode
            self.sim_stats['2 balance'] = self.sim_stats['2 balance'] + profit
            self.sim_stats['2 odd_balance'] = self.sim_stats['2 odd_balance'] + self.odd_2
        if bet == '1x':
            profit = 100*self.odd_1x*mode
            self.sim_stats['1x balance'] = self.sim_stats['1x balance'] + profit
            self.sim_stats['1x odd_balance'] = self.sim_stats['1x odd_balance'] + self.odd_1x
        if bet == 'x2':
            profit = 100*self.odd_x2*mode
            self.sim_stats['x2 balance'] = self.sim_stats['x2 balance'] + profit
            self.sim_stats['x2 odd_balance'] = self.sim_stats['x2 odd_balance'] + self.odd_x2

    def simulation_yield(self):
        ''' Calculates yield'''
        val = ('1','x','2','1x','x2')
        for i in val:
            stakes = self.sim_stats[i]*100
            balance = self.sim_stats[i+' balance']
            if stakes > 0:
                calc_yield = (balance - stakes)/stakes*100
            else:
                calc_yield = 0
            self.sim_stats[i+' yield'] = calc_yield

        # Overall
        stakes = (self.sim_stats['1']+self.sim_stats['x']+self.sim_stats['2']\
                +self.sim_stats['1x']+self.sim_stats['x2'])*100
        balance = self.sim_stats['1 balance']+self.sim_stats['x balance']+\
                self.sim_stats['2 balance']+self.sim_stats['1x balance']+\
                self.sim_stats['x2 balance']
        if stakes > 0:
            calc_yield = (balance - stakes)/stakes*100
        else:
            calc_yield = 0
        self.sim_stats['Overall yield'] = calc_yield
        # 1,x,2
        stakes = (self.sim_stats['1']+self.sim_stats['x']+self.sim_stats['2'])*100
        balance = self.sim_stats['1 balance']+self.sim_stats['x balance']+\
                self.sim_stats['2 balance']
        if stakes > 0:
            calc_yield = (balance - stakes)/stakes*100
        else:
            calc_yield = 0
        self.sim_stats['1,x,2 yield']=calc_yield
        # 1x, x2
        stakes = (self.sim_stats['1x']+self.sim_stats['x2'])*100
        balance = self.sim_stats['1x balance']+self.sim_stats['x2 balance']
        if stakes > 0:
            calc_yield = (balance - stakes)/stakes*100
        else:
            calc_yield = 0
        self.sim_stats['1x,x2 yield'] = calc_yield

    def simulation_avg_odds(self):
        ''' Calculates average hit odds'''
        val = ('1','x','2','1x','x2')
        for i in val:
            num = self.sim_stats[i]
            sum_odds = self.sim_stats[i+' odd_balance']
            if num > 0:
                calc_avg = (sum_odds)/num
            else:
                calc_avg = 0
            self.sim_stats[i+' odd_avg'] = calc_avg
         # Overall
        num = self.sim_stats['1']+self.sim_stats['x']+self.sim_stats['2']\
                +self.sim_stats['1x']+self.sim_stats['x2']
        sum_odds = self.sim_stats['1 odd_balance']+self.sim_stats['x odd_balance']+\
                self.sim_stats['2 odd_balance']+self.sim_stats['1x odd_balance']+\
                self.sim_stats['x2 odd_balance']
        if num > 0:
            calc_avg = (sum_odds)/num
        else:
            calc_avg = 0
        self.sim_stats['Overall odd_avg'] = calc_avg
        # 1x,x2
        num = self.sim_stats['1x']+self.sim_stats['x2']
        sum_odds = self.sim_stats['1x odd_balance']+self.sim_stats['x2 odd_balance']
        if num > 0:
            calc_avg = (sum_odds)/num
        else:
            calc_avg = 0
        self.sim_stats['1x,x2 odd_avg'] = calc_avg
         # 1,x,2
        num = self.sim_stats['1']+self.sim_stats['x']+self.sim_stats['2']
        sum_odds = self.sim_stats['1 odd_balance']+self.sim_stats['x odd_balance']+\
                self.sim_stats['2 odd_balance']
        if num > 0:
            calc_avg = (sum_odds)/num
        else:
            calc_avg = 0
        self.sim_stats['1,x,2 odd_avg'] = calc_avg
    def simulation_overall_accuracy(self):
        ''' Calculates overall accuracy'''
        # Overall
        bets = self.sim_stats['1']+self.sim_stats['x']+self.sim_stats['2']\
                +self.sim_stats['1x']+self.sim_stats['x2']
        hits = self.sim_stats['1 hit']+self.sim_stats['x hit']+\
                self.sim_stats['2 hit']+self.sim_stats['1x hit']+\
                self.sim_stats['x2 hit']
        if bets > 0:
            calc_acc = hits/bets*100
        else:
            calc_acc = 0
        self.sim_stats['Overall'] = calc_acc
        # 1,x,2
        bets = self.sim_stats['1']+self.sim_stats['x']+self.sim_stats['2']
        hits = self.sim_stats['1 hit']+self.sim_stats['x hit']+\
                self.sim_stats['2 hit']
        if bets > 0:
            calc_acc = hits/bets*100
        else:
            calc_acc = 0
        self.sim_stats['1,x,2'] = calc_acc
        # 1x,x2
        bets = self.sim_stats['1x']+self.sim_stats['x2']
        hits = self.sim_stats['1x hit']+self.sim_stats['x2 hit']
        if bets > 0:
            calc_acc = hits/bets*100
        else:
            calc_acc = 0
        self.sim_stats['1x,x2'] = calc_acc

    def simulation_colors(self):
        ''' Gives colours to matches when hit , miss or no bet
        Calculate accuracy stats, yield'''
        green = QtGui.QColor('#11BD00')
        red = QtGui.QColor('#C40202')
        grey = QtGui.QColor('#7C7C7C')
        if self.fth == self.fta:
            result = 'draw'
            self.result = 'x'
        elif self.fth > self.fta:
            result = 'home'
            self.result = '1'
        elif self.fth < self.fta:
            result = 'away'
            self.result = '2'

        if self.min_1<=self.prediction and self.prediction<self.max_1:
            self.bet = '1'
            if self.filter_status ==  'yes':
                 odd_filter =self.odds_filter(self.bet)
                 if odd_filter[0] == 'yes':
                    self.sim_stats['1']+=1
                    self.sim_stats['bets']+=1 # for net frequency calculations
            if result == 'home':
                self.prediction_color = green
                if self.filter_status ==  'yes':
                    odd_filter =self.odds_filter(self.bet)
                    if odd_filter[0] == 'yes': # filter match by odds
                        self.sim_stats['1 hit']+=1
                        self.simulation_stats_balance(self.bet,1)
            else:
                self.prediction_color = red
                if self.filter_status ==  'yes':
                    odd_filter =self.odds_filter(self.bet)
                    if odd_filter[0] == 'yes': # filter match by odds
                        self.simulation_stats_balance(self.bet,0)

        elif self.min_1x<=self.prediction and self.prediction<self.max_1x:
            self.bet = '1x'
            if self.filter_status ==  'yes':
                odd_filter =self.odds_filter(self.bet)
                if odd_filter[0] == 'yes':
                    self.sim_stats['1x']+=1
                    self.sim_stats['bets']+=1
            if result == 'home' or result == 'draw':
                self.prediction_color = green
                if self.filter_status ==  'yes':
                    odd_filter =self.odds_filter(self.bet)
                    if odd_filter[0] == 'yes':
                        self.sim_stats['1x hit']+=1
                        self.simulation_stats_balance(self.bet,1)
            else:
                self.prediction_color = red
                if self.filter_status ==  'yes':
                    odd_filter =self.odds_filter(self.bet)
                    if odd_filter[0] == 'yes': # filter match by odds
                        self.simulation_stats_balance(self.bet,0)

        elif self.min_x<=self.prediction and self.prediction<self.max_x:
            self.bet = 'x'
            if self.filter_status ==  'yes':
                odd_filter =self.odds_filter(self.bet)
                if odd_filter[0] == 'yes':
                    self.sim_stats['x']+=1
                    self.sim_stats['bets']+=1
            if result == 'draw':
                self.prediction_color = green
                if self.filter_status ==  'yes':
                    odd_filter =self.odds_filter(self.bet)
                    if odd_filter[0] == 'yes':
                        self.sim_stats['x hit']+=1
                        self.simulation_stats_balance(self.bet,1)
            else:
                self.prediction_color = red
                if self.filter_status ==  'yes':
                    odd_filter =self.odds_filter(self.bet)
                    if odd_filter[0] == 'yes': # filter match by odds
                        self.simulation_stats_balance(self.bet,0)

        elif self.min_x2<=self.prediction and self.prediction<self.max_x2:
            self.bet = 'x2'
            if self.filter_status ==  'yes':
                odd_filter =self.odds_filter(self.bet)
                if odd_filter[0] == 'yes':
                    self.sim_stats['x2']+=1
                    self.sim_stats['bets']+=1
            if result == 'draw' or result == 'away':
                self.prediction_color = green
                if self.filter_status ==  'yes':
                    odd_filter =self.odds_filter(self.bet)
                    if odd_filter[0] == 'yes':
                        self.sim_stats['x2 hit']+=1
                        self.simulation_stats_balance(self.bet,1)
            else:
                self.prediction_color = red
                if self.filter_status ==  'yes':
                    odd_filter =self.odds_filter(self.bet)
                    if odd_filter[0] == 'yes': # filter match by odds
                        self.simulation_stats_balance(self.bet,0)


        elif self.min_2<=self.prediction and self.prediction<self.max_2:
            self.bet = '2'
            if self.filter_status ==  'yes':
                odd_filter =self.odds_filter(self.bet)
                if odd_filter[0] == 'yes':
                    self.sim_stats['2']+=1
                    self.sim_stats['bets']+=1
            if result == 'away':
                self.prediction_color = green
                if self.filter_status ==  'yes':
                    odd_filter =self.odds_filter(self.bet)
                    if odd_filter[0] == 'yes':
                        self.sim_stats['2 hit']+=1
                        self.simulation_stats_balance(self.bet,1)
            else:
                self.prediction_color = red
                if self.filter_status ==  'yes':
                    odd_filter =self.odds_filter(self.bet)
                    if odd_filter[0] == 'yes': # filter match by odds
                        self.simulation_stats_balance(self.bet,0)

        else:
            self.prediction_color = grey
            self.bet = 'None'
        if self.prediction_color == green:
            self.color ='Hit'
        elif self.prediction_color == red:
            self.color ='Miss'
        elif self.prediction_color == grey:
            self.color ='None'

    def mark_color(self):
        """
        Simulation preview: results:
         Marks selected item to save as profile
        """
        green = QtGui.QColor('#11BD00')
        selected = self.gui.tree_hits.currentItem()
        if selected.background(0) ==  green:
            selected.setBackground(0,selected.background(1))
        else:
            selected.setBackground(0,green)
    def filters_name(self):
        item = self.gui.tree_filters_profile.currentItem()
        file_name = str(item.text(0))
        self.gui.line_filters.setText(file_name)

    def filters_delete(self):
        ''' Deletes match filter'''
        path = os.path.join('profiles','filters','')
        item = self.gui.tree_filters_profile.currentItem()
        file_delete = item.text(0)
        self.delete_file(file_delete,path)
        self.filters_tree()

    def filters_tree(self):
        ''' Tree with saved match filters'''
        self.gui.tree_filters.clear()
        self.gui.tree_filters.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_filters.setSortingEnabled(1)
        dir_exports = os.listdir(os.path.join('profiles','filters'))
        for i in dir_exports:
            item_exp = QtGui.QTreeWidgetItem(self.gui.tree_filters)
            item_exp.setText(0, (i))
        self.gui.tree_filters.setCurrentItem(item_exp)
        self.gui.tree_filters.setSortingEnabled(1)
        self.gui.tree_filters_profile.clear()
        self.gui.tree_filters_profile.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_filters_profile.setSortingEnabled(1)
        self.gui.tree_filters_profile.headerItem().setText(0, ('Match filters'))
        dir_exports = os.listdir(os.path.join('profiles','filters'))
        for i in dir_exports:
            item_exp = QtGui.QTreeWidgetItem(self.gui.tree_filters_profile)
            item_exp.setText(0, (i))
        self.gui.tree_filters_profile.setCurrentItem(item_exp)

    def auto_save(self):
        """Auto saves settings for next session"""
        r_min = self.gui.spin_rounds_min.text()
        r_max = self.gui.spin_rounds_max.text()
        odds_level = self.gui.spin_odds_level.text()
        nets = self.gui.tree_nets.currentItem()
        nets = self.gui.tree_nets.indexOfTopLevelItem(nets)
        filters = self.gui.tree_filters.currentItem()
        filters = self.gui.tree_filters.indexOfTopLevelItem(filters)
        ranges = self.gui.tree_ranges.currentItem()
        ranges = self.gui.tree_ranges.indexOfTopLevelItem(ranges)
        bets = self.gui.tree_bets.currentItem()
        bets = self.gui.tree_bets.indexOfTopLevelItem(bets)


        elements = [r_min, r_max, odds_level, nets, filters, ranges, bets]
        with open(os.path.join('profiles','auto_save','simulator.txt'),'w') as save:
            for i in elements:
                save.write(str(i)+self.nl)
        print 'save'
    def auto_load(self):
        """Restores settings from previous session"""
        with open(os.path.join('profiles','auto_save','simulator.txt'),'r') as load:
            list = load.readlines()
            elements = []
            for i in list:
                i = i.replace('\n','')
                i = i.replace('\r','')
                i = i.replace(',','.')
                elements.append(i)
            self.gui.spin_rounds_min.setValue(float(elements[0]))
            print elements[0]
            self.gui.spin_rounds_max.setValue(float(elements[1]))
            self.gui.spin_odds_level.setValue(float(elements[2]))
            nets = self.gui.tree_nets.topLevelItem(int(elements[3]))
            filters = self.gui.tree_filters.topLevelItem(int(elements[4]))
            ranges = self.gui.tree_ranges.topLevelItem(int(elements[5]))
            bets = self.gui.tree_bets.topLevelItem(int(elements[6]))
                    
            self.gui.tree_nets.setCurrentItem(nets)
            self.gui.tree_filters.setCurrentItem(filters)
            self.gui.tree_ranges.setCurrentItem(ranges)
            self.gui.tree_bets.setCurrentItem(bets)
if __name__ == "__main__":
    APP = QtGui.QApplication(sys.argv)
    MYAPP = SimulatorApp()
    MYAPP.show()
    sys.exit(APP.exec_())
