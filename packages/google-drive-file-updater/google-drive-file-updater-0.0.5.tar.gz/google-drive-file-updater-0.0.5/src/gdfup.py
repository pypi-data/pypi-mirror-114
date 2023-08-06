from gd_fup.updater import GoogleDriveFileUpdater
from gd_fup.service import GoogleDriveService
import sys
from colorama import init
init()
from colorama import Fore, Back, Style

if(len(sys.argv) < 3):
    print(f'{Fore.RED}Please use the following format:')
    print(f'{Fore.MAGENTA}gdfup.py {Fore.GREEN}[Source path] [Destination folder id] {Fore.CYAN}(optional: Path to credentials){Style.RESET_ALL}')
    print(fr'e.g. gdfup.py C:\Users\max\programming 1OEj4Oiz1ILRezPOfPw27SxmPaan-vq1G')
else:
    drive_service = None
    if(len(sys.argv) == 3):
        drive_service = GoogleDriveService()
    elif(len(sys.argv) == 4):
        drive_service = GoogleDriveService(path_credentials=sys.argv[3])

    drive_service.authenticate()

    drive_file_updater = GoogleDriveFileUpdater(drive_service=drive_service, output_console=True)

    drive_file_updater.update_files(
        path_source=sys.argv[1], 
        root_folder_id=sys.argv[2])