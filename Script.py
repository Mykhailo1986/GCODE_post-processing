import sys
import json

import linear_advance_add
from fan_layers_control import fan_on_off
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
    QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy,
)


class MainDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(600, 520)
        self.setWindowTitle(f"Post Processing: {sys.argv[1]}" )
        self.vertical_layout_main_window_1 = QVBoxLayout(self)

        self.LA_layout=LA_widgets(self)
        self.LA_layout.setFixedSize(450,100)
        self.vertical_layout_main_window_1.addWidget(self.LA_layout)
        self.line_1 = QtWidgets.QFrame(self)
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1.setObjectName("line_1")
        self.vertical_layout_main_window_1.addWidget(self.line_1)

        self.Arc_layout = Arc_widgets(self)
        self.vertical_layout_main_window_1.addWidget(self.Arc_layout)


        self.translate_button = QtWidgets.QPushButton("EN", self)
        # self.translate_button.setFixedSize(50, 50)
        self.translate_button.setGeometry(QtCore.QRect(540, 10, 50, 50))
        self.translate_button.setObjectName("translate_button")






        self.retranslate()
        self.show()

    def retranslate(self):
        """Retranslate the widgets"""
        _translate = QtCore.QCoreApplication.translate
        if self.translate_button.text() == "EN":
            self.setWindowTitle(_translate("MainDialog", f"Post Processing{sys.argv[1]}"))
            # LA block
            self.LA_layout.label_checkBox_LA.setText(_translate("MainDialog", "Linear Advance"))
            self.LA_layout.label_line_width.setText(_translate("MainDialog", "Line width"))
            # self.LA_layout.label_line_width.setAlignment(QtCore.Qt.AlignCenter)
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
            self.Arc_layout.label_checkBox_Arc.setText(
                _translate(
                    "MainWindow",
                    " Making circles from segments. "
                    "Converting g1 to g2/g3 commands.",
                )
            )
            # # Look block.
            # self.label_checkBox_look.setText(
            #     _translate(
            #         "MainWindow",
            #         "Pause in printing to looking at the model and move to X",
            #     )
            # )
            # self.label_Y.setText(_translate("MainWindow", "and Y"))
            # self.label_look.setText(_translate("MainWindow", "Look at"))
            # self.spinBox_layer.setSuffix(_translate("MainDialog", " layer"))
            # self.pushButton_add_new_look.setText(
            #     _translate("MainWindow", "Add next stop")
            # )
            # self.pushButton_add_new_look.adjustSize()
            # # Vent block
            # self.label_checkBox_vent.setText(
            #     _translate("MainWindow", "Add lines to make a vent")
            # )
            # self.label_vent_start.setText(_translate("MainWindow", "Vent start"))
            # self.label_vent_start.setAlignment(QtCore.Qt.AlignRight)
            # self.spinBox_vent_start.setSuffix(_translate("MainDialog", " layer"))
            # self.label_vent_power.setText(_translate("MainWindow", "Power:"))
            # self.label_vent_stop.setText(_translate("MainWindow", "vent stop"))
            # self.spinBox_vent_stop.setSuffix(_translate("MainDialog", " layer"))
            # self.pushButton_add_vent.setText(_translate("MainWindow", "Add"))
            #
            # else:
            #     self.setWindowTitle(_translate("MainDialog", "Пост Обробка"))
            #     # LA block
            #     self.LA_layout.label_checkBox_LA.setText(_translate("MainDialog", "Linear Advance"))
            #     self.LA_layout.label_line_width.setText(_translate("MainDialog", "Товщина лінії"))
            #     self.LA_layout.label_line_width.adjustSize()
            #     self.LA_layout.label_layer_height.setText(_translate("MainDialog", "Висота шару"))
            #     self.LA_layout.label_material_diameter.setText(
            #         _translate("MainDialog", "Діаметр матеріалу")
            #     )
            #     self.LA_layout.label_material_linear_advance_factor.setText(
            #         _translate("MainDialog", "Коефіцієнт Linear Advance:")
            #     )
            #     self.LA_layout.doubleSpinBox_line_width.setSuffix(_translate("MainDialog", "мм"))
            #     self.LA_layout.doubleSpinBox_layer_height.setSuffix(_translate("MainDialog", "мм"))
            #     self.LA_layout.doubleSpinBox_material_diameter.setSuffix(
            #         _translate("MainDialog", "мм")
            #     )
            #     # Converting g1 to g2/g3 commands.
            #     self.label_checkBox_Arc.setText(
            #         _translate(
            #             "MainWindow",
            #             "Створення кола з сегментів." "Перетворення з g1 на g2/g3 команди.",
            #         )
            #     )
            #     # Look block
            #     self.label_checkBox_look.setText(
            #         _translate(
            #             "MainWindow", "Пауза для огляду моделі, каретка перемістится по X"
            #         )
            #     )
            #     self.label_checkBox_look.setAlignment(QtCore.Qt.AlignRight)
            #     self.label_Y.setText(_translate("MainWindow", "та Y"))
            #     self.label_Y.setAlignment(QtCore.Qt.AlignCenter)
            #     self.label_look.setText(_translate("MainWindow", "Глянути на"))
            #     self.label_look.setAlignment(QtCore.Qt.AlignRight)
            #     self.spinBox_layer.setSuffix(_translate("MainDialog", " шар"))
            #     self.pushButton_add_new_look.setText(
            #         _translate("MainWindow", "Додати наступну зупинку")
            #     )
            #     self.pushButton_add_new_look.adjustSize()
            #     # Vent block
            #     self.label_checkBox_vent.setText(
            #         _translate("MainWindow", "Додати вентиляцію на шарах.")
            #     )
            #     self.label_vent_start.setText(_translate("MainWindow", "Починаючи з"))
            #
            #     self.spinBox_vent_start.setSuffix(_translate("MainDialog", " шару"))
            #     self.label_vent_power.setText(_translate("MainWindow", "Потужність:"))
            #     self.label_vent_power.adjustSize()
            #     # self.label_vent_power.setAlignment(QtCore.Qt.AlignCenter)
            #     self.label_vent_stop.setText(_translate("MainWindow", "Зупинись"))
            #     self.spinBox_vent_stop.setSuffix(_translate("MainDialog", " шарі"))
            #     self.pushButton_add_vent.setText(_translate("MainWindow", "Додати"))

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

    def some_parent_module(self):
        print("This is a function in the parent widget.")

class LA_widgets(ParentWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.horizontal_layout_LA_1=QHBoxLayout(self)

        self.checkBox_LA = QtWidgets.QCheckBox(self)
        self.checkBox_LA.setObjectName("checkBox_LA")
        self.checkBox_LA.setChecked(False)
        self.checkBox_LA.clicked.connect(self.checkBox_toggled())

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
        self.label_line_width.setAlignment(QtCore.Qt.AlignCenter)
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
        self.label_layer_height.setAlignment(QtCore.Qt.AlignCenter)
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

        #
        # if self.load_parameter("checkBox_LA"):
        #     for widget in self.list_LA:
        #         widget.setEnabled(True)
        # else:
        #     for widget in self.list_LA:
        #         widget.setDisabled(True)
        #
        # self.set_values_LA()
        # self.vertical_layout_LA_8=QVBoxLayout(self)
        # self.line_1 = QtWidgets.QFrame(self)
        # # self.line_1.setGeometry(QtCore.QRect(20, 90, 471, 16))
        # self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        # self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        # self.line_1.setObjectName("line_1")
        # self.vertical_layout_LA_8.addLayout(self.horizontal_layout_LA_1)
        # self.vertical_layout_LA_8.addWidget(self.line_1)




class Arc_widgets(ParentWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vertical_layout_Arc_1=QVBoxLayout(self)

        self.Horizontal_layout_Arc_2 = QHBoxLayout(self)

# Second block for converting g1 to g2/g3 commands.

        self.checkBox_Arc = QtWidgets.QCheckBox(self)
        self.checkBox_Arc.setGeometry(QtCore.QRect(30, 110, 411, 20))
        self.checkBox_Arc.setObjectName("checkBox_Arc")
        # self.checkBox_Arc.setChecked(self.load_parameter("checkBox_Arc"))
        # self.checkBox_Arc.clicked.connect(self.checkBox_Arc_toggled)

        self.label_checkBox_Arc = QtWidgets.QLabel(self)
        self.label_checkBox_Arc.setGeometry(QtCore.QRect(55, 110, 411, 20))
        self.label_checkBox_Arc.setObjectName("label_checkBox_Arc")

        self.arc_group = QButtonGroup()
        self.radioButton_ArcWeider = QRadioButton(self)
        self.radioButton_ArcWeider.setGeometry(QtCore.QRect(80, 140, 411, 20))
        self.radioButton_ArcWeider.setObjectName("radioButton_ArcWeider")
        # self.radioButton_ArcWeider.setChecked(
        #     self.load_parameter("radioButton_ArcWeider")
        # )
        self.arc_group.addButton(self.radioButton_ArcWeider)

        self.label_ArcWeider = QtWidgets.QLabel(self)
        self.label_ArcWeider.setGeometry(QtCore.QRect(100, 140, 411, 20))
        self.label_ArcWeider.setObjectName("label_ArcWeider")
        self.label_ArcWeider.setText("ArcWeider")

        self.radioButton_ArcStraightener = QRadioButton(self)
        self.radioButton_ArcStraightener.setGeometry(QtCore.QRect(300, 140, 411, 20))
        self.radioButton_ArcStraightener.setObjectName("radioButton_ArcStraightener")
        # self.radioButton_ArcStraightener.setChecked(
        #     self.load_parameter("radioButton_ArcStraightener")
        # )
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

        # self.checkBox_Arc_toggled(self.checkBox_Arc.isChecked())











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
    gcode_file = "Cyl.gcode"
    dialog = MainDialog()

    # if len(sys.argv) > 1:
    #     gcode_file = sys.argv[1]
    #     dialog = MainDialog()
    # else:
    #     print(
    #         "File not specifed. Use PostProcessing-Script-for-PrusaSlicer.py <gcode file>."
    #     )
    #     alert = NoFile()

    sys.exit(app.exec_())
