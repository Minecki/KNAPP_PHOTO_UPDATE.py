import os
import shutil
import pathlib
import pandas
import pyodbc

from KNAPP import config as cf
from time import time
from ftplib import FTP

fpt = FTP('ftp://10.2.225.2/')
fpt.login('ftppics', 'ftppics')

# Polaczenie z bazą w pliku config.py
cf.odbc_conf()
Connection = pyodbc.connect(cf.conn_conf)

# r przed "" lub ''przekazuje by wszystko traktowac jako raw string (wtedy nie potrzeba \\)
basedir = r"\\10.248.8.122\Images\images\PL_ecom_approved\\"

# basedir = r"C:\Users\MINECADR\Desktop\Test\\"  # Folder z zdjęciami

movedir = r"C:\Users\MINECADR\Desktop\Test2\\"  # Folder do umieszczenia zdjęć

Query = '''SELECT
  TRIM(MATNR) as SAP,
  TRIM(PRIMARY_IMAGE) 
FROM MDMPLTEAM.BAZA_PROD
WHERE PRIMARY_IMAGE = 
'''

# Pętla dla wszystkich plikow w folderze
for file in os.listdir(basedir):
    filename = os.fsdecode(file)
    # Path do aktualnie przeglądanego pliku
    file_path = os.path.join(basedir, file)
    # Pobiera informację o ostatniej edycji
    time_mod = time() - os.path.getmtime(basedir + filename)
    # Rozszerzenie pliku
    extension = pathlib.Path(basedir + file).suffix
    # Nazwa pliku bez rozszerzenia
    name = pathlib.Path(basedir + file).stem
    # Ostatnia edycja w formacie godzinowym
    lastedit = time_mod // 3600

    # print(filename)
    # print(name)
    # print(extension)
    # print(lastedit)

    # Jezeli czas edycji jest mniejszy niz 24 godziny to kopiuje plik
    if lastedit < 24:
        # Zapytanie do bazy o nr SAP przypisany do danego pliku
        df = pandas.read_sql(Query + "'" + name + "'", Connection)
        if df.iloc[0, df.columns.get_loc('SAP')] != '' or df.iloc[0, df.columns.get_loc('SAP')] is not None:
            value = df.iloc[0, df.columns.get_loc('SAP')]
            shutil.copy(file_path, os.path.join(movedir, value + extension))


