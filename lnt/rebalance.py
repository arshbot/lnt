#!/usr/bin/python

import rpc_pb2 as ln, rpc_pb2_grpc as lnrpc
import grpc, os, codecs

import argparse

parser = argparse.ArgumentParser(description="The rebalance part")
parser.add_argument("-n", "--name", dest="name",
                    help="Name of of this rebalance")
parser.add_argument("-e", "--edit", dest='edit', action="store_true")
parser.set_defaults(edit=False)

macaroon = codecs.encode(open('/Users/harshagoli/Projects/kubefiles/lnd-staging/admin.macaroon', 'rb').read(), 'hex')
os.environ['GRPC_SSL_CIPHER_SUITES'] = 'HIGH+ECDSA'
cert = open('/Users/harshagoli/Projects/kubefiles/lnd-staging/tls.cert', 'rb').read()
ssl_creds = grpc.ssl_channel_credentials(cert)
hannel = grpc.secure_channel('localhost:10009', ssl_creds)
stub = lnrpc.LightningStub(channel)
request = ln.ListChannelsRequest(
        active_only=True,
    )
response = stub.ListChannels(request, metadata=[('macaroon'), macaroon])
response = {
    "channels": [
        {
            "active": False,
            "remote_pubkey": "0206b792e8b1bc1642c96d6e0a9abfe8d848355a51de27a035402358998ddb4c68",
            "channel_point": "71cc6bf0447b595e4a36c57dfcbb2aea08dc81f0f64dee9264cf6232bceffa0d:0",
            "chan_id": "1631773112157011968",
            "capacity": "1000000",
            "local_balance": "0",
            "remote_balance": "999817",
            "commit_fee": "183",
            "commit_weight": "552",
            "fee_per_kw": "253",
            "unsettled_balance": "0",
            "total_satoshis_sent": "0",
            "total_satoshis_received": "0",
            "num_updates": "6",
            "pending_htlcs": [
            ],
            "csv_delay": 144,
            "private": False,
            "initiator": False
        },
        {
            "active": False,
            "remote_pubkey": "02288280138ee2807986828e08cb675d5cea7200eee0bfd3d0fb83d5c92f889b1c",
            "channel_point": "ce4498a8a3da9e795b202d13bd796da74e95707df485fea8f4c2aa51ab6d2e91:0",
            "chan_id": "1631776410691960832",
            "capacity": "10000000",
            "local_balance": "719247",
            "remote_balance": "9280210",
            "commit_fee": "543",
            "commit_weight": "724",
            "fee_per_kw": "750",
            "unsettled_balance": "0",
            "total_satoshis_sent": "0",
            "total_satoshis_received": "719247",
            "num_updates": "4",
            "pending_htlcs": [
            ],
            "csv_delay": 2016,
            "private": True,
            "initiator": False
        },
        {
            "active": True,
            "remote_pubkey": "0246ef94641a9d104243859f40213520411c1f43f8f36289f1ee623a6005e01813",
            "channel_point": "5755950c8bc894680a6cd86b7d7cd71a69457259bda5e131442673386500f56b:1",
            "chan_id": "1631303620691951617",
            "capacity": "1000000",
            "local_balance": "0",
            "remote_balance": "999817",
            "commit_fee": "183",
            "commit_weight": "552",
            "fee_per_kw": "253",
            "unsettled_balance": "0",
            "total_satoshis_sent": "0",
            "total_satoshis_received": "0",
            "num_updates": "27",
            "pending_htlcs": [
            ],
            "csv_delay": 6,
            "private": False,
            "initiator": False
        },
        {
            "active": True,
            "remote_pubkey": "0270685ca81a8e4d4d01beec5781f4cc924684072ae52c507f8ebe9daf0caaab7b",
            "channel_point": "83987b8b9e22b4d248c1afbfb4fe3307be79e65e66bbfd46c10cae349d23d0fa:0",
            "chan_id": "1598452412275752960",
            "capacity": "16777215",
            "local_balance": "5043",
            "remote_balance": "16771988",
            "commit_fee": "184",
            "commit_weight": "724",
            "fee_per_kw": "253",
            "unsettled_balance": "0",
            "total_satoshis_sent": "0",
            "total_satoshis_received": "5043",
            "num_updates": "309",
            "pending_htlcs": [
            ],
            "csv_delay": 2016,
            "private": False,
            "initiator": False
        },
        {
            "active": True,
            "remote_pubkey": "0296a5fa00004defbfefccfb28d51b3f8455df015c1f55eabf3ea5363eadc827d4",
            "channel_point": "226e63c4287372f277588a80f2c634ff46abed59394d1028df13e4ee4316ae25:0",
            "chan_id": "1635240971829051392",
            "capacity": "16777215",
            "local_balance": "999876",
            "remote_balance": "15777155",
            "commit_fee": "184",
            "commit_weight": "724",
            "fee_per_kw": "253",
            "unsettled_balance": "0",
            "total_satoshis_sent": "0",
            "total_satoshis_received": "999876",
            "num_updates": "36",
            "pending_htlcs": [
            ],
            "csv_delay": 2016,
            "private": False,
            "initiator": False
        },
        {
            "active": False,
            "remote_pubkey": "02f02429d49c5bc195329145ec77b9d52332d0a84a159257434cdb5fcb43cd97a4",
            "channel_point": "3226e295ef3ed220c47df8073ed437b928f373fbcbc3d1f42e834d4cbb6b2498:1",
            "chan_id": "1601807022252032001",
            "capacity": "16777215",
            "local_balance": "0",
            "remote_balance": "16768165",
            "commit_fee": "9050",
            "commit_weight": "552",
            "fee_per_kw": "12500",
            "unsettled_balance": "0",
            "total_satoshis_sent": "0",
            "total_satoshis_received": "0",
            "num_updates": "0",
            "pending_htlcs": [
            ],
            "csv_delay": 2016,
            "private": False,
            "initiator": False
        },
        {
            "active": False,
            "remote_pubkey": "03401272107106e216206224fefe02ab0c17d2ee9f3733c5fd244c0319976a93e6",
            "channel_point": "9b2ed510b81c8153a2548fc6597b1d9f269ccf0af19909d6d1450612e1e0b37a:0",
            "chan_id": "1599861986183020544",
            "capacity": "10000000",
            "local_balance": "472567",
            "remote_balance": "9518383",
            "commit_fee": "9050",
            "commit_weight": "724",
            "fee_per_kw": "12500",
            "unsettled_balance": "0",
            "total_satoshis_sent": "0",
            "total_satoshis_received": "472567",
            "num_updates": "2",
            "pending_htlcs": [
            ],
            "csv_delay": 1201,
            "private": True,
            "initiator": False
        },
        {
            "active": False,
            "remote_pubkey": "034fe52e98a0e9d3c21b767e1b371881265d8c7578c21f5afd6d6438da10348b36",
            "channel_point": "62369aeecb9e381b690f83b25a2cb263030f4240afd119af9173286d508e7dff:1",
            "chan_id": "1626448177341202433",
            "capacity": "2000000",
            "local_balance": "280113",
            "remote_balance": "1719701",
            "commit_fee": "186",
            "commit_weight": "724",
            "fee_per_kw": "256",
            "unsettled_balance": "0",
            "total_satoshis_sent": "0",
            "total_satoshis_received": "280113",
            "num_updates": "78",
            "pending_htlcs": [
            ],
            "csv_delay": 240,
            "private": False,
            "initiator": False
        },
        {
            "active": False,
            "remote_pubkey": "036370ec2b003df3e154c1040e8ad4a58320aaffa6a40440845016502a0e9906dd",
            "channel_point": "0c6b4dd4f69ad1179af4e8950e4f88681745096c23d3a909793a93c01a66069b:0",
            "chan_id": "1601870793929588736",
            "capacity": "9061678",
            "local_balance": "0",
            "remote_balance": "9061492",
            "commit_fee": "186",
            "commit_weight": "552",
            "fee_per_kw": "257",
            "unsettled_balance": "0",
            "total_satoshis_sent": "0",
            "total_satoshis_received": "0",
            "num_updates": "50",
            "pending_htlcs": [
            ],
            "csv_delay": 1088,
            "private": False,
            "initiator": False
        },
        {
            "active": True,
            "remote_pubkey": "038863cf8ab91046230f561cd5b386cbff8309fa02e3f0c3ed161a3aeb64a643b9",
            "channel_point": "111a7629cf6aaf4c96e0085d55a515c86a98695a872d49df20e02f75ae6e44f0:0",
            "chan_id": "1600103878740869120",
            "capacity": "16777215",
            "local_balance": "6971300",
            "remote_balance": "9805731",
            "commit_fee": "184",
            "commit_weight": "724",
            "fee_per_kw": "253",
            "unsettled_balance": "0",
            "total_satoshis_sent": "1279882",
            "total_satoshis_received": "251183",
            "num_updates": "1466",
            "pending_htlcs": [
            ],
            "csv_delay": 2016,
            "private": False,
            "initiator": False
        },
        {
            "active": False,
            "remote_pubkey": "03946fb4316f211b928e7db22cc7e7e3ca34524d06f61df813cfb824b252c4b144",
            "channel_point": "a99efce7e2920a6255034748e2ab02442b91dcea1f583dadea576f0591b7c1df:1",
            "chan_id": "1628823122457591809",
            "capacity": "16777215",
            "local_balance": "0",
            "remote_balance": "16768165",
            "commit_fee": "9050",
            "commit_weight": "552",
            "fee_per_kw": "12500",
            "unsettled_balance": "0",
            "total_satoshis_sent": "0",
            "total_satoshis_received": "0",
            "num_updates": "1",
            "pending_htlcs": [
            ],
            "csv_delay": 2016,
            "private": True,
            "initiator": False
        },
        {
            "active": False,
            "remote_pubkey": "03b6384db3982ba0f87bec1155633de02296b650b08290d8c9e811da3a07bcf595",
            "channel_point": "c13feea0f050859855270e51d55e0e0a8b0b2c5778417ee79d7b79dc91ddf91c:0",
            "chan_id": "1600968094886592512",
            "capacity": "16777215",
            "local_balance": "0",
            "remote_balance": "16772690",
            "commit_fee": "4525",
            "commit_weight": "552",
            "fee_per_kw": "6250",
            "unsettled_balance": "0",
            "total_satoshis_sent": "0",
            "total_satoshis_received": "0",
            "num_updates": "60",
            "pending_htlcs": [
            ],
            "csv_delay": 2016,
            "private": False,
            "initiator": False
        },
        {
            "active": False,
            "remote_pubkey": "03bf06b69bad9bd13acd1688b009f7dc57340e9028669645c809dcb7cbcd2e04e0",
            "channel_point": "69a5c9e60618497cdef3f4a9be4272b290e68346a5538d60afcab437536f7924:0",
            "chan_id": "1600188541136470016",
            "capacity": "16772633",
            "local_balance": "0",
            "remote_balance": "16763583",
            "commit_fee": "9050",
            "commit_weight": "552",
            "fee_per_kw": "12500",
            "unsettled_balance": "0",
            "total_satoshis_sent": "0",
            "total_satoshis_received": "0",
            "num_updates": "0",
            "pending_htlcs": [
            ],
            "csv_delay": 2015,
            "private": True,
            "initiator": False
        },
        {
            "active": False,
            "remote_pubkey": "03f7f84f77498ca496ebf9285413d0214766e7b23832bae423b6d9ae13f2533aac",
            "channel_point": "363637c0903dd7d5b588f946695ec63c289608a6adfc17fde6d356552ae98b49:0",
            "chan_id": "1598432621066715136",
            "capacity": "16000000",
            "local_balance": "8331004",
            "remote_balance": "7668453",
            "commit_fee": "543",
            "commit_weight": "724",
            "fee_per_kw": "750",
            "unsettled_balance": "0",
            "total_satoshis_sent": "0",
            "total_satoshis_received": "8331004",
            "num_updates": "90",
            "pending_htlcs": [
            ],
            "csv_delay": 144,
            "private": True,
            "initiator": False
        }
    ]
}


