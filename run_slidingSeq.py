# AUTHOR: Apiwat Sangphukieo
# github: https://github.com/asangphukieo

import os,sys
import argparse

import re

def sliding(seq,winSize,step):
	
	read_line_seq=seq.split('>')
	del read_line_seq[0]
	for each_seq in read_line_seq:
		seq_line=each_seq.split('\n')
		#print seq_line
		sequence =seq_line[1]

		# Verify the inputs
		try: it = iter(sequence)
		except TypeError:
			raise Exception("**ERROR** sequence must be iterable.")
		if not ((type(winSize) == type(0)) and (type(step) == type(0))):
			raise Exception("**ERROR** type(winSize) and type(step) must be int.")
		if step > winSize:
			raise Exception("**ERROR** step must not be larger than winSize.")
		if winSize > len(sequence):
			raise Exception("**ERROR** winSize must not be larger than sequence length.")
	 
		# Pre-compute number of chunks to emit
		numOfChunks = ((len(sequence)-winSize)/step)+1
		
		# Do the work
		n=1
		
		out_file=open("out_sliding.fasta",'a')
		
		for i in range(0,numOfChunks*step,step):
			out_file.write(">"+seq_line[0]+"   "+str(n)+"   "+str(i)+" to "+str(i+winSize)+'\n'+sequence[i:i+winSize]+'\n')
			
			n=n+1
		out_file.close()
	
def main(args=None):
	parser = argparse.ArgumentParser(description='add file name, window size, and step,folder')
	parser.add_argument('-f', '--seqFile',help='Input file', required='True',default='None')
	parser.add_argument('-w', '--winSize',help='window size', required='True',default='120')
	parser.add_argument('-s', '--step',help='step size', required='True',default='40')
	parser.add_argument('-p', '--path',help='tmp folder', required='True',default='./tmp/')
	Input = parser.parse_args(args)

	seqFile=Input.seqFile
	winSize=int(Input.winSize)
	step=int(Input.step)
	path=Input.path
	
	#if input file ismultiple line fasta
	os.system("perl fasta1line.pl "+path+seqFile+" "+path+"one_line.fasta")
	
	out_file=open("out_sliding.fasta",'w')
	out_file.write("")
	out_file.close()
	
	one_line_file=open(path+"one_line.fasta",'r')
	one_line_read=one_line_file.read()
	one_line_file.close()
	
	sliding(one_line_read,winSize,step) 
	


if __name__ == '__main__':
	main(sys.argv[1:])
	
	
#os.system("perl fasta1line.pl sliding_file.fasta one_line.fasta")
#os.system("python SlideGenome.py -f 'one_line.fasta' -w 200 -s 100 >log")
#Usage: python run_slidingSeq.py -f 'sequence.fasta' -w 200 -s 100 -p './'

