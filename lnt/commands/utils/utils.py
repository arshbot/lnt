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
    return stub
