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
parser.add_argument("input", help="wav file that has to be cut",
                    type=str)
parser.add_argument("starttime", help="timecode in the form of hh:mm:ss:f where f is a float >= 0 and < 1 (e.g. 0.5)",
                    type=str)
parser.add_argument("endtime", help="timecode in the form of hh:mm:ss:f where f is a float >= 0 and < 1 (e.g. 0.5)",
                    type=str)
parser.add_argument("chunklength", help="timecode in the form of hh:mm:ss:f where f is a float >= 0 and < 1 (e.g. 0.5)",
                    type=str)
parser.add_argument("-v", "--verbosity", action="count",
                    help="increase output verbosity")
args = parser.parse_args()


# ==== stuff ====

# handy variable names, file check and validation of all arguments
fname = args.input
fnamebase = re.findall('(.+).wav',fname)

try:
    fhand = scipy.io.wavfile.read(fname)
except:
    print('Sorry, file -',fname,'- could not be opened. Exiting.')
    quit()

starttime = args.starttime
endtime = args.endtime
chunklength = args.chunklength

if not is_timecode(starttime) or not is_timecode(endtime) or not is_timecode(chunklength):
    print('Sorry, a timecode was not well formed. Exiting.')
    quit()

smprate = fhand[0]
filelength = len(fhand[1])
duration = timecode_to_samples(endtime, smprate) - timecode_to_samples(starttime, smprate)

if filelength - timecode_to_samples(endtime, smprate) < 0:
    print("Sorry, the endtime seems to be longer than the wav file itself. Exiting.")
    quit()

validate_parameters(fname, fhand[0], starttime, endtime, chunklength)


# ==== the algorithm ====

# from now on we calculate in samples.
starttime = timecode_to_samples(starttime, smprate)
endtime = timecode_to_samples(endtime, smprate)
chunklength = timecode_to_samples(chunklength, smprate)

# total number of chunks that have full chunklength
totalfullchunks = int(duration / chunklength)
# print('Debug -- totalfullchunks:',totalfullchunks)

# list for all chunks
chunks = []

# chunk as tuple with starttime and endtime
chunk = (0, 0)

# write the first chunk
chunk = (starttime, starttime + chunklength)
chunks.append(chunk)

# write remaining chunks with full chunklength
chunkcount = 1
while chunkcount < totalfullchunks:
    chunk = (chunks[chunkcount-1][1], chunks[chunkcount-1][1] + chunklength)
    chunks.append(chunk)
    chunkcount = chunkcount + 1

# write the remaining portion as an additional chunk, if it doesn't fit
if chunks[chunkcount-1][1] < starttime + duration:
    chunk = (chunks[chunkcount-1][1], starttime + duration)
    chunks.append(chunk)
    chunkcount = chunkcount + 1

if args.verbosity == 2:
    print(chunks)


# ==== write chunks to disk ====

# we possibly get thousands of files, so everything goes into a subfolder
def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    return path

subfolder = make_sure_path_exists(str(fname+'-cut'))

outfname = ''
starttime = 0
endtime = 0

for chunk in range(len(chunks)):
    starttime = chunks[chunk][0]
    endtime = chunks[chunk][1]

    outfname = str(fnamebase[0]+'-'+str(starttime)+'-'+str(endtime)+'.wav')
    outfname = os.path.join(subfolder, outfname)

    try:
        scipy.io.wavfile.write(outfname,smprate,fhand[1][starttime:endtime])
        if args.verbosity == 1 or args.verbosity == 2:
           print(outfname)
    except:
        print('Sorry, file -',outfname,'- could not be written.')
        quit()

print(chunkcount,'files have been written.')
quit()