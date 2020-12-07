import tkinter as tk
import heapq

records = []

loader_queue = [] # queue
weigh_queue = [] # queue
future_event_list = [] # min priority_queue

n_loader = 2
n_scale = 1

n_trucks_in_loader = 0
n_trucks_in_weigh = 0
n_trucks_travel = 6
n_trucks = n_trucks_in_loader + n_trucks_in_weigh + n_trucks_travel

n_events = 50

# asumsi distribusi normal
load_time_mean = 10
load_time_std = 3
weigh_time_mean = 15
weigh_time_std = 4
travel_time_mean = 30
travel_time_std = 10

import numpy as np
get_load_time = lambda : int(round(np.random.normal(load_time_mean, load_time_std)))
get_weigh_time = lambda : int(round(np.random.normal(weigh_time_mean, weigh_time_std)))
get_travel_time = lambda : int(round(np.random.normal(travel_time_mean, travel_time_std)))

trucks_in_loader = []
trucks_in_scale = []

for i in range(n_trucks_in_loader):
    next_event = (0, 'EL', "DT%d" % i)
    heapq.heappush(future_event_list, next_event)
    heapq.heappush(trucks_in_loader, next_event)

for i in range(n_trucks_in_weigh):
    next_event = (0, 'EW', "DT%d" % (n_trucks_in_loader + i))
    heapq.heappush(future_event_list, next_event)
    heapq.heappush(trucks_in_scale, next_event)

for i in range(n_trucks_travel):
    heapq.heappush(future_event_list, (0, 'ALQ', "DT%d" % (n_trucks_in_loader + n_trucks_in_weigh + i)))

n_empty_scale = n_scale - len(trucks_in_scale)
n_empty_loader = n_loader - len(trucks_in_loader)

print("INISIAL")
print("------------------")
print("clock: ", 0)
print("loader queue: ", loader_queue)
print("trucks in loader: ", sorted(trucks_in_loader))
print("weigh queue: ", weigh_queue)
print("trucks in scale: ", sorted(trucks_in_scale))
print("fel: ", sorted(future_event_list))
print()

for i in range(n_events): # banyak event yang akan diproses
    # proses future event list paling depan, update clocknya
    event = heapq.heappop(future_event_list)
    clock = event[0]

    if event[1] == 'EL':
        heapq.heappop(trucks_in_loader)
        # langsung pindah ke weigh queue
        if n_empty_scale > 0:
            # langsung masukkan ke scale, set jadwal kalau scale kelar
            next_event = (clock + get_load_time(), 'EW', event[2])
            heapq.heappush(future_event_list, next_event)
            heapq.heappush(trucks_in_scale, next_event)
            n_empty_scale -= 1
        else:
            weigh_queue.append((event[2], clock))

        # isi loader yang kosong, atau catat empty loader kalau tidak ada queue
        if len(loader_queue) > 0:
            next_to_load = loader_queue.pop(0)
            next_event = (clock + get_load_time(), 'EL', next_to_load[0])
            heapq.heappush(future_event_list, next_event)
            heapq.heappush(trucks_in_loader, next_event)
        else:
            n_empty_loader += 1
    elif event[1] == 'EW':
        heapq.heappop(trucks_in_scale)
        # set jadwal untuk masuk ALQ setelah travelling
        heapq.heappush(future_event_list, (clock + get_travel_time(), 'ALQ', event[2]))

        # isi scale yang kosong, atau catat empty scale kalau tidak ada queue
        if len(weigh_queue) > 0:
            next_to_weigh = weigh_queue.pop(0)  # id truck, clock
            next_event = (clock + get_weigh_time(), 'EW', next_to_weigh[0])
            heapq.heappush(future_event_list, next_event)
            heapq.heappush(trucks_in_scale, next_event)
        else:
            n_empty_scale += 1
    elif event[1] == 'ALQ':
        if n_empty_loader > 0:
            # langsung masukkan ke loader
            next_event = (clock + get_load_time(), 'EL', event[2])
            heapq.heappush(future_event_list, next_event)
            heapq.heappush(trucks_in_loader, next_event)
            n_empty_loader -= 1
        else:
            loader_queue.append((event[2], clock))  # (id truck, clock)

    
    print("ITERASI %d" % i)
    print("------------------")
    print("clock: ", clock)
    print("loader queue: ", loader_queue)
    print("trucks in loader: ", sorted(trucks_in_loader))
    print("weigh queue: ", weigh_queue)
    print("trucks in scale: ", sorted(trucks_in_scale))
    print("fel: ", sorted(future_event_list))
    print()

    records.append(
        [
            clock,
            loader_queue,
            sorted(trucks_in_loader),
            weigh_queue,
            sorted(trucks_in_scale),
            sorted(future_event_list)
        ]
    )

#main
window = tk.Tk()

columns = [
    "Clock t",
    "LQ(t)",
    "L(t)",
    "WQ(t)",
    "W(t)",
    "Loader Queue",
    "Weigh Queue",
    "Future Event List",
    "BL",
    "BS"
]

for i,c in enumerate(columns):
    tk.Label(window, text=c, borderwidth=1).grid(row=0,column=i)

for i,record in enumerate(records,start=1):
    for j,c in enumerate(record):
        tk.Label(window, text=c, borderwidth=1).grid(row=i,column=j)

window.mainloop()
