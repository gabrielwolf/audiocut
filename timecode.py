import re


def is_timecode(arg):
    match = re.match('^[0-9]+:[0-5]*[0-9]:[0-5]*[0-9]:0[.]?[0-9]*$', arg)
    if match:
        return True
    else:
        return False


def timecode_to_samples(timecode, sample_rate):
    if not is_timecode(timecode):
        # print('Debug: argument is not timecode')
        return False
    if type(sample_rate) != int:
        # print('Debug -- timecode_to_samples(timecode, sample_rate): argument sample_rate is not an int')
        return False
    if sample_rate <= 0:
        # print('Debug -- samples_to_timecode(samples, sample_rate): argument sample_rate is 0 or negative')
        return False

    values = timecode.split(':')
    hours = int(values[0])
    minutes = int(values[1])
    seconds = int(values[2])
    fraction = float(values[3])

    total = hours * 60 * 60 * sample_rate + \
            minutes * 60 * sample_rate + \
            seconds * sample_rate + \
            int(fraction * sample_rate)
    return total


def samples_to_timecode(samples, sample_rate):
    if type(samples) != int:
        # print('Debug -- samples_to_timecode(samples, sample_rate): argument samples is not an int')
        return False
    if samples < 0:
        # print('Debug -- samples_to_timecode(samples, sample_rate): argument samples is negative')
        return False
    if type(sample_rate) != int:
        # print('Debug -- samples_to_timecode(samples, sample_rate): argument sample_rate is not an int')
        return False
    if sample_rate <= 0:
        # print('Debug -- samples_to_timecode(samples, sample_rate): argument sample_rate is 0 or negative')
        return False

    smp_per_hour = 60 * 60 * sample_rate
    smp_per_min = 60 * sample_rate
 
    hours = int(samples / smp_per_hour)
    samples -= hours * smp_per_hour
 
    minutes = int(samples / smp_per_min)
    samples -= minutes * smp_per_min
 
    seconds = int(samples / sample_rate)
    samples -= seconds * sample_rate
 
    fraction = float(samples / sample_rate)

    result = '{0:02d}:{1:02d}:{2:02d}:{3:f}'.format(hours, minutes, seconds, fraction)
    if is_timecode(result):
        return result
    else:
        print('Debug -- samples_to_timecode(samples, sample_rate): something went wrong')
        return False


def compare_timecode(a, b):
    if not is_timecode(a):
        # print('Debug: a is not timecode')
        return False
    if not is_timecode(b):
        # print('Debug: b is not timecode')
        return False
    return timecode_to_samples(a, 44100) - timecode_to_samples(b, 44100)


def validate_parameters(file_name, sample_rate, start_time, end_time, chunk_length):
    result = 0
    arguments = {
        'file_name': False,
        'sample_rate': False,
        'start_time': False,
        'end_time': False,
        'chunk_length': False}
    if type(file_name) == str:
        if re.search('[.]wav$', file_name):
            arguments['file_name'] = True
    if type(sample_rate) == int:
        if sample_rate > 0:
            arguments['sample_rate'] = True
    if type(start_time) == str:
        if is_timecode(start_time):
            if compare_timecode(start_time, end_time) < 0:
                arguments['start_time'] = True
    if type(end_time) == str:
        if is_timecode(end_time):
            arguments['end_time'] = True
    if type(chunk_length) == str:
        if is_timecode(chunk_length):
            if timecode_to_samples(chunk_length, sample_rate) <= timecode_to_samples(end_time, sample_rate) - timecode_to_samples(start_time, sample_rate):
                arguments['chunk_length'] = True
    for argument in arguments:
        # print('Debug:', argument, arguments[argument])
        if not arguments[argument]:
            result = result + 1
    if result > 0:
        print('Command line arguments not well formed!')
        for argument in arguments:
            if not arguments[argument]:
                print('Error in argument', argument)
        quit()
    else:
        return True
