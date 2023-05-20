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
$ python3 -c "from pstats import Stats; s = Stats('full.prof'); s.sort_stats('tottime'); s.print_stats()"
Fri May 19 22:30:21 2023    full.prof

         48 function calls in 3.523 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        4    1.277    0.319    1.277    0.319 <string>:1(worker_11_N10000000_numcalls4)
        3    0.961    0.320    0.961    0.320 <string>:1(worker_10_N10000000_numcalls3)
        2    0.641    0.320    0.641    0.320 <string>:1(worker_9_N10000000_numcalls2)
        1    0.320    0.320    0.320    0.320 <string>:1(worker_8_N10000000_numcalls1)
        4    0.111    0.028    0.111    0.028 <string>:1(worker_7_N1000000_numcalls4)
        3    0.090    0.030    0.090    0.030 <string>:1(worker_6_N1000000_numcalls3)
        2    0.063    0.031    0.063    0.031 <string>:1(worker_5_N1000000_numcalls2)
        1    0.035    0.035    0.035    0.035 <string>:1(worker_4_N1000000_numcalls1)
        4    0.010    0.003    0.010    0.003 <string>:1(worker_3_N100000_numcalls4)
        3    0.008    0.003    0.008    0.003 <string>:1(worker_2_N100000_numcalls3)
        2    0.005    0.003    0.005    0.003 <string>:1(worker_1_N100000_numcalls2)
        1    0.003    0.003    0.003    0.003 <string>:1(worker_0_N100000_numcalls1)
       12    0.000    0.000    0.000    0.000 :0(print)
        1    0.000    0.000    3.523    3.523 /home/jgerity/personal/playground/python/profiling/interruptable_profile/profiler_target.py:38(main)
        1    0.000    0.000    0.000    0.000 :0(setprofile)
        1    0.000    0.000    3.523    3.523 profile:0(target_main())
        1    0.000    0.000    3.523    3.523 :0(exec)
        1    0.000    0.000    3.523    3.523 <string>:1(<module>)
        1    0.000    0.000    0.000    0.000 :0(items)
        0    0.000             0.000          profile:0(profiler)



```

## Partial (interrupted) profile

```
$ # this bash idiom invokes the profiler, then sends the process a SIGTERM after 0.5 sec
$ python3 run_profiler.py --outfile partial.prof & PID=$!; sleep 0.5; kill -s SIGTERM ${PID}; wait ${PID} 2>/dev/null
[2] 2127596
worker_0_N100000_numcalls1()
worker_1_N100000_numcalls2()
worker_2_N100000_numcalls3()
worker_3_N100000_numcalls4()
worker_4_N1000000_numcalls1()
worker_5_N1000000_numcalls2()
worker_6_N1000000_numcalls3()
worker_7_N1000000_numcalls4()
worker_8_N10000000_numcalls1()
$ python3 -c "from pstats import Stats; s = Stats('partial.prof'); s.sort_stats('tottime'); s.print_stats()"
Fri May 19 22:32:07 2023    partial.prof

         37 function calls in 0.548 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.225    0.225    0.225    0.225 <string>:1(worker_8_N10000000_numcalls1)
        4    0.112    0.028    0.112    0.028 <string>:1(worker_7_N1000000_numcalls4)
        3    0.088    0.029    0.088    0.029 <string>:1(worker_6_N1000000_numcalls3)
        2    0.062    0.031    0.062    0.031 <string>:1(worker_5_N1000000_numcalls2)
        1    0.035    0.035    0.035    0.035 <string>:1(worker_4_N1000000_numcalls1)
        4    0.010    0.002    0.010    0.002 <string>:1(worker_3_N100000_numcalls4)
        3    0.007    0.002    0.007    0.002 <string>:1(worker_2_N100000_numcalls3)
        2    0.005    0.003    0.005    0.003 <string>:1(worker_1_N100000_numcalls2)
        1    0.003    0.003    0.003    0.003 <string>:1(worker_0_N100000_numcalls1)
        9    0.000    0.000    0.000    0.000 :0(print)
        1    0.000    0.000    0.548    0.548 /home/jgerity/personal/playground/python/profiling/interruptable_profile/profiler_target.py:38(main)
        1    0.000    0.000    0.000    0.000 :0(setprofile)
        1    0.000    0.000    0.548    0.548 :0(exec)
        1    0.000    0.000    0.548    0.548 profile:0(target_main())
        1    0.000    0.000    0.000    0.000 run_profiler.py:17(_dump_on_sigterm)
        1    0.000    0.000    0.548    0.548 <string>:1(<module>)
        1    0.000    0.000    0.000    0.000 :0(items)
        0    0.000             0.000          profile:0(profiler)



```
