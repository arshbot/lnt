def construct_rebalance_image(channels, from_channels, to_channel):
    rebase_image = ""

    for from_c in from_channels:
        rebase_image += "{}:{} -> {},\n".format(channels[from_c]["local_balance"], from_c, to_channel)
    return rebase_image

def write_rebalance_image():

    if True: # TODO: Add naming option
        # TODO: Better random naming
        rebal_name = sha1(str(channels).encode('utf8')).digest().hex()[:20] + ".rebal"

    with open(LNT_DIR_REBAL+"/"+rebal_name, 'w') as f:
        f.write(rebase_image)
    return
