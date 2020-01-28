from os.path import expanduser
HOME = expanduser("~")

DEFAULT_DIR_PATH = HOME + "/.lnt"
DEFAULT_CONF = "lnt.conf"
DEFAULT_CONF_PATH = DEFAULT_DIR_PATH + "/" + DEFAULT_CONF
DEFAULT_REBAL_PATH = DEFAULT_DIR_PATH + "/rebalances"

VIEW_CHANNEL_COLUMNS_DEFAULT = ["CHANNEL_ID","CAPACITY","LOCAL_BAL","LOCAL/CAP","FORWARDS", \
    "PENDING_HTLCS","LAST_USED","CHANNELS_W/_PEER", "ALIAS"]
VIEW_CHANNEL_COLUMNS_MAP = {
    "CAPACITY": 'capacity',
    "LOCAL_BAL": 'local_balance',
    "LOCAL/CAP": 'local/cap',
    "FORWARDS": 'forwards',
    "PENDING_HTLCS": 'pending_htlcs',
    "LAST_USED": 'last_update',
    "CHANNELS_W/_PEER": 'num_channels_with_peer'
}

VIEW_CHANNEL_COLUMNS_EXTRA = []
VIEW_CHANNEL_COLUMNS_TOTAL = VIEW_CHANNEL_COLUMNS_DEFAULT + VIEW_CHANNEL_COLUMNS_EXTRA

DEFAULT_MONTHS_AGO = 3

EMPTY_CONF = """
[LND]
MacaroonPath = ~/.lnd/data/chain/bitcoin/testnet/admin.macaroon
TlsCert = ~/.lnd/tls.cert
Host = localhost:10009

[LNT]
Testnet = True
"""
