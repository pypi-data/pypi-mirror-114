import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload

class GoogleDriveService:
    SCOPES = ['https://www.googleapis.com/auth/drive']
    def __init__(self, path_credentials='credentials.json', path_token='token.json'):
        self.path_credentials = path_credentials
        self.path_token = path_token
        self.service = None

    def authenticate(self):
        creds = None
        if os.path.exists(self.path_token):
            creds = Credentials.from_authorized_user_file(self.path_token, self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.path_credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.path_token, 'w') as token:
                token.write(creds.to_json())

        self.service = build('drive', 'v3', credentials=creds)

    def get_metadata_drive_file(self, folder_id, file_name):
        results = self.service.files().list(q=f"'{folder_id}' in parents and name = '{file_name}'",
                                          spaces='drive',
                                          fields='nextPageToken, files(id, name, modifiedTime)').execute()
        items = results.get('files', [])
        return items[0]

    def upload_file(self, folder_id, source_path, file_name):
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        media = MediaFileUpload(f'{source_path}\{file_name}',
                                resumable=True)
        file = self.service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()

    def create_folder(self, folder_name, parent_folder_id):
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_folder_id]
        }
        file = self.service.files().create(body=file_metadata,
                                            fields='id').execute()
        return file.get('id')

    def get_id_of_folder(self, folder_name, parent_folder_id):
        results = self.service.files().list(q = f"mimeType = 'application/vnd.google-apps.folder' and name = '{folder_name}'", fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        return items[0].get('id')

    def folder_exists(self, folder_name, parent_folder_id):
        results = self.service.files().list(q = f"mimeType = 'application/vnd.google-apps.folder' and name = '{folder_name}' and '{parent_folder_id}' in parents", fields="nextPageToken, files(id)").execute()
        items = results.get('files', [])
        return len(items) > 0

    def file_exists(self, file_name, folder_id):
        results = self.service.files().list(q = f"mimeType != 'application/vnd.google-apps.folder' and name = '{file_name}' and '{folder_id}' in parents", fields="nextPageToken, files(id)").execute()
        items = results.get('files', [])
        return len(items) > 0

    def delete_file(self, file_name, folder_id):
        results = self.service.files().list(q = f"mimeType != 'application/vnd.google-apps.folder' and name = '{file_name}' and '{folder_id}' in parents", fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        file_id = items[0].get('id')

        self.service.files().delete(fileId=file_id).execute()

    def get_files_in_folder(self, folder_name):
        results = self.service.files().list(q = f"mimeType = 'application/vnd.google-apps.folder' and name = '{folder_name}'", pageSize=10, fields="nextPageToken, files(id, name)").execute()
        folderIdResult = results.get('files', [])
        id = folderIdResult[0].get('id')

        results = self.service.files().list(q = "'" + id + "' in parents", pageSize=10, fields="nextPageToken, files(id, name, mimeType)").execute()
        items = results.get('files', [])