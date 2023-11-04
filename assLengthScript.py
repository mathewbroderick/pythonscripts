#!/local/cluster/bin/python

import sys
from Bio import SeqIO

fastaFiles = sys.argv[1:]

outputFile = "assemblyLen.txt"

with open(outputFile, "w") as outFile:
	for i in fastaFiles:
		totalLen = 0

		for j in SeqIO.parse(i, "fasta"):
			totalLen += len(j.seq)

		outFile.write("{}: {} bp\n".format(i, totalLen))


