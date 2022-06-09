# Solar Data Pipe 
Test sandbox for a data pipeline to extract time series data in batches from a Solar API using GCP resources.

## Architecture
![GCP Architecture Flowchart](design/architecture.drawio.png)

### GCP Cloud Scheduler
Hourly trigger to publish a message to a PubSub topic.

Cloud Scheduler is effectively a CRON scheduler for GCP resources. This resource manages cron jobs for 3 types of target (HTTP, PubSub and AppEngine)

In this example we configure Cloud Scheduler to send a message to a PubSub topic, which in turn triggers a Cloud Function.
~~~
gcloud scheduler jobs create pubsub get-solar   # gcloud cli command to create a cloud scheduler job with a PubSub target called "get-solar"
    --schedule="0 * * * *" \                    # schedule (cron format)
    --topic=trigger-get-hourly-solar-data \     # Name of target PubSub topic 
    --message="go solar" \                      # Message content to post to PubSub topic
    --location=australia-southeast1             # Location of the job
~~~
### GCP Pub/Sub
Receive message from Cloud Scheduler, trigger Cloud Function in response

Pub/Sub is an asynchronous messaging service (similar to Kafka). 

In this example we have configured a PubSub topic to act as an intermediary between Cloud Scheduler and Cloud Functions.
~~~
gcloud pubsub topic create get-hourly-solar-data-trigger # gcloud cli command to create a PubSub topic called "trigger-get-hourly-solar-data"
~~~