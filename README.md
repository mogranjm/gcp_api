# Solar Data Pipe 
Test data pipeline to extract time series data in batches from a Solar API using GCP resources.

## Architecture
![GCP Architecture Flowchart](design/architecture.drawio.png)

### GCP Cloud Scheduler
Hourly trigger to publish a message to a PubSub topic.

Cloud Scheduler is effectively a CRON scheduler for GCP resources. This resource manages cron jobs for 3 types of target (HTTP, PubSub and AppEngine)

In this example we configure Cloud Scheduler to send a message to a PubSub topic, which in turn triggers a Cloud Function.
~~~
# CREATE
gcloud scheduler jobs create pubsub get-solar   # gcloud cli command to create a cloud scheduler job with a PubSub target called "get-solar"
    --schedule="0 * * * *" \                    # schedule (cron format)
    --topic=trigger-get-solar-data \            # Name of target PubSub topic 
    --message-body="go solar" \                 # Message content to post to PubSub topic
    --location=australia-southeast1             # Location of the job

# UPDATE                                        
gcloud scheduler jobs update pubsub get-solar   # gcloud cli command to update a cloud scheduler pubsub job already defined
    --schedule="*/10 7-18 * * *" \              # change cron schedule to 7am-6pm (Melbourne winter daylight hours)
    --time-zone="Australia/Melbourne            # change timezone (previously omitted)
~~~
### GCP Pub/Sub
Receive message from Cloud Scheduler, trigger Cloud Function in response

Pub/Sub is an asynchronous messaging service (similar to Kafka). 

In this example we have configured a PubSub topic to act as an intermediary between Cloud Scheduler and Cloud Functions.
~~~
gcloud pubsub topics create trigger-get-solar-data # gcloud cli command to create a PubSub topic called "trigger-get-solar-data"
~~~

### GCP Cloud Functions
Call the Solar API, process data and append text file in Cloud Storage

Cloud Functions are serverless, single-purpose functions executed in your preferred runtime.

This is the meat of the data pipeline. Here, we use a Python script to query the GoodWe Solar API for the previous hour's production data of the configured solar inverter.
The data returned from the API is filtered, processed and appended to a file stored in a Cloud Storage bucket.
~~~
gcloud functions deploy get-solar-data \                    # gcloud cli command to deploy a cloud function with the name "get-solar-data"
    --region=australia-southeast1                           # gcp region to run the function
    --runtime=python39                                      # language the function is written in 
    --trigger-topic=trigger-get-solar-data                  # function trigger (our pubsub topic)
    --source=gs://<BUCKET_NAME>/<PATH_TO_CODE>.zip          # source code location
    --entry-point=get_current_solar_data                    # name of the function as defined in main.py (if python)
    --service-account=<SERVICE_ACCOUNT>@<PROJECT_NAME>.iam.gserviceaccount.com
~~~

### GOODWE Solar API
The GoodWe Solar API is an undocumented API that can be used to obtain data produced by a compatible and configured solar inverter.

Luckily, there is an open source Python project [pygoodwe](github.com/yaleman/pygoodwe) that allows access to the inverter's data as long as you're registered on the GoodWe SEMS portal.

Essentially, we instantiate a SingleInverter object (provided by pygoodwe) using credentials stored in a .env file. The init method of this class uses the credentials to login, get the current inverter state and store it as a dictionary.
In this example, we parse the SingleInverter data dictionary to extract the datapoints of interest then upload them as a blob to a csv file in a Cloud Storage bucket.


### GCP Cloud Storage
Host function source code, store data records

Cloud Storage is the Google Blob storage service (like Amazon S3 or Azure Blob Storage)

Usage of Cloud Storage service requires appropriate permissions. When connecting in the source code, this requires the administration of a Service Account.
~~~
# CREATE BUCKET
gsutil mb gs://solar-storage-service \  # bucket for solar data
    -b ON                               # Uniform bucket-level access on
    -l australia-southeast1             # bucket location

# PROVISION SERVICE ACCOUNT, GET KEY
gcloud iam service-accounts-create <SERVICE_ACCOUNT_NAME>
gcloud projects add-iam-policy-binding <PROJECT_ID> \
    --member="serviceAccount:<SERVICE_ACCOUNT_NAME>@<PROJECT_ID>.iam.gserviceaccount.com
    --role="roles/storage.objectCreator"
gcloud iam service-accounts keys create <KEY_NAME>.json \ 
    --iam-account=<SERVICE_ACCOUNT_NAME>@<PROJECT_ID>.iam.gserviceaccount.com
~~~