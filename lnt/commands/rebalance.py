# Mark standard lib imports
from hashlib import sha1
import grpc, os, codecs, argparse

# Mark 3rd party lib imports
import rpc_pb2 as ln, rpc_pb2_grpc as lnrpc
from PyInquirer import style_from_dict, Token, prompt, Separator

# Mark local imports
from graphics.styles import prompt_style
# TODO: Pull these const from config
from constants import DEFAULT_LNT_DIR

# Mark debugging imports
from ptpdb import set_trace


parser = argparse.ArgumentParser(description="The rebalance part")
parser.add_argument("-n", "--name", dest="name",
                    help="Name of of this rebalance")
parser.add_argument("-e", "--edit", dest='edit', action="store_true")
parser.set_defaults(edit=False)

macaroon = codecs.encode(open('/Users/harshagoli/Projects/kubefiles/lnd-staging/admin.macaroon', 'rb').read(), 'hex')
os.environ['GRPC_SSL_CIPHER_SUITES'] = 'HIGH+ECDSA'
cert = open('/Users/harshagoli/Projects/kubefiles/lnd-staging/tls.cert', 'rb').read()
ssl_creds = grpc.ssl_channel_credentials(cert)
channel = grpc.secure_channel('localhost:10009', ssl_creds)
stub = lnrpc.LightningStub(channel)
request = ln.ListChannelsRequest(active_only=True)
response = stub.ListChannels(request, metadata=[('macaroon', macaroon)])

channels = response.channels
channels_d = { 
    str(c.chan_id): {
        "active": c.active,
        "remote_pubkey": c.remote_pubkey,
        "channel_point": c.channel_point,
        "capacity": c.capacity,
        "local_balance": c.local_balance,
        "remote_balance": c.remote_balance,
        "commit_fee": c.commit_fee,
        "commit_weight": c.commit_weight,
        "fee_per_kw": c.fee_per_kw,
        "total_satoshis_sent": c.total_satoshis_sent,
        "total_satoshis_received": c.total_satoshis_received,
        "num_updates": c.num_updates,
        "csv_delay": c.csv_delay,
    } for c in channels
}

def ratio_graphic(local, remote):
	total = local + remote
	local_ratio = int((round(local/total, 1) * 10) / 2)
	remote_ratio = int((round(remote/total, 1) * 10) / 2)
	return local_ratio * "🁢" + ( (5 - local_ratio) * "-" )  + ( (5 - remote_ratio) * "-" ) + remote_ratio * "🁢"

def vars_to_string(chan_id, local_balance, remote_balance, nick=None):
	total_balance = local_balance + remote_balance
	nick = "-" if nick == None else nick
	# TODO, pretty this up -> https://stackoverflow.com/a/9996049/5838056
	return "{}, {}, {}, {}, {}".format(nick, chan_id, local_balance,
            remote_balance, ratio_graphic(local_balance, remote_balance))


channel_choices_from = {
    "type" : "checkbox",
    "qmark": "⚡️",
    "message" : "CHOOSE FROM nick, channel id, local_balance, remote_balace, graphic",
    "name" : "channel_choices_from",
    "choices" :  [ {'name' : vars_to_string(c.chan_id, c.local_balance, c.remote_balance, nick=None) } for c in channels ],
    "validate" : lambda answer: 'You must choose at least one channel' if len(answer) == 0 else True
}

channel_choices_to = {
    'type': 'list',
    'message': 'CHOOSE TO nick, channel id, local_balance, remote_balace, graphic',
    "name" : "channel_choices_to",
    'choices': [ {'name' : vars_to_string(c.chan_id, c.local_balance, c.remote_balance, nick=None) } for c in channels ]
}

from_channels = prompt(channel_choices_from, style=prompt_style)
from_channels = [ x.split(",")[1][1:] for x in from_channels['channel_choices_from'] ]
to_channel = prompt(channel_choices_to, style=prompt_style)
to_channel = to_channel['channel_choices_to'].split(",")[1][1:]

LNT_DIR_REBAL = LNT_DIR+"/rebalances"
if not os.path.exists(LNT_DIR):
    os.makedirs(LNT_DIR)

if not os.path.exists(LNT_DIR_REBAL):
    os.makedirs(LNT_DIR_REBAL)

rebase_image = ""

# Construct rebase
for from_c in from_channels:
    rebase_image += "{}:{} -> {},\n".format(channels_d[from_c]["local_balance"], from_c, to_channel)

if True: # TODO: Add naming option
    # TODO: Better random naming
    rebal_name = sha1(str(channels).encode('utf8')).digest().hex()[:20] + ".rebal"

with open(LNT_DIR_REBAL+"/"+rebal_name, 'w') as f:
    f.write(rebase_image)

print(rebase_image)

