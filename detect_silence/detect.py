"""
Detecting periods of silence in a WAV file. Based on a question in #python on freenode

This implementation takes a very naive approach of looking at (non-sliding) 
windows of arbitrary width over the WAV, and looking at the sum of squares.

This is a very fragile implementation. Off the top of my head, I can say for
sure that choosing `THRESHOLD` based on std() would break badly on files with
extreme (lots or very little) amounts of silence.

Speech samples taken from 
http://www.voiptroubleshooter.com/open_speech/american.html
"""

import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt
import scipy.io.wavfile
import numpy as np
import glob

class WavWindow():
    def __init__(self, wav, sample_rate, width):
        """
        A helper class for a sliding window of width `width` over a WAV file
        
        Parameters
        ----------
        wav - an ndarray representing wav data (as returned from scipy.io.wavfile.read)
        sample_rate - int, sample rate in Hz (as returned from scipy.io.wavfile.read)
        width - window width, in s
        """
        self.wavfile = wav.astype(int)
        self.sample_rate = sample_rate
        self.width = width
        dt = 1./sample_rate
        tmax = dt*wav.size
        self._t = np.arange(0, tmax, dt)
    
    def _idx(self, t0):
        t0 = np.asarray(t0)
        if t0.size > 1:
            t0 = t0.reshape((-1, 1))
        return np.argwhere((self._t > t0) & (self._t < (t0 + self.width)))
    
    def __getitem__(self, t0):
        """
        Return the slice of the wav corresponding to the window from the start time `t0` to `t0+width`
        
        N.B. does *not* return a value for any windowed values outside of the wav, the return dataset may be empty
        """
        return self.wavfile[self._idx(t0)]
    
    def t(self, t0):
        return self._t[self._idx(t0)]

        
for fn in glob.glob('*.wav'):
    plt.figure(facecolor='white')
    rate, wv = scipy.io.wavfile.read(fn)
    dt = 1./rate  # s
    WINWIDTH = 0.5  # in s
    # WINSIZE = max(int(WINWIDTH/dt), 1)  # number of samples

    t = dt*np.arange(wv.size)
    win = WavWindow(wv, rate, WINWIDTH)
    # THRESH = 1/200*wv.std()*WINWIDTH*rate  # completely arbitrary
    THRESH = np.sqrt((wv**2).std()) * WINWIDTH*rate / 10 / 2  # slightly less arbitrary...?
    plt.plot(t, wv)
    from itertools import cycle
    c = cycle('rkg')
    for t0 in np.arange(0, t.max(), WINWIDTH):
  
        w = win.t(t0)
        sq = win[t0]**2
        amp = np.sqrt(sq.sum())
        if amp <= THRESH:
            c = 'r'
            val = 1.1*wv.max()
        else:
            c = 'k'
            val = 1.2*wv.max()
        plt.hlines(val, w[0], w[-1], c, '-')
  
    plt.xlabel('t (s)')
    plt.title('{fn} (red indicates suspected silent regions, WINWIDTH={WINWIDTH:.1f} sec)'.format(fn=fn, WINWIDTH=WINWIDTH))
    plt.savefig('{fn}.png'.format(fn=fn))
