import rpc.rpc_pb2 as ln, rpc.rpc_pb2_grpc as lnrpc

def create_stub(ctx):
    macaroon = codecs.encode(open( , 'rb').read(), 'hex')
    os.environ['GRPC_SSL_CIPHER_SUITES'] = 'HIGH+ECDSA'
    cert = open('/Users/harshagoli/Projects/kubefiles/lnd-staging/tls.cert', 'rb').read()
    ssl_creds = grpc.ssl_channel_credentials(cert)
    channel = grpc.secure_channel('localhost:10009', ssl_creds)
    stub = lnrpc.LightningStub(channel)
    return stub
