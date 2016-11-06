import scipy.io.wavfile, re

print('This script cuts a *.wav file in blocks of seconds.')
fname = input('Which file should be used? ')
#fname = 'angel.wav'
try:
    fhand = scipy.io.wavfile.read(fname)
except:
    print('Sorry, file -',fname,'- could not be opened.')
    exit()

starttime = int(input('What second sould be startet at? '))
endtime = int(input('What second should be ended on? '))

smpfreq = fhand[0]

# for smp in fhand[1][0:480000:1]:
#     print ('Debug: ',smp)

fnamepart = re.findall('(.+).wav',fname)

i = starttime

while i <= endtime:
    istring = str(i)
    outfname = str(fnamepart[0]+'-'+istring.zfill(4)+'.wav')
    scipy.io.wavfile.write(outfname,smpfreq,fhand[1][smpfreq*i:smpfreq*i+smpfreq:1])
    i = i + 1