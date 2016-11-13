import scipy.io.wavfile
import re

def timecode_to_samples(timecode, smprate):
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
