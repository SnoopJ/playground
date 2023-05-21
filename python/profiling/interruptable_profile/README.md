This sample shows how to invoke [`profile.Profile`](https://docs.python.org/3/library/profile.html#profile.Profile)
in a way that writes out a profile file if the profiler is terminated early by
the `SIGTERM` signal.

`profiler_target.py` defines a program to be profiled with a bunch of worker
functions that simulate the uneven distribution of work of a 'real' program,
and `run_profiler.py` creates a profiler instance and registers a [`signal`](https://docs.python.org/3/library/signal.html)
handler to dump the results if the program terminates early.

I wrote this example because of a need to profile a subprocess running inside
of a larger application. Unfortunately, `cProfile` does not itself provide this
behavior, so I had to do it myself.

**NOTE:** an earlier version of this sample incorrectly used [`atexit`](https://docs.python.org/3/library/atexit.html)
to try and solve the issue I was having. It turns out this is neither correct
nor necessary, because registered `atexit` handlers are not executed on `SIGTERM`,
and program termination caused by a `KeyboardInterrupt` is already correctly
handled by `profile`.


## Full profile
```
$ python3 run_profiler.py main.py --outfile full.prof
worker_0_N100000_numcalls1()
worker_1_N100000_numcalls2()
worker_2_N100000_numcalls3()
worker_3_N100000_numcalls4()
worker_4_N1000000_numcalls1()
worker_5_N1000000_numcalls2()
worker_6_N1000000_numcalls3()
worker_7_N1000000_numcalls4()
worker_8_N10000000_numcalls1()
worker_9_N10000000_numcalls2()
worker_10_N10000000_numcalls3()
worker_11_N10000000_numcalls4()
$ python3 -c "from pstats import Stats; s = Stats('full.prof'); s.sort_stats('tottime'); s.print_stats(15)"
Sun May 21 16:40:16 2023    full.prof

         4250 function calls (4108 primitive calls) in 3.641 seconds

   Ordered by: internal time
   List reduced from 168 to 15 due to restriction <15>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        4    1.314    0.328    1.314    0.328 <string>:1(worker_11_N10000000_numcalls4)
        3    0.993    0.331    0.993    0.331 <string>:1(worker_10_N10000000_numcalls3)
        2    0.658    0.329    0.658    0.329 <string>:1(worker_9_N10000000_numcalls2)
        1    0.331    0.331    0.331    0.331 <string>:1(worker_8_N10000000_numcalls1)
        4    0.117    0.029    0.117    0.029 <string>:1(worker_7_N1000000_numcalls4)
        3    0.093    0.031    0.093    0.031 <string>:1(worker_6_N1000000_numcalls3)
        2    0.062    0.031    0.062    0.031 <string>:1(worker_5_N1000000_numcalls2)
        1    0.034    0.034    0.034    0.034 <string>:1(worker_4_N1000000_numcalls1)
        4    0.010    0.002    0.010    0.002 <string>:1(worker_3_N100000_numcalls4)
        3    0.007    0.002    0.007    0.002 <string>:1(worker_2_N100000_numcalls3)
        2    0.005    0.003    0.005    0.003 <string>:1(worker_1_N100000_numcalls2)
        1    0.003    0.003    0.003    0.003 <string>:1(worker_0_N100000_numcalls1)
     26/6    0.002    0.000    0.006    0.001 /usr/lib/python3.8/sre_parse.py:493(_parse)
        1    0.001    0.001    3.641    3.641 profile:0(<code object <module> at 0x7fe5d1a16870, file "main.py", line 1>)
     37/6    0.001    0.000    0.003    0.001 /usr/lib/python3.8/sre_compile.py:71(_compile)


```

## Partial (interrupted) profile

```
$ # this bash idiom invokes the profiler, then sends the process a SIGTERM after 0.5 sec
$ python3 run_profiler.py main.py --outfile partial.prof & PID=$!; sleep 0.5; kill -s SIGTERM ${PID}; wait ${PID} 2>/dev/null
[2] 2369232
worker_0_N100000_numcalls1()
worker_1_N100000_numcalls2()
worker_2_N100000_numcalls3()
worker_3_N100000_numcalls4()
worker_4_N1000000_numcalls1()
worker_5_N1000000_numcalls2()
worker_6_N1000000_numcalls3()
worker_7_N1000000_numcalls4()
worker_8_N10000000_numcalls1()
$ python3 -c "from pstats import Stats; s = Stats('partial.prof'); s.sort_stats('tottime'); s.print_stats(15)"
Sun May 21 16:40:56 2023    partial.prof

         4239 function calls (4097 primitive calls) in 0.565 seconds

   Ordered by: internal time
   List reduced from 166 to 15 due to restriction <15>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.223    0.223    0.223    0.223 <string>:1(worker_8_N10000000_numcalls1)
        4    0.116    0.029    0.116    0.029 <string>:1(worker_7_N1000000_numcalls4)
        3    0.092    0.031    0.092    0.031 <string>:1(worker_6_N1000000_numcalls3)
        2    0.061    0.031    0.061    0.031 <string>:1(worker_5_N1000000_numcalls2)
        1    0.033    0.033    0.033    0.033 <string>:1(worker_4_N1000000_numcalls1)
        4    0.010    0.002    0.010    0.002 <string>:1(worker_3_N100000_numcalls4)
        3    0.008    0.003    0.008    0.003 <string>:1(worker_2_N100000_numcalls3)
        2    0.005    0.003    0.005    0.003 <string>:1(worker_1_N100000_numcalls2)
        1    0.003    0.003    0.003    0.003 <string>:1(worker_0_N100000_numcalls1)
     26/6    0.002    0.000    0.006    0.001 /usr/lib/python3.8/sre_parse.py:493(_parse)
        1    0.001    0.001    0.565    0.565 profile:0(<code object <module> at 0x7fc7e3132870, file "main.py", line 1>)
     37/6    0.001    0.000    0.003    0.001 /usr/lib/python3.8/sre_compile.py:71(_compile)
      563    0.001    0.000    0.001    0.000 :0(append)
      463    0.001    0.000    0.001    0.000 /usr/lib/python3.8/sre_parse.py:254(get)
  477/436    0.001    0.000    0.001    0.000 :0(len)


```
