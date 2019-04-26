# Example of web application (microservice) which converts docx document to pdf 

Content of MS Word docx document should be encoded with base64 before posted as json  
docx to pdf it done via libreoffice and decoded afterwards 

This app is demonstration of [Cloud Run](https://cloud.google.com/run/) service on Google Cloud Platform  

to build Docker container run:

`gcloud builds submit --config=cloudbuild.yaml --substitutions=_SERVICE_NAME="testimage",TAG_NAME="v0.0.1"`