# audiocut
A Python 3 script that cuts a wave file into chunks with the length of a second.
The chunks are named in the form of `foo-xxxx.wav`, where xxxx represents the start time of the chunk in seconds. We have many of them, so they are being written into a subfolder `foo.wav-cut/`.

The purpose of this script is to have sample accurate chunks, that are can be put together again.

## Usage ##
Example:

    $ python audiocut.py -v foo.wav 0 23
    foo.wav-cut/foo-0000.wav
    foo.wav-cut/foo-0001.wav
    foo.wav-cut/foo-0002.wav
    foo.wav-cut/foo-0003.wav
    foo.wav-cut/foo-0004.wav
    foo.wav-cut/foo-0005.wav
    foo.wav-cut/foo-0006.wav
    foo.wav-cut/foo-0007.wav
    foo.wav-cut/foo-0008.wav
    foo.wav-cut/foo-0009.wav
    foo.wav-cut/foo-0010.wav
    foo.wav-cut/foo-0011.wav
    foo.wav-cut/foo-0012.wav
    foo.wav-cut/foo-0013.wav
    foo.wav-cut/foo-0014.wav
    foo.wav-cut/foo-0015.wav
    foo.wav-cut/foo-0016.wav
    foo.wav-cut/foo-0017.wav
    foo.wav-cut/foo-0018.wav
    foo.wav-cut/foo-0019.wav
    foo.wav-cut/foo-0020.wav
    foo.wav-cut/foo-0021.wav
    foo.wav-cut/foo-0022.wav
    foo.wav-cut/foo-0023.wav
    24 files have been written.

Help:

    $ python audiocut.py -h
    usage: audiocut.py [-h] [-v] input starttime endtime

    positional arguments:
      input            wav file that has to be cut
      starttime        start time in seconds
      endtime          end time in seconds
  
    optional arguments:
      -h, --help       show this help message and exit
      -v, --verbosity  increase output verbosity

## Limitations ##
At the time of writing (Nov 2016) the used library [scipy.io.wavfile](https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html) can't read 24bit wave!

## ToDo ##
* Make start time and end time optional (and chunk the whole file)
* Make chunk length variable.
