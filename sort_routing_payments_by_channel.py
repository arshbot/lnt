import json, os
from pprint import pprint
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--rpc", action="store_const", const="USE_RPC", help="Uses gRPC to retrieve values instead of json")
parser.add_argument("-st", "--start_time", dest="start_time", help="Starting point of the forwarding history request in UNIX timestamp. Required if --rpc")
parser.add_argument("-et", "--end_time", dest="end_time", help="End point of the forwarding history request in UNIX timestamp. Required if --rpc")
parser.add_argument("-f", "--forwarded-payments", dest="fwded_payments_f",
                    help="Json file path of forwarded payments", metavar="FILE")
parser.add_argument("-c", "--channels", dest="channels_f",
                    help="Json file path of all channels for node")
parser.add_argument("-t", "--top", dest="num_to_print", default=5, type=int, help="Top x to return")
args = parser.parse_args()

# Get values to sort
if args.rpc == "USE_RPC":
    import subprocess, grpc, codecs
    import rpc_pb2 as ln, rpc_pb2_grpc as lnrpc
    cert = open(os.environ.get("TLS_CERT_PATH"), "rb").read()
    ssl_creds = grpc.ssl_channel_credentials(cert)
    channel = grpc.secure_channel(os.environ.get("LND_URL"), ssl_creds)
    stub = lnrpc.LightningStub(channel)

    MACAROON = codecs.encode(open(os.environ.get("MACAROON_PATH"), 'rb').read(), 'hex')

    req = ln.ForwardingHistoryRequest(start_time=args.start_time, end_time=args.end_time)
    res = stub.ForwardingHistory(req, metadata=[("macaroon", MACAROON)])

    fwded_payments = res.forwarding_events

    req = ln.ListChannelsRequest()
    res = stub.ListChannels(req, metadata=[("macaroon", MACAROON)])

    channels = res.channels

    def cleanup_generated():
        cleanup = "rm rpc.proto rpc_pb2.py rpc_pb2_grpc.py"
        subprocess.Popen(cleanup.split())

else:
    with open(args.fwded_payments_f) as f:
        fwded_payments = json.load(f)['forwarding_events']
    
    with open(args.channels_f) as f:
        channels = json.load(f)['channels']

routes = {}

def id_to_pubkey(id):
    for channel in channels:
        if channel['chan_id'] == id:
            return channel['remote_pubkey']
    return id

# (routed, earned_fees, payments_routed)
for payment in fwded_payments:

    route = id_to_pubkey(payment['chan_id_in'])+"-"+id_to_pubkey(payment['chan_id_out'])
    if route in routes:
        routes[route][0] += int(payment['amt_in'])
        routes[route][1] += int(payment['fee'])
    else:
        routes[route] = [int(payment['amt_in']), int(payment['fee']), 0 ]
    
    routes[route][2] += 1

sort_by_routed_sum = sorted(routes.items(), reverse=True, key=lambda kv: kv[1][0])
sort_by_earned_fees = sorted(routes.items(), reverse=True, key=lambda kv: kv[1][1])
sort_by_routed_num = sorted(routes.items(), reverse=True, key=lambda kv: kv[1][2])

counter = 1
print("Most satoshis flowed through")
for route in sort_by_routed_sum:
    from_route, to_route = route[0].split("-")
    print("#{} - {} to {} routed {} satoshis".format(counter, from_route, to_route, route[1][0]))
    counter += 1
    if counter > args.num_to_print:
        break

counter = 1
print("")
print("Most fees earned")
for route in sort_by_earned_fees:
    from_route, to_route = route[0].split("-")
    print("#{} - {} to {} earned {} satoshis".format(counter, from_route, to_route, route[1][1]))
    counter += 1
    if counter > args.num_to_print:
        break

counter = 1
print("")
print("Most payments routed")
for route in sort_by_earned_fees:
    from_route, to_route = route[0].split("-")
    print("#{} - {} to {} earned {} satoshis".format(counter, from_route, to_route, route[1][2]))
    counter += 1
    if counter > args.num_to_print:
        break
