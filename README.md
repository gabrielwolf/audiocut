# audiocut
A Python 3 script that cuts a wave file into chunks of a variable length in seconds.
The chunks are named in the form of `foo-xxxxx-yyyyy.wav`, where xxxxx and yyyyy represent start and stop samples of the chunk. We have many of them, so they are put into a subfolder `foo.wav-cut/`

The purpose of this script is to create sample accurate chunks which can be put together again.

#### Bug: start time has to be zero ####

## Usage ##
Examples:

    $ python audiocut.py -v foo.wav 0 23 1
    foo.wav-cut/foo-0-48000.wav
    foo.wav-cut/foo-48000-96000.wav
    foo.wav-cut/foo-96000-144000.wav
    foo.wav-cut/foo-144000-192000.wav
    foo.wav-cut/foo-192000-240000.wav
    foo.wav-cut/foo-240000-288000.wav
    foo.wav-cut/foo-288000-336000.wav
    foo.wav-cut/foo-336000-384000.wav
    foo.wav-cut/foo-384000-432000.wav
    foo.wav-cut/foo-432000-480000.wav
    foo.wav-cut/foo-480000-528000.wav
    foo.wav-cut/foo-528000-576000.wav
    foo.wav-cut/foo-576000-624000.wav
    foo.wav-cut/foo-624000-672000.wav
    foo.wav-cut/foo-672000-720000.wav
    foo.wav-cut/foo-720000-768000.wav
    foo.wav-cut/foo-768000-816000.wav
    foo.wav-cut/foo-816000-864000.wav
    foo.wav-cut/foo-864000-912000.wav
    foo.wav-cut/foo-912000-960000.wav
    foo.wav-cut/foo-960000-1008000.wav
    foo.wav-cut/foo-1008000-1056000.wav
    foo.wav-cut/foo-1056000-1104000.wav
    23 files have been written.

    $ python audiocut.py -v foo.wav 0 30 3
    foo.wav-cut/foo-0-144000.wav
    foo.wav-cut/foo-144000-288000.wav
    foo.wav-cut/foo-288000-432000.wav
    foo.wav-cut/foo-432000-576000.wav
    foo.wav-cut/foo-576000-720000.wav
    foo.wav-cut/foo-720000-864000.wav
    foo.wav-cut/foo-864000-1008000.wav
    foo.wav-cut/foo-1008000-1152000.wav
    foo.wav-cut/foo-1152000-1296000.wav
    foo.wav-cut/foo-1296000-1440000.wav
    10 files have been written.

Help:

    $ python audiocut.py -h
    usage: audiocut.py [-h] [-v] input starttime endtime chunklength

    positional arguments:
      input            wav file that has to be cut
      starttime        start time in seconds
      endtime          end time in seconds
      chunklength      chunk length in seconds

    optional arguments:
      -h, --help       show this help message and exit
      -v, --verbosity  increase output verbosity

## Limitations ##
At the time of writing (Nov 2016) the used library [scipy.io.wavfile](https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html) can't read 24bit wave!

## ToDo ##
* Make start time and end time optional (and chunk the whole file)
