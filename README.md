# audiocut
A Python 3 script that cuts a wave file into chunks of a variable length in seconds.
The chunks are named in the form of `foo-xxxxxxxxxx-yyyyyyyyyy.wav`, where xxxxxxxxxx and yyyyyyyyyy represent start and stop samples of the chunk. We have many of them, so they are put into a subfolder `foo.wav-cut/`

The purpose of this script is to create sample accurate chunks which can be put together again.

Given times are represented as timecode in the form of hh:mm:ss:f  
hh = hours, mm = minutes, ss = seconds, f = fraction of a second, that is a rational number smaller than 1 and bigger or equal than 0 (e.g. 0.33)

## Usage ##
Examples:

    $ python audiocut.py -v foo.wav 0:0:0:0 0:1:0:0 0:0:7:0
    foo.wav-cut/foo-0000000000-0000336000.wav
    foo.wav-cut/foo-0000336000-0000672000.wav
    foo.wav-cut/foo-0000672000-0001008000.wav
    foo.wav-cut/foo-0001008000-0001344000.wav
    foo.wav-cut/foo-0001344000-0001680000.wav
    foo.wav-cut/foo-0001680000-0002016000.wav
    foo.wav-cut/foo-0002016000-0002352000.wav
    foo.wav-cut/foo-0002352000-0002688000.wav
    foo.wav-cut/foo-0002688000-0002880000.wav
    9 files have been written.

    $ python audiocut.py -v foo.wav 0:0:15:0 0:0:20:0 0:0:1:0.5
    foo.wav-cut/foo-0000720000-0000792000.wav
    foo.wav-cut/foo-0000792000-0000864000.wav
    foo.wav-cut/foo-0000864000-0000936000.wav
    foo.wav-cut/foo-0000936000-0000960000.wav
    4 files have been written.

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
