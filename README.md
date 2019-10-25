# cloud-iot-core-protobuf-sample

In this guide you set up an end-to-end IoT ingestion pipeline, from a simulated client device to Cloud Functions via Cloud IoT Core.
The main purpose is to show-case usage to Protocol Buffers to serialize and deserialize the messages send over MQTT connection.

## Generated Python protocol buffer class
The Python protocol buffer class is already generated for this tutorial. The class is generated based on the [proto definition file](proto/measurement.proto).
Follow the [Python Generated Code](https://developers.google.com/protocol-buffers/docs/reference/python-generated) to understand the process of Python protocol buffer class.

## Before you begin

1.  [Select or create a GCP project](https://console.cloud.google.com/projectselector2/home/dashboard).
1.  Make sure that [billing is enabled](https://cloud.google.com/billing/docs/how-to/modify-project) for your GCP project.
1.  [Enable the Cloud IoT, Cloud Pub/Sub and Cloud Functions](https://console.cloud.google.com/flows/enableapi?apiid=cloudiot.googleapis.com,pubsub.googleapis.com,cloudfunctions.googleapis.com).

## Get the tutorial source code in Cloud Shell

1.  In the GCP Console, [open Cloud Shell](http://console.cloud.google.com/?cloudshell=true).
1.  Clone the source code repository:

        cd $HOME
        git clone https://github.com/kingman/cloud-iot-core-protobuf-sample.git


## Set environment variables

To make it easier to run commands when you create cloud resources, set environment variables in Cloud Shell to hold the names and properties of the resources:

    export PROJECT_ID=$(gcloud config list --format 'value(core.project)')
    export EVENT_TOPIC=proto-event
    export REGISTRY_ID=proto-reg
    export REGION=europe-west1
    export DEVICE_ID=proto-device
    export PRIVATE_KEY_FILE='rsa_private.pem'
    export ALGORITHM='RS256'
    export CA_CERTS='roots.pem'


## Generate device key pair

In cloud shell run:

    cd $HOME/cloud-iot-core-protobuf-sample/client
    openssl req -x509 -nodes -newkey rsa:2048 -keyout rsa_private.pem -out rsa_cert.pem -subj "/CN=unused"

## Set up cloud resources

1.  Create the Cloud Pub/Sub topic:

        gcloud pubsub topics create $EVENT_TOPIC

1.  Create the Cloud IoT Core registry:

        gcloud iot registries create $REGISTRY_ID \
          --region $REGION \
          --event-notification-config=topic=$EVENT_TOPIC

1.  Create the the sensor board identity in the newly created Cloud IoT Core registry with the public key:

        cd $HOME/cloud-iot-core-protobuf-sample/client
        gcloud iot devices create $DEVICE_ID \
          --region=$REGION \
          --registry=$REGISTRY_ID \
          --public-key=path=rsa_cert.pem,type=rsa-x509-pem

1.  Deploy Cloud Functions

        cd $HOME/cloud-iot-core-protobuf-sample/cf
        gcloud functions deploy process_proto \
          --trigger-topic $EVENT_TOPIC \
          --runtime python37 \
          --region $REGION

## Set up client simulator
In cloud shell run:

    cd $HOME/cloud-iot-core-protobuf-sample/client
    virtualenv env && source env/bin/activate
    pip install -r requirements.txt
    wget https://pki.google.com/roots.pem

## Run client simulator
In cloud shell run:

    python run_client.py

## Verify messages in cloud
In Cloud Functions log verify the messages are being logged as JSON
