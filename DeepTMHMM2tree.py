### Boas Pucker ###
### b.pucker@tu-bs.de ###
### v0.3 ###

__cite__ = """Pucker, 2022: xxx """

__usage__ = """
					python3 DeepTMHMM2tree.py
					--tmr <TMR_GFF_FILE>
					--out <OUTPUT_FOLDER>
					
					optional:
					--info <INFO_FILE>
					--name <OUTPUT_FILE_NAME_PREFIX>
					
					bug reports and feature requests: b.pucker@tu-bs.de
					"""

import sys, os, re
from operator import itemgetter

# --- end of imports --- #

def load_deephmtmm_results( tmr_gff_file ):
	"""! @brief load DeepTMHMM results from GFF3 file """
	
	data = {}
	with open( tmr_gff_file, "r" ) as f:
		line = f.readline()
		while line:
			if line[0] != '#':
				parts = line.strip().split('\t')
				if len( parts ) > 1:
					if parts[1] == "TMhelix":
						add_helix = 1
					else:
						add_helix = 0
					try:
						data[ parts[0] ] += add_helix
					except KeyError:
						data.update( { parts[0]: add_helix } )
			line = f.readline()
	return data


def main( arguments ):
	"""! @brief run everything """
	
	tmr_gff_file = arguments[ arguments.index( '--tmr' )+1 ]
	output_folder = arguments[ arguments.index( '--out' )+1 ]
	
	if output_folder[-1] != "/":
		output_folder += "/"
	if not os.path.exists( output_folder ):
		os.makedirs( output_folder )
	
	if '--info' in arguments:
		info_file = arguments[ arguments.index( '--info' )+1 ]
		print( info_file )
		info = {}
		with open( info_file, "r" ) as f:
			line = f.readline()
			while line:
				parts = line.strip().split('\t')
				info.update( { parts[0]: parts[1] } )
				line = f.readline()
	else:
		info = {}
	
	if '--name' in arguments:
		ID = arguments[ arguments.index( '--name' )+1 ]
	else:
		ID = ""
	
	data = load_deephmtmm_results( tmr_gff_file )
	
	colors = [ "#3d85c6","#bcbcbc","#f44336","#00ff00","#E7872B","#5AAA46","#C43E96","#94221F","#171717","#72BEB7","#AA7A38","#E9C61D","#155289" ]
	
	
	# --- writing first output file --- #
	my_labels = []
	my_colors = []
	helix_factor_levels = sorted( list( set( data.values() ) ) )
	for factor in helix_factor_levels:
		my_colors.append( colors[ len( my_labels ) ] )
		my_labels.append( str( factor ) + "xTMhelix" )
	
	constant_lines = [ 	"DATASET_BINARY",
									"SEPARATOR COMMA",
									"DATASET_LABEL,TMhelix",
									"COLOR,#ff0000",
									"",
									"FIELD_SHAPES" + ",1"*len( my_labels ),
									"FIELD_LABELS," + ",".join( my_labels ),
									"FIELD_COLORS," + ",".join( my_colors ),
									"DATA"
								]
	
	output_file1 = output_folder + ID + "TMhelix.txt"
	with open( output_file1, "w" ) as out:
		out.write( "\n".join( constant_lines ) + "\n" )
		for key in list( data.keys() ):
			new_line = [ key.replace(".", "_").replace("(", "_").replace(")", "_") ]
			value = data[ key ]
			for factor in helix_factor_levels:
				if value == factor:
					new_line.append( "1" )
				else:
					new_line.append( "-1" )
			out.write( ",".join( new_line ) + "\n" )
	
	
	# --- writing second output file --- #
	colors = colors[::-1]	#invert list of colors
	my_labels = []
	my_colors = []
	info_factor_levels = sorted( list( set( info.values() ) ) )
	for factor in info_factor_levels:
		my_colors.append( colors[ len( my_labels ) ] )
		my_labels.append( str( factor ) )
	
	constant_lines = [ 	"DATASET_BINARY",
									"SEPARATOR COMMA",
									"DATASET_LABEL,clade",
									"COLOR,#ff0000",
									"",
									"FIELD_SHAPES" + ",2"*len( my_labels ),
									"FIELD_LABELS," + ",".join( my_labels ),
									"FIELD_COLORS," + ",".join( my_colors ),
									"DATA"
								]
	
	output_file2 = output_folder + ID + "clade.txt"
	with open( output_file2, "w" ) as out:
		out.write( "\n".join( constant_lines ) + "\n" )
		print( info_factor_levels )
		for key in list( data.keys() ):
			try:
				inf = info[ key ]
			except KeyError:
				try:
					inf = info[ key ]	#.replace(".", "_") 
				except KeyError:
					inf = "-"
					print( key )
			new_line = [ key.replace(".", "_").replace("(", "_").replace(")", "_") ]
			for factor in info_factor_levels:
				if inf == factor:
					new_line.append( "1" )
				else:
					new_line.append( "-1" )
			out.write( ",".join( new_line ) + "\n" )


if '--tmr' in sys.argv and '--out' in sys.argv:
	main( sys.argv )
else:
	sys.exit( __usage__ )
