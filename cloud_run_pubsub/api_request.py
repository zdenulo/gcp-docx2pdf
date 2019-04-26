
"""
Request to Cloud Run service via Service Account
"""

from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

SERVICE_FILENAME = 'cr-test-secret.json'
BUCKET_NAME = ''  # name of the bucket where Docx file is saved
API_URL = ''  # change to url of you Cloud Run service


audience = API_URL

credentials = service_account.IDTokenCredentials.from_service_account_file(SERVICE_FILENAME, target_audience=audience)

session = AuthorizedSession(credentials)

data = {"message": {"attributes": {"bucketId": BUCKET_NAME, "objectId": "demo.docx"}}}

r = session.post(API_URL, json=data)
print(r.text)

