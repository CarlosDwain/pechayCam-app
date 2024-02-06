# The PechayCam App
<p align="center">
  <img src="icons/PechayCam App Logo.png" alt="Logo" width="300">
</p>

## Overview

This repository contains the source code for a client-server application that leverages a trained model to classify plant diseases and estimate their severity in hydroponically grown Pechay.

<p align="center">
  <img src="icons/Overall architecture 2.jpg" alt="Logo" >
</p>

The architectural diagram illustrates the interplay between the client and server components. At its heart lies the laptop server, hosting the trained deep learning model designed to recognize diseases in Pechay plants and assess their severity. By deploying this model as a REST API, it becomes readily available for inference by the Raspberry Pi. This setup not only ensures efficient utilization of resources but also facilitates scalability, making the model accessible across various platforms including mobile and desktop applications.

### System Workflow
The system operates in a structured sequence, outlined in the workflow diagram below. Initially, upon image capture, the system verifies the Plant ID and Server IP accuracy. If validated, the image data is formatted into JSON and transmitted to the application server via an HTTP post request. Any discrepancies prompt the user to reattempt image capture.

<p align="center">
  <img src = "icons/System Workflow.jpg" alt="Logo" width="400">
</p>

On the server side, upon receiving the JSON data, it is converted back into a numpy array format. This data is then fed into a multioutput CNN model, which provides insights into both the plant disease and its severity. The resulting information is formatted into JSON and sent back to the client.

The client verifies the success of the server response. If unsuccessful, the user is advised to try capturing the image again. Conversely, upon successful reception, the result is converted into string format and stored in an SQLite database. Finally, the processed data is displayed on a 3.5-inch screen, marking the end of the system's operation.

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

## Setting Up PyQt5 Development Environment

To start developing PyQt5 applications, first setup `pyeng` in your computer and then follow these steps to set up your development environment:

1. **Create a Virtual Environment**: Begin by creating a virtual environment named `pyqt5` or `pyside6` using your preferred virtual environment manager.

    ```bash
    python -m venv venv-name

2. **Activate the Virtual Environment**: Activate the virtual environment by running the appropriate activation command for your operating system.

    ```bash
    venv-name\Scripts\activate

3. **Install PyQt5 or PySide6**: Install either PyQt5 or PySide6 package using pip, depending on your preference.

    ```bash
    pip install PyQt5
    ```

    or

    ```bash
    pip install PySide6
    ```

4. **Install PyQt5 Tools**: Optionally, you can install PyQt5 tools to enhance your development experience.

    ```bash
    pip install pyqt5-tools
    ```

5. **Access PyQt5 Designer**: Navigate to the PyQt5 bin directory in your virtual environment. For example, if your virtual environment is located at `D:\username\python_envs\pyqt5`, you can find the Designer app at `D:\username\python_envs\pyqt5\Lib\site-packages\qt5_applications\Qt\bin`.

    ```bash
    cd D:\username\python_envs\pyqt5\Lib\site-packages\qt5_applications\Qt\bin
    ```

    In this directory, you will find the PyQt5 Designer application, which you can use to design and create PyQt5 GUI applications visually.

With these steps completed, you're ready to start developing PyQt5 applications using the powerful tools provided by the PyQt5 framework.
