from waverw import timecode_to_samples
from waverw import samples_to_timecode
from waverw import read_a_wave_file
from waverw import write_a_wave_file

print('\n== Unit-Tests ==\n')

# If the word "timecode" is used in this document, a string in the form of hh:mm:ss:smp is assumed.
# The letters stand for numbers that follow these conditions:
# hh       : mm                    : ss                    : smp
# int >= 0 : int >= 0 && int <= 59 : int >= 0 && int <= 59 : float >= 0 && float < 1


# ==== contract ==== timecode_to_samples(timecode, smprate)
    # == precondition ==
    # timecode  := timecode
    # smprate   := int >= 0

    # == postcondition ==
    # The function returns a positive int, that represents the number of samples
    # corresponding to a given timecode and sample rate

print('----> def timecode_to_samples(timecode, smprate)')
if(timecode_to_samples('00:00:02:0', 44100) == 88200):
    print('OK.')
else:
    print('Failed.')


# ==== contract ==== samples_to_timecode(samples, smprate)
    # == precondition ==
    # samples   := int >= 0
    # smprate   := int >= 0

    # == postcondition ==
    # The function returns a string in the form of a timecode, that represents
    # the time, corresponding to a given number of samples and a given sample rate

print('----> def samples_to_timecode(samples, smprate)')
if(samples_to_timecode(88200,44100) == '00:00:02:0.000000'):
    print('OK.')
else:
    print('Failed.')


# ==== contract ==== read_a_wave_file(fname, starttime, endtime)
    # == precondition ==
    # fname     := name of a wave file, that should be read
    # starttime := a positive timecode, smaller than the endtime timecode
    # endtime   := a positive timecode, smaller or equal to the length of the file

    # == postcondition ==
    # the segment of the wave file is returned as adarray

print('----> def read_a_wav_file(fname, starttime, endtime)')
if(read_a_wave_file('zyn.wav', '0:0:0:0', '0:0:1:0') is not False):
    print('OK.')
else:
    print('Failed.')


# ==== contract ==== write_a_wave_file(fname, starttime, endtime)
    # == precondition ==
    # fname     := name of a wave file, that should be read
    # starttime := a positive timecode, smaller than the endtime timecode
    # endtime   := a positive timecode, smaller or equal to the length of the file

    # == postcondition ==
    # a segment of the wave file was written and True was given back

print('----> def write_a_wav_file(fname, starttime, endtime)')
if(write_a_wave_file('zyn.wav', '0:0:15:0', '0:0:20:0') is not False):
    print('OK.')
else:
    print('Failed.')
