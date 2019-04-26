import requests
import base64

SERVICE_URL = ''  # change to url of you Cloud Run service

# make request service
with open('demo.docx', 'rb') as f:
    content = f.read()
    content = base64.b64encode(content)

resp = requests.post(SERVICE_URL, json={'docx_content': str(content, 'utf8')})

# Save response / PDF file
if resp.status_code == 200:
    out_content = resp.json().get('pdf_content', '')
    if out_content:
        with open('output.pdf', 'wb') as fx:
            decoded = base64.b64decode(out_content)
            fx.write(decoded)
else:
    print(resp.text)