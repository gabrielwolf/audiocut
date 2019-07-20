import os
import errno
import argparse
import scipy.io.wavfile
import re
from timecode import is_timecode
from timecode import timecode_to_samples
from timecode import validate_parameters

# ==== command line arguments and help ====

parser = argparse.ArgumentParser()
parser.add_argument("input", help="wav file that has to be cut", type=str)
parser.add_argument("start_time", help="Timecode in the form of hh:mm:ss:f where f is a float >= 0 and < 1 (e.g. 0.5)",
                    type=str)
parser.add_argument("end_time", help="Timecode in the form of hh:mm:ss:f where f is a float >= 0 and < 1 (e.g. 0.5)",
                    type=str)
parser.add_argument("regular_chunk_length",
                    help="Timecode in the form of hh:mm:ss:f where f is a float >= 0 and < 1 (e.g. 0.5)", type=str)
parser.add_argument("-v", "--verbosity", action="count", help="increase output verbosity")
args = parser.parse_args()


# ==== file handling ====

file_name = args.input
file_name_base = re.findall('(.+).wav', file_name)

try:
    file_handler = scipy.io.wavfile.read(file_name)
except OSError:
    print('Sorry, file -', file_name, '- could not be opened. Exiting.')
    quit()


# ==== parameter testing

start_time = args.start_time
end_time = args.end_time
regular_chunk_length = args.regular_chunk_length

if not is_timecode(start_time) or not is_timecode(end_time) or not is_timecode(regular_chunk_length):
    print('Sorry, a Timecode was not well formed. Exiting.')
    quit()

sample_rate = file_handler[0]
total_time_of_input_file = len(file_handler[1])
total_time_of_all_chunks = timecode_to_samples(end_time, sample_rate) - timecode_to_samples(start_time, sample_rate)

if total_time_of_input_file - timecode_to_samples(end_time, sample_rate) < 0:
    print("Sorry, the end_time seems to be longer than the wav file itself. Exiting.")
    quit()

validate_parameters(file_name, file_handler[0], start_time, end_time, regular_chunk_length)


# ==== the algorithm ====

start_time = timecode_to_samples(start_time, sample_rate)
end_time = timecode_to_samples(end_time, sample_rate)
regular_chunk_length = timecode_to_samples(regular_chunk_length, sample_rate)

total_count_of_regular_chunks = int(total_time_of_all_chunks / regular_chunk_length)

chunks = []
first_chunk = (start_time, start_time + regular_chunk_length)
chunks.append(first_chunk)
chunk_count = 1

while chunk_count < total_count_of_regular_chunks:
    chunk = (chunks[chunk_count - 1][1], chunks[chunk_count - 1][1] + regular_chunk_length)
    chunks.append(chunk)
    chunk_count = chunk_count + 1

# if chunks don't fit regularly, calculate the remaining part
if chunks[chunk_count - 1][1] < start_time + total_time_of_all_chunks:
    chunk = (chunks[chunk_count - 1][1], start_time + total_time_of_all_chunks)
    chunks.append(chunk)
    chunk_count = chunk_count + 1

if args.verbosity == 2:
    print(chunks)


# ==== write everything to disk ====

def create_sub_folder(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    return path


sub_folder = create_sub_folder(str(file_name + '-cut'))

for chunk in range(len(chunks)):
    start_time = chunks[chunk][0]
    end_time = chunks[chunk][1]

    out_file_name = '{0}-{1:010d}-{2:010d}.wav'.format(file_name_base[0], start_time, end_time)
    out_file_name = os.path.join(sub_folder, out_file_name)

    try:
        scipy.io.wavfile.write(out_file_name, sample_rate, file_handler[1][start_time:end_time])
        if args.verbosity == 1 or args.verbosity == 2:
            print(out_file_name)
    except OSError:
        print('Sorry, file ', out_file_name, ' could not be written.')
        quit()

print(chunk_count, 'files have been written.')
quit()
