### Boas Pucker ###
### b.pucker@tu-bs.de ###
### v0.1 ###

__cite__ = """Pucker, 2022: xxx """

__usage__ = """
					python3 fastaClades2info.py
					--fasta <FASTA_FILE_FOLDER>
					--out <OUTPUT_FILE>
					
					bug reports and feature requests: b.pucker@tu-bs.de
					"""

import sys, os, re, glob

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


def main( arguments ):
	"""! @brief run everything """
	
	fasta_file_folder = arguments[ arguments.index( '--fasta' )+1 ]
	output_file = arguments[ arguments.index( '--out' )+1 ]
	
	fasta_files = glob.glob( fasta_file_folder + "*.fasta" )
	with open( output_file, "w" ) as out:
		for filename in fasta_files:
			ID = filename.split('/')[-1].split('.fasta')[0]
			seqs = load_sequences( filename )
			for key in list( seqs.keys() ):
				# if key[-1] in "0123456789":
					# underscore_positions = [ x.start() for x in re.finditer( '_', key ) ]
					# if len( underscore_positions ) > 0:
						# if key[-2:] == "_1":
							# key = key[ :underscore_positions[ -3 ] ] + "@" + key[ underscore_positions[ -3 ]+1: ]
						# else:	
							# key = key[ :underscore_positions[ -1 ] ] + "@" + key[ underscore_positions[ -1 ]+1: ]
				out.write( key + "\t" + ID + "\n" )


if '--fasta' in sys.argv and '--out' in sys.argv:
	main( sys.argv )
else:
	sys.exit( __usage__ )
