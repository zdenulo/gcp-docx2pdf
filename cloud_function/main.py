
import io

OUT_FOLDER = '/tmp'

SERVICE_FILENAME = ''  # set path to service account filename

from googleapiclient.discovery import build
from google.oauth2 import service_account

from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

credentials = service_account.Credentials.from_service_account_file(SERVICE_FILENAME,
                                                                    scopes=['https://www.googleapis.com/auth/drive']
                                                                    )


drive = build('drive', 'v3', credentials=credentials)


def upload_to_gdrive(filepath):
    """Uploads Docx file as Google Doc
    :param filepath: path  of file which will be converted on local computer
    :returns ID of Google Doc file
    """
    file_metadata = {'name': filepath,
                     'mimeType': 'application/vnd.google-apps.document'}

    media = MediaFileUpload(filepath,
                            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    file = drive.files().create(body=file_metadata,
                                media_body=media,
                                fields='id').execute()
    print('File ID: %s' % file.get('id'))
    return file.get('id')


def download_as_pdf(file_id):
    """Downloads Google Doc file as PDF
    :param file_id: ID of Google Doc file
    """
    request = drive.files().export_media(fileId=file_id,
                                         mimeType='application/pdf')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    fh.seek(0)
    filename = file_id + '.pdf'
    with open(filename, 'wb') as fx:
        fx.write(fh.getvalue())


def delete_gdrive_file(file_id):
    """Deleted file on Google Drive
    :param file_id: ID of Google Drive file
    """
    response = drive.files().delete(fileId=file_id).execute()
    print(response)


def main(request):
    if request.method != 'POST':
        pass


if __name__ == '__main__':
    file_id = upload_to_gdrive('demo.docx')
    download_as_pdf(file_id)
    delete_gdrive_file(file_id)