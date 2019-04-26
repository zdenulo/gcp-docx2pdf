# Converting Docx to PDF with Google Cloud Platform

repository contains examples how to do online conversion  of Microsoft Word (Docx) to PDF using products on Google Cloud Platform.  
They are meant to run as (micro)services with different context (HTTP request, asynchronous execution).

## Samples
- [cloud_function](./cloud_function) - Can be used to deploy to Cloud Functions
- [cloud_run](./cloud_run) - Simple webapp deployed on Cloud Run using Docker image. It uses libreoffice to do conversion to PDF. 
Input is content of docx file, it returns PDF content in response
- [cloud_run_pubsub](./cloud_run_pubsub) Simple webapp deployed on Cloud Run using Docker image. It's called by Pub Sub.
When file is uploaded to Cloud Storage bucket, Pub Sub notification is triggered which calls Cloud Run service and uploads PDF file to
output bucket  


 




 

