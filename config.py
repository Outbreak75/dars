import os
import sys


def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)

    return os.path.join(datadir, filename)


# Select either local or remote database location
# Selection is for testing purporses
# Comment out unused location
# Shared databae location
# DB_PATH = r'P:\\DSRM\\dsrm.db'
# Local database location
DB_PATH = find_data_file('dsrm.db')
PWD_ICO = find_data_file('pwd_ico.png')
UNAME_ICO = find_data_file('uname_ico.png')
CATEGORY_ICO = find_data_file('category_ico.png')
ROOT_CAUSE_ICO = find_data_file('root_cause_ico.png')
DESCRIPTION_ICO = find_data_file('description_ico.png')
REQUESTED_CD_ICO = find_data_file('requested_cd_ico.png')
TARGET_CD_ICO = find_data_file('target_cd_ico.png')
DATE_OBSERVED_ICO = find_data_file('date_observed_ico.png')
DROPDOWN_PNG = find_data_file('dropdown.png')

DOWN_ARROW = find_data_file('down_arrow.png')

ADD_NEW_PNG = find_data_file('add_new.png')
COPY_PNG = find_data_file('copy.png')
CLEAR_FILTERS_PNG = find_data_file('clear_filters.png')
DELETE_PNG = find_data_file('delete.png')
EXPORT_PNG = find_data_file('export.png')
IMPORT_PNG = find_data_file('import.png')
MY_TOOLS_PNG = find_data_file('my_tools.png')
REOPEN_PNG = find_data_file('reopen.png')
SETTINGS_PNG = find_data_file('settings.png')
UPDATE_PNG = find_data_file('update.png')

DENTON_LOGO_PNG = find_data_file('DentonLogo.png')


DENTON_LOGO_ICO = find_data_file('dentonlogo.ico')

DEFAULT_PWD = 'password'


def main():
    pass


if __name__ == '__main__':
    main()
