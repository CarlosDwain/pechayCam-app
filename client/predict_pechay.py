import json
import requests

from PyQt5 import QtWidgets
 
def predict_pechay(self,image,ip):
    url = f'http://{ip}:5000/predict'
    data = {"image":image} #a key-value pair where value is a list
    data_json = json.dumps(data) # Serialize: used to convert a Python object into a JSON-formatted string.
    headers = {'Content-type':'application/json'} # a way of saying that the data that will be sent as a json format
    try:
        # This will raise requests.exceptions.Timeout if the connection takes longer than 5 seconds.
        # It's important to handle errors in this way so that your application continues to run and respond to user input, 
        # rather than becoming unresponsive.
        response = requests.post(url, data=data_json, headers=headers, timeout=5) # POST - send data to the server and extracts it
        result = json.loads(response.text) #Deserialize: json.loads() used to convert a JSON-formatted string into a Python object
        return result
    except:
        QtWidgets.QMessageBox.warning(self,'Error', 'Could not connect to the specified IP address\n\nNote: Check if the server is running or Wrong IP selection')