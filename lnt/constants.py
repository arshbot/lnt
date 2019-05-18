from os.path import expanduser
HOME = expanduser("~")

DEFAULT_DIR_PATH = HOME + "/.lnt"
DEFAULT_CONF = "conf"
DEFAULT_CONF_PATH = DEFAULT_DIR_PATH + "/" + DEFAULT_CONF
DEFAULT_REBAL_PATH = DEFAULT_DIR_PATH + "/rebalances"

EMPTY_CONF ="""
[LND]
# Replace the below values with your respective files for your
# lnd node

# MacaroonPath = ~/admin.macaroon
# TlsCert = ~/tls.cert
# Host = localhost:10009

[LNT]
"""
