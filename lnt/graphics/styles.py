from PyInquirer import style_from_dict, Token, prompt, Separator
from lnt.graphics.utils import vars_to_string

# Mark styles
prompt_style = style_from_dict({
    Token.Separator: '#6C6C6C',
    Token.QuestionMark: '#FF9D00 bold',
    #Token.Selected: '',  # default
    Token.Selected: '#5F819D',
    Token.Pointer: '#FF9D00 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#5F819D bold',
    Token.Question: '',
})


# Mark prompt configurations
def get_channel_choice_from(channels):

    choices = [ {'name' : vars_to_string(c_id, c['local_balance'], c['remote_balance'], nick=None) } for c_id, c in channels.items() ]

    validate = lambda answer: 'You must choose at least one channel' if len(answer) == 0 else True

    return {
        "type" : "checkbox",
        "qmark": "⚡️",
        "message" : "CHOOSE FROM nick, channel id, local_balance, remote_balace, graphic",
        "name" : "channel_choices_from",
        "choices" :  choices,
        "validate" : validate,
    }

def get_channel_choice_to(channels):


    choices = [ {'name' : vars_to_string(c_id, c['local_balance'],
        c['remote_balance'], nick=None) } for c_id, c in channels.items() ]

    return {
        'type': 'list',
        'message': 'CHOOSE TO nick, channel id, local_balance, remote_balace, graphic',
        "name" : "channel_choices_to",
        'choices': choices
    }

