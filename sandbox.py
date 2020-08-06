# file for testing random shit!
import time
import random

num_sims = 1000
num_elements = 10000

t_total = 0
for i in range(num_sims):
    words_s = ''
    t0 = time.time()
    for i in range(num_elements):
        words_s += str(i) + ', '
    t1 = time.time()
    t_total += t1 - t0

ave_time = t_total / num_sims
print(f"{num_sims} strings loaded with {num_elements} elements. "
      f"average time elapsed {ave_time * 1000:.4f} ms per load.")

t_total = 0
for i in range(num_sims):
    target = str(random.randint(0, num_elements - 1)) + ', '
    t0 = time.time()
    target in words_s
    t1 = time.time()
    t_total += t1 - t0

ave_time = t_total / num_sims
print(f"{num_sims} searches conducted on strings. "
      f"average time elapsed {ave_time * 1000:.4f} ms per search.")

t_total = 0
for i in range(num_sims):
    words_l = []
    t0 = time.time()
    for i in range(num_elements):
        words_l.append(i)
    t1 = time.time()
    t_total += t1 - t0

ave_time = t_total / num_sims
print(f"{num_sims} lists loaded with {num_elements} elements. "
      f"average time elapsed {ave_time * 1000:.4f} ms per load.")

t_total = 0
for i in range(num_sims):
    target = random.randint(0, num_elements - 1)
    t0 = time.time()
    target in words_l
    t1 = time.time()
    t_total += t1 - t0

ave_time = t_total / num_sims
print(f"{num_sims} searches conducted on lists. "
      f"average time elapsed {ave_time * 1000:.4f} ms per search.")

t_total = 0
for i in range(num_sims):
    t0 = time.time()
    copy = words_l.copy()
    t1 = time.time()
    t_total += t1 - t0

ave_time = t_total / num_sims
print(f"{num_sims} lists copied via copy() function. "
      f"average time elapsed {ave_time * 1000:.4f} ms per copy.")

t_total = 0
for i in range(num_sims):
    t0 = time.time()
    copy = words_l[:]
    t1 = time.time()
    t_total += t1 - t0

ave_time = t_total / num_sims
print(f"{num_sims} lists copied via [:] slice. "
      f"average time elapsed {ave_time * 1000:.4f} ms per copy.")
