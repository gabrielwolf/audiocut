from waverw import is_timecode
from waverw import timecode_to_samples
from waverw import samples_to_timecode
from waverw import compare_timecode
from waverw import validate_parameters

print('=== Unit-Tests ===\n')

# If the word "timecode" is used in this document, a string in the form of hh:mm:ss:smp is assumed.
# The letters stand for numbers that follow these conditions:
# hh       : mm                    : ss                    : smp
# int >= 0 : int >= 0 && int <= 59 : int >= 0 && int <= 59 : float >= 0 && float < 1

# ==== contract ==== is_timecode(arg)
    # == precondition ==
    # arg  := str

    # == postcondition ==
    # The function returns True if the given argument is a timecode
    # otherwise it returns False

print('----> def is_timecode(arg)')
if is_timecode('0:0:2:0'):
    print('OK.')
else:
    print('Failed.')


# ==== contract ==== timecode_to_samples(timecode, smprate)
    # == precondition ==
    # timecode  := timecode
    # smprate   := int >= 0

    # == postcondition ==
    # The function returns a positive int, that represents the number of samples
    # corresponding to a given timecode and sample rate

print('----> def timecode_to_samples(timecode, smprate)')
if timecode_to_samples('00:00:02:0', 44100) == 88200:
    print('Calc OK.')
else:
    print('Calc Failed.')
if not timecode_to_samples('00:00:70:0', 44100):
    print('Bad input OK.')
else:
    print('Bad input Failed.')


# ==== contract ==== samples_to_timecode(samples, smprate)
    # == precondition ==
    # samples   := int >= 0
    # smprate   := int > 0

    # == postcondition ==
    # The function returns a string in the form of a timecode, that represents
    # the time, corresponding to given numbers of samples and sample rate

print('----> def samples_to_timecode(samples, smprate)')
if samples_to_timecode(88200,44100) == '00:00:02:0.000000':
    print('Calc OK.')
else:
    print('Calc Failed.')
if not samples_to_timecode(5,0):
    print('Bad input OK.')
else:
    print('Bad input Failed.')

# ==== contract ==== compare_timecode(a, b)
    # == precondition ==
    # a  := timecode
    # b  := timecode

    # == postcondition ==
    # The function returns 0 if both timecodes are equal,
    # a positive number if a is bigger than b and
    # a negative number if a is smaller than b

print('----> def compare_timecode(a, b)')
if compare_timecode('0:0:2:0', '0:0:2:0') == 0:
    print('Equals OK.')
else:
    print('Equals Failed.')
if compare_timecode('0:0:2:0', '0:0:1:0') > 0:
    print('Bigger OK.')
else:
    print('Bigger Failed.')
if compare_timecode('0:0:1:0', '0:0:2:0') < 0:
    print('Smaller OK.')
else:
    print('Smaller Failed.')
if not compare_timecode('0:0:1:0', '0:0:70:0'):
    print('Bad input OK.')
else:
    print('Bad input Failed.')


# ==== contract ==== validate_parameters(fname, smprate, starttime, endtime, chunklength)

# == precondition ==
# fname       := filename - str
# smprate     := sample rate - int >= 0
# starttime   := timecode - str
# endtime     := timecode - str
# chunklength := timecode - str

# == postcondition ==
# True is returned when all arguments are well formed, starttime is smaller than endtime
# and chunklength is smaller or equal to the duration between starttime end endtime


print('----> def validate_parameters(fname, smprate, starttime, endtime, chunklength)')
if validate_parameters('test.wav', 44100, '0:0:2:0.6', '0:0:5:0.6', '0:0:1:0'):
    print('OK.')
else:
    print('Failed.')