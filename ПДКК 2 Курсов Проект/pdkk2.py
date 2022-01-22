from math import *
from mailmerge import MailMerge

def prt(v):
    n = [name for name in globals() if globals()[name] is v]
    print(n[0],"=", v)

def prtTime(frame):
    return ('Transmited: %2.3fs Recived: %2.3fs ACK recived: %2.3fs' % (frame['transmited'], frame['recived'], frame['ACK recived']))

bitSpeed = 19200
transferAmount = 13500
maxFrameSize = 1500
latency = 1.2
rejFrame = 3

prt(bitSpeed)
prt(transferAmount)
prt(maxFrameSize)
prt(latency)

frameInfoSize = maxFrameSize - 6
nOfFrames = ceil(transferAmount / frameInfoSize)
lastFrameSize = maxFrameSize
if (transferAmount % frameInfoSize) != 0:
    lastFrameSize = transferAmount - (nOfFrames-1)*frameInfoSize

prt(frameInfoSize)
prt(nOfFrames)
prt(lastFrameSize)

def calcConn(t, n):
    tt = 0
    fl = 0
    if n >= (nOfFrames - 1):
        fl = (lastFrameSize * 8 / bitSpeed)
    else:
        fl = ((maxFrameSize * 8) / bitSpeed)
    tt = t + fl
    tr = tt + latency
    tra = tr + latency + (6 * 8 / bitSpeed)
    return {'transmited': tt,
            'recived': tr,
            'ACK recived': tra,
            'FrameLength': fl,
            'ACKLength': (6 * 8 / bitSpeed),
            'StartTime': t}

def fTime(tm):
    return ('%.3g' % tm).replace('.', ',')

lines=[]
first=True
last=True
def printToWord(tInfo, n, i, err=False):
    global first
    global last
    resp = 'ACK'
    if err:
        resp = 'REJ'

    fl = fTime(tInfo['FrameLength'])
    al = fTime(tInfo['ACKLength'])
    if first:
        fl = '(%s * 8 / %s)' % (fTime(float(maxFrameSize)), str(bitSpeed))
        al = '(6 * 8 / %s)' % (str(bitSpeed),)
        first=False

    
    if last and (n == nOfFrames-1):
        fl = '(%s * 8 / %s)' % (fTime(float(lastFrameSize)), str(bitSpeed))
        last=False
    return {
        'Recived': fTime(tInfo['recived']),
        'Index': str(i),
        'Latency': fTime(latency),
        'FrameLength': fl,
        'FrameNumber': str(n),
        'EndTime': fTime(tInfo['transmited']),
        'StartTime': fTime(tInfo['StartTime']),
        'ACKLength': al,
        'ACKRecivedTime': fTime(tInfo['ACK recived']),
        'Resp': resp
        }

time = 2*(6 * 8 / bitSpeed + latency)
print(time)
tWatch = 10000000
index = 1
for i in range(0, nOfFrames):
    tInfo = calcConn(time, i)
    time = tInfo['transmited']

    err=False
    if i == rejFrame:
        tWatch = tInfo['ACK recived']
        err=True

    print("Frame",str(i)+":", prtTime(tInfo))
    lines.append(printToWord(tInfo, i, index, err))
    index = index+1
    if tWatch <= time:
        break

for i in range(rejFrame-1, nOfFrames):
    tInfo = calcConn(time, i)
    time = tInfo['transmited']
    lines.append(printToWord(tInfo, i, index))
    index = index+1
    print("Frame",str(i)+":", prtTime(tInfo))

template = "template.docx"
document = MailMerge(template)
document.merge_templates(lines, separator='continuous_section')
document.write('test-output.docx')



