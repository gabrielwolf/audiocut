import os
import errno
import argparse
import scipy.io.wavfile
import re

# At the time of writing (Nov 2016) scipy.io.wavfile can not read 24bit wave!
# ToDo: Make chunk size variable.

# Parse command line arguments

parser = argparse.ArgumentParser()
parser.add_argument("input", help="wav file that has to be cut",
                    type=str)
parser.add_argument("starttime", help="start time in seconds",
                    type=int)
parser.add_argument("endtime", help="end time in seconds",
                    type=int)
parser.add_argument("chunklength", help="chunk length in seconds",
                    type=int)
parser.add_argument("-v", "--verbosity", action="count",
                    help="increase output verbosity")
args = parser.parse_args()


# Helper function

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    return path


# Read input file and its meta data

fname = args.input
fnamepart = re.findall('(.+).wav',fname)
try:
    fhand = scipy.io.wavfile.read(fname)
except:
    print('Sorry, file -',fname,'- could not be opened.')
    exit()
smpfreq = fhand[0]
chunklength = args.chunklength 


# We have maybe thousands of files, so we make a subfolder we can fill later

subfolder = make_sure_path_exists(str(fname+'-cut'))


# Now we iterate over the file and write chunks

# Bug: start time can't be set manually, it has to be fixed to 0 now.
# i = args.starttime
i = 0
filecount = 0

while i * chunklength + chunklength <= args.endtime:
    if i == 0:
        writestart = 0
    else:
        writestart = (i * chunklength) * smpfreq
    if i == 0:
        writeend = chunklength * smpfreq
    else:
        writeend = (i * chunklength + chunklength) * smpfreq

    if args.verbosity == 2:
        print('Start:',writestart)
        print('End:',writeend)

    outfname = str(fnamepart[0]+'-'+str(writestart)+'-'+str(writeend)+'.wav')
    outfname = os.path.join(subfolder, outfname)

    try:
        scipy.io.wavfile.write(
            outfname,
            smpfreq,
            fhand[1][writestart:writeend:1])
        filecount = filecount + 1
        if args.verbosity == 1 or args.verbosity == 2:
            print(outfname)
    except:
        print('Sorry, file -',outfname,'- could not be written.')
        exit()
    i = i + 1

print(filecount,'files have been written.')