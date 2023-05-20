This sample shows how to invoke [`profile.Profile`](https://docs.python.org/3/library/profile.html#profile.Profile)
in a way that writes out a profile file even if the profiler is terminated
early (i.e. by `SIGTERM`).

`profiler_target.py` defines a program to be profiled with a bunch of worker
functions that simulate the uneven distribution of work of a 'real' program,
and `run_profiler.py` creates a profiler instance and registers an [`atexit`](https://docs.python.org/3/library/atexit.html)
handler to dump the results if the program terminates early.

I wrote this example because of a need to profile a subprocess running inside
of a larger application. Unfortunately, `cProfile` does not itself provide this
behavior, so I had to do it myself.


## Full profile
```
$ python3 run_profiler.py --outfile full.prof
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
$ python3 -c "from pstats import Stats; s = Stats('full.prof'); s.sort_stats('tottime'); s.print_stats()"
Fri May 19 20:26:27 2023    full.prof

         48 function calls in 3.527 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        4    1.284    0.321    1.284    0.321 <string>:1(worker_11_N10000000_numcalls4)
        3    0.961    0.320    0.961    0.320 <string>:1(worker_10_N10000000_numcalls3)
        2    0.640    0.320    0.640    0.320 <string>:1(worker_9_N10000000_numcalls2)
        1    0.319    0.319    0.319    0.319 <string>:1(worker_8_N10000000_numcalls1)
        4    0.110    0.028    0.110    0.028 <string>:1(worker_7_N1000000_numcalls4)
        3    0.087    0.029    0.087    0.029 <string>:1(worker_6_N1000000_numcalls3)
        2    0.062    0.031    0.062    0.031 <string>:1(worker_5_N1000000_numcalls2)
        1    0.036    0.036    0.036    0.036 <string>:1(worker_4_N1000000_numcalls1)
        4    0.010    0.003    0.010    0.003 <string>:1(worker_3_N100000_numcalls4)
        3    0.008    0.003    0.008    0.003 <string>:1(worker_2_N100000_numcalls3)
        2    0.005    0.003    0.005    0.003 <string>:1(worker_1_N100000_numcalls2)
        1    0.004    0.004    0.004    0.004 <string>:1(worker_0_N100000_numcalls1)
       12    0.000    0.000    0.000    0.000 :0(print)
        1    0.000    0.000    3.527    3.527 /home/jgerity/personal/playground/python/profiling/interruptable_profile/profiler_target.py:38(main)
        1    0.000    0.000    0.000    0.000 :0(setprofile)
        1    0.000    0.000    3.527    3.527 :0(exec)
        1    0.000    0.000    3.527    3.527 profile:0(target_main())
        1    0.000    0.000    3.527    3.527 <string>:1(<module>)
        1    0.000    0.000    0.000    0.000 :0(items)
        0    0.000             0.000          profile:0(profiler)


```

## Partial (interrupted) profile

```
$ python3 run_profiler.py --outfile partial.prof
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
^CTraceback (most recent call last):
  File "run_profiler.py", line 27, in <module>
    main()
  File "run_profiler.py", line 21, in main
    pr.runctx("target_main()", globals=globals(), locals=globals())
  File "/usr/lib/python3.8/profile.py", line 422, in runctx
    exec(cmd, globals, locals)
  File "<string>", line 1, in <module>
  File "/home/jgerity/personal/playground/python/profiling/interruptable_profile/profiler_target.py", line 42, in main
    func()
  File "<string>", line 2, in worker_9_N10000000_numcalls2
KeyboardInterrupt

$ python3 -c "from pstats import Stats; s = Stats('partial.prof'); s.sort_stats('tottime'); s.print_stats()"
Fri May 19 20:27:08 2023    partial.prof

         39 function calls in 1.303 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        2    0.653    0.327    0.653    0.327 <string>:1(worker_9_N10000000_numcalls2)
        1    0.320    0.320    0.320    0.320 <string>:1(worker_8_N10000000_numcalls1)
        4    0.116    0.029    0.116    0.029 <string>:1(worker_7_N1000000_numcalls4)
        3    0.089    0.030    0.089    0.030 <string>:1(worker_6_N1000000_numcalls3)
        2    0.063    0.031    0.063    0.031 <string>:1(worker_5_N1000000_numcalls2)
        1    0.035    0.035    0.035    0.035 <string>:1(worker_4_N1000000_numcalls1)
        4    0.010    0.003    0.010    0.003 <string>:1(worker_3_N100000_numcalls4)
        3    0.008    0.003    0.008    0.003 <string>:1(worker_2_N100000_numcalls3)
        2    0.006    0.003    0.006    0.003 <string>:1(worker_1_N100000_numcalls2)
        1    0.003    0.003    0.003    0.003 <string>:1(worker_0_N100000_numcalls1)
        1    0.001    0.001    0.001    0.001 :0(setprofile)
       10    0.000    0.000    0.000    0.000 :0(print)
        1    0.000    0.000    1.303    1.303 /home/jgerity/personal/playground/python/profiling/interruptable_profile/profiler_target.py:38(main)
        1    0.000    0.000    1.303    1.303 :0(exec)
        1    0.000    0.000    1.303    1.303 profile:0(target_main())
        1    0.000    0.000    1.303    1.303 <string>:1(<module>)
        1    0.000    0.000    0.000    0.000 :0(items)
```
