# Docx to PDF conversion using Google Drive (Google Doc)

## Setup
you need to create Service Account with which you'll make request to Google Drive and save locally key json file.  
In `settings.py` define absolute path to you service account file.  
To run locally, you need to install dependencies:  
`pip install -r requirements.txt` 


Process consists of following:
1. upload file to Google Doc
2. Download as PDF
3. Delete original file on Drive  

The code is meant to be deployed on Cloud Function, although **handling of input is not implemented 
(`main` function in `main.py`)** 
i.e. you can provide in json for example path in Cloud Storage where Docx file is and where it should be saved

*note* This conversion is not one of the quickest  
