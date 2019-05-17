from PyInquirer import style_from_dict, Token, prompt, Separator

def ratio_graphic(local, remote):
    total = local + remote
    local_ratio = int((round(local/total, 1) * 10) / 2)
    remote_ratio = int((round(remote/total, 1) * 10) / 2)

    return local_ratio * "🁢" + ( (5 - local_ratio) * "-" )  + ( (5 - remote_ratio) * "-" ) + remote_ratio * "🁢"

def vars_to_string(chan_id, local_balance, remote_balance, nick=None):
    total_balance = local_balance + remote_balance
    nick = "-" if nick == None else nick
    # TODO, pretty this up -> https://stackoverflow.com/a/9996049/5838056
    return "{}, {}, {}, {}, {}".format(nick, chan_id, local_balance,
            remote_balance, ratio_graphic(local_balance, remote_balance))
