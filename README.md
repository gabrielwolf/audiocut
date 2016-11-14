# audiocut
A Python 3 script that cuts a wave file into chunks of a variable length in seconds.
The chunks are named in the form of `foo-xxxxx-yyyyy.wav`, where xxxxx and yyyyy represent start and stop samples of the chunk. We have many of them, so they are put into a subfolder `foo.wav-cut/`

The purpose of this script is to create sample accurate chunks which can be put together again.

Given times are represented as timecode in the form of hh:mm:ss:f  
hh = hours, mm = minutes, ss = seconds, f = fraction of a second, that is a rational number smaller than 1 and bigger or equal than 0 (e.g. 0.33)

## Usage ##
Examples:

    $ python audiocut.py -v foo.wav 0:0:0:0 0:1:0:0 0:0:7:0
    foo.wav-cut/foo-0-336000.wav
    foo.wav-cut/foo-336000-672000.wav
    foo.wav-cut/foo-672000-1008000.wav
    foo.wav-cut/foo-1008000-1344000.wav
    foo.wav-cut/foo-1344000-1680000.wav
    foo.wav-cut/foo-1680000-2016000.wav
    foo.wav-cut/foo-2016000-2352000.wav
    foo.wav-cut/foo-2352000-2688000.wav
    foo.wav-cut/foo-2688000-2880000.wav
    9 files have been written.

    $ python audiocut.py -v foo.wav 0:0:0:0 0:0:5:0 0:0:1:0
    foo.wav-cut/foo-0-48000.wav
    foo.wav-cut/foo-48000-96000.wav
    foo.wav-cut/foo-96000-144000.wav
    foo.wav-cut/foo-144000-192000.wav
    foo.wav-cut/foo-192000-240000.wav
    5 files have been written.

Help:

    $ python audiocut.py -h
    usage: audiocut.py [-h] [-v] input starttime endtime chunklength

    positional arguments:
      input            wav file that has to be cut
      starttime        timecode in the form of hh:mm:ss:f where f is a float >= 0
                       and < 1 (e.g. 0.5)
      endtime          timecode in the form of hh:mm:ss:f where f is a float >= 0
                       and < 1 (e.g. 0.5)
      chunklength      timecode in the form of hh:mm:ss:f where f is a float >= 0
                       and < 1 (e.g. 0.5)

    optional arguments:
      -h, --help       show this help message and exit
      -v, --verbosity  increase output verbosity

## Limitations ##
At the time of writing (Nov 2016) the used library [scipy.io.wavfile](https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html) can't read 24bit wave!

## ToDo ##
* Make start time and end time optional (and chunk the whole file)
