from Bio import SeqIO
try:
  from Bio.Alphabet import generic_dna
except ImportError: # Alphabet gone
  generic_dna = None

from Bio.Seq import Seq 
from Bio.SeqRecord import SeqRecord 
import inspect
import copy
import sys
import os
import re
from pathlib import Path
import csv
from collections import OrderedDict
from rich.progress import Progress
from rich import print as rprint

def get_mge_patterns(mge_file_path = None):
  """
  get_mge_patterns read text file with pattern match regular expressions and return a list of compiled regexs

  Args:
      mge_file_path (string, optional): path to custom mge_file_path. Defaults to None.
  
  Returns:
      string: A list of regex patterns as strings
  """

  if not mge_file_path:
    mge_file_path = os.path.join(os.path.dirname(__file__), "mge_patterns.txt")
  mge_patterns = []
  with open(mge_file_path) as mge_file:
    for line in mge_file.readlines():
      pattern = re.compile(line.rstrip())
      mge_patterns.append(pattern)
  return mge_patterns

def get_features(genome_file_path, file_format):
  """
  get_features get features from an annotated file

  Args:
      genome_file_path (string): path to annotated rich text sequence
      file_format (string): type of rich sequence genbank or embl

  Returns:
      list: A list of record features
  """
  record = SeqIO.read(genome_file_path, file_format)
  return record.features

def create_gff_line(accession, mge):
  """
  create_gff_line create a string formatted as a gff line

  Args:
      accession (string): The accession for the gff feature
      mge (dict): A dictionary containing mge features
  
  Returns
      string: A gff formatted line
  """
  description = mge['description']
  description_string = ';'.join([f'{match}="{",".join(description[match])}"' for match in description])
  return f'{accession}\t.\t{mge["type"]}\t{mge["start"]}\t{mge["end"]}\t.\t{mge["strand"]}\t.\t{description_string}\n'

def search_features_for_patterns(features, mge_patterns):
  """
  search_features_for_patterns search a list of features for those which contains MGE like annotations based on regexs

  Args:
      features (list): A list of Bio features
      mge_patterns (regex): A list of MGE regexs encoded as strings
  
  Returns:
      list: A list of MGEs extracted from the features encoded as dicts with keys
            * type
            * start
            * end
            * strand
            * description
  """
  mges = []
  for feature in features:
    qualifiers = OrderedDict()
    for qualifier in feature.qualifiers:
      if qualifier in ['product','note']:
          qualifiers[qualifier] = feature.qualifiers[qualifier]
    if len(qualifiers) > 0:
      matches = OrderedDict()
      for qualifier in qualifiers:
        for qualifier_value in qualifiers[qualifier]:
          for pattern in mge_patterns:
            if pattern.match(qualifier_value):
              if qualifier not in matches:
                matches[qualifier] = []
              matches[qualifier].append(qualifier_value)
      if len(matches) > 0:
        if feature.strand:
          if feature.strand == 1:
            strand = "+"
          elif feature.strand == -1:
            strand = "-"
        else:
          strand = "."
        mges.append(
          {
            "type": feature.type,
            "start": feature.location.start.position + 1,
            "end": feature.location.end.position,
            "strand": strand,
            "description": matches
          }
        )
  return mges

def find_mges(genome_file_path, file_format, mge_file_path = None):
  """
  find_mges find MGEs in a genome file

  Args:
      genome_file_path (string): path to a rich annotated genome file
      file_format (string): format of genome file, either genbank or embl
      mge_file_path (string, optional): Path to a file containing user custom MGE regexs. Defaults to None.

  Returns:
      list: A list of dicts with the keys: type, start, end, strand, description
  """
  features = get_features(genome_file_path, file_format)
  mge_patterns = get_mge_patterns(mge_file_path)
  mges = search_features_for_patterns(features, mge_patterns)
  return mges


def merge_mges(mges, merge_interval):
  """
  merge_mges Merge MGEs if they are in close proximity as defined by the merge_interval gap

  Args:
      mges (list): A list of MGEs dicts
      merge_interval (integer): A number representing the maximum distance two MGEs can be apart without merging them

  Returns:
      list: A list of merged MGE dicts with keys type, start, end, strand, description
  """
  previous_mge = {}
  merged_mge = { "type": None, "start": None, "end": None, "strand": None, "description": {}}
  number_mges_merged = 1
  merged_mges = []
  for mge in mges:
    if not previous_mge:
      previous_mge = mge
    else:
      # check if this mge should be merged with previous
      if mge['start'] - previous_mge['end'] <= merge_interval: # merge if less than interval
        if not merged_mge['start']:
          merged_mge['start'] = previous_mge['start']
        merged_mge['end'] = mge['end']
        if not merged_mge['strand']:
          merged_mge['strand'] = previous_mge['strand']
        if mge['strand'] != merged_mge['strand']:
            merged_mge['strand'] = '.'

        if not merged_mge['description']:
          merged_mge['description'] = copy.deepcopy(previous_mge['description'])
        # merge the descriptions
        for match in mge['description']:
          if match not in merged_mge['description']:
            merged_mge['description'][match] = []
          merged_mge['description'][match].extend(mge['description'][match])
        number_mges_merged += 1
      else:
        # check if a mge has been merged
        if merged_mge['start']:
          merged_mge['type'] = f"{number_mges_merged} merged features"
          merged_mges.append(merged_mge)
          # reset merged_mge
          merged_mge = { "type": None, "start": None, "end": None, "strand": None, "description": {}}
          number_mges_merged = 1
        else:
          merged_mges.append(previous_mge)
      previous_mge = mge
    
    # Final merge
  if merged_mge['start']:
    merged_mge['type'] = f"{number_mges_merged} merged features"
    merged_mges.append(merged_mge)
    # reset merged_mge
    merged_mge = { "type": None, "start": None, "end": None, "strand": None, "description": {}}
  else:
    merged_mges.append(previous_mge)

  return merged_mges
        

def create_mge_gff_file(genome_file_path, file_format, mges):
  """
  create_mge_gff_file Create a gff file containing putative MGE features

  Args:
      genome_file_path (string): path to a rich annotated genome file
      file_format (string): Format of the genome file. Either genbank or embl
      mges (list): A list of MGEs encoded as dicts with keys: type, start, end, strand, description

  Returns:
      string: path of the gff file created
  """
  record = SeqIO.read(genome_file_path, file_format)
  gff_file_path = Path(genome_file_path).with_suffix('.mge.gff')
  with open(gff_file_path, "w") as gff_file:
    for mge in mges:
      gff_file.write(create_gff_line(record.name, mge))
  return gff_file_path

def extract_position_ranges_from_gff_file(gff_file_path):
  """
  extract_position_ranges_from_gff_file extract ranges from a GFF file

  Args:
      gff_file_path (string): path to a GFF file containing MGE features

  Returns:
      list: A list of tuples where the first element of each tuple is the start position of a MGE and the second the end position
  """
  with open(gff_file_path) as gff_file:
    reader = csv.reader(gff_file, delimiter='\t')
    start_and_end_positions = []
    for row in reader:
      try:
        start_and_end_positions.append((int(row[3]), int(row[4])))
      except IndexError as error:
        sys.exit(f"{error}\n\nThe GFF file is not formatted correctly\nProblem with the line below. Please check tabs and the format\n{' '.join(row)}")
  return start_and_end_positions

def find_min_and_max_positions(positions):
  """
  find_min_and_max_positions Find the minimum and maximum position within a list of GFF positions encoded as tuples

  Args:
      positions (list): A lits of tuples where the MGE positions are encoded as (start_pos, end_pos)
  Returns:
    tuple: A tuple with the min_pos and end pos
  """
  min_pos = min([pos[0] for pos in positions])
  max_pos= max([pos[1] for pos in positions])
  return min_pos, max_pos

def check_alignment(alignment_length, gff_ranges):
  """
  check_alignment A function to check that none of the gff positions are outside of the alignment length

  Args:
      alignment_length (integer): length of the alignment
      gff_ranges (list): List of gff positions as tuples (start_pos, end_pos)
  """
  # get max position specified in the GFF file
  min_pos, max_pos = find_min_and_max_positions(gff_ranges)
  # check max pos doesn't exceed alignment length
  if alignment_length < max_pos:
    sys.exit(f'The maximum position {max_pos} specified in the GFF file exceeds the alignment length')

def get_fasta_length(fasta_path):
  """
  get_fasta_length Find the length of an alignment

  Args:
      fasta_path (string): path to the fasta alignment
  
  Returns
      integer: length of the alignment
  """
  with open(fasta_path) as input_alignment:
    current_sequence = ""
    for line in input_alignment:
      if line[0] == ">":
        if current_sequence != "":
          return(len(current_sequence)) # Multiple fasta sequence
        else: # first sequence
          next
      else:
        current_sequence += line.strip()
    return len(current_sequence) # Single fasta sequence

def get_number_of_sequences(fasta_path):
  """
  get_number_of_sequences Find number of sequences in a fasta alignment file

  Args:
      fasta_path (string): path to a fasta alignment
  
  Returns:
      int: number of sequences
  """

  sequences_text = open(fasta_path).read()
  number_of_sequences = sequences_text.count(">")
  return number_of_sequences

def mask_sequence(sequence, gff_ranges, masking_character):
  """
  mask_sequence Mask out a sequence with a masking character based on a list of gff positions encoded as (start_pos, end_pos) tuples

  Args:
      sequence (string): Sequence to be masked
      gff_ranges (list): A list of MGE positions in the alignment encoded as tuples
      masking_character (string): masking character, usually N

  Returns:
      string: The masked sequence as a string
  """
  for gff_range in gff_ranges:
    start = gff_range[0] -1
    end = gff_range[1]
    difference = end - start
    sequence = f'{sequence[:start]}{masking_character*difference}{sequence  [end:]}'
  return sequence

def write_masked_sequence(sequence, seq_id, gff_ranges, masking_character, output_alignment):
  """
  write_masked_sequence Write out a masked sequence to a file

  Args:
      sequence (string): masked sequence
      seq_id (string): id for the sequence record
      gff_ranges (list): A list of MGE positions in the alignment encoded as tuples
      masking_character (string): masking character, usually N
      output_alignment (file handle): handle to write masked sequences to
  """
  sequence = mask_sequence(sequence, gff_ranges, masking_character)
  if generic_dna: # deals with deprecate Alphabet
    record = SeqRecord(Seq(sequence, generic_dna), id=seq_id, description = "")
  else:
    record = SeqRecord(Seq(sequence), id=seq_id, description = "")

  output_alignment.write(record.format("fasta"))

def mask_mges(fasta_path, gff_file_path, masking_character):
  """
  mask_mges mask mges within an alignment file based on MGE positions encoded in a gff file

  Args:
      fasta_path (string): path to a fasta alignment with sequences to be masked
      gff_file_path (string): path to a GFF file containing positions of putative MGE features
      masking_character (string): masking character, usually N

  Returns:
      string: path to masked MGE file
  """
  # find length of pseudoalignment
  alignment_length = get_fasta_length(fasta_path)
  number_of_sequences = get_number_of_sequences(fasta_path)

  gff_ranges = extract_position_ranges_from_gff_file(gff_file_path)
  check_alignment(alignment_length, gff_ranges)

  rprint(f"Masking [bold red]{len(gff_ranges)}[/] regions in the alignment ([bold red]{number_of_sequences}[/] sequences, length [bold red]{alignment_length}[/])")
  masked_fasta_path = Path(fasta_path).with_suffix('.masked.fas') 
  with open(fasta_path) as input_alignment, open(masked_fasta_path, 'w') as output_alignment:
    sequence = []
    index = 0
    with Progress() as progress:
      masking_task = progress.add_task("[red]Masking sequences...", total=number_of_sequences)
      completed=-1
      for line in input_alignment:
        if line[0] == ">":
          completed +=1
          progress.update(masking_task, completed=completed)
          if sequence: # previous sequence finished
            write_masked_sequence("".join(sequence), seq_id, gff_ranges, masking_character, output_alignment)
            sequence = []
          seq_id = line.rstrip().replace(">", "")
        else:
          sequence.append(line.rstrip())
      write_masked_sequence("".join(sequence), seq_id, gff_ranges, masking_character, output_alignment)
  return masked_fasta_path
  

def print_default_regex_patterns():
  """
  print_default_regex_patterns print out the default MGE patterns pre-defined by the MGEmasker package
  """
  mge_file_path = os.path.join(os.path.dirname(__file__), "mge_patterns.txt")
  with open(mge_file_path) as mge_file:
    for line in mge_file.readlines():
      print(line.rstrip())


  