import os, grpc, codecs
import lnt.rpc.rpc_pb2 as ln, lnt.rpc.rpc_pb2_grpc as lnrpc

def create_stub(ctx):
    cfg = ctx.parent.parent.config['LND']
    macaroon = codecs.encode(open(cfg['MacaroonPath'], 'rb').read(), 'hex')
    os.environ['GRPC_SSL_CIPHER_SUITES'] = 'HIGH+ECDSA'
    cert = open(cfg['TlsCert'], 'rb').read()
    ssl_creds = grpc.ssl_channel_credentials(cert)
    channel = grpc.secure_channel(cfg['Host'], ssl_creds)
    stub = lnrpc.LightningStub(channel)
    return stub, macaroon

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
            "csv_delay": c.csv_delay,
        } for c in channels
    }
    return channels_d
