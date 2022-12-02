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
    email = request.args.get("email", None)
    ip = request.args.get("ip", None)

    #request_value = request.get_json()

    #email = int(request_value["email"])
    #ip = int(request_value["ip"])

    if email != None:
        result = predict(email, ip)
    else:
        result = ""

    write(email, ip, result)
    return (
        """<form action="" method="get">
                email_address input: <input type="text" name="email">
                ip_address input: <input type="text" name="ip">
                <input type="submit" value="Fraud or Not">
            </form>"""

        + "result: "
        + str(result)
    )

@app.route("/json", methods=['GET', 'POST'])
def jsonify():
    request_value = request.get_json()
    return request_value

def write(email, ip, result):
    filedf = "fraud_detector.csv"
    # write new data into csv
    with open(filedf, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([email, ip, result])
        print("file written")

def predict(email, ip):
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
    eventVariables = { 'email_address' : email, 'ip_address' : ip})

    return response['ruleResults'][0]['outcomes']

    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True, use_reloader=False)
