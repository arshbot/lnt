# lnt

Lightning Network Tools (lnt) is a toolset for interacting and managing your [lnd](https://github.com/lightningnetwork/lnd) node.

## Installation

From source:

```
git clone --recursive https://github.com/arshbot/lnt.git
cd lnt
python setup.py install
```

From Pypi: 

```
pip install lnt
```

## Feature progress

- [x] View channels
- [ ] View invoices
- [ ] View rebalances
- [ ] View payments
- [ ] Create channel
- [ ] Create invoice
- [x] Create rebalance image
- [ ] Execute rebalance image
- [ ] Send payment

## Usage

View channels

```
$ lnt view channel

CHANNEL ID           CAPACITY   LOCAL_BAL  LOCAL/CAP   UPDATE NUM   PENDING HTLCS   LAST USED
1724858866081988609  15000000   14999817     100.00%           23   0               2019-08-05 17:03
1598452412275752960  16777215   351919         2.10%          460   0               2019-08-05 17:19
1635240971829051392  16777215   1055656        6.29%          271   0               2019-08-05 08:31
1724681844702183425  3700000    1859791       50.26%           20   0               2019-07-11 19:33
1722901735378124801  2000000    1868996       93.45%           54   0               2019-07-01 15:00
1728227769702547457  2500000    2499817       99.99%            0   0               2019-08-04 23:42
1664184515930226688  1000000    0              0.00%          102   0               2019-08-05 18:08
1626448177341202433  2000000    1656571       82.83%          577   0               2019-08-04 21:34
1600103878740869120  16777215   221046         1.32%         1795   0               2019-08-05 08:00
```

## Config

lnt expects an `lnt` folder in your `~/` directory for config and storage purposes. If it does not find one, it will create it.

An example conf file:
```
[LND]
MacaroonPath = /home/arshbot/Projects/kubefiles/staging/readonly.macaroon
TlsCert = /home/arshbot/Projects/kubefiles/staging/tls.cert
Host = localhost:10009

[LNT]
# LND specific options to come soon!
```


## Contribution

If you'd like to implement one of the lacking features on the roadmap, you are welcome to do so. If you'd like to add a new feature, please open an issue for discussion. 

All commands must a verb noun pattern. For example: `lnt create payment` is the base command for all actions involving sending or paying over the lighting network. Currently there are only two verbs ( `create` and `view` ), each sharing the same 4 nouns ( `channel`, `invoice`, `rebalance`, `payment` ).

### Will there be a solution for rebalancing included in this tool?

Yes. However, it will not be an automatic rebalancer that is often seen in the space. I don't believe that the proper tool should be on autopilot as it'll end up fighting other similar tools attempting to rebalance in the opposite direction.

I believe the proper solution is to create ideal states that are executed once in a while on the user's discretion. A little bit more effort, but doesn't end up making the channel unusable for any forwarded payments. 

### Development

To set up this tool for your local development needs:

```
git clone --recursive https://github.com/arshbot/lnt.git
cd lnt
pipenv shell
pipenv install lnt/

# Here, you should attempt to run lnt from path. There might be an issue as I've only tested this on mac and linux
lnt --help
```

The protos included should be fine but sometimes get corrupted. To regenerate the protos:
```
# from the repo root
cd lnt
cd rpc

rm -rf .*

git clone https://github.com/googleapis/googleapis.git
curl -o rpc.proto -s https://raw.githubusercontent.com/lightningnetwork/lnd/master/lnrpc/rpc.proto
python -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. rpc.proto

# Run lnt after and debug, there are some python path issues that will come up that must be resolved. Make an issue if lost
```

