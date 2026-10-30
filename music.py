"""Musique originale synthétisée (libre de droits) pour les réels : beat 124 bpm."""
import numpy as np, wave
def make(path,dur,bpm=124,sr=44100,fadein=0.5):
    t=np.arange(int(dur*sr))/sr; y=np.zeros_like(t); beat=60/bpm
    def env(x,d): return np.exp(-x/d)
    for k in range(int(dur/beat)+1):
        s=k*beat; i=int(s*sr); n=int(0.25*sr); x=np.arange(min(n,len(y)-i))/sr
        if i>=len(y): break
        y[i:i+len(x)]+=0.9*np.sin(2*np.pi*(120*env(x,0.04)+45)*x)*env(x,0.12)   # kick
        h=int((s+beat/2)*sr)
        if h<len(y):
            m=min(int(0.05*sr),len(y)-h); y[h:h+m]+=0.15*np.random.randn(m)*env(np.arange(m)/sr,0.015)  # hi-hat
        notes=[220,261.6,329.6,392,329.6,261.6,196,261.6][k%8]
        for sub in (0,beat/2):
            j=int((s+sub)*sr)
            if j<len(y):
                x=np.arange(min(int(0.3*sr),len(y)-j))/sr
                y[j:j+len(x)]+=0.22*np.sign(np.sin(2*np.pi*notes*x))*env(x,0.1)*0.6+0.12*np.sin(2*np.pi*notes*2*x)*env(x,0.15)
    y*=np.minimum(1,np.minimum(t/fadein if fadein>0 else 1,(dur-t)/1.0)); y=y/np.abs(y).max()*0.8
    with wave.open(str(path),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((y*32767).astype('<i2').tobytes())
    return path
