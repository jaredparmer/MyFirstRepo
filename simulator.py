# file for testing puzzle solves
import time
import random
import statistics

""" simulation function that takes given arguments and performs given
function with those arguments for given number of times, then reports
summary results.
"""
def simulate(fn, *args, num_sims=1000):
    times = []
    for i in range(num_sims):
        t0 = time.time()
        fn(*args)
        t1 = time.time()
        times.append(t1 - t0)

    mean = statistics.mean(times)
    var = statistics.variance(times)

    print(f"{fn} called {num_sims} times.")
    print(f"\tmean \t {mean * 1000:.10f} ms per call")
    print(f"\tvar \t {var * 1000:.10f} ms per call")
