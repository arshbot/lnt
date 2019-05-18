from hashlib import sha1
from lnt import constants

def construct_rebalance_image(channels, from_channels, to_channel, max=False):
    rebase_image = ""

    for from_c in from_channels:
        value_to_rebal = channels[from_c]["local_balance"]
 
        if max:
            value_to_rebal = "MAX"

        rebase_image += "{}:{} -> {},\n".format(value_to_rebal, from_c, to_channel)

    return rebase_image

def write_rebalance_image(image, name=None):

    if name:
        rebal_name = name + ".rebal"
    else:
        rebal_name = sha1(str(image).encode('utf8')).digest().hex()[:20] + ".rebal"

    with open(constants.DEFAULT_REBAL_PATH+"/"+rebal_name, 'w') as f:
        f.write(image)
    return

def parse_rebalanace_image(image):
    return

def perform_rebalance(image):
   return 
