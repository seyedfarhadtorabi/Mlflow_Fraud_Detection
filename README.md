# Mlflow_Fraud_Detection

## To build, Docker needs:
	Dockerfile
	app.py
	requirements.txt

## From command prompt type:
	docker build -t testimage .
	docker images --all
	docker run --name testcontainer -p 5000:5000 testimage