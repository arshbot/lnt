#!/usr/bin/python

import argparse


parser = argparse.ArgumentParser(description="Create some ish")

parser.add_argument('string', metavar='[ object ]', help="objects like channels, opayment, invoice, rebal")
print(parser.parse_args())

