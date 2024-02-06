# The PechayCam App
<p align="center">
  <img src="icons/PechayCam App Logo.png" alt="Logo" width="200">
</p>

## Overview

This repository contains the source code for a client-server application that leverages a trained model to classify plant diseases and estimate their severity in hydroponically grown Pechay.

<p align="center">
  <img src="icons/PechayCam App Logo.png" alt="Logo" width="200">
</p>

### Project Structure
### Client Directory Details

| File                  | Description                                                                                                             |
|-----------------------|-------------------------------------------------------------------------------------------------------------------------|
| main.py               |  Contains the `MainWindow` class responsible for the backend functionality of the GUI.                                   |
| mainwindow_pyqt5.py   | Handles the user interface of the main window, including buttons, dropdown menus, and the image feed.                   |
| predict_dialog_reco.py| Manages the UI for displaying prediction results and feedback in a dialog box when the predict button is clicked.       |
| predict_pechay.py     | Facilitates communication with the server for sending image data and extracting prediction results using JSON format.   |
| report_dialog_pyqt5.py| Displays a dialog box with plant information such as ID, date, time, and health status upon clicking the report button. |
| logo_rc.py            | Contains images converted into Python code for easy import into other scripts, such as displaying logos or icons.       |
| database.db           | A database file created to store the plant ID, date, time and prediction result.                                        |

### Server Directory Details

| File                   | Description                                                                                                              |
|------------------------|--------------------------------------------------------------------------------------------------------------------------|
| pechayCam_server.py    | Hosts the Multioutput CNN model and handles the incoming post request from the client. Outputs the plant disease and severity estimation then sends the result back to the client. |
| inceptionV3_arch.h5    | Stores the architecture of the trained CNN model used for disease classification and severity estimation. The pre-trained model used here is the inceptionV3. |
| inceptionV3_weights.h5 | Stores the weights of the trained CNN model used for disease classification and severity estimation. |
