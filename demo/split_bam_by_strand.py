#!/usr/bin/env python3

import os
import argparse

def get_args():
    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('bam', help='Input BAM file')
    p.add_argument("-o", "--output-prefix", help="Output prefix", default="split", dest="prefix")
    p.add_argument("--plus-minus-name", "-sn", nargs=2, default=["fwd", "rev"], help="Plus and minus strand names")
    p.add_argument("--libtype", "-l", choices=["RF", "FR", "R", "F"], required=True, help="Library type")
    p.add_argument("-t", "--threads", type=int, default=1, help="Number of threads")
    return p.parse_args()

def main():
    args = get_args()
    plus, minus = args.plus_minus_name
    if args.libtype == "F":
        cmd = f"""samtools view -@ {args.threads} -b -F 16 -o {args.prefix}.{plus}.bam {args.bam} && samtools index {args.prefix}.{plus}.bam && \
                samtools view -@ {args.threads} -b -f 16 -o {args.prefix}.{minus}.bam {args.bam} && samtools index {args.prefix}.{minus}.bam
                """
    elif args.libtype == "R":
        cmd = f"""samtools view -@ {args.threads} -b -f 16 -o {args.prefix}.{plus}.bam {args.bam} && samtools index {args.prefix}.{plus}.bam && \
                samtools view -@ {args.threads} -b -F 16 -o {args.prefix}.{minus}.bam {args.bam} && samtools index {args.prefix}.{minus}.bam"""
    elif args.libtype == "FR":
        cmd = f"""
               samtools view  -@ {args.threads} -b -f 128 -F 16 -o {args.prefix}.{minus}.1.bam {args.bam} && samtools index {args.prefix}.{minus}.1.bam && \
               samtools view  -@ {args.threads} -b -f 64 -F 32 -o {args.prefix}.{minus}.2.bam {args.bam} && samtools index {args.prefix}.{minus}.2.bam && \
               samtools merge -@ {args.threads} -f {args.prefix}.{minus}.bam {args.prefix}.{minus}.1.bam {args.prefix}.{minus}.2.bam && rm {args.prefix}.{minus}.1.bam {args.prefix}.{minus}.2.bam && \
               samtools index -@ {args.threads} {args.prefix}.{minus}.bam && \
               samtools view  -@ {args.threads} -b -f 144 -o {args.prefix}.{plus}.1.bam {args.bam} && samtools index {args.prefix}.{plus}.1.bam && \
               samtools view  -@ {args.threads} -b -f 96 -o {args.prefix}.{plus}.2.bam {args.bam} && samtools index {args.prefix}.{plus}.2.bam && \
               samtools merge -@ {args.threads} -f {args.prefix}.{plus}.bam {args.prefix}.{plus}.1.bam {args.prefix}.{plus}.2.bam && rm {args.prefix}.{plus}.1.bam {args.prefix}.{plus}.2.bam && \
               samtools index -@ {args.threads} {args.prefix}.{plus}.bam
               """
    elif args.libtype == "RF":
        cmd = f"""
               samtools view  -@ {args.threads} -b -f 128 -F 16 -o {args.prefix}.{plus}.1.bam {args.bam} && samtools index {args.prefix}.{plus}.1.bam && \
               samtools view  -@ {args.threads} -b -f 64 -F 32 -o {args.prefix}.{plus}.2.bam {args.bam} && samtools index {args.prefix}.{plus}.2.bam && \
               samtools merge -@ {args.threads} -f {args.prefix}.{plus}.bam {args.prefix}.{plus}.1.bam {args.prefix}.{plus}.2.bam && rm {args.prefix}.{plus}.1.bam {args.prefix}.{plus}.2.bam && \
               samtools index -@ {args.threads} {args.prefix}.{plus}.bam && \
               samtools view  -@ {args.threads} -b -f 144 -o {args.prefix}.{minus}.1.bam {args.bam} && samtools index {args.prefix}.{minus}.1.bam && \
               samtools view  -@ {args.threads} -b -f 96 -o {args.prefix}.{minus}.2.bam {args.bam} && samtools index {args.prefix}.{minus}.2.bam && \
               samtools merge -@ {args.threads} -f {args.prefix}.{minus}.bam {args.prefix}.{minus}.1.bam {args.prefix}.{minus}.2.bam && rm {args.prefix}.{minus}.1.bam {args.prefix}.{minus}.2.bam && \
               samtools index -@ {args.threads} {args.prefix}.{minus}.bam
               """
        
        # """
        # samtools view -b -f 128 -F 16 $DATA > fwd1.bam
        # samtools index fwd1.bam

        # samtools view -b -f 64 -F 32 $DATA > fwd2.bam
        # samtools index fwd2.bam

        # samtools view -b -f 144 $DATA > rev1.bam
        # samtools index rev1.bam

        # samtools view -b -f 96 $DATA > rev2.bam
        # samtools index rev2.bam
        # """
    os.system(cmd)

        
        
        
        
        
if __name__ == "__main__":
    main()
