### Boas Pucker ###
### b.pucker@tu-bs.de ###

__version__ = "v0.1"

__reference__ = "Pucker, 2023"

__usage__ = """
					Motif scanner  """ + __version__ + """("""+ __reference__ +""")
					
					Usage:
					python3 motif_scanner.py
					--motif <MOTIF_INPUT_FILE>
					--seq <SEQ_INPUT_FILE>
					--out <OUTPUT_FILE>
				
					bug reports and feature requests: b.pucker@tu-bs.de
					"""

import os, sys, re

# --- end of imports --- #

def load_sequences( fasta_file ):
	"""! @brief load candidate gene IDs from file """
	
	sequences = {}
	with open( fasta_file ) as f:
		header = f.readline()[1:].strip()
		seq = []
		line = f.readline()
		while line:
			if line[0] == '>':
					sequences.update( { header: "".join( seq ) } )
					header = line.strip()[1:]
					seq = []
			else:
				seq.append( line.strip() )
			line = f.readline()
		sequences.update( { header: "".join( seq ) } )	
	return sequences


def load_motifs( motif_file ):
	"""! @brief load all motifs from given file """
	
	motifs, motif_names = [], []
	with open( motif_file, "r" ) as f:
		line = f.readline()
		while line:
			parts = line.strip().split('\t')
			if len( parts ) == 2:
				motifs.append( { 'id': parts[0], 'seq': parts[1].replace("/", "").replace("]", "]{1}") } )
				motif_names.append( parts[0] )
			line = f.readline()
	return motifs, motif_names


def main( arguments ):
	"""! @brief run everything """
	
	motif_file = arguments[ arguments.index('--motif')+1 ]
	seq_input_file = arguments[ arguments.index('--seq')+1 ]
	output_file = arguments[ arguments.index('--out')+1 ]
	
	motifs, motif_names = load_motifs( motif_file )
	seqs = load_sequences( seq_input_file )
	
	with open( output_file, "w" ) as out:
		out.write( "seqID\t" + "\t".join( motif_names ) + "\n" )
		for key in sorted( list( seqs.keys() ) ):	#iterate over all sequences
			current_seq = seqs[ key ]
			new_line = [ key ]	#collect match status for each motif
			for entry in motifs:	#iterate over all motifs
				x = re.compile( entry['seq'] )
				print( entry['seq'] )
				try:
					hit_pos = x.search( current_seq ).end()
					current_seq = current_seq[ hit_pos: ]	#clip off sequence to ensure that motifs are only detected in the correct order
					new_line.append( "1" )
				except AttributeError:
					new_line.append( "0" )
			out.write( "\t".join( new_line ) + "\n" )


if '--motif' in sys.argv and '--seq' in sys.argv and '--out' in sys.argv:
	main( sys.argv )
else:
	sys.exit( __usage__ )
