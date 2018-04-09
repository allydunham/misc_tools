#!/usr/bin/env python3
"""
Script to split VCF file into smaller subsections
"""
import argparse
import fileinput
import os

def main(args):
    """Main script"""
    if args.entries <= 0:
        raise ValueError("Entries argument must be positive")

    # Collect header
    with fileinput.input(args.vcf) as vcf_file:
        header = []
        for line in vcf_file:
            if line[0] == '#':
                # collect header lines
                header.append(line)
            else:
                break

        header = ''.join(header)

    # Split vcf records
    with fileinput.input(args.vcf) as vcf_file:
        file_count = 0
        path = '/'.join(args.out.split('/')[-1])
        os.makedirs(path, exist_ok=True)
        outfile = open(''.join((args.out, '.', str(file_count), '.vcf')), mode='w')
        entry_count = 0
        outfile.write(header)

        for line in vcf_file:
            if line[0] == '#':
                continue

            elif entry_count >= args.entries:
                file_count += 1
                outfile = open(''.join((args.out, '.', str(file_count), '.vcf')), mode='w')
                outfile.write(header)
                outfile.write(line)
                entry_count = 1

            else:
                outfile.write(line)
                entry_count += 1




def parse_args():
    """Process input arguments"""
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('vcf', metavar='V', help="VCF file to split")

    parser.add_argument('--entries', '-e', default=10000, type=int,
                        help="Number of entries per file")

    parser.add_argument('--out', '-o', default='split',
                        help="Output file prefix")

    return parser.parse_args()

if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)
