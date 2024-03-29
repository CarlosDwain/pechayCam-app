# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'predict_dialog_reco.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_predict_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(421, 243)
        Dialog.setStyleSheet("QDialog{\n"
"    background-color: #1b1b27;\n"
"}\n"
"#pred_label{\n"
"    color: rgb(255, 170, 0);\n"
"}\n"
"#pred_edit,#severity_edit{\n"
"    background-color: transparent;\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"#reco_edit{\n"
"    background-color: transparent;\n"
"    color: rgb(181, 226, 176);\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pred_label = QtWidgets.QLabel(Dialog)
        self.pred_label.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pred_label.setFont(font)
        self.pred_label.setAlignment(QtCore.Qt.AlignCenter)
        self.pred_label.setObjectName("pred_label")
        self.verticalLayout.addWidget(self.pred_label)
        self.pred_edit = QtWidgets.QLineEdit(Dialog)
        self.pred_edit.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.pred_edit.setFont(font)
        self.pred_edit.setFrame(False)
        self.pred_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.pred_edit.setObjectName("pred_edit")
        self.verticalLayout.addWidget(self.pred_edit)
        self.severity_edit = QtWidgets.QLineEdit(Dialog)
        self.severity_edit.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.severity_edit.setFont(font)
        self.severity_edit.setFrame(False)
        self.severity_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.severity_edit.setObjectName("severity_edit")
        self.verticalLayout.addWidget(self.severity_edit)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setMinimumSize(QtCore.QSize(10, 0))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setLineWidth(0)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout.addWidget(self.frame_2)
        self.reco_edit = QtWidgets.QTextEdit(self.frame)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.reco_edit.setFont(font)
        self.reco_edit.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.reco_edit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.reco_edit.setLineWidth(1)
        self.reco_edit.setCursorWidth(1)
        self.reco_edit.setObjectName("reco_edit")
        self.horizontalLayout.addWidget(self.reco_edit)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setMinimumSize(QtCore.QSize(10, 0))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_3.setLineWidth(0)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout.addWidget(self.frame_3)
        self.verticalLayout.addWidget(self.frame)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pred_label.setText(_translate("Dialog", "Predicted Health Status:"))
        self.pred_edit.setPlaceholderText(_translate("Dialog", "Disease Result"))
        self.severity_edit.setPlaceholderText(_translate("Dialog", "Severity Result"))
        self.reco_edit.setPlaceholderText(_translate("Dialog", "Recommendation"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
