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


# We have thousands of files so we make a subfolder to write them into later

subfolder = make_sure_path_exists(str(fname+'-cut'))


# Now we can iterate second wise over the file and write our chunks

i = args.starttime
while i <= args.endtime:
    istring = str(i)
    outfname = str(fnamepart[0]+'-'+istring.zfill(4)+'.wav')
    outfname = os.path.join(subfolder, outfname)
    try:
        scipy.io.wavfile.write(
            outfname,
            smpfreq,
            fhand[1][smpfreq*i:smpfreq*i+smpfreq:1] # Here's the magic
            )
        if args.verbosity == 1:
            print(outfname)
    except:
        print('Sorry, file -',outfname,'- could not be written.')
        exit()
    i = i + 1

print(i,'files have been written.')