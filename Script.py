import sys
import json

import first_layers_look
import linear_advance_add
import fan_layers_control
import extrusion_width_hight
from linear_advance_add import add_LA
import first_layers_look
from arc_helper import arc_weider, arc_straightener
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QRadioButton,
    QButtonGroup,
    QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QFormLayout,
)


class MainDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(600, 520)
        self.setWindowTitle(f"Post Processing: {sys.argv[1]}" )
        self.vertical_layout_main_window_1 = QVBoxLayout(self)
        self.horizontal_layout_main_window_2 = QVBoxLayout(self)

        self.LA_layout=LA_widgets(self)

        self.LA_layout.setFixedSize(500,100)
        self.vertical_layout_main_window_1.addWidget(self.LA_layout)
        self.line_1 = Line(self)
        self.vertical_layout_main_window_1.addWidget(self.line_1)

        self.arc_layout = Arc_widgets(self)
        # self.Arc_layout.setFixedSize(450, 100)
        self.vertical_layout_main_window_1.addWidget(self.arc_layout)
        self.line_2 = Line(self)
        self.vertical_layout_main_window_1.addWidget(self.line_2)

        self.look_layout = Look_widgets(self)
        # self.Look_layout.setFixedSize(450, 100)
        self.vertical_layout_main_window_1.addWidget(self.look_layout)
        self.line_3 = Line(self)
        self.vertical_layout_main_window_1.addWidget(self.line_3)

        self.fan_layout = Fan_widgets(self)
        self.vertical_layout_main_window_1.addWidget(self.fan_layout)


        self.translate_button = QtWidgets.QPushButton("Укр", self)
        self.translate_button.setGeometry(QtCore.QRect(540, 10, 50, 50))
        self.translate_button.setObjectName("translate_button")
        self.translate_button.clicked.connect(self.change_language)

        self.pushButton_run = QtWidgets.QPushButton(self)

        self.pushButton_run.setObjectName("pushButton_add_vent")
        self.pushButton_run.setGeometry(QtCore.QRect(500, 420, 80, 80))
        self.pushButton_run.setFont(QFont("Arial", 14, 75, True))
        self.pushButton_run.setText("Run")
        self.pushButton_run.setStyleSheet("color: green")
        self.pushButton_run.clicked.connect(self.run)
        # self.horizontal_layout_main_window_2.addWidget(self.fan_layout)
        # self.horizontal_layout_main_window_2.addWidget(self.pushButton_run)
        # self.vertical_layout_main_window_1.addLayout(self.horizontal_layout_main_window_2)



        self.retranslate()
        self.show()

    def retranslate(self):
        """Retranslate the widgets"""
        _translate = QtCore.QCoreApplication.translate
        if self.translate_button.text() == "Укр":
            # self.resize(600, 520)
            # self.pushButton_run.setGeometry(QtCore.QRect(500, 420, 80, 80))
            self.setWindowTitle(_translate("MainDialog", f"Post Processing: {sys.argv[1]}"))
            # LA block
            self.LA_layout.label_checkBox_LA.setText(_translate("MainDialog", "Linear Advance"))
            self.LA_layout.label_line_width.setText(_translate("MainDialog", "Line width"))
            self.LA_layout.label_layer_height.setText(_translate("MainDialog", "Layer height"))
            self.LA_layout.label_material_diameter.setText(
                _translate("MainDialog", "Material diameter")
            )
            self.LA_layout.label_material_linear_advance_factor.setText(
                _translate("MainDialog", "Material linear advance factor :")
            )
            self.LA_layout.doubleSpinBox_line_width.setSuffix(_translate("MainDialog", "mm"))
            self.LA_layout.doubleSpinBox_layer_height.setSuffix(_translate("MainDialog", "mm"))
            self.LA_layout.doubleSpinBox_material_diameter.setSuffix(
                _translate("MainDialog", "mm")
            )
            # #  Arc block.
            self.arc_layout.label_checkBox_Arc.setText(
                _translate(
                    "MainWindow",
                    " Making circles from segments. "
                    "Converting g1 to g2/g3 commands.",
                )
            )
            # Look block.
            self.look_layout.label_checkBox_look.setText(
                _translate(
                    "MainWindow",
                    "Pause in printing to looking at the model and move to X",
                )
            )

            self.look_layout.label_Y.setText(_translate("MainWindow", "and Y"))
            self.look_layout.label_brim.setText(_translate("MainWindow", "Pause after brim"))
            self.look_layout.pushButton_rem_new_look.setText(_translate("MainWindow", "Delete"))
            self.look_layout.label_look.setText(_translate("MainWindow", "Look at"))
            self.look_layout.spinBox_layer.setSuffix(_translate("MainDialog", " layer"))
            self.look_layout.pushButton_add_new_look.setText(
                _translate("MainWindow", "Add next stop")
            )
            self.look_layout.pushButton_add_new_look.adjustSize()



            # Vent block
            self.fan_layout.label_checkBox_vent.setText(
                _translate("MainWindow", "Add lines to make a vent")
            )
            self.fan_layout.label_vent_start.setText(_translate("MainWindow", "Vent start"))
            self.fan_layout.spinBox_vent_start.setSuffix(_translate("MainDialog", " layer"))
            self.fan_layout.label_vent_power.setText(_translate("MainWindow", "Power:"))
            self.fan_layout.label_vent_stop.setText(_translate("MainWindow", "vent stop"))
            self.fan_layout.spinBox_vent_stop.setSuffix(_translate("MainDialog", " layer"))
            self.fan_layout.pushButton_add_vent.setText(_translate("MainWindow", "Add"))
        else:
            # self.resize(650, 520)
            # self.pushButton_run.setGeometry(QtCore.QRect(550, 420, 80, 80))
            self.setWindowTitle(_translate("MainDialog", f"Пост Обробка: {sys.argv[1]}"))
            # LA block
            self.LA_layout.label_checkBox_LA.setText(_translate("MainDialog", "Linear Advance"))
            self.LA_layout.label_line_width.setText(_translate("MainDialog", "Товщина лінії"))
            self.LA_layout.label_layer_height.setText(_translate("MainDialog", "Висота шару"))
            self.LA_layout.label_material_diameter.setText(
                _translate("MainDialog", "Діаметр матеріалу")
            )
            self.LA_layout.label_material_linear_advance_factor.setText(
                _translate("MainDialog", "Коефіцієнт Linear Advance:")
            )
            self.LA_layout.doubleSpinBox_line_width.setSuffix(_translate("MainDialog", "мм"))
            self.LA_layout.doubleSpinBox_layer_height.setSuffix(_translate("MainDialog", "мм"))
            self.LA_layout.doubleSpinBox_material_diameter.setSuffix(
                _translate("MainDialog", "мм")
            )
            # Converting g1 to g2/g3 commands.
            self.arc_layout.label_checkBox_Arc.setText(
                _translate(
                    "MainWindow",
                    "Створення кола з сегментів." "Перетворення з g1 на g2/g3 команди.",
                )
            )
            # Look block
            self.look_layout.label_checkBox_look.setText(
                _translate(
                    "MainWindow", "Пауза для огляду моделі, каретка перемістится по X"
                )
            )


            self.look_layout.label_Y.setText(_translate("MainWindow", "та Y"))
            self.look_layout.label_brim.setText(_translate("MainWindow", "Зупинка після краю (brim)"))
            self.look_layout.pushButton_rem_new_look.setText(_translate("MainWindow", "Видалити"))
            self.look_layout.label_look.setText(_translate("MainWindow", "Глянути на"))

            self.look_layout.spinBox_layer.setSuffix(_translate("MainDialog", " шар"))
            self.look_layout.pushButton_add_new_look.setText(
                _translate("MainWindow", "Додати наступну зупинку")
            )
            self.look_layout.pushButton_add_new_look.adjustSize()
            # Vent block
            self.fan_layout.label_checkBox_vent.setText(
                _translate("MainWindow", "Додати вентиляцію на шарах.")
            )
            self.fan_layout.label_vent_start.setText(_translate("MainWindow", "Починаючи з"))
            self.fan_layout.spinBox_vent_start.setSuffix(_translate("MainDialog", " шару"))
            self.fan_layout.label_vent_power.setText(_translate("MainWindow", "Потужність:"))
            self.fan_layout.label_vent_power.adjustSize()
            self.fan_layout.label_vent_stop.setText(_translate("MainWindow", "Зупинись"))
            self.fan_layout.spinBox_vent_stop.setSuffix(_translate("MainDialog", " шарі"))
            self.fan_layout.pushButton_add_vent.setText(_translate("MainWindow", "Додати"))

    def change_language(self):

        if self.translate_button.text() == "EN":
            self.translate_button.setText("Укр")
        else:
            self.translate_button.setText("EN")
        self.retranslate()

    def run(self):
        "Apply  all changes"

        self.save_config()

        if self.LA_layout.checkBox_LA.isChecked():
            add_LA(
                sys.argv[1],
                self.LA_layout.doubleSpinBox_line_width.value(),
                self.LA_layout.doubleSpinBox_layer_height.value(),
                self.LA_layout.doubleSpinBox_material_linear_advance_factor.value(),
                self.LA_layout.doubleSpinBox_material_diameter.value(),
            )

        if self.arc_layout.checkBox_Arc.isChecked():
            if self.arc_layout.radioButton_ArcWeider.isChecked():
                arc_weider(sys.argv[1])
            if self.arc_layout.radioButton_ArcStraightener.isChecked():
                arc_straightener(sys.argv[1])

        if self.look_layout.checkBox_look.isChecked():
            if self.look_layout.checkBox_brim.isChecked():
                first_layers_look.pause_after_brim(sys.argv[1],
                                                   self.spinBox_X.value(),
                                                   self.spinBox_Y.value(),
                                                   1
                                                   )

            for widget in self.look_layout.widgets_list:
                if widget.objectName() == "spinBox_layer" and widget.value()>0:
                    first_layers_look.layer_look(
                        sys.argv[1],
                        widget.value(),
                        self.spinBox_X.value(),
                        self.spinBox_Y.value(),
                    )

        if self.fan_layout.checkBox_vent.isChecked():
            for i, widget in enumerate(self.fan_layout.widgets_list):
                if widget.objectName() == "spinBox_vent_start":
                    # print ("vent",widget.value() )
                    # print( "power1",self.fan_layout.widgets_list[i+2].value())
                    fan_layers_control.fan_on(sys.argv[1], widget.value(), self.fan_layout.widgets_list[i + 2].value())
                if widget.objectName() == "spinBox_vent_stop":
                    fan_layers_control.fan_off(sys.argv[1], widget.value())

        # sys.exit()
    def save_config(self):

        data = {
            "checkBox_LA": self.LA_layout.checkBox_LA.isChecked(),
            "checkBox_Arc": self.arc_layout.checkBox_Arc.isChecked(),
            "checkBox_look": self.look_layout.checkBox_look.isChecked(),
            "checkBox_brim": self.look_layout.checkBox_brim.isChecked(),
            "checkBox_vent": self.fan_layout.checkBox_vent.isChecked(),

            "radioButton_ArcStraightener": self.arc_layout.radioButton_ArcStraightener.isChecked(),
            "radioButton_ArcWeider": self.arc_layout.radioButton_ArcWeider.isChecked(),
            "doubleSpinBox_material_linear_advance_factor": self.LA_layout.doubleSpinBox_material_linear_advance_factor.value(),
            "spinBox_X": self.look_layout.spinBox_X.value(),
            "spinBox_Y": self.look_layout.spinBox_Y.value(),
            "translate_button": self.translate_button.text(),
        }
        # Convert the dictionary to JSON
        json_data = json.dumps(data)

        # Save the JSON data to a file
        with open("config.json", "w") as file:
            file.write(json_data)

    def closeEvent(self, event):
        """save parameters before exit"""
        self.save_config()
        event.accept()



class ParentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.widgets_list=[]

    def checkBox_toggled(self, is_checked):
        """Check if the Look CheckBox is toggled, and change ability for use the LA widgets"""
        if is_checked:
            for widget in self.widgets_list:
                widget.setEnabled(True)
        else:
            for widget in self.widgets_list:
                widget.setDisabled(True)

    def load_parameter(self, name: str):
        try:
            # Load the JSON data from the file
            with open("config.json", "r") as file:
                json_data = file.read()

            # Convert the JSON data to a dictionary
            data = json.loads(json_data)
            return data.get(name, False)
        except FileNotFoundError:
            # Handle the case when the file is not found
            print("Checkbox state file not found.")

        except json.JSONDecodeError:
            # Handle the case when the JSON data is not valid
            print("Invalid JSON data in checkbox state file.")
        if "Spin" in name:
            return 0
        elif "translate" in name:
            return "EN"
        else:
            return False

# class Line(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.line = QtWidgets.QFrame(self)
#         self.line.setFrameShape(QtWidgets.QFrame.HLine)
#         self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
#         self.line.setObjectName("line")

class Line(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.setFixedWidth(500)
        self.setObjectName("line")

class LA_widgets(ParentWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.horizontal_layout_LA_1=QHBoxLayout(self)

        self.checkBox_LA = QtWidgets.QCheckBox(self)
        self.checkBox_LA.setObjectName("checkBox_LA")
        self.checkBox_LA.setChecked(self.load_parameter(self.checkBox_LA.objectName()))
        self.checkBox_LA.clicked.connect(self.checkBox_toggled)

        self.horizontal_layout_LA_1.addWidget(self.checkBox_LA)
        self.label_checkBox_LA = QtWidgets.QLabel(self)
        self.label_checkBox_LA.setObjectName("label_checkBox_LA")
        self.label_checkBox_LA.setText("LA parameter")
        self.horizontal_layout_LA_1.addWidget(self.label_checkBox_LA)
        self.horizontal_layout_LA_1.addSpacing(20)
        self.spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontal_layout_LA_1.addSpacerItem(self.spacer_item)

        self.vertical_layout_LA_2 = QVBoxLayout(self)

        self.horizontal_layout_LA_3 = QHBoxLayout(self)

        self.vertical_layout_LA_4 = QVBoxLayout(self)
        self.label_line_width = QtWidgets.QLabel(self)
        # self.label_line_width.setAlignment(QtCore.Qt.AlignCenter)
        self.label_line_width.setObjectName("label_line_width")
        self.vertical_layout_LA_4.addWidget(self.label_line_width)
        self.doubleSpinBox_line_width = QtWidgets.QDoubleSpinBox(self)

        self.doubleSpinBox_line_width.setFixedWidth(70)
        self.doubleSpinBox_line_width.setSingleStep(0.1)
        self.doubleSpinBox_line_width.setObjectName("doubleSpinBox_line_width")
        self.vertical_layout_LA_4.addWidget(self.doubleSpinBox_line_width)
        self.horizontal_layout_LA_3.addLayout(self.vertical_layout_LA_4)
        self.horizontal_layout_LA_3.addSpacing(10)

        self.vertical_layout_LA_5 = QVBoxLayout(self)
        self.label_layer_height = QtWidgets.QLabel(self)
        # self.label_layer_height.setAlignment(QtCore.Qt.AlignCenter)
        self.label_layer_height.setObjectName("label_layer_height")
        self.vertical_layout_LA_5.addWidget(self.label_layer_height)
        self.doubleSpinBox_layer_height = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox_layer_height.setFixedWidth(70)
        self.doubleSpinBox_layer_height.setSingleStep(0.04)
        self.doubleSpinBox_layer_height.setObjectName("doubleSpinBox_layer_height")
        self.vertical_layout_LA_5.addWidget(self.doubleSpinBox_layer_height, alignment=QtCore.Qt.AlignCenter)
        self.horizontal_layout_LA_3.addLayout(self.vertical_layout_LA_5)
        self.horizontal_layout_LA_3.addSpacing(10)

        self.vertical_layout_LA_6 = QVBoxLayout(self)
        self.label_material_diameter = QtWidgets.QLabel(self)
        self.label_material_diameter.setObjectName("label_material_diameter")
        self.vertical_layout_LA_6.addWidget(self.label_material_diameter)
        self.doubleSpinBox_material_diameter = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox_material_diameter.setFixedWidth(70)
        self.doubleSpinBox_material_diameter.setSingleStep(0.05)
        self.doubleSpinBox_material_diameter.setValue(1.75)
        self.doubleSpinBox_material_diameter.setObjectName(
            "doubleSpinBox_material_diameter"        )
        self.vertical_layout_LA_6.addWidget(self.doubleSpinBox_material_diameter, alignment=QtCore.Qt.AlignCenter)
        self.horizontal_layout_LA_3.addLayout(self.vertical_layout_LA_6)

        self.vertical_layout_LA_2.addLayout(self.horizontal_layout_LA_3)

        self.horizontal_layout_LA_7 = QHBoxLayout(self)
        self.label_material_linear_advance_factor = QtWidgets.QLabel(self)
        self.label_material_linear_advance_factor.setObjectName(
            "label_material_linear_advance_factor"
        )
        self.horizontal_layout_LA_7.addWidget(self.label_material_linear_advance_factor, alignment=QtCore.Qt.AlignRight)
        self.doubleSpinBox_material_linear_advance_factor = QtWidgets.QDoubleSpinBox(
            self
        )
        self.doubleSpinBox_material_linear_advance_factor.setFixedWidth(50)
        self.doubleSpinBox_material_linear_advance_factor.setObjectName(
            "doubleSpinBox_material_linear_advance_factor"
        )
        self.horizontal_layout_LA_7.addWidget(self.doubleSpinBox_material_linear_advance_factor,alignment=QtCore.Qt.AlignLeft)

        self.vertical_layout_LA_2.addLayout(self.horizontal_layout_LA_7)

        self.horizontal_layout_LA_1.addLayout(self.vertical_layout_LA_2)


        self.widgets_list: list(QtWidgets) = [
            self.label_checkBox_LA,
            (self.label_line_width),
            (self.label_layer_height),
            (self.label_material_diameter),
            (self.label_material_linear_advance_factor),
            (self.doubleSpinBox_line_width),
            (self.doubleSpinBox_layer_height),
            (self.doubleSpinBox_material_diameter),
            self.doubleSpinBox_material_linear_advance_factor,
        ]
        self.checkBox_toggled(self.load_parameter(self.checkBox_LA.objectName()))


class Arc_widgets(ParentWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vertical_layout_Arc_1=QVBoxLayout(self)

        self.horizontal_layout_Arc_2 = QFormLayout(self)
        self.horizontal_layout_Arc_3 = QHBoxLayout(self)
        self.horizontal_layout_Arc_3.addSpacing(100)

# Second block for converting g1 to g2/g3 commands.

        self.checkBox_Arc = QtWidgets.QCheckBox(self)
        self.checkBox_Arc.setObjectName("checkBox_Arc")
        self.checkBox_Arc.setChecked(self.load_parameter("checkBox_Arc"))
        self.checkBox_Arc.clicked.connect(self.checkBox_toggled)
        # self.horizontal_layout_Arc_2.addWidget(self.checkBox_Arc)
        self.label_checkBox_Arc = QtWidgets.QLabel(self)
        self.label_checkBox_Arc.setObjectName("label_checkBox_Arc")
        # self.horizontal_layout_Arc_2.addWidget(self.label_checkBox_Arc , alignment=QtCore.Qt.AlignLeft)
        self.horizontal_layout_Arc_2.addRow(self.checkBox_Arc,self.label_checkBox_Arc)

        self.arc_group = QButtonGroup()
        self.radioButton_ArcWeider = QRadioButton(self,text="ArcWeider")
        self.radioButton_ArcWeider.setObjectName("radioButton_ArcWeider")
        self.radioButton_ArcWeider.setChecked(
            self.load_parameter("radioButton_ArcWeider")      )
        self.arc_group.addButton(self.radioButton_ArcWeider)
        self.horizontal_layout_Arc_3.addWidget(self.radioButton_ArcWeider)
        self.radioButton_ArcStraightener = QRadioButton(self,text="ArcStraightener")
        self.radioButton_ArcStraightener.setObjectName("radioButton_ArcStraightener")
        self.radioButton_ArcStraightener.setChecked(
            self.load_parameter("radioButton_ArcStraightener")        )
        self.arc_group.addButton(self.radioButton_ArcStraightener)
        self.horizontal_layout_Arc_3.addWidget(self.radioButton_ArcStraightener)

        self.vertical_layout_Arc_1.addLayout(self.horizontal_layout_Arc_2)
        self.vertical_layout_Arc_1.addLayout(self.horizontal_layout_Arc_3)

        self.widgets_list: list(QtWidgets) = [
            self.label_checkBox_Arc,
            self.radioButton_ArcWeider,
            self.radioButton_ArcStraightener
        ]

        self.checkBox_toggled(self.checkBox_Arc.isChecked())


class Look_widgets(ParentWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vertical_layout_look_1=QVBoxLayout(self)

        self.horizontal_layout_look_2 = QHBoxLayout(self)
        self.horizontal_layout_look_3 = QHBoxLayout(self)
        self.horizontal_layout_look_4 = QHBoxLayout(self)
        self.horizontal_layout_look_4.addSpacing(50)
        # self.horizontal_layout_look_4.setContentsMargins(50, 0, 0, 0)
        self.vertical_layout_look_5 = QVBoxLayout(self)
        self.horizontal_layout_look_6 = QHBoxLayout(self)

        self.form_layout_look = QFormLayout(self)

        # self.horizontal_layout_Arc_3 = QHBoxLayout(self)
        # self.horizontal_layout_Arc_3.addSpacing(100)

        # 3rd block for look at the model
        self.checkBox_look = QtWidgets.QCheckBox(self)
        self.checkBox_look.setObjectName("checkBox_look")
        self.checkBox_look.setChecked(self.load_parameter("checkBox_look"))
        self.checkBox_look.clicked.connect(self.checkBox_toggled)
        self.horizontal_layout_look_2.addWidget(self.checkBox_look)

        self.label_checkBox_look = QtWidgets.QLabel(self)

        self.label_checkBox_look.setObjectName("label_checkBox_look")
        self.horizontal_layout_look_2.addWidget(self.label_checkBox_look)
        self.bed_size = first_layers_look.bad_size(sys.argv[1])

        self.spinBox_X = QtWidgets.QSpinBox(self)
        self.spinBox_X.setObjectName("spinBox_X")
        self.spinBox_X.setMaximum(self.bed_size[0])
        self.spinBox_X.setWrapping(True)
        self.spinBox_X.setValue(self.load_parameter("spinBox_X"))
        self.horizontal_layout_look_2.addWidget(self.spinBox_X)

        self.label_Y = QtWidgets.QLabel(self)
        self.label_Y.setObjectName("label_Y")
        self.horizontal_layout_look_2.addWidget(self.label_Y)

        self.spinBox_Y = QtWidgets.QSpinBox(self)
        self.spinBox_Y.setObjectName("spinBox_Y")
        self.spinBox_Y.setMaximum(self.bed_size[1])
        self.spinBox_Y.setWrapping(True)
        self.spinBox_Y.setValue(self.load_parameter("spinBox_Y"))
        self.horizontal_layout_look_2.addWidget(self.spinBox_Y,alignment=QtCore.Qt.AlignLeft)
        self.horizontal_layout_look_2.addStretch()

        self.vertical_layout_look_1.addLayout(self.horizontal_layout_look_2)

        self.horizontal_layout_look_3.addSpacing(50)
        self.checkBox_brim=QtWidgets.QCheckBox(self)
        self.checkBox_brim.setObjectName("checkBox_brim")
        self.checkBox_brim.setChecked(self.load_parameter("checkBox_look"))
        self.checkBox_brim.clicked.connect(self.checkBox_brim_toggled)
        self.horizontal_layout_look_3.addWidget(self.checkBox_brim, alignment=QtCore.Qt.AlignRight)
        # self.horizontal_layout_look_2 = QHBoxLayout(self)

        self.label_brim=QtWidgets.QLabel(self)
        self.label_brim.setObjectName("label_brim")
        self.horizontal_layout_look_3.addWidget(self.label_brim, alignment=QtCore.Qt.AlignLeft)
        self.horizontal_layout_look_3.addStretch()

        # self.form_layout_look.addRow(self.checkBox_brim,self.label_brim)

        self.vertical_layout_look_1.addLayout(self.horizontal_layout_look_3)



        self.layer_look_list:list[QtWidgets]=list()

        self.label_look = QtWidgets.QLabel(self)

        self.label_look.setObjectName("label_look")
        self.horizontal_layout_look_4.addWidget(self.label_look)
        self.layer_look_list.append(self.label_look)

        self.spinBox_layer = QtWidgets.QSpinBox(self)
        self.spinBox_layer.setMaximum(500000)
        # self.spinBox_layer.setMaximumWidth(30)
        self.spinBox_layer.setObjectName("spinBox_layer")
        self.layer_look_list.append(self.label_look)
        self.horizontal_layout_look_4.addWidget(self.spinBox_layer)

        self.pushButton_rem_new_look = QtWidgets.QPushButton(self)

        self.pushButton_rem_new_look.setObjectName("pushButton_rem_new_look")

        self.pushButton_rem_new_look.clicked.connect(self.remove_new_look)
        self.horizontal_layout_look_4.addWidget(self.pushButton_rem_new_look)
        # self.horizontal_layout_look_4.addStretch()

        self.vertical_layout_look_5.addLayout(self.horizontal_layout_look_4)

        self.horizontal_layout_look_6.addLayout(self.vertical_layout_look_5)






        # self.vertical_layout_look_1.addLayout(self.horizontal_layout_look_5)
        # self.form_layout_look.addRow(self.label_look, self.spinBox_layer)
        # self.horizontal_layout_look_4.addLayout(self.form_layout_look)
        self.looks_count: int = 1

        self.pushButton_add_new_look = QtWidgets.QPushButton(self)
        self.pushButton_add_new_look.setGeometry(QtCore.QRect(260, 215, 70, 30))
        self.pushButton_add_new_look.setObjectName("pushButton_add_new_look")
        self.pushButton_add_new_look.clicked.connect(self.add_new_look)

        self.horizontal_layout_look_6.addWidget(self.pushButton_add_new_look)#, alignment=QtCore.Qt.AlignCenter)

        self.horizontal_layout_look_6.addStretch()

        self.vertical_layout_look_1.addLayout(self.horizontal_layout_look_6)

        # self.horizontal_layout_look_3.addWidget(self.pushButton_add_new_look)
        # self.vertical_layout_look_1.addLayout(self.horizontal_layout_look_4)
        self.widgets_list: list(QtWidgets) = [
            self.label_checkBox_look,
            self.spinBox_X,
            self.label_Y,
            self.spinBox_Y,
            self.label_look,
            self.spinBox_layer,
            self.pushButton_add_new_look,
            self.checkBox_brim,
            self.label_brim,
            self.pushButton_rem_new_look,
        ]

        self.checkBox_toggled(self.load_parameter("checkBox_look"))

    def remove_new_look(self):
        '''Remove button with 3 previous added items'''
        if self.pushButton_rem_new_look == self.sender():
            self.spinBox_layer.setValue(0)
            return

        index:int=None
        for i, widget in enumerate(self.widgets_list):
            if widget == self.sender():  # Find the index of the clicked button
                index = i
                break
        if  index is not None:
            self.widgets_list[index].setParent(None)
            self.widgets_list[index - 1].setParent(None)
            self.widgets_list[index - 2].setParent(None)
            del self.widgets_list[max(0, index - 2):index + 1] #The max(0, index - 2) is used to ensure that the indices are within the valid range.






    def add_new_look(self):
        """Adding up to 3 aditional SpinBoxes"""

        horizontal_layout=QHBoxLayout(self)
        horizontal_layout.setContentsMargins(50, 0, 0, 0)
        label_look = QtWidgets.QLabel(self)
        label_look.setText(self.label_look.text())
        self.layer_look_list.append(label_look)
        self.widgets_list.append(label_look)
        horizontal_layout.addWidget(label_look)

        spinBox_layer = QtWidgets.QSpinBox(self)
        spinBox_layer.setSuffix(self.spinBox_layer.suffix())
        spinBox_layer.setMaximum(500000)
        self.layer_look_list.append(spinBox_layer)
        self.widgets_list.append(spinBox_layer)
        horizontal_layout.addWidget(spinBox_layer)

        pushButton_rem_new_look = QtWidgets.QPushButton(self)
        pushButton_rem_new_look.setText(self.pushButton_rem_new_look.text())
        pushButton_rem_new_look.clicked.connect(self.remove_new_look)
        self.layer_look_list.append(pushButton_rem_new_look)
        self.widgets_list.append(pushButton_rem_new_look)
        horizontal_layout.addWidget(pushButton_rem_new_look)


        self.vertical_layout_look_5.addLayout(horizontal_layout)
        self.horizontal_layout_look_6.addLayout(self.vertical_layout_look_5)




    def checkBox_brim_toggled(self, is_checked):
        """Check if the brim CheckBox is toggled"""
        if is_checked:
            self.label_brim.setEnabled(True)
        else:
            self.label_brim.setDisabled(True)





# class Fan_widgets(ParentWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#
#         self.vertical_layout_fan_1 = QVBoxLayout(self)
#         self.horizontal_layout_fan_2 = QHBoxLayout(self)
#         self.horizontal_layout_fan_3 = QHBoxLayout(self)
#         self.vertical_layout_fan_4 = QVBoxLayout(self)
#         self.horizontal_layout_fan_5 = QHBoxLayout(self)
#
#         self.checkBox_vent = QtWidgets.QCheckBox(self)
#
#         self.checkBox_vent.setObjectName("checkBox_vent")
#         self.checkBox_vent.setChecked(self.load_parameter("checkBox_vent"))
#         self.checkBox_vent.clicked.connect(self.checkBox_toggled)
#         self.horizontal_layout_fan_2.addWidget(self.checkBox_vent)
#         self.label_checkBox_vent = QtWidgets.QLabel(self)
#
#         self.label_checkBox_vent.setObjectName("label_checkBox_vent")
#         self.horizontal_layout_fan_2.addWidget(self.label_checkBox_vent)
#         self.horizontal_layout_fan_2.addStretch()
#         self.vertical_layout_fan_1.addLayout(self.horizontal_layout_fan_2)
#
#
#
#
#
#         self.label_vent_start = QtWidgets.QLabel(self)
#         self.label_vent_start.setObjectName("label_vent_start")
#         self.horizontal_layout_fan_5.addWidget(self.label_vent_start)
#
#         self.spinBox_vent_start = QtWidgets.QSpinBox(self)
#         self.spinBox_vent_start.setFixedWidth(65)
#         self.spinBox_vent_start.setObjectName("spinBox_vent_start")
#         self.spinBox_vent_start.setMaximum(500000)
#
#         self.horizontal_layout_fan_5.addWidget(self.spinBox_vent_start)
#
#         self.label_vent_power = QtWidgets.QLabel(self)
#         self.label_vent_power.setObjectName("label_vent_power")
#         self.horizontal_layout_fan_5.addWidget(self.label_vent_power)
#
#         self.spinBox_vent_power = QtWidgets.QSpinBox(self)
#         self.spinBox_vent_power.setMaximum(255)
#         self.spinBox_vent_power.setValue(255)
#         self.spinBox_vent_power.setWrapping(True)
#         self.spinBox_vent_power.setObjectName("spinBox_vent_power")
#         self.horizontal_layout_fan_5.addWidget(self.spinBox_vent_power)
#
#         self.label_vent_stop = QtWidgets.QLabel(self)
#         self.label_vent_stop.setObjectName("label_vent_stop")
#         self.horizontal_layout_fan_5.addWidget(self.label_vent_stop)
#
#         self.spinBox_vent_stop = QtWidgets.QSpinBox(self)
#         self.spinBox_vent_stop.setMaximum(500000)
#         self.spinBox_vent_stop.setFixedWidth(65)
#         self.spinBox_vent_stop.setObjectName("spinBox_vent_stop")
#         self.horizontal_layout_fan_5.addWidget(self.spinBox_vent_stop)
#
#         self.vertical_layout_fan_4.addLayout(self.horizontal_layout_fan_5)
#         self.horizontal_layout_fan_3.addLayout(self.vertical_layout_fan_4)
#
#
#         self.pushButton_add_vent = QtWidgets.QPushButton(self)
#
#         self.pushButton_add_vent.setObjectName("pushButton_add_vent")
#         self.pushButton_add_vent.clicked.connect(self.add_new_vent)
#         self.horizontal_layout_fan_3.addWidget(self.pushButton_add_vent)
#         self.horizontal_layout_fan_3.addStretch()
#         self.vertical_layout_fan_1.addLayout(self.horizontal_layout_fan_3)
#
#         self.count_vent: int = 1
#
#         self.widgets_list: list(QtWidgets) = [
#             self.label_checkBox_vent,
#             self.label_vent_start,
#             self.spinBox_vent_start,
#             self.label_vent_power,
#             self.spinBox_vent_power,
#             self.spinBox_vent_stop,
#             self.label_vent_stop,
#             self.pushButton_add_vent,
#         ]
#
#         self.checkBox_toggled(self.load_parameter("checkBox_vent"))
#
#     def add_new_vent(self):
#         horizontal_layout=QHBoxLayout(self)
#         label_vent_start = QtWidgets.QLabel(self)
#         label_vent_start.setText(self.label_vent_start.text())
#         label_vent_start.setObjectName("label_vent_start")
#         horizontal_layout.addWidget(label_vent_start)
#         self.widgets_list.append(label_vent_start)
#
#         spinBox_vent_start = QtWidgets.QSpinBox(self)
#         spinBox_vent_start.setMaximum(500000)
#         spinBox_vent_start.setFixedWidth(65)
#         spinBox_vent_start.setSuffix(self.spinBox_vent_start.suffix())
#         spinBox_vent_start.setObjectName("spinBox_vent_start")
#         horizontal_layout.addWidget(spinBox_vent_start)
#         self.widgets_list.append(spinBox_vent_start)
#
#         label_vent_power = QtWidgets.QLabel(self)
#         label_vent_power.setText(self.label_vent_power.text())
#         label_vent_power.setObjectName("label_vent_power")
#         horizontal_layout.addWidget(label_vent_power)
#         self.widgets_list.append(label_vent_power)
#
#         spinBox_vent_power = QtWidgets.QSpinBox(self)
#         spinBox_vent_power.setMaximum(255)
#         spinBox_vent_power.setValue(255)
#         spinBox_vent_power.setWrapping(True)
#         spinBox_vent_power.setObjectName("spinBox_vent_power")
#         horizontal_layout.addWidget(spinBox_vent_power)
#         self.widgets_list.append(spinBox_vent_power)
#
#         spinBox_vent_stop = QtWidgets.QSpinBox(self)
#         spinBox_vent_stop.setMaximum(500000)
#         spinBox_vent_stop.setFixedWidth(65)
#         spinBox_vent_stop.setSuffix(self.spinBox_vent_stop.suffix())
#         spinBox_vent_stop.setObjectName("spinBox_vent_stop")
#         horizontal_layout.addWidget(spinBox_vent_stop)
#         self.widgets_list.append(spinBox_vent_stop)
#
#         label_vent_stop = QtWidgets.QLabel(self)
#         label_vent_stop.setText(self.label_vent_stop.text())
#         label_vent_stop.setGeometry(QtCore.QRect(260, 410, 55, 20))
#         label_vent_stop.setObjectName("label_vent_stop")
#         horizontal_layout.addWidget(label_vent_stop)
#         self.widgets_list.append(label_vent_stop)
#
#         self.vertical_layout_fan_4.addLayout((horizontal_layout))
#
#
#
#     def names_list(self):
#         '''Tries to names the widgets when they appears'''
#
#         name_dictionary = {
#             "EN": {
#                 "label_vent_start": "Vent start"},
#             "UKR": {}
#         }
#
#         try:
#             for widget in self.widgets_list:
#                 print("button is",dialog.translate_button.text())
#                 if isinstance(widget, QtWidgets.QLabel):
#                     print("label")
#                 elif isinstance(widget, QtWidgets.QSpinBox):
#
#                     print("QSpinBox")
#         except:
#             pass

class Fan_widgets(ParentWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.vertical_layout_fan_1 = QVBoxLayout(self)
        self.horizontal_layout_fan_1 = QHBoxLayout(self)
        self.horizontal_layout_fan_2 = QHBoxLayout(self)
        self.horizontal_layout_fan_2.addSpacing(50)
        self.vertical_layout_fan_2 = QVBoxLayout(self)
        self.vertical_layout_fan_3 = QVBoxLayout(self)
        self.vertical_layout_fan_4 = QVBoxLayout(self)
        self.vertical_layout_fan_5 = QVBoxLayout(self)

        # self.vertical_layout_fan_5 = QVBoxLayout(self)
        # self.horizontal_layout_fan_5 = QHBoxLayout(self)

        self.checkBox_vent = QtWidgets.QCheckBox(self)

        self.checkBox_vent.setObjectName("checkBox_vent")
        self.checkBox_vent.setChecked(self.load_parameter("checkBox_vent"))
        self.checkBox_vent.clicked.connect(self.checkBox_toggled)
        self.horizontal_layout_fan_1.addWidget(self.checkBox_vent)
        self.label_checkBox_vent = QtWidgets.QLabel(self)

        self.label_checkBox_vent.setObjectName("label_checkBox_vent")
        self.horizontal_layout_fan_1.addWidget(self.label_checkBox_vent)
        self.horizontal_layout_fan_1.addStretch()
        self.vertical_layout_fan_1.addLayout(self.horizontal_layout_fan_1)





        self.label_vent_start = QtWidgets.QLabel(self)
        self.label_vent_start.setObjectName("label_vent_start")
        self.vertical_layout_fan_2.addWidget(self.label_vent_start)

        self.spinBox_vent_start = QtWidgets.QSpinBox(self)
        self.spinBox_vent_start.setFixedWidth(65)
        self.spinBox_vent_start.setObjectName("spinBox_vent_start")
        self.spinBox_vent_start.setMaximum(500000)
        self.vertical_layout_fan_2.addWidget(self.spinBox_vent_start)

        self.horizontal_layout_fan_2.addLayout(self.vertical_layout_fan_2)


        self.label_vent_power = QtWidgets.QLabel(self)
        self.label_vent_power.setObjectName("label_vent_power")
        self.vertical_layout_fan_3.addWidget(self.label_vent_power)

        self.spinBox_vent_power = QtWidgets.QSpinBox(self)
        self.spinBox_vent_power.setMaximum(255)
        self.spinBox_vent_power.setValue(255)
        self.spinBox_vent_power.setWrapping(True)
        self.spinBox_vent_power.setObjectName("spinBox_vent_power")
        self.vertical_layout_fan_3.addWidget(self.spinBox_vent_power)

        self.horizontal_layout_fan_2.addLayout(self.vertical_layout_fan_3)

        self.label_vent_stop = QtWidgets.QLabel(self)
        self.label_vent_stop.setObjectName("label_vent_stop")
        self.vertical_layout_fan_4.addWidget(self.label_vent_stop)

        self.spinBox_vent_stop = QtWidgets.QSpinBox(self)
        self.spinBox_vent_stop.setMaximum(500000)
        self.spinBox_vent_stop.setFixedWidth(65)
        self.spinBox_vent_stop.setObjectName("spinBox_vent_stop")
        self.vertical_layout_fan_4.addWidget(self.spinBox_vent_stop)
        self.horizontal_layout_fan_2.addLayout(self.vertical_layout_fan_4)


        self.label_del = QtWidgets.QLabel(self)
        self.label_del.setObjectName("label_vent_stop")
        self.vertical_layout_fan_5.addWidget(self.label_del)
        self.horizontal_layout_fan_2.addLayout(self.vertical_layout_fan_5)

        # self.pushButton_remove_vent = QtWidgets.QPushButton(self)
        # # self.pushButton_remove_vent.setText(dialog.look_layout.pushButton_rem_new_look.text())
        # self.pushButton_remove_vent.setObjectName("pushButton_remove_vent")
        # self.pushButton_remove_vent.clicked.connect(self.remove_new_vent)
        # self.vertical_layout_fan_5.addWidget(self.pushButton_remove_vent)
        # self.widgets_list.append(self.pushButton_remove_vent)
        # self.horizontal_layout_fan_2.addLayout(self.vertical_layout_fan_5)

        # self.vertical_layout_fan_4.addLayout(self.horizontal_layout_fan_5)
        # self.horizontal_layout_fan_2.addLayout(self.vertical_layout_fan_4)


        self.pushButton_add_vent = QtWidgets.QPushButton(self)
        self.pushButton_add_vent.setObjectName("pushButton_add_vent")
        # self.pushButton_add_vent.setFixedSize(80, 50)
        self.pushButton_add_vent.clicked.connect(self.add_new_vent)
        self.horizontal_layout_fan_2.addWidget(self.pushButton_add_vent)
        self.horizontal_layout_fan_2.addStretch()
        self.vertical_layout_fan_1.addLayout(self.horizontal_layout_fan_2)

        self.count_vent: int = 1

        self.widgets_list: list(QtWidgets) = [
            self.label_checkBox_vent,
            self.label_vent_start,
            self.spinBox_vent_start,
            self.label_vent_power,
            self.spinBox_vent_power,
            self.spinBox_vent_stop,
            self.label_vent_stop,
            self.pushButton_add_vent,
        ]

        self.checkBox_toggled(self.load_parameter("checkBox_vent"))

    def add_new_vent(self):
        '''Create new area with spins'''

        spinBox_vent_start = QtWidgets.QSpinBox(self)
        spinBox_vent_start.setMaximum(500000)
        spinBox_vent_start.setFixedWidth(65)
        spinBox_vent_start.setSuffix(self.spinBox_vent_start.suffix())
        spinBox_vent_start.setObjectName("spinBox_vent_start")
        self.vertical_layout_fan_2.addWidget(spinBox_vent_start)
        self.widgets_list.append(spinBox_vent_start)

        spinBox_vent_power = QtWidgets.QSpinBox(self)
        spinBox_vent_power.setMaximum(255)
        spinBox_vent_power.setValue(255)
        spinBox_vent_power.setWrapping(True)
        spinBox_vent_power.setObjectName("spinBox_vent_power")
        self.vertical_layout_fan_3.addWidget(spinBox_vent_power)
        self.widgets_list.append(spinBox_vent_power)

        spinBox_vent_stop = QtWidgets.QSpinBox(self)
        spinBox_vent_stop.setMaximum(500000)
        spinBox_vent_stop.setFixedWidth(65)
        spinBox_vent_stop.setSuffix(self.spinBox_vent_stop.suffix())
        spinBox_vent_stop.setObjectName("spinBox_vent_stop")
        self.vertical_layout_fan_4.addWidget(spinBox_vent_stop)
        self.widgets_list.append(spinBox_vent_stop)

        pushButton_remove_vent = QtWidgets.QPushButton(self)
        pushButton_remove_vent.setText(dialog.look_layout.pushButton_rem_new_look.text())
        pushButton_remove_vent.setFixedSize(70,24)
        pushButton_remove_vent.setObjectName("pushButton_remove_vent")
        pushButton_remove_vent.clicked.connect(self.remove_new_vent)
        self.vertical_layout_fan_5.addWidget(pushButton_remove_vent)
        self.widgets_list.append(pushButton_remove_vent)
    def remove_new_vent(self):
        '''Remove button with 3 previous added spins'''
        #
        # if self.pushButton_remove_vent == self.sender():
        #     self.spinBox_vent_start.setValue(0)
        #     self.spinBox_vent_power.setValue(0)
        #     self.spinBox_vent_stop.setValue(0)
        index:int=None
        for i, widget in enumerate(self.widgets_list):
            if widget == self.sender():  # Find the index of the clicked button
                index = i
                print(index)
                break
        if  index is not None:

            self.widgets_list[index].setParent(None)
            self.widgets_list[index - 1].setParent(None)
            self.widgets_list[index - 2].setParent(None)
            self.widgets_list[index - 3].setParent(None)
            del self.widgets_list[max(0, index - 3):index + 1] #The max(0, index - 3) is used to ensure that the indices are within the valid range.






    def names_list(self):
        '''Tries to names the widgets when they appears'''

        name_dictionary = {
            "EN": {
                "label_vent_start": "Vent start"},
            "UKR": {}
        }

        try:
            for widget in self.widgets_list:
                print("button is",dialog.translate_button.text())
                if isinstance(widget, QtWidgets.QLabel):
                    print("label")
                elif isinstance(widget, QtWidgets.QSpinBox):

                    print("QSpinBox")
        except:
            pass




class NoFile(QMessageBox):
    def __init__(self):
        super().__init__()
        self.resize(400, 150)
        self.setWindowTitle("Error")
        self.setText(
            "File not specifed. \nUse PostProcessing-Script-for-PrusaSlicer.py <gcode file>."
        )

        self.setIcon(QMessageBox.Critical)

        self.translate_button = QtWidgets.QPushButton("EN", self)
        self.translate_button.setGeometry(QtCore.QRect(10, 66, 50, 50))
        self.translate_button.setObjectName("translate_button")
        self.translate_button.clicked.connect(self.change_language)

        self.show()

    def change_language(self):
        if self.translate_button.text() == "EN":
            self.translate_button.setText("UKR")
            self.setText(
                "Вибачте. Але здаеться ви не прикріпили файл.\n"
                "Виконайте: \n PostProcessing-Script-for-PrusaSlicer.exe <gcode file>\n"
                "(замість <gcode file> встайте свій файл)."
            )
            self.setWindowTitle("Помилка")
        else:
            self.translate_button.setText("EN")
            self.setText(
                "File not specifed. \nUse PostProcessing-Script-for-PrusaSlicer.py <gcode file>."
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    if len(sys.argv) > 1:
        if ".gcode" in sys.argv[1]:
            gcode_file = sys.argv[1]
            dialog = MainDialog()
        else:
            print(
                "File not specifed. Use PostProcessing-Script-for-PrusaSlicer.py <gcode file>."
            )
            alert = NoFile()
    else:
        print(
            "File not specifed. Use PostProcessing-Script-for-PrusaSlicer.py <gcode file>."
        )
        alert = NoFile()
    sys.exit(app.exec_())
