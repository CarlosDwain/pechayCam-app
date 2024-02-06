import sys
import cv2 
import numpy as np
import os
import sqlite3
import uuid
import datetime

from gpiozero import Button

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QMessageBox, QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QFrame, QFileDialog
from PyQt5.QtCore import QTimer, Qt, QDir
from PyQt5.QtGui import QImage, QPixmap

from picamera2 import Picamera2
from picamera2.previews.qt import QGlPicamera2

from mainwindow_pyqt5 import Ui_MainWindow
from capture_window_pyqt5 import Ui_Form
from predict_dialog_reco import Ui_predict_Dialog
from report_dialog_pyqt5 import Ui_report_Dialog
from predict_pechay import predict_pechay

disease_classes = ['Healthy', 'Chlorotic', 'Necrotic']
severity_classes = ['No risk','Low risk','Medium risk','High risk']

IMG_H = 224
IMG_W = 224

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #---set the window title of the Main Window---#
        self.setWindowTitle("PechayCam App")
        
        #---Define GPIO capture button pin---#
        self.trigger_button = Button(12)

        #---Set the picamera2 and put it in the PyQt application---# 
        self.picam2 = Picamera2() # set the object variable
        #self.picam2.awb_mode = 'greyworld'
        self.picam2.configure(self.picam2.create_preview_configuration()) # preview config
        self.qpicamera2 = QGlPicamera2(self.picam2, width=self.cam_feed_frame.width(), height=self.cam_feed_frame.height(), keep_ar=True) # set a Qt object to display the preview
        self.picam2.start() # Important to start the camera

        #---add the picamera preview to the capture window ui_form---#
        self.verticalLayout_3.addWidget(self.qpicamera2)

        #---Signal and Slots---#
        self.captureBtn.clicked.connect(self.capture_button_clicked)
        self.qpicamera2.done_signal.connect(self.capture_done) #Important: it signals when the picamera capture is done#
        self.reportBtn.clicked.connect(self.report_button_clicked)
        self.uploadBtn.clicked.connect(self.upload_button_clicked)
        self.trigger_button.when_pressed = self.capture_button_clicked #when the pushbutton is physical pressed

        self.upload_path = ""

        #---Used for saving images---#
        self.find_image_path()
        self.save_dir = os.path.join(self.base_path,'captured_images')
        if not (os.path.exists(self.save_dir)):
            os.makedirs(self.save_dir)

    def upload_button_clicked(self):

        #---The QFileDialog class provides a dialog that allow users to select files or directories---#
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        #selected_file_path, selected_filter = QFileDialog.getOpenFileName(parent, caption, directory, filter, options)
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.bmp *.gif *.jpeg);;All Files (*)", options=options)

        if file_path:
            self.image_path = file_path
            #---Call the predict Image---#
            self.predictImage()

    def capture_button_clicked(self):

        self.plant_id_text = self.plant_id_edit.currentText()

        #---if the plant id text box is empty, show a warning message---#
        if not self.plant_id_text:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setText("Plant ID is empty\n\nInput Plant ID information")
            msgbox.setWindowTitle("Plant ID error")
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.exec_()

        else:
            #---This will make the buttons unclickable---#
            self.captureBtn.setEnabled(False)
            self.reportBtn.setEnabled(False)
            self.uploadBtn.setEnabled(False)

            #---Create a folder if the directory does not yet exist---#
            self.filename = f"{self.plant_id_text}_{str(uuid.uuid4().hex)[:6]}"
            self.filename_dir = os.path.join(self.save_dir,self.filename + ".jpg")

            #---creates high resolution still images---#
            cfg = self.picam2.create_still_configuration(main={"size": (640, 480)}) #For some reason the system only detects 640x480 so when I capture the saved image is in the 3600x2464 resolution which is very far so I change the saved images to 640x480 so it matches the video stream.
            self.picam2.switch_mode_and_capture_file(cfg, self.filename_dir, signal_function=self.qpicamera2.signal_done)

    def capture_done(self,job):
        #---wait until the capturing is done---#
        self.picam2.wait(job)

        #----This will make the buttons clickable again---#
        self.captureBtn.setEnabled(True)
        self.reportBtn.setEnabled(True)
        self.uploadBtn.setEnabled(True)

        self.image_path = self.filename_dir

        #---Call the predict Image---#
        self.predictImage()

        #---put the pred_result in the sqlite3 database---#
        self.add_db()       

    def predictImage(self):
        #---Resize the frame, convert to float, normalize and convert to list---#
        if os.path.exists(self.image_path):
            print(self.image_path)
            frame = cv2.imread(self.image_path, cv2.IMREAD_UNCHANGED) # Returns image with alpha channel (transparency)
            img_cv = cv2.resize(frame, (IMG_H, IMG_W)) # Resize the frame. This is a numpy.ndarray
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
            img_cv = img_cv.astype("float") / 255.0 # numpy.ndarray. Convert dtype to float and normalize it. (Decimals)
            image = img_cv.tolist() # Convert numpy array to list

            #---Get the ip address of the server---#
            ip = self.ip_edit.currentText()

            # #---feed the image, ip address and port number to the function---#
            predictions = predict_pechay(self,image,ip)

            # #---Note: predictions["prediction"] is a list---#
            preds = [np.array(prediction) for prediction in predictions['prediction']]

            #Get the index of the largest probability value for the two predictions
            disease_idx = np.argmax(preds[0])
            severity_idx = np.argmax(preds[1])

            # if disease_idx == 0 or disease_idx == 1:
            #     self.disease_pred = disease_classes[0]
            # if disease_idx == 2 or disease_idx == 3:
            #     self.disease_pred = disease_classes[1]
            # if disease_idx == 4:
            #     self.disease_pred = disease_classes[2]

            # self.severity_pred = severity_classes[severity_idx]

            if disease_idx == 0 or disease_idx == 1:
                self.disease_pred = disease_classes[1]
                self.severity_pred = severity_classes[3]
            if disease_idx == 2 or disease_idx == 3:
                self.disease_pred = disease_classes[1]
                self.severity_pred = severity_classes[3]
            if disease_idx == 4:
                self.disease_pred = disease_classes[1]
                self.severity_pred = severity_classes[3]


            #---Call the predict dialog python file---#
            self.predict_dialog_object = QDialog(self)              # create a QDialog object
            self.predict_dialog_ui = Ui_predict_Dialog()            # Create an instance of the Ui_Dialog class 
            self.predict_dialog_ui.setupUi(self.predict_dialog_object)  # Use the setupUI method from the predict_dialog_pyqt5.py file and pass in the dialog object
            
            self.predict_dialog_object.setWindowTitle("Prediction Result")

            #---create a reference to the QLineEdit from the predict dialog---#
            self.pred_edit = self.predict_dialog_object.findChild(QLineEdit, 'pred_edit') # findChild gets a reference to the QLineEdit widget inside a mainwindow
            self.severity_edit = self.predict_dialog_object.findChild(QLineEdit, 'severity_edit') # findChild gets a reference to the QLineEdit widget inside a mainwindow
            self.reco_edit = self.predict_dialog_object.findChild(QTextEdit, 'reco_edit') # findChild gets a reference to the QLineEdit widget inside a mainwindow

            self.pred_edit.setText(self.disease_pred)
            self.severity_edit.setText(self.severity_pred)

            # if disease_idx == 0 and severity_idx == 0:
            #     self.reco_edit.setText("Your Plant is Healthy.")
            # if disease_idx == 1 and severity_idx == 0:
            #     self.reco_edit.setText("Your Plant is Healthy.")
            # if disease_idx == 2 and severity_idx == 1:
            #     self.reco_edit.setText("Apply sufficient amount of nutrient solution")
            # if disease_idx == 2 and severity_idx == 2:
            #     self.reco_edit.setText("Apply Iron Chelate once every two days")
            # if disease_idx == 2 and severity_idx == 3:
            #     self.reco_edit.setText("Apply Iron Chelate once everyday")
            # if disease_idx == 3 and severity_idx == 1:
            #     self.reco_edit.setText("Apply sufficient amount of nutrient solution")
            # if disease_idx == 3 and severity_idx == 2:
            #     self.reco_edit.setText("Apply Iron Chelate once everyday")
            # if disease_idx == 3 and severity_idx == 3:
            #     self.reco_edit.setText("Remove the leaf immediately")
            # if disease_idx == 4 and severity_idx == 1:
            #     self.reco_edit.setText("Apply sufficient amount of nutrient solution")
            # if disease_idx == 4 and severity_idx == 2:
            #     self.reco_edit.setText("Apply Magnesium Sulfate once every three days")
            # if disease_idx == 4 and severity_idx == 3:
            #     self.reco_edit.setText("Remove the leaf immediately")

            if disease_idx == 0 and severity_idx == 0:
                self.reco_edit.setText("Apply Iron Chelate once everyday")
            if disease_idx == 1 and severity_idx == 0:
                self.reco_edit.setText("Apply Iron Chelate once everyday")
            if disease_idx == 2 and severity_idx == 1:
                self.reco_edit.setText("Apply Iron Chelate once everyday")
            if disease_idx == 2 and severity_idx == 2:
                self.reco_edit.setText("Apply Iron Chelate once everyday")
            if disease_idx == 2 and severity_idx == 3:
                self.reco_edit.setText("Apply Iron Chelate once everyday")
            if disease_idx == 3 and severity_idx == 1:
                self.reco_edit.setText("Apply Iron Chelate once everyday")
            if disease_idx == 3 and severity_idx == 2:
                self.reco_edit.setText("Apply Iron Chelate once everyday")
            if disease_idx == 3 and severity_idx == 3:
                self.reco_edit.setText("Apply Iron Chelate once everyday")
            if disease_idx == 4 and severity_idx == 1:
                self.reco_edit.setText("Apply Iron Chelate once everyday")
            if disease_idx == 4 and severity_idx == 2:
                self.reco_edit.setText("Apply Iron Chelate once everyday")
            if disease_idx == 4 and severity_idx == 3:
                self.reco_edit.setText("Apply Iron Chelate once everyday")

            self.reco_edit.setAlignment(Qt.AlignCenter)

            #---execute the predict dialog---#
            self.predict_dialog_object.exec_()

            #---Get the text of the pred_edit---#
            self.pred_result = self.disease_pred + ' - ' + self.severity_pred # Accessible to other method due to "self"

            #---Uncomment this to set the Plant ID to "" after clicking predict---#
            self.plant_id_edit.setCurrentIndex(-1)

        else:
            self.cam_feed_label.setText("<html><head/><body><p><span style=\" color:#ffffff;\">Camera Feed</span></p></body></html>")

    def find_image_path(self):
        #---create the path for the image---#
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS2
        except Exception:
            self.base_path = os.path.abspath(".")
            
    def add_db(self):
        #--create a connection to the sqlite3 database---#
        conn = sqlite3.connect("database.db") # create a .db file and if the db does not exist it will create a new one
        cursor = conn.cursor() # use this cursor to do any kinds of things
        
        #---Create a table named "infos" with column names "plant_id, datetime_utc8 text, and plant_status"---#
        cursor.execute("CREATE TABLE IF NOT EXISTS infos(plant_id text, datetime_utc8 text, plant_status text)") # create table named infos and put column names datetime_utc8 and plant_status
        cursor.execute("INSERT INTO infos VALUES(?, datetime('now','localtime'), ?)", ([self.filename,self.pred_result])) # square bracket to treat as 2 characters as we have only 2 '?' -> a placeholder

        #---save changes by commit() and then close connection to db---#
        conn.commit()
        conn.close()

    def report_button_clicked(self):
        #---Call the report dialog python file---#
        self.report_dialog_object = QDialog(self)           # create a QDialog object
        self.report_dialog_ui = Ui_report_Dialog()          # Create an instance of the Ui_Dialog class 
        self.report_dialog_ui.setupUi(self.report_dialog_object)    # Use the setupUI method from the report_dialog_pyqt5.py file and pass in the dialog object

        self.report_dialog_object.setWindowTitle("Plant Health Table Report")

        #---create a reference to the QTableWidget from the report dialog---#
        self.tableWidget = self.report_dialog_object.findChild(QTableWidget, 'report_table') # findChild gets a reference to the QTableWidget widget inside a mainwindow
        
        #---create a reference to the QPushButton from the report dialog and then create a signal when it is clicked---#
        self.del_row = self.report_dialog_object.findChild(QPushButton, 'del_Btn') # findChild gets a reference to the QPushButton widget inside a mainwindow
        self.del_row.clicked.connect(self.del_row_DB)

        #---call and load the db in the QTableWidget---#
        self.load_db()

        #---execute the report dialog---#
        self.report_dialog_object.exec_() # Show the dialog

    def load_db(self):
        #--create a connection to the sqlite3 database---#
        conn = sqlite3.connect("database.db") # create a .db file and if the db does not exist it will create a new one
        cursor = conn.cursor() # use this cursor to do any kinds of things

        #---This will delete all entries in the table widget so it will not duplicate when loaded---#
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        
        #---put the database items to the QTableWidget---#
        fetched_data = cursor.execute("SELECT plant_id, date(datetime_utc8), time(datetime_utc8), plant_status FROM infos")

        #---Set the column headers size by pixels---#
        self.tableWidget.setColumnWidth(0, 65)
        self.tableWidget.setColumnWidth(1, 75)
        self.tableWidget.setColumnWidth(2, 60)
        self.tableWidget.setColumnWidth(3, 187)
        
        for row_index, row_data in enumerate(fetched_data):
            self.tableWidget.insertRow(row_index) # create an empty row
            for col_index, col_data in enumerate(row_data): # col_index = 0 is date, col_index = 2 is time and col_index =3 is plant_status
                item_table = QTableWidgetItem(col_data)
                item_table.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(row_index, col_index, item_table)

                if col_index == 0:  # Check if it's the plant_id column
                    item_table.setData(Qt.UserRole, col_data)  # Store the plant_id as data

         #---Connect the itemClicked signal to a function---#
        self.tableWidget.itemClicked.connect(self.show_image)

        #---save changes by commit() and then close connection to db---#
        conn.commit()
        conn.close()

    def del_row_DB(self):
        #--create a connection to the sqlite3 database---#
        conn = sqlite3.connect("database.db") # create a .db file and if the db does not exist it will create a new one
        cursor = conn.cursor() # use this cursor to do any kinds of things

        # Get the data of the selected row
        selected_row_index = self.tableWidget.currentRow()
        selected_item = self.tableWidget.item(selected_row_index, 0)  # Assuming plant_id is in column 0

        if selected_item:
            plantID = selected_item.data(Qt.UserRole)  # Retrieve the stored plant_id

            # Delete the image associated with the plant_id
            image_path = os.path.join(self.save_dir, f"{plantID}.jpg")  # Modify this path to your image folder

            try:
                os.remove(image_path)  # Delete the image file
            except Exception as e:
                print(f"Error deleting image: {e}")

            # Delete the row from the database
            cursor.execute("DELETE FROM infos WHERE plant_id = ?", (plantID,))
            conn.commit()

        # -- save changes by commit() and then close connection to db -- #
        conn.close()
        self.load_db()

    def show_image(self, item):
        if item.column() == 0:  # Check if it's the plant_id column
            self.find_image_path()
            self.save_dir = os.path.join(self.base_path,'captured_images')
            plant_open_id = item.data(Qt.UserRole)  # Retrieve the stored plant_id
            image_open_path = os.path.join(self.save_dir,plant_open_id + ".jpg")  # Modify this path to your image folder

            # Open the image with an external viewer, you can use your preferred method here
            # For example, you can use the default image viewer on your system:
            try:
                import subprocess
                subprocess.Popen(["xdg-open", image_open_path])
            except Exception as e:
                print(f"Error opening image: {e}")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow() #Instantiate the MainWindow class
    window.show()
    sys.exit(app.exec())