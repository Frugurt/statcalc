import sys 
import os 
from PyQt5 import QtCore, QtGui, QtWidgets
from queue import Queue
import design
import pprint
import json
import item_simulation
from fbs_runtime.application_context import ApplicationContext
pp = pprint.PrettyPrinter(indent=4)

directory = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(directory, "primary_affixes.json")) as f:
   affix_primary = json.load(f)

with open(os.path.join(directory, "secondary_affixes.json")) as f:
   affix_secondary = json.load(f)
   
with open(os.path.join(directory, "primary_types.json")) as f:
   types_primary = json.load(f)
   
with open(os.path.join(directory, "secondary_types.json")) as f:
   types_secondary = json.load(f)
   
with open(os.path.join(directory, "multi.json")) as f:
   multi_data = json.load(f)

class ExampleApp(QtWidgets.QMainWindow, design.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.data = {"name":"item", 
                     "class":None, 
                     "stats":{
                             "type":None, 
                             "subtype":None,
                             "num_primary":4,
                             "num_secondary":2,
                             "guaranteed_primary":[],
                             "guaranteed_secondary":[],
                             "desired_rolls":[]
                             }
                     }
        self.available_pr = []
        self.availabel_sec = []
        self.des_pr_list = []
        self.des_sec_list = []
        self.thread = QtCore.QThread()
        
        self.setupUi(self)
                     
        self.primary_special = [self.special_check_1, self.special_check_2, self.special_check_3, self.special_check_4, self.special_check_5, self.special_check_6, self.special_check_7]
        self.primary_affix = [self.affix_box_1, self.affix_box_2, self.affix_box_3, self.affix_box_4, self.affix_box_5, self.affix_box_6, self.affix_box_7]
        self.primary_min = [self.min_line_1, self.min_line_2, self.min_line_3, self.min_line_4, self.min_line_5, self.min_line_6, self.min_line_7]
        self.primary_max = [self.max_line_1, self.max_line_2, self.max_line_3, self.max_line_4, self.max_line_5, self.max_line_6, self.max_line_7]
        self.primary_multi = [self.multi_line_1, self.multi_line_2, self.multi_line_3, self.multi_line_4, self.multi_line_5, self.multi_line_6, self.multi_line_7]
        self.primary_reroll = [self.reroll_check_1, self.reroll_check_2, self.reroll_check_3, self.reroll_check_4, self.reroll_check_5, self.reroll_check_6, self.reroll_check_7]
        
        self.secondary_special = [self.special_check_8, self.special_check_9, self.special_check_10, self.special_check_11]
        self.secondary_affix = [self.affix_box_8, self.affix_box_9, self.affix_box_10, self.affix_box_11]
        self.secondary_min = [self.min_line_8, self.min_line_9, self.min_line_10, self.min_line_11]
        self.secondary_max = [self.max_line_8, self.max_line_9, self.max_line_10, self.max_line_11]
        self.secondary_multi = [self.multi_line_8, self.multi_line_9, self.multi_line_10, self.multi_line_11]
        self.secondary_reroll = [self.reroll_check_8, self.reroll_check_9, self.reroll_check_10, self.reroll_check_11]
        
        self.des_pr = [self.desired_affix_1, self.desired_affix_2, self.desired_affix_3, self.desired_affix_4, self.desired_affix_5, self.desired_affix_6, self.desired_affix_7]
        self.des_pr_min = [self.desired_min_1, self.desired_min_2, self.desired_min_3, self.desired_min_4, self.desired_min_5, self.desired_min_6, self.desired_min_7]
        self.des_pr_mult = [self.desired_multi_1, self.desired_multi_2, self.desired_multi_3, self.desired_multi_4, self.desired_multi_5, self.desired_multi_6, self.desired_multi_7]
        
        self.des_sec = [self.desired_affix_8, self.desired_affix_9, self.desired_affix_10, self.desired_affix_11]
        self.des_sec_min = [self.desired_min_8, self.desired_min_9, self.desired_min_10, self.desired_min_11]
        self.des_sec_mult = [self.desired_multi_8, self.desired_multi_9, self.desired_multi_10, self.desired_multi_11]
                     
        self.type_box.addItems(["select item type", "1h", "2h", "offhand", "shield", "boots", "pants", "ring", "belt", "glove", "bracer", "chest", "shoulder", "amulet", "helmet"])
        self.type_box.currentIndexChanged.connect(self.type_changed)
        self.subtype_box.currentIndexChanged.connect(self.subtype_changed)
        self.class_box.currentIndexChanged.connect(self.class_changed)
        self.class_box.addItems(["DH", "monk", "wiz", "WD", "necro", "barb", "sader"])
        self.primarySpinBox.valueChanged.connect(self.n_changed)
        self.secondarySpinBox.valueChanged.connect(self.m_changed)
        self.ancient_check.stateChanged.connect(self.ancient_click)
    
        
        for i in range(7):
            self.primary_special[i].stateChanged.connect(lambda x, i=i: self.pr_special_clicked(i))
        for i in range(4):
            self.secondary_special[i].stateChanged.connect(lambda x, i=i: self.sec_special_clicked(i))
            
        for i in range(7):
            self.primary_affix[i].currentIndexChanged.connect(lambda x, i=i: self.pr_affix_chosen(i))
        for i in range(4):
            self.secondary_affix[i].currentIndexChanged.connect(lambda x, i=i: self.sec_affix_chosen(i))
            
        for i in range(7):
            self.primary_affix[i].editTextChanged.connect(self.pr_des_update)
        for i in range(4):
            self.secondary_affix[i].editTextChanged.connect(self.sec_des_update)
            
        for i in range(7):
            self.primary_min[i].editingFinished.connect(self.save_guaranteed)
            self.primary_max[i].editingFinished.connect(self.save_guaranteed)
            self.primary_multi[i].editingFinished.connect(self.save_guaranteed)
            self.primary_reroll[i].stateChanged.connect(self.save_guaranteed)
        
        for i in range(4):
            self.secondary_min[i].editingFinished.connect(self.save_guaranteed)
            self.secondary_max[i].editingFinished.connect(self.save_guaranteed)
            self.secondary_multi[i].editingFinished.connect(self.save_guaranteed)
            self.secondary_reroll[i].stateChanged.connect(self.save_guaranteed)
            
        self.saveButton.clicked.connect(self.save_desired)
        
        self.startButton.clicked.connect(self.start_simulation)
        self.clearButton.clicked.connect(self.clear_desired)
        
    def type_changed(self):
        self.data["stats"]["type"] = self.type_box.currentText()
        item_type = self.type_box.currentText()
        if item_type != "select item type":
            self.available_pr = types_primary[item_type]["affixes"]
            self.available_sec = types_secondary[item_type]["affixes"]
            self.pr_des_update()
            self.sec_des_update()
        for i in range(self.data["stats"]["num_primary"]):
            self.primary_affix[i].clear()
            self.primary_affix[i].addItems(["???"] + self.available_pr)
            self.primary_min[i].setText("")
            self.primary_max[i].setText("")
            self.primary_multi[i].setText("")
        for i in range(self.data["stats"]["num_secondary"]):
            self.secondary_affix[i].clear()
            self.secondary_affix[i].addItems(["???"] + self.available_sec)
            self.secondary_min[i].setText("")
            self.secondary_max[i].setText("")
            self.secondary_multi[i].setText("")
        if item_type in ["1h", "2h", "offhand", "shield", "belt", "chest", "helmet"]:
            self.subtype_box.setEnabled(True)
            self.subtype_box.clear()
            if item_type == "1h":
                self.subtype_box.addItems(["dagger", "sword", "axe", "spear", "mace", "flail", "scythe", "ceremonial_knife", "mighty_weapom", "wand", "fist", "hand_xbow"])
            if item_type == "2h":
                self.subtype_box.addItems(["big_flail", "big_mighty_weapon", "big_sword", "big_axe", "big_mace", "polearm", "staff", "big_scythe", "daibo", "bow", "xbow"])
            if item_type == "shield":
                self.subtype_box.addItems(["shield", "crusader_shield"])
            if item_type == "offhand":
                self.subtype_box.addItems(["source", "mojo", "phylactery", "quiver"])
            if item_type == "belt":
                self.subtype_box.addItems(["belt", "mighty_belt"])
            if item_type == "chest":
                self.subtype_box.addItems(["chest", "cloak"])
            if item_type == "helmet":
                self.subtype_box.addItems(["helmet", "wizard_hat", "voodoo_mask", "spirit_stone"])
        else:
            self.subtype_box.clear()
            self.subtype_box.setEnabled(False)
        
    def subtype_changed(self):
        self.data["stats"]["subtype"] = self.subtype_box.currentText()
        subtype = self.subtype_box.currentText()
        if subtype in types_primary[self.data["stats"]["type"]]:
            self.available_pr = types_primary[self.data["stats"]["type"]][subtype] + types_primary[self.data["stats"]["type"]]["affixes"]
            self.pr_des_update()
        if subtype in types_secondary[self.data["stats"]["type"]]:
            self.available_sec = types_secondary[self.data["stats"]["type"]][subtype] + types_secondary[self.data["stats"]["type"]]["affixes"]
            self.sec_des_update()
        
        for i in range(self.data["stats"]["num_primary"]):
            self.primary_affix[i].clear()
            self.primary_affix[i].addItems(["???"] + self.available_pr)
            self.primary_min[i].setText("")
            self.primary_max[i].setText("")
            self.primary_multi[i].setText("")
        for i in range(self.data["stats"]["num_secondary"]):
            self.secondary_affix[i].clear()
            self.secondary_affix[i].addItems(["???"] + self.available_sec)
            self.secondary_min[i].setText("")
            self.secondary_max[i].setText("")
            self.secondary_multi[i].setText("")
        
        if subtype in ["quiver", "cloak", "hand_xbow"]:
            self.class_box.clear()
            self.class_box.addItem("DH")
        elif subtype in ["spirit_stone", "fist", "daibo"]:
            self.class_box.clear()
            self.class_box.addItem("monk")
        elif subtype in ["source", "wand", "wizard_hat"]:
            self.class_box.clear()
            self.class_box.addItem("wiz")
        elif subtype in ["ceremonial_knife", "mojo", "voodoo_mask"]:
            self.class_box.clear()
            self.class_box.addItem("WD")
        elif subtype in ["phylactery", "scythe", "big_scythe"]:
            self.class_box.clear()
            self.class_box.addItem("necro")
        elif subtype in ["mighty_weapon", "big_mighty_weapon", "mighty_belt"]:
            self.class_box.clear()
            self.class_box.addItem("barb")
        elif subtype in ["flail", "big_flail", "crusader_shield"]:
            self.class_box.clear()
            self.class_box.addItem("sader")
        else:
            self.class_box.clear()
            self.class_box.addItems(["DH", "monk", "wiz", "WD", "necro", "barb", "sader"])
        
    def class_changed(self):
        self.data["class"] = self.class_box.currentText()
        for i in range(self.primarySpinBox.value()):
            self.update_pr_boxes(i)
        
    def toggle_primary(self, i, state):
        self.primary_special[i].setEnabled(state)
        self.primary_affix[i].clear()
        if state:
            self.primary_affix[i].addItems(["???"] + self.available_pr)
        self.primary_affix[i].setEnabled(state)
        self.primary_min[i].setEnabled(state)
        self.primary_max[i].setEnabled(state)
        self.primary_multi[i].setEnabled(state)
        self.primary_reroll[i].setEnabled(state)
        self.des_pr[i].setEnabled(state)
        self.des_pr_min[i].setEnabled(state)
        self.des_pr_mult[i].setEnabled(state)
        
    def toggle_secondary(self, i, state):
        self.secondary_special[i].setEnabled(state)
        self.secondary_affix[i].clear()
        if state:
            self.secondary_affix[i].addItems(["???"] + self.available_sec)
        self.secondary_affix[i].setEnabled(state)
        self.secondary_min[i].setEnabled(state)
        self.secondary_max[i].setEnabled(state)
        self.secondary_multi[i].setEnabled(state)
        self.secondary_reroll[i].setEnabled(state)
        self.des_sec[i].setEnabled(state)
        self.des_sec_min[i].setEnabled(state)
        self.des_sec_mult[i].setEnabled(state)
        
        
    def n_changed(self):
        n = self.primarySpinBox.value()
        self.data["stats"]["num_primary"] = n
        for i in range(n):
            self.toggle_primary(i, True)
        for i in range(n, 7):
            self.toggle_primary(i, False)
        
    def m_changed(self):
        m = self.secondarySpinBox.value()
        self.data["stats"]["num_secondary"] = m
        for i in range(m):
            self.toggle_secondary(i, True)
        for i in range(m, 4):
            self.toggle_secondary(i, False)
    
    def pr_special_clicked(self, i):
        state = self.primary_special[i].isChecked()
        self.primary_affix[i].clear()
        if not state:
            self.primary_affix[i].addItems(["???"] + self.available_pr)
        self.primary_affix[i].setEditable(state)
        self.primary_min[i].setReadOnly(not state)
        self.primary_max[i].setReadOnly(not state)
        self.primary_multi[i].setReadOnly(not state)
        if state:
            self.primary_min[i].setText("1")
            self.primary_max[i].setText("1")
            self.primary_multi[i].setText("1")
        else:
            self.primary_min[i].setText("")
            self.primary_max[i].setText("")
            self.primary_multi[i].setText("")
        
    def sec_special_clicked(self, i):
        state = self.secondary_special[i].isChecked()
        self.secondary_affix[i].clear()
        if not state:
            self.secondary_affix[i].addItems(["???"] + self.available_sec)
        self.secondary_affix[i].setEditable(state)
        self.secondary_min[i].setReadOnly(not state)
        self.secondary_max[i].setReadOnly(not state)
        self.secondary_multi[i].setReadOnly(not state)
        if state:
            self.secondary_min[i].setText("1")
            self.secondary_max[i].setText("1")
            self.secondary_multi[i].setText("1")
        else:
            self.secondary_min[i].setText("")
            self.secondary_max[i].setText("")
            self.secondary_multi[i].setText("")
            
    def update_multi_box(self, box, affix):
        if affix in multi_data["by_class"]:
            for thing in multi_data["by_class"][affix]:
                if self.type_box.currentText() in thing["type"]:
                    multi = thing["stats"][self.class_box.currentText()]
        elif affix in multi_data["by_slot"]:
            multi = multi_data["by_slot"][self.type_box.currentText()]
        else:
            multi = affix_primary[affix]["multi"]
        box.setText(str(multi))
    
    def update_pr_boxes(self, i):
        affix = self.primary_affix[i].currentText()
        if affix == "???" or affix == "":
            return
        if not self.primary_special[i].isChecked():
            min_str = "min"
            max_str = "max"
            ranges = {}
            for th in affix_primary[affix]["ranges"]:
                if self.type_box.currentText() in th["type"] or self.subtype_box.currentText() in th["type"]:
                    ranges = th
                    break
            if self.ancient_check.isChecked():
                min_str = "ancient_min"
                max_str = "ancient_max"
            if affix != "avgdmg":
                self.primary_min[i].setText(str(ranges[min_str]))
                self.primary_max[i].setText(str(ranges[max_str]))
            else:
                l_ranges = {}
                u_ranges = {}
                for th in affix_primary["min_damage"]["ranges"]:
                    if self.type_box.currentText() in th["type"] or self.subtype_box.currentText() in th["type"]:
                        l_ranges = th
                        break
                for th in affix_primary["max_damage"]["ranges"]:
                    if self.type_box.currentText() in th["type"] or self.subtype_box.currentText() in th["type"]:
                        u_ranges = th
                        break
                self.primary_min[i].setText(str(l_ranges[min_str] + u_ranges[min_str]))
                self.primary_max[i].setText(str(l_ranges[max_str] + u_ranges[max_str]))
            self.update_multi_box(self.primary_multi[i], affix)
            
    def pr_affix_chosen(self, i):
        self.update_pr_boxes(i)
        self.pr_des_update()
        
    def update_sec_boxes(self, i):
        affix = self.secondary_affix[i].currentText()
        if affix == "???" or affix == "":
            return
        if not self.secondary_special[i].isChecked():
            min_str = "min"
            max_str = "max"
            ranges = {}
            for th in affix_secondary[affix]["ranges"]:
                if self.type_box.currentText() in th["type"] or self.subtype_box.currentText() in th["type"]:
                    ranges = th
                    break
            if self.ancient_check.isChecked():
                min_str = "ancient_min"
                max_str = "ancient_max"
            self.secondary_min[i].setText(str(ranges[min_str]))
            self.secondary_max[i].setText(str(ranges[max_str]))
            self.update_multi_box(self.secondary_multi[i], affix)
        
    def sec_affix_chosen(self, i):
        self.update_sec_boxes(i)
        self.sec_des_update()
            
    def save_guaranteed(self):
        self.data["stats"]["guaranteed_primary"] = []
        for i in range(self.data["stats"]["num_primary"]):
            if self.primary_affix[i].currentText() == "???" or self.primary_affix[i].currentText() == "":
                continue
            if self.primary_special[i].isChecked():
                try:
                    stat_min = int(self.primary_min[i].text())
                except ValueError:
                    stat_min = 1
                try:
                    stat_max = int(self.primary_max[i].text())
                except ValueError:
                    stat_max = stat_min
                try:
                    stat_mult = int(self.primary_multi[i].text())
                except ValueError:
                    stat_mult = 1
                self.data["stats"]["guaranteed_primary"] += [{"affix":self.primary_affix[i].currentText(),
                                                             "special":True, 
                                                             "min":stat_min,
                                                             "max":stat_max,
                                                             "multistat":stat_mult, 
                                                             "reroll":self.primary_reroll[i].isChecked()}]
            else:
                self.data["stats"]["guaranteed_primary"] += [{"affix":self.primary_affix[i].currentText()}]
        
        self.data["stats"]["guaranteed_secondary"] = []
        for i in range(self.data["stats"]["num_secondary"]):
            if self.secondary_affix[i].currentText() == "???" or self.secondary_affix[i].currentText() == "":
                continue
            if self.secondary_special[i].isChecked():
                try:
                    stat_min = int(self.secondary_min[i].text())
                except ValueError:
                    stat_min = 1
                try:
                    stat_max = int(self.secondary_max[i].text())
                except ValueError:
                    stat_max = stat_min
                try:
                    stat_mult = int(self.secondary_multi[i].text())
                except ValueError:
                    stat_mult = 1
                self.data["stats"]["guaranteed_secondary"] += [{"affix":self.secondary_affix[i].currentText(),
                                                             "special":True, 
                                                             "min":stat_min,
                                                             "max":stat_max,
                                                             "multistat":stat_mult, 
                                                             "reroll":self.secondary_reroll[i].isChecked()}]
            else:
                self.data["stats"]["guaranteed_secondary"] += [{"affix":self.secondary_affix[i].currentText()}]
                
    def pr_des_update(self):
        self.des_pr_list = [] + self.available_pr
        for i in range(self.data["stats"]["num_primary"]):
            affix = self.primary_affix[i].currentText()
            if self.primary_special[i].isChecked() and affix != "":
                self.des_pr_list += [affix]
        for i in range(self.data["stats"]["num_primary"]):
            self.des_pr[i].clear()
            self.des_pr[i].addItems(["any"] + self.des_pr_list)
        self.save_guaranteed()
                
    def sec_des_update(self):
        self.des_sec_list = [] + self.available_sec
        for i in range(self.data["stats"]["num_secondary"]):
            affix = self.secondary_affix[i].currentText()
            if self.secondary_special[i].isChecked() and affix != "":
                self.des_sec_list += [affix]
        for i in range(self.data["stats"]["num_secondary"]):
            self.des_sec[i].clear()
            self.des_sec[i].addItems(["any"] + self.des_sec_list)
        self.save_guaranteed()
            
    
    def ancient_click(self):
        for i in range(self.primarySpinBox.value()):
            self.update_pr_boxes(i)
        for i in range(self.secondarySpinBox.value()):
            self.update_sec_boxes(i)
    
    def save_desired(self):
        config = {}
        for i in range(self.primarySpinBox.value()):
            if self.des_pr[i].currentText() != "any":
                try:
                    min_value = float(self.des_pr_min[i].text())
                except ValueError:
                    min_value = 0
                try:
                    mult_value = float(self.des_pr_mult[i].text())
                except ValueError:
                    mult_value = 0
                config[self.des_pr[i].currentText()] = {"min":min_value, "multistat_order":mult_value}
                    
        for i in range(self.secondarySpinBox.value()):
            if self.des_sec[i].currentText() != "any":
                try:
                    min_value = float(self.des_sec_min[i].text())
                except ValueError:
                    min_value = 0
                try:
                    mult_value = float(self.des_sec_mult[i].text())
                except ValueError:
                    mult_value = 0
                config[self.des_sec[i].currentText()] = {"min":min_value, "multistat_order":mult_value}
        self.data["stats"]["desired_rolls"] += [{"ancient":self.ancient_check.isChecked(), "configuration":config}]
        config_text = ""
        if self.ancient_check.isChecked():
            config_text += "Ancient, "
        for key in config:
            config_text += "({}:{:.1f}+)  ".format(key, config[key]["min"])
        self.saved_text.append(config_text)
        
    def clear_desired(self):
        self.data["stats"]["desired_rolls"] = []
        self.saved_text.clear()
    
    @QtCore.pyqtSlot(str)
    def append_text(self,text):
        if text[0] == "\r":
            self.output_text.setFocus()
            self.output_text.moveCursor(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
            self.output_text.moveCursor(QtGui.QTextCursor.StartOfLine, QtGui.QTextCursor.MoveAnchor)
            self.output_text.moveCursor(QtGui.QTextCursor.End, QtGui.QTextCursor.KeepAnchor)
            self.output_text.textCursor().removeSelectedText()
            self.output_text.textCursor().deletePreviousChar()
        self.output_text.moveCursor(QtGui.QTextCursor.End)
        self.output_text.insertPlainText( text )
    
    @QtCore.pyqtSlot()
    def start_simulation(self):
        self.output_text.clear()
        try:
            num_tries = int(self.triesLine.text())
        except ValueError:
            num_tries = 100000
        with open("temp.json", "w") as f:
            json.dump(self.data, f, indent=4)
        self.thread.quit()
        self.thread.wait()
        self.thread = QtCore.QThread()
        self.simulation = MCSimulation(num_tries)
        self.simulation.moveToThread(self.thread)
        self.thread.started.connect(self.simulation.run)
        self.thread.start()
        
        #item_tester = item_simulation.ItemTest("temp.json")
        #item_tester.test(num_tries)
        
    def debug(self):
        pp.pprint(self.data)
        
        #print(self.des_pr_list)
        #print(self.des_sec_list)
        

# The new Stream Object which replaces the default stream associated with sys.stdout
# This object just puts data in a queue!
class WriteStream(object):
    def __init__(self,queue):
        self.queue = queue

    def write(self, text):
        self.queue.put(text)
    
    def flush(self):
        pass

# A QObject (to be run in a QThread) which sits waiting for data to come through a Queue.Queue().
# It blocks until data is available, and one it has got something from the queue, it sends
# it to the "MainThread" by emitting a Qt Signal 
class MyReceiver(QtCore.QObject):
    mysignal = QtCore.pyqtSignal(str) 

    def __init__(self,queue,*args,**kwargs):
        QtCore.QObject.__init__(self,*args,**kwargs)
        self.queue = queue

    @QtCore.pyqtSlot()
    def run(self):
        while True:
            text = self.queue.get()
            self.mysignal.emit(text)

# An example QObject (to be run in a QThread) which outputs information with print
class MCSimulation(QtCore.QObject):
    def __init__(self, n):
        super(MCSimulation, self).__init__()
        self.num_tries = n
        
    @QtCore.pyqtSlot()
    def run(self):
        item_tester = item_simulation.ItemTest("temp.json")
        item_tester.test(self.num_tries)     
        
#class OutLog:
#    def __init__(self, edit, out=None, color=None):
#        """(edit, out=None, color=None) -> can write stdout, stderr to a
#        QTextEdit.
#        edit = QTextEdit
#        out = alternate stream ( can be the original sys.stdout )
#        color = alternate color (i.e. color stderr a different color)
#        """
#        self.edit = edit
#        self.out = None
#        self.color = color
#
#    def write(self, m):
#        if self.color:
#            tc = self.edit.textColor()
#            self.edit.setTextColor(self.color)
#        
#        if m[0] == "\r":
#            self.edit.setFocus()
#            self.edit.moveCursor(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
#            self.edit.moveCursor(QtGui.QTextCursor.StartOfLine, QtGui.QTextCursor.MoveAnchor)
#            self.edit.moveCursor(QtGui.QTextCursor.End, QtGui.QTextCursor.KeepAnchor)
#            self.edit.textCursor().removeSelectedText()
#            self.edit.textCursor().deletePreviousChar()
#        self.edit.moveCursor(QtGui.QTextCursor.End)
#        self.edit.insertPlainText( m )
#
#        if self.color:
#            self.edit.setTextColor(tc)
#
#        if self.out:
#            self.out.write(m)
#    def flush(self):
#        pass

class AppContext(ApplicationContext):           # 1. Subclass ApplicationContext
    def run(self):                              # 2. Implement run()
        queue = Queue()
        sys.stdout = WriteStream(queue)

        #app = QtWidgets.QApplication(sys.argv) 
        window = ExampleApp() 
        window.show()

        thread = QtCore.QThread()
        my_receiver = MyReceiver(queue)
        my_receiver.mysignal.connect(window.append_text)
        my_receiver.moveToThread(thread)
        thread.started.connect(my_receiver.run)
        thread.start()
        return self.app.exec_()                 # 3. End run() with this line



def main():
    appctxt = AppContext()                      # 4. Instantiate the subclass
    exit_code = appctxt.run()                   # 5. Invoke run()
    sys.exit(exit_code) 

if __name__ == '__main__':  
    main()  