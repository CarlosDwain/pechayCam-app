# The PechayCam App
<p align="center">
  <img src="icons/PechayCam App Logo.png" alt="Logo" width="300">
</p>

## Overview

This repository contains the source code for a client-server application that leverages a trained model to classify plant diseases and estimate their severity in hydroponically grown Pechay.

<p align="center">
  <img src="icons/Overall architecture 2.jpg" alt="Logo">
</p>

The overall architecture illustrated in the figure above shows the communication between the client and server. At the core of the architecture is the laptop server, which houses the deep learning model trained to output the Pechay plant disease and disease severity. Deploying the deep learning model as a REST API allows the Raspberry Pi to utilize it for inference. This architecture can also be used to make the model accessible for mobile or desktop applications, which is good for scalability.

### Project Structure
### Client Directory Details

| File                         | Description                                                                                                             |
|------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| client/main.py               |  Contains the `MainWindow` class responsible for the backend functionality of the GUI.                                  |
| client/mainwindow_pyqt5.py   | Handles the user interface of the main window, including buttons, dropdown menus, and the image feed.                   |
| client/predict_dialog_reco.py| Manages the UI for displaying prediction results and feedback in a dialog box when the predict button is clicked.       |
| client/predict_pechay.py     | Facilitates communication with the server for sending image data and extracting prediction results using JSON format.   |
| client/report_dialog_pyqt5.py| Displays a dialog box with plant information such as ID, date, time, and health status upon clicking the report button. |
| client/logo_rc.py            | Contains images converted into Python code for easy import into other scripts, such as displaying logos or icons.       |
| client/database.db           | A database file created to store the plant ID, date, time and prediction result.                                        |

### Server Directory Details

| File                          | Description                                                                                                              |
|-------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| server/pechayCam_server.py    | Hosts the Multioutput CNN model and handles the incoming post request from the client. Outputs the plant disease and severity estimation then sends the result back to the client. |
| server/inceptionV3_arch.h5    | Stores the architecture of the trained CNN model used for disease classification and severity estimation. The pre-trained model used here is the inceptionV3. |
| server/inceptionV3_weights.h5 | Stores the weights of the trained CNN model used for disease classification and severity estimation. |
