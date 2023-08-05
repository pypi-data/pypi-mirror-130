import matplotlib.pyplot as plt
import numpy as np
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time

from fast_map import fast_map#, fast_map_simple


def io_and_cpu_expensive_blocking_function(x):
    time.sleep(1)
    for i in range(10 ** 6):
        pass
    return x

def cpu_expensive_blocking_function(x):
    for i in range(10 ** 6):
        pass
    return x

# def get_fast_map_simple(numbers, workers, func):
#     gen_obj = fast_map_simple(func, numbers, threads_limit=workers)
#     for i in gen_obj:
#         pass

def get_fast_map(numbers, func, workers=None):
    for i in fast_map(func, numbers, threads_limit=workers): pass

def get_ThreadPoolExecutor(numbers, func, workers=None):
    if workers:
        with ThreadPoolExecutor(workers) as executor:
            for i in executor.map(func, numbers): pass
    else:
        with ThreadPoolExecutor() as executor:
            for i in executor.map(func, numbers): pass


def get_ProcessPoolExecutor(numbers, func, workers=None):
    if workers:
        with ProcessPoolExecutor(workers) as executor:
            for i in executor.map(func, numbers): pass
    else:
        with ProcessPoolExecutor() as executor:
            for i in executor.map(func, numbers): pass

def get_standard_map(numbers, func, **kw):
    for i in map(func, numbers): pass

def display(labels, results, title='', x_label='', colors=None):
    x = np.arange(len(labels))  # the label locations
    width = 0.8 / len(results) # the width of the bars

    fig, ax = plt.subplots()
    rects = []
    print(labels, results)
    width_to_add = 0
    for i, (name, durations) in enumerate(results.items()):
        x2 = x - width*(len(results)/2) + width_to_add
        if colors:
            rects.append( ax.bar(x2, durations, width, label=name, color=colors[i]) )
        else:
            rects.append( ax.bar(x2, durations, width, label=name) )
        width_to_add += width

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Duration')
    ax.set_xlabel(x_label)
    ax.set_title(title)
    ax.set_xticks(x, labels)
    ax.legend(loc='upper left')

    for rect in rects:
        ax.bar_label(rect, fmt='%.1f', padding=3)

    fig.tight_layout()

    plt.show()


def input_types_tests():
    def t_single(a):
        return a**a
    def t_multi(a, b):
        return a+b
    def t_str_single(a):
        return a
    def t_str_multi(a, b):
        return '|'.join([a,b])
    def t_list(a):
        return '|'.join([str(s) for s in a])
        
    for i in fast_map(t_single, [1,2,3,4]):
        print(i)
    for i in fast_map(t_multi, (1,2), (3,4)):
        print(i)
        
    for i in fast_map(t_str_multi, ('abc', 'efg'), ('a', 'b')):
        print(i)
    for i in fast_map(t_str_single, ['abc', 'efg', 'a', 'b']):
        print(i)
    for i in fast_map(t_single, range(10)):
        print(i)
    for i in fast_map(t_list, ([1,2,3],)):
        print(i)



def test_cpu():
    from functools import partial
    #############################
    #  cpu only test
    #############################

    funcs = {
        'ProcessPoolExecutor (default max_workers)' : get_ProcessPoolExecutor,
        'fast_map (1 thread per 1 task)' : partial(get_fast_map, workers=None),
        'fast_map (threads_limit=30)' : partial(get_fast_map, workers=30),
        'fast_map (threads_limit=8)' : partial(get_fast_map, workers=8),
        'standard map' : get_standard_map,
        'ThreadPoolExecutor (default max_workers)' : get_ThreadPoolExecutor
        }
    results = {name:[] for name in funcs.keys()} 

    labels = []

    for i in range(100, 701, 300):
    # for i in range(100, 101):
        labels.append(f'{i}')
        for j, (name, func) in enumerate(funcs.items()):
            start_time = time.time()  
            func(range(i), cpu_expensive_blocking_function)
            duration = time.time() - start_time
            print(name, duration)
            results[name].append( duration )

    display(labels,
            results,
            title = 'Strictly CPU-expensive tasks performance comparison',
            x_label = 'Number of tasks',
            colors=['orange', 'darkgreen', 'green', 'lightgreen', 'red', 'royalblue'])

        
def test_io_cpu():
    ############################# 
    # concurrency test (cpu + io)
    #############################
    funcs = {
        'fast_map' : get_fast_map,
        'ProcessPoolExecutor' : get_ProcessPoolExecutor,
        'ThreadPoolExecutor'  : get_ThreadPoolExecutor,
        #'fast_map_simple': get_fast_map_simple,
        }

    results = {name:[] for name in funcs.keys()} 
    labels = []
    
    for i in range(20, 30, 2): 
    # for i in range(20, 21): 
    # for i in range(1,2): 
        workers = int(i**(i*0.08))
        numbers = range(workers)
        labels.append( f'{workers}' ) 
        print('workers =', workers)

        for j, (name, func) in enumerate(funcs.items()):

            start_time = time.time()
            # ProcessPoolExecutor fails at around 1000 workers but takes significant amount
            # of time before raising exception (it also affects further tests).
            # So condition below is used.
            if workers > 1000 and func == get_ProcessPoolExecutor:
                duration = -1
            else: 
                try:
                    func(numbers, io_and_cpu_expensive_blocking_function, workers)
                    duration = time.time() - start_time
                except Exception as e:
                    print(e)
                    duration = -1
            results[name].append( duration )
            print(name, 'finished in:', duration)
            print()

    display(labels,
            results, 
            title='IO and CPU expensive task performance comparison (each task has its own worker to achieve full concurrency)', 
            x_label='Number of tasks', 
            colors=['darkgreen', 'orange', 'royalblue'])




if __name__ == '__main__':
    test_cpu()
    test_io_cpu()
