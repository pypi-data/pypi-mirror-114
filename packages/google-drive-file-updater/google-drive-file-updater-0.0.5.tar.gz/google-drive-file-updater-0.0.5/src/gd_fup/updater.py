import os
import win32com.client
from .progress_bar import Progressbar
from .service import GoogleDriveService
from datetime import datetime

from colorama import init
init()
from colorama import Fore, Back, Style

class GoogleDriveFileUpdater:
    def __init__(self, drive_service, output_console=True):
        self.drive_service = drive_service
        self.output_console = output_console

    def __get_num_files(self, path):
        num_files = 0
        for base, dirs, files in os.walk(path):
            num_files += len(dirs) + len(files);
        return num_files

    def __modified_date_file(self, path, file_name):
        sh = win32com.client.gencache.EnsureDispatch('Shell.Application', 0)
        ns = sh.NameSpace(path)

        item = ns.ParseName(str(file_name))
        last_modified = ns.GetDetailsOf(item, 3) # 3 --> last modified
        return datetime.strptime(last_modified, '%d.%m.%Y %H:%M')

    def __replace_file_if_newer(self, source_path, folder_id, file_name):
        source_last_modified = self.__modified_date_file(source_path, file_name)
        drive_last_modified = datetime.strptime(self.drive_service.get_metadata_drive_file(folder_id, file_name).get('modifiedTime'), '%Y-%m-%dT%H:%M:%S.%fZ')
    
        if(source_last_modified > drive_last_modified):
            self.drive_service.delete_file(file_name, folder_id)
            self.drive_service.upload_file(folder_id, source_path, file_name)
            self.progressbar.print_progress(self.iteration, f'{Fore.MAGENTA}Updated {Fore.CYAN}{file_name}{Style.RESET_ALL}')

    def __update_files_rec(self, path_source, folder_id):
        for file_name in os.listdir(path_source):
            full_path_source = fr'{path_source}\{file_name}'
            if(os.path.isfile(full_path_source)):
                if(self.drive_service.file_exists(file_name, folder_id)):
                    self.__replace_file_if_newer(path_source, folder_id, file_name)
                else:
                    self.drive_service.upload_file(folder_id, path_source, file_name)
                    self.progressbar.print_progress(self.iteration, f'{Fore.GREEN}Uploaded {Fore.CYAN}{file_name}{Style.RESET_ALL}')
            else:
                next_source_path = fr'{path_source}\{file_name}'
                if(not self.drive_service.folder_exists(file_name, folder_id)):
                    new_folder_id = self.drive_service.create_folder(file_name, folder_id)
                    self.progressbar.print_progress(self.iteration, f'{Fore.GREEN}Created new folder {Fore.CYAN}{file_name} {Fore.GREEN}with id {Style.RESET_ALL}{new_folder_id}')
                    self.__update_files_rec(next_source_path, new_folder_id)
                else:
                    next_folder_id = self.drive_service.get_id_of_folder(file_name, folder_id)
                    self.__update_files_rec(next_source_path, next_folder_id)
            self.iteration += 1
            self.progressbar.print_progress(self.iteration)

    def update_files(self, path_source, root_folder_id):
        self.num_files = self.__get_num_files(path_source)
        self.progressbar = Progressbar(self.num_files, 50, 'Progress', 'Complete', 2)
        self.iteration = 0
        if(self.drive_service.service == None):
            self.drive_service.authenticate()

        self.__update_files_rec(path_source, root_folder_id)