import sys, subprocess, struct, math
src=sys.argv[1]; SR=22050; win=SR//100
for label,t in [('DANESA tecleo',486.6),('VIDEOCENTRO tecleo',368.9),('silencio de control 4.05',4.0)]:
    for hp in (None,4000):
        af=f'highpass=f={hp}' if hp else 'anull'
        raw=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-t','0.8','-i',src,'-vn','-ac','1','-ar',str(SR),'-af',af,'-f','s16le','-'],capture_output=True).stdout
        x=struct.unpack('<%dh'%(len(raw)//2),raw)
        e=[20*math.log10((math.sqrt(sum(v*v for v in x[i:i+win])/win) or 1e-9)/32768) for i in range(0,len(x)-win,win)]
        print(label,'agudos' if hp else 'total ',' '.join(f'{v:4.0f}' for v in e))
