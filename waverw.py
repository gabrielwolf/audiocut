import scipy.io.wavfile
import re

def is_timecode(arg):
    match = re.match('[0-9]+:[0-5]*[0-9]:[0-5]*[0-9]:0[.]?[0-9]*', arg)
    if match:
        return True
    else:
        return False


def timecode_to_samples(timecode, smprate):
    if not is_timecode(timecode):
        print('Debug: argument is not timecode')
        return False
    else:
        values = timecode.split(':')
        h = int(values[0])
        m = int(values[1])
        s = int(values[2])
        fraction = float(values[3])
        total = h * 3600 * smprate + m * 60 * smprate + \
            s * smprate + int(fraction * smprate)
        return total


def samples_to_timecode(samples, smprate):
    return '{0:02d}:{1:02d}:{2:02d}:{3:f}'.format(int(samples / (3600 * smprate)),
                                                  int(samples /
                                                      (60 * smprate) % 60),
                                                  int(samples / smprate % 60),
                                                  float((samples % smprate)) / smprate)


def compare_timecode(a, b):
    if not is_timecode(a):
        print('Debug: a is not timecode')
        return False
    if not is_timecode(b):
        print('Debug: b is not timecode')
        return False
    return timecode_to_samples(a, 44100) - timecode_to_samples(b, 44100)


def validate_parameters(fname, smprate, starttime, endtime, chunklength):
    result = 0
    arguments = {
        'fname': False,
        'smprate': False,
        'starttime': False,
        'endtime': False,
        'chunklength': False }
    if type(fname) == str:
        if re.search('[.]wav$', fname):
            arguments['fname'] = True
    if type(smprate) == int:
        if smprate > 0:
            arguments['smprate'] = True
    if type(starttime) == str:
        if is_timecode(starttime):
            if compare_timecode(starttime, endtime) < 0:
                arguments['starttime'] = True
    if type(endtime) == str:
        if is_timecode(endtime):
            arguments['endtime'] = True
    if type(chunklength) == str:
        if is_timecode(chunklength):
            if timecode_to_samples(chunklength, smprate) <= timecode_to_samples(endtime, smprate) - timecode_to_samples(starttime, smprate):
                arguments['chunklength'] = True
    for argument in arguments:
        # print('Debug:',argument, arguments[argument])
        if arguments[argument] == False:
            result = result + 1
    if result > 0:
        print(arguments)
        raise Exception("Command line arguments not well formed! Have a look at the line starting with {' some lines above. False means something wrong.")
    else:
        return True


def read_a_wave_file(fname, starttime, endtime):
    try:
        fhand = scipy.io.wavfile.read(fname)
    except:
        return False
    excerpt = fhand[1][timecode_to_samples(
        starttime, fhand[0]):timecode_to_samples(endtime, fhand[0])]
    return fhand[0], excerpt


def write_a_wave_file(fname, starttime, endtime):
    fhand = read_a_wave_file(fname, starttime, endtime)

    outputstarttime = str(timecode_to_samples(starttime, fhand[0]))
    outputendtime = str(timecode_to_samples(endtime, fhand[0]))

    fnamebase = re.findall('(.+).wav', fname)
    outfname = fnamebase[0] + '_' + \
        outputstarttime + '-' + outputendtime + '.wav'

    try:
        scipy.io.wavfile.write(
            outfname,
            fhand[0],
            fhand[1])
        return True
    except:
        return False
