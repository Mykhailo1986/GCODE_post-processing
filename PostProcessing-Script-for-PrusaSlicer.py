import sys
import json

import linear_advance_add
from fan_layers_control import fan_on
import extrusion_width_hight
from linear_advance_add import add_LA
from first_layers_look import layer_look
from arc_helper import arc_weider, arc_straightener
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QRadioButton,
    QButtonGroup,
    QMessageBox,
)


class MainDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(600, 520)

        self.translate_button = QtWidgets.QPushButton(self)
        self.translate_button.setText(self.load_parameter("translate_button"))
        self.translate_button.setGeometry(QtCore.QRect(550, 0, 50, 50))
        self.translate_button.setObjectName("translate_button")
        self.translate_button.clicked.connect(self.change_language)

        # Firts block for Line Advance

        self.checkBox_LA = QtWidgets.QCheckBox(self)
        self.checkBox_LA.setGeometry(QtCore.QRect(30, 35, 111, 20))
        self.checkBox_LA.setObjectName("checkBox_LA")
        self.checkBox_LA.setChecked(False)
        self.checkBox_LA.clicked.connect(self.checkBox_LA_toggled)

        self.label_checkBox_LA = QtWidgets.QLabel(self)
        self.label_checkBox_LA.setGeometry(QtCore.QRect(55, 35, 111, 20))
        self.label_checkBox_LA.setObjectName("label_checkBox_LA")

        self.label_line_width = QtWidgets.QLabel(self)
        self.label_line_width.setGeometry(QtCore.QRect(180, 10, 61, 20))
        self.label_line_width.setAlignment(QtCore.Qt.AlignCenter)
        self.label_line_width.setObjectName("label_line_width")

        self.label_layer_height = QtWidgets.QLabel(self)
        self.label_layer_height.setGeometry(QtCore.QRect(280, 10, 81, 20))
        self.label_layer_height.setObjectName("label_layer_height")

        self.label_material_diameter = QtWidgets.QLabel(self)
        self.label_material_diameter.setGeometry(QtCore.QRect(380, 10, 111, 20))
        self.label_material_diameter.setObjectName("label_material_diameter")

        self.label_material_linear_advance_factor = QtWidgets.QLabel(self)
        self.label_material_linear_advance_factor.setGeometry(
            QtCore.QRect(190, 70, 200, 20)
        )
        self.label_material_linear_advance_factor.setObjectName(
            "label_material_linear_advance_factor"
        )

        self.doubleSpinBox_line_width = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox_line_width.setGeometry(QtCore.QRect(190, 35, 68, 20))
        self.doubleSpinBox_line_width.setSingleStep(0.1)
        self.doubleSpinBox_line_width.setObjectName("doubleSpinBox_line_width")

        self.doubleSpinBox_layer_height = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox_layer_height.setGeometry(QtCore.QRect(280, 35, 68, 20))
        self.doubleSpinBox_layer_height.setSingleStep(0.04)
        self.doubleSpinBox_layer_height.setObjectName("doubleSpinBox_layer_height")

        self.doubleSpinBox_material_diameter = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox_material_diameter.setGeometry(QtCore.QRect(390, 35, 68, 20))
        self.doubleSpinBox_material_diameter.setSingleStep(0.05)
        self.doubleSpinBox_material_diameter.setValue(1.75)
        self.doubleSpinBox_material_diameter.setObjectName(
            "doubleSpinBox_material_diameter"
        )

        self.doubleSpinBox_material_linear_advance_factor = QtWidgets.QDoubleSpinBox(
            self
        )
        self.doubleSpinBox_material_linear_advance_factor.setGeometry(
            QtCore.QRect(375, 70, 68, 20)
        )
        self.doubleSpinBox_material_linear_advance_factor.setAlignment(
            QtCore.Qt.AlignRight
        )
        self.doubleSpinBox_material_linear_advance_factor.setObjectName(
            "doubleSpinBox_material_linear_advance_factor"
        )

        self.list_LA: list(QtWidgets) = [
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

        if self.load_parameter("checkBox_LA"):
            for widget in self.list_LA:
                widget.setEnabled(True)
        else:
            for widget in self.list_LA:
                widget.setDisabled(True)

        self.set_values_LA()

        self.line_1 = QtWidgets.QFrame(self)
        self.line_1.setGeometry(QtCore.QRect(20, 90, 471, 16))
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1.setObjectName("line_1")

        # Second block for converting g1 to g2/g3 commands.

        self.checkBox_Arc = QtWidgets.QCheckBox(self)
        self.checkBox_Arc.setGeometry(QtCore.QRect(30, 110, 411, 20))
        self.checkBox_Arc.setObjectName("checkBox_Arc")
        self.checkBox_Arc.setChecked(self.load_parameter("checkBox_Arc"))
        self.checkBox_Arc.clicked.connect(self.checkBox_Arc_toggled)

        self.label_checkBox_Arc = QtWidgets.QLabel(self)
        self.label_checkBox_Arc.setGeometry(QtCore.QRect(55, 110, 411, 20))
        self.label_checkBox_Arc.setObjectName("label_checkBox_Arc")

        self.arc_group = QButtonGroup()
        self.radioButton_ArcWeider = QRadioButton(self)
        self.radioButton_ArcWeider.setGeometry(QtCore.QRect(80, 140, 411, 20))
        self.radioButton_ArcWeider.setObjectName("radioButton_ArcWeider")
        self.radioButton_ArcWeider.setChecked(
            self.load_parameter("radioButton_ArcWeider")
        )
        self.arc_group.addButton(self.radioButton_ArcWeider)

        self.label_ArcWeider = QtWidgets.QLabel(self)
        self.label_ArcWeider.setGeometry(QtCore.QRect(100, 140, 411, 20))
        self.label_ArcWeider.setObjectName("label_ArcWeider")
        self.label_ArcWeider.setText("ArcWeider")

        self.radioButton_ArcStraightener = QRadioButton(self)
        self.radioButton_ArcStraightener.setGeometry(QtCore.QRect(300, 140, 411, 20))
        self.radioButton_ArcStraightener.setObjectName("radioButton_ArcStraightener")
        self.radioButton_ArcStraightener.setChecked(
            self.load_parameter("radioButton_ArcStraightener")
        )
        self.arc_group.addButton(self.radioButton_ArcStraightener)

        self.label_ArcStraightener = QtWidgets.QLabel(self)
        self.label_ArcStraightener.setGeometry(QtCore.QRect(320, 140, 411, 20))
        self.label_ArcStraightener.setObjectName("label_ArcStraightener")
        self.label_ArcStraightener.setText("ArcStraightener")

        self.list_arc: list(QtWidgets) = [
            self.label_checkBox_Arc,
            self.radioButton_ArcWeider,
            self.label_ArcWeider,
            self.radioButton_ArcStraightener,
            self.label_ArcStraightener,
        ]

        self.checkBox_Arc_toggled(self.checkBox_Arc.isChecked())

        self.line_2 = QtWidgets.QFrame(self)
        self.line_2.setGeometry(QtCore.QRect(20, 160, 471, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        # 3rd block for look at the model
        self.checkBox_look = QtWidgets.QCheckBox(self)
        self.checkBox_look.setGeometry(QtCore.QRect(30, 190, 341, 20))
        self.checkBox_look.setObjectName("checkBox_look")
        self.checkBox_look.setChecked(self.load_parameter("checkBox_look"))
        self.checkBox_look.clicked.connect(self.checkBox_look_toggled)

        self.label_checkBox_look = QtWidgets.QLabel(self)
        self.label_checkBox_look.setGeometry(QtCore.QRect(55, 190, 320, 20))
        self.label_checkBox_look.setObjectName("label_checkBox_look")

        self.spinBox_X = QtWidgets.QSpinBox(self)
        self.spinBox_X.setGeometry(QtCore.QRect(380, 190, 40, 20))
        self.spinBox_X.setObjectName("spinBox_X")
        self.spinBox_X.setValue(self.load_parameter("spinBox_X"))

        self.label_Y = QtWidgets.QLabel(self)
        self.label_Y.setGeometry(QtCore.QRect(430, 190, 40, 20))
        self.label_Y.setObjectName("label_Y")

        self.spinBox_Y = QtWidgets.QSpinBox(self)
        self.spinBox_Y.setGeometry(QtCore.QRect(470, 190, 40, 20))
        self.spinBox_Y.setObjectName("spinBox_Y")
        self.spinBox_Y.setValue(self.load_parameter("spinBox_Y"))

        self.label_look = QtWidgets.QLabel(self)
        self.label_look.setGeometry(QtCore.QRect(70, 220, 65, 20))
        self.label_look.setObjectName("label_look")

        self.spinBox_layer = QtWidgets.QSpinBox(self)
        self.spinBox_layer.setGeometry(QtCore.QRect(140, 220, 60, 20))
        self.spinBox_layer.setObjectName("spinBox_layer")
        self.spinBox_layer.setValue(2)

        self.looks_count: int = 1

        self.pushButton_add_new_look = QtWidgets.QPushButton(self)
        self.pushButton_add_new_look.setGeometry(QtCore.QRect(260, 215, 70, 30))
        self.pushButton_add_new_look.setObjectName("pushButton_add_new_look")
        self.pushButton_add_new_look.clicked.connect(self.add_new_look)

        self.list_look: list(QtWidgets) = [
            self.label_checkBox_look,
            self.spinBox_X,
            self.label_Y,
            self.spinBox_Y,
            self.label_look,
            self.spinBox_layer,
            self.pushButton_add_new_look,
        ]

        self.checkBox_look_toggled(self.load_parameter("checkBox_look"))

        self.line_3 = QtWidgets.QFrame(self)
        self.line_3.setGeometry(QtCore.QRect(20, 270, 491, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")

        # Vent Block

        self.checkBox_vent = QtWidgets.QCheckBox(self)
        self.checkBox_vent.setGeometry(QtCore.QRect(30, 370, 181, 20))
        self.checkBox_vent.setObjectName("checkBox_vent")
        self.checkBox_vent.setChecked(self.load_parameter("checkBox_vent"))
        self.checkBox_vent.clicked.connect(self.checkBox_vent_toggled)

        self.label_checkBox_vent = QtWidgets.QLabel(self)
        self.label_checkBox_vent.setGeometry(QtCore.QRect(55, 370, 180, 20))
        self.label_checkBox_vent.setObjectName("label_checkBox_vent")

        self.label_vent_start = QtWidgets.QLabel(self)
        self.label_vent_start.setGeometry(QtCore.QRect(45, 410, 78, 20))
        self.label_vent_start.setObjectName("label_vent_start")

        self.spinBox_vent_start = QtWidgets.QSpinBox(self)
        self.spinBox_vent_start.setGeometry(QtCore.QRect(130, 410, 60, 20))
        self.spinBox_vent_start.setObjectName("spinBox_vent_start")

        self.label_vent_power = QtWidgets.QLabel(self)
        self.label_vent_power.setGeometry(QtCore.QRect(200, 390, 60, 20))
        self.label_vent_power.setObjectName("label_vent_power")

        self.spinBox_vent_power = QtWidgets.QSpinBox(self)
        self.spinBox_vent_power.setGeometry(QtCore.QRect(200, 410, 40, 20))
        self.spinBox_vent_power.setMaximum(255)
        self.spinBox_vent_power.setValue(255)
        self.spinBox_vent_power.setWrapping(True)
        self.spinBox_vent_power.setObjectName("spinBox_vent_power")

        self.spinBox_vent_stop = QtWidgets.QSpinBox(self)
        self.spinBox_vent_stop.setGeometry(QtCore.QRect(320, 410, 60, 20))
        self.spinBox_vent_stop.setObjectName("spinBox_vent_stop")

        self.label_vent_stop = QtWidgets.QLabel(self)
        self.label_vent_stop.setGeometry(QtCore.QRect(260, 410, 55, 20))
        self.label_vent_stop.setObjectName("label_vent_stop")

        self.pushButton_add_vent = QtWidgets.QPushButton(self)
        self.pushButton_add_vent.setGeometry(QtCore.QRect(390, 405, 70, 30))
        self.pushButton_add_vent.setObjectName("pushButton_add_vent")
        self.pushButton_add_vent.clicked.connect(self.add_new_vent)

        self.count_vent: int = 1

        self.list_vent: list(QtWidgets) = [
            self.label_checkBox_vent,
            self.label_vent_start,
            self.spinBox_vent_start,
            self.label_vent_power,
            self.spinBox_vent_power,
            self.spinBox_vent_stop,
            self.label_vent_stop,
            self.pushButton_add_vent,
        ]

        self.checkBox_vent_toggled(self.load_parameter("checkBox_vent"))

        self.pushButton_run = QtWidgets.QPushButton(self)
        self.pushButton_run.setGeometry(QtCore.QRect(500, 420, 80, 80))
        self.pushButton_run.setObjectName("pushButton_add_vent")
        self.pushButton_run.setFont(QFont("Arial", 14, 75, True))
        self.pushButton_run.setText("Run")
        self.pushButton_run.setStyleSheet("color: green")
        self.pushButton_run.clicked.connect(self.run)

        self.label_copyright = QtWidgets.QLabel(self)
        self.label_copyright.setText("©Mykhailo Kucher 2023\nEmail: I_am_Misha@i.ua ")
        # Customize the font and style of the label
        font = self.label_copyright.font()
        font.setBold(True)
        font.setPointSize(12)
        self.label_copyright.setFont(font)
        self.label_copyright.setGeometry(QtCore.QRect(30, 450, 300, 80))
        self.label_copyright.setObjectName("label_copyright")

        self.retranslate()
        self.show()

    def run(self):

        self.save_config()
        if (
            self.checkBox_vent.isChecked()
            and self.spinBox_vent_start.value() == 0
            and self.spinBox_vent_stop.value() == 0
        ):
            fan_on(
                gcode_file,
                self.spinBox_vent_start.value(),
                self.spinBox_vent_power.value(),
                self.spinBox_vent_stop.value(),
            )
            try:
                fan_on(
                    gcode_file,
                    self.spinBox_vent_start_2.value(),
                    self.spinBox_vent_power_2.value(),
                    self.spinBox_vent_stop_2.value(),
                )
                fan_on(
                    gcode_file,
                    self.spinBox_vent_start_3.value(),
                    self.spinBox_vent_power_3.value(),
                    self.spinBox_vent_stop_3.value(),
                )
                fan_on(
                    gcode_file,
                    self.spinBox_vent_start_4.value(),
                    self.spinBox_vent_power_4.value(),
                    self.spinBox_vent_stop_4.value(),
                )
            except:
                pass
        if self.checkBox_LA.isChecked():

            add_LA(
                gcode_file,
                self.doubleSpinBox_line_width.value(),
                self.doubleSpinBox_layer_height.value(),
                self.doubleSpinBox_material_linear_advance_factor.value(),
                self.doubleSpinBox_material_diameter.value(),
            )
        if self.checkBox_look.isChecked():
            layer_look(
                gcode_file,
                self.spinBox_layer.value(),
                self.spinBox_X.value(),
                self.spinBox_Y.value(),
            )
            try:
                layer_look(
                    gcode_file,
                    self.spinBox_layer_2.value(),
                    self.spinBox_X_2.value(),
                    self.spinBox_Y_2.value(),
                )
                layer_look(
                    self.spinBox_layer_3.value(),
                    self.spinBox_X_3.value(),
                    self.spinBox_Y_3.value(),
                )
                layer_look(
                    gcode_file,
                    self.spinBox_layer_4.value(),
                    self.spinBox_X_4.value(),
                    self.spinBox_Y_4.value(),
                )
            except:
                pass
        if self.checkBox_Arc.isChecked():
            if self.radioButton_ArcWeider.isChecked():
                arc_weider(gcode_file)
            if self.radioButton_ArcStraightener.isChecked():
                arc_straightener(gcode_file)

        sys.exit()

    def checkBox_LA_toggled(self, is_checked):
        """Check if the LA CheckBox is toggled, and change ability for use the LA widgets"""

        if is_checked:
            if linear_advance_add.check_LA_in_gcode(gcode_file):
                LA_exist = QMessageBox()
                LA_exist.setText(
                    "Your G-code already contains a linear advance option,\n"
                    " there may be no need to modify or add additional instructions \n"
                    "for linear advance in your post-processing script. "
                    if self.translate_button.text() == "EN"
                    else "Ваш G-code Вже має linear advance функцію,\n"
                    " не має потреби додавати цю опцію"
                )

                LA_exist.setIcon(QMessageBox.Information)
                LA_exist.setWindowTitle("Already exist")
                LA_exist.exec_()

            for widget in self.list_LA:
                widget.setEnabled(True)
        else:
            for widget in self.list_LA:
                widget.setDisabled(True)

    def checkBox_Arc_toggled(self, is_checked):
        """Check if the Arc CheckBox is toggled, and change ability for use the LA widgets"""
        if is_checked:
            for widget in self.list_arc:
                widget.setEnabled(True)
        else:
            for widget in self.list_arc:
                widget.setDisabled(True)

    def checkBox_look_toggled(self, is_checked):
        """Check if the Look CheckBox is toggled, and change ability for use the LA widgets"""
        if is_checked:
            for widget in self.list_look:
                widget.setEnabled(True)
        else:
            for widget in self.list_look:
                widget.setDisabled(True)

    def checkBox_vent_toggled(self, is_checked):
        """Check if the fan CheckBox is toggled, and change ability for use the LA widgets"""
        if is_checked:
            for widget in self.list_vent:
                widget.setEnabled(True)
        else:
            for widget in self.list_vent:
                widget.setDisabled(True)

    def change_language(self):
        if self.translate_button.text() == "EN":
            self.translate_button.setText("UKR")
        else:
            self.translate_button.setText("EN")
        self.retranslate()

    def add_new_look(self):
        """Adding up to 3 aditional SpinBoxes"""

        if self.looks_count == 1:
            self.label_look_2 = QtWidgets.QLabel(self)
            self.label_look_2.setText(self.label_look.text())
            self.label_look_2.setGeometry(
                QtCore.QRect(70, 220 + 30 * self.looks_count, 65, 20)
            )
            self.label_look_2.setObjectName("label_look_2")
            self.label_look_2.show()

            self.spinBox_layer_2 = QtWidgets.QSpinBox(self)
            self.spinBox_layer_2.setSuffix(self.spinBox_layer.suffix())
            self.spinBox_layer_2.setGeometry(
                QtCore.QRect(140, 220 + 30 * self.looks_count, 60, 20)
            )
            self.spinBox_layer_2.setObjectName("spinBox_layer_2")
            self.spinBox_layer_2.show()
            self.list_look.append(self.spinBox_layer_2)

            self.line_3.setGeometry(
                QtCore.QRect(20, 270 + 30 * self.looks_count, 491, 16)
            )

        elif self.looks_count == 2:
            self.label_look_3 = QtWidgets.QLabel(self)
            self.label_look_3.setText(self.label_look.text())
            self.label_look_3.setGeometry(
                QtCore.QRect(70, 220 + 30 * self.looks_count, 65, 20)
            )
            self.label_look_3.setObjectName("label_look_3")
            self.label_look_3.show()

            self.spinBox_layer_3 = QtWidgets.QSpinBox(self)
            self.spinBox_layer_3.setSuffix(self.spinBox_layer.suffix())
            self.spinBox_layer_3.setGeometry(
                QtCore.QRect(140, 220 + 30 * self.looks_count, 60, 20)
            )
            self.spinBox_layer_3.setObjectName("spinBox_layer_3")
            self.spinBox_layer_3.show()
            self.list_look.append(self.spinBox_layer_3)

            self.line_3.setGeometry(
                QtCore.QRect(20, 270 + 30 * self.looks_count, 491, 16)
            )

        elif self.looks_count == 3:
            self.label_look_4 = QtWidgets.QLabel(self)
            self.label_look_4.setText(self.label_look.text())
            self.label_look_4.setGeometry(
                QtCore.QRect(70, 220 + 30 * self.looks_count, 65, 20)
            )
            self.label_look_4.setObjectName("label_look_4")
            self.label_look_4.show()

            self.spinBox_layer_4 = QtWidgets.QSpinBox(self)
            self.spinBox_layer_4.setSuffix(self.spinBox_layer.suffix())
            self.spinBox_layer_4.setGeometry(
                QtCore.QRect(140, 220 + 30 * self.looks_count, 60, 20)
            )
            self.spinBox_layer_4.setObjectName("spinBox_layer_4")
            self.spinBox_layer_4.show()
            self.list_look.append(self.spinBox_layer_4)
            # self.pushButton_add_new_look.setDisabled(True)

        else:
            self.pushButton_add_new_look.setDisabled(True)
            if self.translate_button.text() == "EN":
                QtWidgets.QMessageBox.information(
                    self, "No more looks", "You can't add more looks"
                )
            else:
                QtWidgets.QMessageBox.information(
                    self, "Не лізе (((", "Неможливо додати білше шарів для перегляду"
                )

        self.looks_count += 1

    def add_new_vent(self):
        """Adding up to 3 aditional vent SpinBoxes"""
        if self.count_vent == 1:

            self.label_vent_start_2 = QtWidgets.QLabel(self)
            self.label_vent_start_2.setText(self.label_vent_start.text())
            self.label_vent_start_2.setGeometry(
                QtCore.QRect(45, 410 + 30 * self.count_vent, 78, 20)
            )
            self.label_vent_start_2.setObjectName("label_vent_start_2")
            self.label_vent_start_2.show()
            self.list_vent.append(self.label_vent_start_2)

            self.spinBox_vent_start_2 = QtWidgets.QSpinBox(self)
            self.spinBox_vent_start_2.setSuffix(self.spinBox_vent_start.suffix())
            self.spinBox_vent_start_2.setGeometry(
                QtCore.QRect(130, 410 + 30 * self.count_vent, 60, 20)
            )
            self.spinBox_vent_start_2.setObjectName("spinBox_vent_start_2")
            self.spinBox_vent_start_2.show()
            self.list_vent.append(self.spinBox_vent_start_2)

            self.spinBox_vent_power_2 = QtWidgets.QSpinBox(self)
            self.spinBox_vent_power_2.setGeometry(
                QtCore.QRect(200, 410 + 30 * self.count_vent, 40, 20)
            )
            self.spinBox_vent_power_2.setMaximum(255)
            self.spinBox_vent_power_2.setValue(255)
            self.spinBox_vent_power_2.setWrapping(True)
            self.spinBox_vent_power_2.setObjectName("spinBox_vent_power_2")
            self.spinBox_vent_power_2.show()
            self.list_vent.append(self.spinBox_vent_power_2)

            self.spinBox_vent_stop_2 = QtWidgets.QSpinBox(self)
            self.spinBox_vent_stop_2.setSuffix(self.spinBox_vent_stop.suffix())
            self.spinBox_vent_stop_2.setGeometry(
                QtCore.QRect(320, 410 + 30 * self.count_vent, 60, 20)
            )
            self.spinBox_vent_stop_2.setObjectName("spinBox_vent_stop_2")
            self.spinBox_vent_stop_2.show()
            self.list_vent.append(self.spinBox_vent_stop_2)

            self.label_vent_stop_2 = QtWidgets.QLabel(self)
            self.label_vent_stop_2.setText(self.label_vent_stop.text())
            self.label_vent_stop_2.setGeometry(
                QtCore.QRect(260, 410 + 30 * self.count_vent, 55, 20)
            )
            self.label_vent_stop_2.setObjectName("label_vent_stop_2")
            self.label_vent_stop_2.show()
            self.list_vent.append(self.label_vent_stop_2)

        elif self.count_vent == 2:
            self.label_vent_start_3 = QtWidgets.QLabel(self)
            self.label_vent_start_3.setText(self.label_vent_start.text())
            self.label_vent_start_3.setGeometry(
                QtCore.QRect(45, 410 + 30 * self.count_vent, 78, 20)
            )
            self.label_vent_start_3.setObjectName("label_vent_start_3")
            self.label_vent_start_3.show()
            self.list_vent.append(self.label_vent_start_3)

            self.spinBox_vent_start_3 = QtWidgets.QSpinBox(self)
            self.spinBox_vent_start_3.setSuffix(self.spinBox_vent_start.suffix())
            self.spinBox_vent_start_3.setGeometry(
                QtCore.QRect(130, 410 + 30 * self.count_vent, 60, 20)
            )
            self.spinBox_vent_start_3.setObjectName("spinBox_vent_start_3")
            self.spinBox_vent_start_3.show()
            self.list_vent.append(self.spinBox_vent_start_3)

            self.spinBox_vent_power_3 = QtWidgets.QSpinBox(self)
            self.spinBox_vent_power_3.setGeometry(
                QtCore.QRect(200, 410 + 30 * self.count_vent, 40, 20)
            )
            self.spinBox_vent_power_3.setMaximum(255)
            self.spinBox_vent_power_3.setValue(255)
            self.spinBox_vent_power_3.setWrapping(True)
            self.spinBox_vent_power_3.setObjectName("spinBox_vent_power_3")
            self.spinBox_vent_power_3.show()
            self.list_vent.append(self.spinBox_vent_power_3)

            self.spinBox_vent_stop_3 = QtWidgets.QSpinBox(self)
            self.spinBox_vent_stop_3.setSuffix(self.spinBox_vent_stop.suffix())
            self.spinBox_vent_stop_3.setGeometry(
                QtCore.QRect(320, 410 + 30 * self.count_vent, 60, 20)
            )
            self.spinBox_vent_stop_3.setObjectName("spinBox_vent_stop_3")
            self.spinBox_vent_stop_3.show()
            self.list_vent.append(self.spinBox_vent_stop_3)

            self.label_vent_stop_3 = QtWidgets.QLabel(self)
            self.label_vent_stop_3.setText(self.label_vent_stop.text())
            self.label_vent_stop_3.setGeometry(
                QtCore.QRect(260, 410 + 30 * self.count_vent, 55, 20)
            )
            self.label_vent_stop_3.setObjectName("label_vent_stop_3")
            self.label_vent_stop_3.show()
            self.list_vent.append(self.label_vent_stop_3)

            self.label_copyright.setGeometry(
                QtCore.QRect(30, 450 + 30 * self.count_vent, 300, 80)
            )
            self.resize(600, 520 + 30 * self.count_vent)
            self.show()

        elif self.count_vent == 3:
            self.label_vent_start_4 = QtWidgets.QLabel(self)
            self.label_vent_start_4.setText(self.label_vent_start.text())
            self.label_vent_start_4.setGeometry(
                QtCore.QRect(45, 410 + 30 * self.count_vent, 78, 20)
            )
            self.label_vent_start_4.setObjectName("label_vent_start_4")
            self.label_vent_start_4.show()
            self.list_vent.append(self.label_vent_start_4)

            self.spinBox_vent_start_4 = QtWidgets.QSpinBox(self)
            self.spinBox_vent_start_4.setSuffix(self.spinBox_vent_start.suffix())
            self.spinBox_vent_start_4.setGeometry(
                QtCore.QRect(130, 410 + 30 * self.count_vent, 60, 20)
            )
            self.spinBox_vent_start_4.setObjectName("spinBox_vent_start_4")
            self.spinBox_vent_start_4.show()
            self.list_vent.append(self.spinBox_vent_start_4)

            self.spinBox_vent_power_4 = QtWidgets.QSpinBox(self)
            self.spinBox_vent_power_4.setGeometry(
                QtCore.QRect(200, 410 + 30 * self.count_vent, 40, 20)
            )
            self.spinBox_vent_power_4.setMaximum(255)
            self.spinBox_vent_power_4.setValue(255)
            self.spinBox_vent_power_4.setWrapping(True)
            self.spinBox_vent_power_4.setObjectName("spinBox_vent_power_4")
            self.spinBox_vent_power_4.show()
            self.list_vent.append(self.spinBox_vent_power_4)

            self.spinBox_vent_stop_4 = QtWidgets.QSpinBox(self)
            self.spinBox_vent_stop_4.setSuffix(self.spinBox_vent_stop.suffix())
            self.spinBox_vent_stop_4.setGeometry(
                QtCore.QRect(320, 410 + 30 * self.count_vent, 60, 20)
            )
            self.spinBox_vent_stop_4.setObjectName("spinBox_vent_stop_4")
            self.spinBox_vent_stop_4.show()
            self.list_vent.append(self.spinBox_vent_stop_4)

            self.label_vent_stop_4 = QtWidgets.QLabel(self)
            self.label_vent_stop_4.setText(self.label_vent_stop.text())
            self.label_vent_stop_4.setGeometry(
                QtCore.QRect(260, 410 + 30 * self.count_vent, 55, 20)
            )
            self.label_vent_stop_4.setObjectName("label_vent_stop_4")
            self.label_vent_stop_4.show()
            self.list_vent.append(self.label_vent_stop_4)

        else:
            self.pushButton_add_vent.setDisabled(True)
            if self.translate_button.text() == "EN":
                QtWidgets.QMessageBox.information(
                    self, "No more vents", "You can't add more vents"
                )
            else:
                QtWidgets.QMessageBox.information(
                    self, "Обдув", "Неможливо додати білше обдувів"
                )
        self.count_vent += 1

    def set_values_LA(self):
        """Set values from config.json file"""

        self.gcode_file = sys.argv[1]
        # if not linear_advance_add.check_LA_in_gcode(self.gcode_file)

        self.checkBox_LA.setChecked(self.load_parameter(self.checkBox_LA.objectName()))
        self.doubleSpinBox_line_width.setValue(
            extrusion_width_hight.line_width(self.gcode_file)
        )
        self.doubleSpinBox_layer_height.setValue(
            extrusion_width_hight.layer_higth(self.gcode_file)
        )
        self.doubleSpinBox_material_diameter.setValue(1.75)
        self.doubleSpinBox_material_linear_advance_factor.setValue(
            self.load_parameter("doubleSpinBox_material_linear_advance_factor")
        )

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

    def save_config(self):

        data = {
            "checkBox_LA": self.checkBox_LA.isChecked(),
            "checkBox_Arc": self.checkBox_Arc.isChecked(),
            "checkBox_look": self.checkBox_look.isChecked(),
            "checkBox_vent": self.checkBox_vent.isChecked(),
            "radioButton_ArcStraightener": self.radioButton_ArcStraightener.isChecked(),
            "radioButton_ArcWeider": self.radioButton_ArcWeider.isChecked(),
            "doubleSpinBox_material_linear_advance_factor": self.doubleSpinBox_material_linear_advance_factor.value(),
            "spinBox_X": self.spinBox_X.value(),
            "spinBox_Y": self.spinBox_Y.value(),
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

    def retranslate(self):
        """Retranslate the widgets"""
        _translate = QtCore.QCoreApplication.translate
        if self.translate_button.text() == "EN":
            self.setWindowTitle(_translate("MainDialog", "Post Processing"))
            # LA block
            self.label_checkBox_LA.setText(_translate("MainDialog", "Linear Advance"))
            self.label_line_width.setText(_translate("MainDialog", "Line width"))
            self.label_line_width.setAlignment(QtCore.Qt.AlignCenter)
            self.label_layer_height.setText(_translate("MainDialog", "Layer height"))
            self.label_material_diameter.setText(
                _translate("MainDialog", "Material diameter")
            )
            self.label_material_linear_advance_factor.setText(
                _translate("MainDialog", "Material linear advance factor :")
            )
            self.doubleSpinBox_line_width.setSuffix(_translate("MainDialog", "mm"))
            self.doubleSpinBox_layer_height.setSuffix(_translate("MainDialog", "mm"))
            self.doubleSpinBox_material_diameter.setSuffix(
                _translate("MainDialog", "mm")
            )
            #  Arc block.
            self.label_checkBox_Arc.setText(
                _translate(
                    "MainWindow",
                    " Making circles from segments. "
                    "Converting g1 to g2/g3 commands.",
                )
            )
            # Look block.
            self.label_checkBox_look.setText(
                _translate(
                    "MainWindow",
                    "Pause in printing to looking at the model and move to X",
                )
            )
            self.label_Y.setText(_translate("MainWindow", "and Y"))
            self.label_look.setText(_translate("MainWindow", "Look at"))
            self.spinBox_layer.setSuffix(_translate("MainDialog", " layer"))
            self.pushButton_add_new_look.setText(
                _translate("MainWindow", "Add next stop")
            )
            self.pushButton_add_new_look.adjustSize()
            # Vent block
            self.label_checkBox_vent.setText(
                _translate("MainWindow", "Add lines to make a vent")
            )
            self.label_vent_start.setText(_translate("MainWindow", "Vent start"))
            self.label_vent_start.setAlignment(QtCore.Qt.AlignRight)
            self.spinBox_vent_start.setSuffix(_translate("MainDialog", " layer"))
            self.label_vent_power.setText(_translate("MainWindow", "Power:"))
            self.label_vent_stop.setText(_translate("MainWindow", "vent stop"))
            self.spinBox_vent_stop.setSuffix(_translate("MainDialog", " layer"))
            self.pushButton_add_vent.setText(_translate("MainWindow", "Add"))

        else:
            self.setWindowTitle(_translate("MainDialog", "Пост Обробка"))
            # LA block
            self.label_checkBox_LA.setText(_translate("MainDialog", "Linear Advance"))
            self.label_line_width.setText(_translate("MainDialog", "Товщина лінії"))
            self.label_line_width.adjustSize()
            self.label_layer_height.setText(_translate("MainDialog", "Висота шару"))
            self.label_material_diameter.setText(
                _translate("MainDialog", "Діаметр матеріалу")
            )
            self.label_material_linear_advance_factor.setText(
                _translate("MainDialog", "Коефіцієнт Linear Advance:")
            )
            self.doubleSpinBox_line_width.setSuffix(_translate("MainDialog", "мм"))
            self.doubleSpinBox_layer_height.setSuffix(_translate("MainDialog", "мм"))
            self.doubleSpinBox_material_diameter.setSuffix(
                _translate("MainDialog", "мм")
            )
            # Converting g1 to g2/g3 commands.
            self.label_checkBox_Arc.setText(
                _translate(
                    "MainWindow",
                    "Створення кола з сегментів." "Перетворення з g1 на g2/g3 команди.",
                )
            )
            # Look block
            self.label_checkBox_look.setText(
                _translate(
                    "MainWindow", "Пауза для огляду моделі, каретка перемістится по X"
                )
            )
            self.label_checkBox_look.setAlignment(QtCore.Qt.AlignRight)
            self.label_Y.setText(_translate("MainWindow", "та Y"))
            self.label_Y.setAlignment(QtCore.Qt.AlignCenter)
            self.label_look.setText(_translate("MainWindow", "Глянути на"))
            self.label_look.setAlignment(QtCore.Qt.AlignRight)
            self.spinBox_layer.setSuffix(_translate("MainDialog", " шар"))
            self.pushButton_add_new_look.setText(
                _translate("MainWindow", "Додати наступну зупинку")
            )
            self.pushButton_add_new_look.adjustSize()
            # Vent block
            self.label_checkBox_vent.setText(
                _translate("MainWindow", "Додати вентиляцію на шарах.")
            )
            self.label_vent_start.setText(_translate("MainWindow", "Починаючи з"))

            self.spinBox_vent_start.setSuffix(_translate("MainDialog", " шару"))
            self.label_vent_power.setText(_translate("MainWindow", "Потужність:"))
            self.label_vent_power.adjustSize()
            # self.label_vent_power.setAlignment(QtCore.Qt.AlignCenter)
            self.label_vent_stop.setText(_translate("MainWindow", "Зупинись"))
            self.spinBox_vent_stop.setSuffix(_translate("MainDialog", " шарі"))
            self.pushButton_add_vent.setText(_translate("MainWindow", "Додати"))


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
        gcode_file = sys.argv[1]
        dialog = MainDialog()
    else:
        print(
            "File not specifed. Use PostProcessing-Script-for-PrusaSlicer.py <gcode file>."
        )
        alert = NoFile()

    sys.exit(app.exec_())
