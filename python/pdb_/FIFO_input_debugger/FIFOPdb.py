"""
Based on a question asked in #python on Libera.chat on 10 Dec 2022 about
debugging a program that reads from stdin

See README.md for more information
"""
import os
import sys
from pdb import Pdb
from tempfile import mktemp


class FIFOPdb(Pdb):
    def __init__(self):
        self._fifo_fn = mktemp()
        os.mkfifo(self._fifo_fn)

        super().__init__()

        self._fifo = None

    def _ensure_input(self):
        if not self._fifo:
            print(f"Run `cat > {self._fifo_fn}` in a separate terminal to begin debugging input there")
            self._fifo = open(self._fifo_fn, 'r')
            self.stdin = self._fifo
            # NOTE: our FIFO will be ignored if we don't also set this parameter
            self.use_rawinput = 0

    def set_trace(self, *args, **kwargs):
        self._ensure_input()
        super().set_trace(frame=sys._getframe().f_back)


    def __del__(self):
        if hasattr(self, "_fifo"):
            self._fifo.close()
            os.remove(self._fifo_fn)



debugger = FIFOPdb()
set_trace = debugger.set_trace
