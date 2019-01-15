'deal with args'
import argparse

def init():
    'init arguments'
    parser = argparse.ArgumentParser(description='this is help')
    parser.add_argument('-r', '--register', action='store_true', help='register a user')
    parser.add_argument('-l', '--login', action='store_true', help='login a user')
    parser.add_argument('-d', '--debug', action='store_true', help='use debug chat room')
    return parser.parse_args()
