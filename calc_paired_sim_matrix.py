### Boas Pucker ###
### b.pucker@tu-bs.de ###
### v0.11 ###

__usage__ = """
						python3 calc_paired_sim_matrix.py
						--in <INPUT_FILE>
						--out <OUTPUT_FOLDER>
						
						optional:
						--aln <ALIGNMENT_TOOL>[mafft](mafft|muscle)
						--mafft <PATH_TO_MAFFT>
						--muscle <PATH_TO_MUSCLE>
						"""

import os, sys, glob, subprocess

# --- end of imports --- #


def load_sequences( fasta_file ):
	"""! @brief load candidate gene IDs from file """
	
	sequences = {}
	with open( fasta_file ) as f:
		header = f.readline()[1:].strip()
		if " " in header:
			header = header.split(' ')[0]
		seq = []
		line = f.readline()
		while line:
			if line[0] == '>':
					sequences.update( { header: "".join( seq ) } )
					header = line.strip()[1:]
					if " " in header:
						header = header.split(' ')[0]
					seq = []
			else:
				seq.append( line.strip() )
			line = f.readline()
		sequences.update( { header: "".join( seq ) } )	
	return sequences


def calc_aln_sim( aln_file ):
	"""! @brief calculate alignment similarity """
	
	alignment = load_sequences( aln_file )
	aln_seq1 = list( alignment.values() )[0]
	aln_seq2 = list( alignment.values() )[1]
	matches = 0
	for k, aa in enumerate( aln_seq1 ):
		if aa == aln_seq2[ k ]:
			matches += 1
	return matches / ( float( len( aln_seq1.replace("-", "") ) + len( aln_seq2.replace("-", "") ) ) / 2.0 )


def main( arguments ):
	"""! @brief run everything """
	
	input_file = arguments[ arguments.index('--in')+1 ]
	output_folder = arguments[ arguments.index('--out')+1 ]
	
	if '--aln' in arguments:
		alignment_method = arguments[ arguments.index('--aln')+1 ]
		if not alignment_method in [ "mafft", "muscle" ]:
			alignment_method = "mafft"
	else:
		alignment_method = "mafft"
	
	if '--mafft' in arguments:
		mafft = arguments[ arguments.index('--mafft')+1 ]
	else:
		mafft = "mafft"
	
	if '--muscle' in arguments:
		muscle = arguments[ arguments.index('--muscle')+1 ]
	else:
		muscle = "muscle"
	
	if output_folder[ -1 ] != "/":
		output_folder += "/"
	
	if not os.path.exists( output_folder ):
		os.makedirs( output_folder )
	
	seqs = load_sequences( input_file )
	
	final_output_file = output_folder + "SEQUECE_SIMILARITY_MATRIX.txt"
	seq_names = list( seqs.keys() )
	data = {}
	with open( final_output_file, "w" ) as final_out:
		final_out.write( "\t".join( [ "SequenceNames" ] + seq_names ) + "\n" )
		for idx1, key1 in enumerate( seq_names ):
			new_line = [ key1 ]
			for idx2, key2 in enumerate( seq_names ):
				if idx2 > idx1:
					aln_input_file = output_folder + key1.replace("@", "") + "_%_" + key2.replace("@", "") + ".fasta"
					aln_file = aln_input_file + ".aln"
					if not os.path.isfile( aln_file ):	#check if alignment file is not already present
						# --- generate sequence file --- #
						with open( aln_input_file, "w" ) as out:
							out.write( '>' + key1 + "\n" + seqs[ key1 ] + "\n>" + key2 + "\n" + seqs[ key2 ] + "\n" )
						
						# --- generate alignment --- #
						if alignment_method == "mafft":
							p = subprocess.Popen( args= mafft + " " + aln_input_file + " > " + aln_file, shell=True )
							p.communicate()
						else:
							p = subprocess.Popen( args= muscle + " -align " + aln_input_file + " -output " + aln_file, shell=True )
							p.communicate()
						os.remove( aln_input_file )
					# --- calculate sequence similarity based on alignment --- #
					sim = calc_aln_sim( aln_file )
					new_line.append( sim )
					data.update( { key1 + "_%_" + key2: sim } )
				elif idx2 == idx1:
					new_line.append( 0 )
				else:
					sim = data[ key2 + "_%_" + key1 ]
					new_line.append( sim )
			final_out.write( "\t".join( list( map( str, new_line ) ) ) + "\n" )


if '--in' in sys.argv and '--out' in sys.argv:
	main( sys.argv )
else:
	sys.exit( __usage__ )
