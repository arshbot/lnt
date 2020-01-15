# lnt

Lightning Network Tools (lnt) is a toolset for interacting and managing your [lnd](https://github.com/lightningnetwork/lnd) node.

## Installation

Python 3.6 required

From source:

```
git clone --recursive https://github.com/thesis/lnt.git
cd lnt
python setup.py install
```

From Pypi: 

```
pip3 install lnt
```

### Config setup

lnt expects an admin macaroon and tls cert in the default **testnet** LND path locations. If your LND dirs are different, or you want to use this against mainnet, take a look at the config section below.

## Feature progress

- [x] View channels
- [x] Forwarding events input into view channel output
- [x] Add alias info to view channel output
- [x] Add sorting options to view channel output
- [x] Kill channel
- [ ] Kill zombie channels
- [ ] View invoices
- [ ] View payments
- [ ] View payments by last node in hop
- [ ] Create channel
- [ ] Create invoice
- [ ] Send payment

## Usage

View channels with sorting options

```
$ lnt view channel --max local/cap  

CHANNEL_ID           CAPACITY    LOCAL_BAL  LOCAL/CAP   FORWARDS   PENDING_HTLCS   LAST_USED          CHANNELS_W/_PEER   ALIAS
1631776410691960832  10000000    7419528       74.20%   0          0               2019-11-19 19:25   1                  
1715412961679638528  6211145     2387442       38.44%   0          0               2019-11-12 13:57   1                  
1732367430983155712  3000000     879679        29.32%   0          0               2019-08-23 20:39   1                  023a0c37a419776aca94
1767994906258309120  2087056925  1684500        0.08%   0          0               2019-11-21 05:04   1                  0270685ca81a8e4d4d01
1663766701515276289  30915126    0              0.00%   0          0               2019-04-29 14:00   1                  BakimonoLND
1741923286541336577  1761156214  51588          0.00%   0          0               2019-11-18 17:19   1                  WagOne
1733044730145341441  1000000     0              0.00%   0          0               2019-08-28 04:33   1                  03ade33d362ecb7a62bdd
1767997105277960193  18239461648 0              0.00%   0          0               2019-11-21 08:51   1                  aranguren.org
1742018944049741825  14401836    0              0.00%   0          0               2019-11-19 02:15   1                  CALL_OF_KTULU [LND]
1601870793929588736  25838893    0              0.00%   0          0               2019-02-23 18:34   1                  LN Testnet node
1709436016472031232  718165815   0              0.00%   0          0               2019-07-03 00:50   1                  Fireduck test
1736929304724045825  5000000     0              0.00%   0          0               2019-11-12 13:57   1                  
1601807022252032001  16777215    0              0.00%   0          0               2019-11-12 13:57   1                  
1660159203848814593  47740049    0              0.00%   0          0               2019-08-11 15:04   1                  MOONLAMBO
1631303620691951617  5100421     0              0.00%   0          0               2019-03-06 14:33   1                  SNONAS  
```

Kill channel by channel id ( force close )

```
$ lnt kill channel --id 1601807022252032001 -f

Closing Tx Confirming: 8cd225cac4871085580223cfc92b3b4658964d19b60075f3cfef4169e46f1759
View it here: https://blockstream.info/testnet/8cd225cac4871085580223cfc92b3b4658964d19b60075f3cfef4169e46f1759
```

## Config

lnt expects an `lnt` folder in your `~/` directory for config and storage purposes. If it does not find one, it will create it.

**Mainnet Usage:** If you have LND installed in the standard way, simply replace `testnet` in the default path with `mainnet`. If your LND installation is a bit custom, replace the `MacaroonPath` and `TlsCert` as needed. Be sure to set [LNT] Testnet to `False`.

An example conf file:
```
[LND]
MacaroonPath = /home/arshbot/Projects/kubefiles/staging/readonly.macaroon
TlsCert = /home/arshbot/Projects/kubefiles/staging/tls.cert
Host = localhost:10009

[LNT]
Testnet = True
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
git clone --recursive https://github.com/thesis/lnt.git
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

