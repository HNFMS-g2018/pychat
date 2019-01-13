'change curse'

def cup(times):
    'set curse up [times] line'
    print('\033[{:d}A'.format(times), end='')

def cdown(times):
    'set curse down [times] line'
    print('\033[{:d}B'.format(times), end='')
