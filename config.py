from exchangelib import Account, Credentials

def odbc_conf():
    global conn_conf
    conn_conf= (
    'DRIVER={iSeries Access ODBC Driver};'
    'SYSTEM=S780F1B0;'
    'DATABASE=SL1CACHE;'
    'UID=roboplmd;'
    'PWD=hlwf70sat4;'
    )
def kartoteki():
    global credentials
    global account
    credentials = Credentials('kartoteki@onninen.com', 'K@myczek123')
    account = Account('kartoteki@onninen.com', credentials=credentials, autodiscover=True)