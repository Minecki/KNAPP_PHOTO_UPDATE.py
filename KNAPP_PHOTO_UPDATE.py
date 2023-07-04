import os
import shutil
import pathlib
import subprocess
import warnings
warnings.filterwarnings("ignore")
import pandas
import pyodbc
from sqlalchemy.sql.elements import Null
import config as cf
from time import time
from ftplib import FTP


# Polaczenie z bazą w pliku config.py
cf.odbc_conf()
Connection = pyodbc.connect(cf.conn_conf)

basedir = "\\\\XXXXXXXXXXX\\Images\\images\\PL_ecom_approved\\"

Query = '''SELECT
  TRIM(MATNR) as SAP,
  TRIM(PRIMARY_IMAGE) 
FROM MDMPLTEAM.BAZA_PROD
WHERE PRIMARY_IMAGE = 
'''

# Pętla dla wszystkich plikow w folderze
for file in os.scandir(basedir):
    filename = os.fsdecode(file)
    print(filename)
    # Path do aktualnie przeglądanego pliku
    file_path = os.path.join(basedir, file)
    # Pobiera informację o ostatniej edycji
    time_mod = time() - os.path.getmtime(filename)
    # Rozszerzenie pliku
    extension = pathlib.Path(file).suffix
    # Nazwa pliku bez rozszerzenia
    name = pathlib.Path(file).stem
    # Ostatnia edycja w formacie godzinowym
    lastedit = time_mod // 3600

    # Jezeli czas edycji jest mniejszy niz 24 godziny to kopiuje plik
    if lastedit > 24:
        # Zapytanie do bazy o nr SAP przypisany do danego pliku
        df = pandas.read_sql(Query + "'" + name + "'", Connection)
        #print(df.iloc[0, df.columns.get_loc('SAP')])
        if df.empty == False:
            if df.iloc[0, df.columns.get_loc('SAP')] != '' or df.iloc[0, df.columns.get_loc('SAP')] is not Null or df.empty == False:
                print("Nr sap = " + df.iloc[0, df.columns.get_loc('SAP')] )
                value = df.iloc[0, df.columns.get_loc('SAP')]
                shutil.copy(file_path, os.path.join(movedir, value + extension))



