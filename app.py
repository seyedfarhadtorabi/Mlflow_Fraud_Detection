import csv
from flask import Flask, flash, request, redirect, url_for
import boto3
import uuid
from decouple import config 
access=config('ACCESS_KEY') 
secret=config('SECRET_KEY')
app = Flask(__name__)

@app.route("/status")
def status():
    return "success"

@app.route("/", methods=['GET', 'POST'])
def index():
    A1 = request.args.get("A1", None)
    A2 = request.args.get("A2", None)

    #request_value = request.get_json()

    #A1 = int(request_value["A1"])
    #A2 = int(request_value["A2"])

    if A1 != None:
        result = predict(A1, A2)
    else:
        result = ""

    write(A1, A2, result)
    return (
        """<form action="" method="get">
                email_address input: <input type="text" name="A1">
                ip_address input: <input type="text" name="A2">
                <input type="submit" value="Fraud or Not">
            </form>"""

        + "result: "
        + str(result)
    )

@app.route("/json", methods=['GET', 'POST'])
def jsonify():
    request_value = request.get_json()
    return request_value

def write(A1, A2, result):
    filedf = "fraud_detector.csv"
    # write new data into csv
    with open(filedf, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([A1, A2, result])
        print("file written")

def predict(A1, A2):
    """Predict Fraud or Not Fraud."""
    print("predicting")
    
    ENTITY_TYPE    = "mlflowent"
    EVENT_TYPE     = "mlflow_eve"
    DETECTOR_NAME  = "mlflow_detect"
    DETECTOR_VER   = "1"
    eventId = uuid.uuid1()

    fraudDetector = boto3.client('frauddetector', region_name='us-east-1',aws_access_key_id = str(access),
    aws_secret_access_key = str(secret))

    response = fraudDetector.get_event_prediction(
    detectorId = DETECTOR_NAME,
    eventId = str(eventId),
    eventTypeName = EVENT_TYPE,
    eventTimestamp = '2020-07-13T23:18:21Z',
    entities = [{'entityType':ENTITY_TYPE, 'entityId':str(eventId.int)}],
    eventVariables = { 'email_address' : A1, 'ip_address' : A2})

    return response['ruleResults'][0]['outcomes']

    

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int("5000"), debug=True, use_reloader=False)
