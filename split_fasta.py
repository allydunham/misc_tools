#!/usr/bin/env python3
"""
Script to split a fasta file down into single sequence files named based on the seq name
"""
import argparse
import os

from Bio import SeqIO

def main(args):
    """Main script"""
    for seq in SeqIO.parse(args.fasta, 'fasta'):
        filename = '{}.fa'.format(seq.id).lower()
        if not os.path.isfile(filename) or check_continue(message='{} already exists. Overwrite?'.format(filename)):
            SeqIO.write(seq, filename, 'fasta')

def check_continue(message=''):
    """Ask user for yes no confirmation"""
    user_input = input(' '.join([message, '[Yes/No]'])).lower()
    if user_input in ('y', 'yes'):
        return True
    elif user_input in ('n', 'no'):
        return False
    else:
        return check_continue(message=message)

def parse_args():
    """Process input arguments"""
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('fasta', metavar='F', help="Input fasta file")

    return parser.parse_args()

if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)
