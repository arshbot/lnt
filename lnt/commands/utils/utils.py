import os, grpc, codecs, requests
import lnt.rpc.rpc_pb2 as ln, lnt.rpc.rpc_pb2_grpc as lnrpc


def create_stub(ctx):
    cfg = ctx.parent.parent.config['LND']

    mac_path = os.path.expanduser(cfg['MacaroonPath'])
    macaroon = codecs.encode(open(mac_path, 'rb').read(), 'hex')

    os.environ['GRPC_SSL_CIPHER_SUITES'] = 'HIGH+ECDSA'

    cert_path = os.path.expanduser(cfg['TlsCert'])
    cert = open(cert_path, 'rb').read()

    ssl_creds = grpc.ssl_channel_credentials(cert)
    channel = grpc.secure_channel(cfg['Host'], ssl_creds)
    stub = lnrpc.LightningStub(channel)
    return stub, macaroon

def normalize_self_info(response):
    return {a:getattr(response, a) for a in dir(response)[-15:]}

def normalize_node_info(response):
    return {
            'channels': response.channels,
            'node': {
                'last_update': response.node.last_update,
                'pub_key': response.node.pub_key,
                'alias': response.node.alias,
                'addresses': [
                    {'network':x.network, 'addr': x.addr} for x in
                        response.node.addresses
                ],
                'color': response.node.color,
            },
            'num_channels': response.num_channels,
            'total_capacity': response.total_capacity,
    }

def normalize_channels(channels):
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
            "pending_htlcs": c.pending_htlcs,
            "csv_delay": c.csv_delay,
        } for c in channels
    }
    return channels_d


def normalize_get_chan_response(chaninfo):
    chaninfo_d = {
        "channel_id": chaninfo.channel_id,
        "chan_point": chaninfo.chan_point,
        "last_update": chaninfo.last_update,
        "node1_pub": chaninfo.node1_pub,
        "node2_pub": chaninfo.node2_pub,
        "capacity": chaninfo.capacity,
        "node1_policy": {
            "time_lock_delta": chaninfo.node1_policy.time_lock_delta,
            "min_htlc": chaninfo.node1_policy.min_htlc,
            "fee_base_msat": chaninfo.node1_policy.fee_base_msat,
            "fee_rate_milli_msat": chaninfo.node1_policy.fee_rate_milli_msat,
            "max_htlc_msat": chaninfo.node1_policy.max_htlc_msat,
        },
        "node2_policy": {
            "time_lock_delta": chaninfo.node2_policy.time_lock_delta,
            "min_htlc": chaninfo.node2_policy.min_htlc,
            "fee_base_msat": chaninfo.node2_policy.fee_base_msat,
            "fee_rate_milli_msat": chaninfo.node2_policy.fee_rate_milli_msat,
            "max_htlc_msat": chaninfo.node2_policy.max_htlc_msat,
        }
    }
    return chaninfo_d


def get_1ml_info(testnet:bool, pub_key):
    resp = requests.get("https://1ml.com{}/node/{}/json".format('/testnet' if testnet else '', pub_key))
    return resp.json() if resp.status_code == 200 else {}
