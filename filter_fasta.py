#!/usr/bin/env python3
"""
Script to extract specific regions from a fasta file

ToDo
- Currently very makeshift chromosome/seq name identifying
"""
import argparse
import fileinput
import textwrap

from Bio import SeqIO

def main(args):
    """Main script"""

    ## Import loci to identify
    loci = {}
    with fileinput.input(args.bed) as bed:
        next(bed)
        for i in bed:
            i = i.strip().split()
            if not i[0] in loci.keys():
                loci[i[0]] = {i[3]:(int(i[1]), int(i[2]), i[5])}
            else:
                loci[i[0]][i[3]] = (int(i[1]), int(i[2]), i[5])

    for seq in SeqIO.parse(args.fasta, 'fasta'):
        chrom = seq.id.split('.')[1]
        if chrom in loci.keys():
            for name, loc in loci[chrom].items():
                sub_seq = seq.seq[loc[0]-1 - args.pad: loc[1] + args.pad]
                print('>', args.id, '_', name, sep='')
                print(*textwrap.wrap(str(sub_seq), width=80), sep='\n')


def parse_args():
    """Process input arguments"""
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('fasta', metavar='F', help="Fasta formatted input file")

    parser.add_argument('--bed', '-b', help='Bed formatted file containing regions to filter to')

    parser.add_argument('--pad', '-p', default=0, type=int,
                        help='Number of base pairs to pad on either end')

    parser.add_argument('--id', '-i', default='', type=str, help='ID to append to all output names')

    return parser.parse_args()

if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)
