import sys,os
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog,QColorDialog, QMessageBox
from PyQt6.QtCore import Qt, QCoreApplication
from ui_file import Ui_MainWindow




class application(QMainWindow):
    def __init__(self)->None:
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        self.folder_name = ""
        self.translate = ""

        self.ui.target_location_pushButton.clicked.connect(lambda :self.select_folder(1))
        self.ui.save_location_pushButton.clicked.connect(lambda :self.select_folder(2))
        self.ui.start_pushButton.clicked.connect(self.start_convert)
        self.ui.pick_color_pushButton.clicked.connect(self.pick_color)
        self.ui.give_name_lineEdit.textChanged.connect(lambda x: setattr(self, 'folder_name', self.ui.give_name_lineEdit.text()))

        self.ui.comboBox.currentIndexChanged.connect(lambda x: setattr(self, 'translate', self.ui.comboBox.currentText()))
        self.ui.English_pushButton.clicked.connect(self.translate_app)

        self.target_loc = ""
        self.save_loc = ""
        self.picked_color =""

        self.lang = ""
        self.add_langs()
        

    def add_langs(self):
        with open("translate.json","r",encoding="utf-8") as file:   
            data = json.load(file)

        self.lang = data[data['langs'][0]]
        self.ui.comboBox.addItems(data['langs'])
        self.retranslateUi()
    

    def translate_app(self):
        with open("translate.json","r",encoding="utf-8") as file:   
            data = json.load(file)

            self.lang = data[data['langs'][self.ui.comboBox.currentIndex()]]
        
        self.retranslateUi()


    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.ui.MainWindow.setWindowTitle(_translate("MainWindow", "SVG file color changer"))
        self.ui.target_location_pushButton.setText(_translate("MainWindow", self.lang['target_location_pushButton']))
        self.ui.save_location_pushButton.setText(_translate("MainWindow", self.lang['save_location_pushButton']))
        self.ui.pick_color_pushButton.setText(_translate("MainWindow", self.lang['pick_color_pushButton']))
        self.ui.give_name_label.setText(_translate("MainWindow", self.lang['give_name_label']))
        self.ui.start_pushButton.setText(_translate("MainWindow", self.lang['start_pushButton']))
        self.ui.English_pushButton.setText(_translate("MainWindow", self.lang['lang']))


    def select_folder(self,sender):
        folder = QFileDialog.getExistingDirectory(self,self.lang['select_folder_ask'])
        if folder:
            if sender == 1:
                if not self.check_svg(folder):
                    QMessageBox.warning(None,self.lang['error_title'],self.lang['error_msg_no_svg'])
                    return None 
                if self.save_loc == folder:
                    QMessageBox.warning(None,self.lang['error_title'],self.lang['error_msg_save_and_target_loc_same'])
                    return None
                self.ui.target_location_lineEdit.setText(folder)
                self.target_loc = folder
                
            else:
                if self.target_loc == folder:
                    QMessageBox.warning(None,self.lang['error_title'],self.lang['error_msg_save_and_target_loc_same'])
                    return None
                self.ui.save_location_lineEdit.setText(folder)
                self.save_loc = folder
    
    def check_svg(self,folder_path)->bool:
        for file in os.listdir(folder_path):
            if file.endswith('.svg'):
                with open(os.path.join(folder_path,file),mode="r") as svg:
                    content = svg.read()
                    start_index = content.find('stroke="#') + len('stroke="#')
                    end_index = content.find('"', start_index)
                    current_color  = content[start_index-1:end_index]
                    self.ui.color_current.setStyleSheet(f"background-color: {current_color}")
                    print(current_color)
                return True
        return False


    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.ui.color_name.setText(color.name())
            self.picked_color =color.name()
            self.ui.color_show.setStyleSheet(f"background-color: {color.name()}")

    def start_convert(self):
        if not self.picked_color:
            QMessageBox.warning(None,self.lang['error_title'],self.lang['error_msg_pick_color'])
        if not self.target_loc:
            QMessageBox.warning(None,self.lang['error_title'],self.lang['error_msg_pick_target'])
        if not self.save_loc:
            QMessageBox.warning(None,self.lang['error_title'],self.lang['error_msg_pick_save'])
        if not self.folder_name:
            QMessageBox.warning(None,self.lang['error_title'],self.lang['error_msg_give_name'])

        try:
            os.mkdir(os.path.join(self.save_loc,self.folder_name))
        except PermissionError:
            QMessageBox.warning(None,self.lang['error_title'],self.lang['error_msg_permission'])
        except Exception as E:
            QMessageBox.warning(None,self.lang['error_title'],self.lang['error_msg_exist'])

        for file in filter(lambda x:x.endswith('.svg')   ,os.listdir(self.target_loc)):
            with open(os.path.join(self.target_loc,file),mode="r") as svg:
                    content = svg.read()
                    start_index = content.find('stroke="#') + len('stroke="#')
                    end_index = content.find('"', start_index)
                    modified_svg_code = content[:start_index-1] + self.picked_color + content[end_index:]
            with open(os.path.join(self.save_loc,self.folder_name,file),mode="w") as svg:
                svg.write(modified_svg_code)
        
        QMessageBox.information(None,"Process Done","svg color chnaged")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = application()
    sys.exit(app.exec())


