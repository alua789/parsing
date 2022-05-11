from concurrent.futures import ThreadPoolExecutor
from threading import *
import time

def func_1(num):
    for i in range(0, num):
        print(f"Function_1 {i} run")
        time.sleep(1)

def func_2():
    for i in range(0, 10):
        print(f"Function_2 {i} run")
        time.sleep(1)
#
# x1 = time.time()
# func_1(10)
# func_1(10)
# func_1(5)
# print(time.time()-x1)

# t1 = Thread(target=func_1(10))
# t3 = Thread(target=func_1(10))
# t2 = Thread(target=func_1(5))
start = time.time()
# t1.start()
# t2.start()
# t3.start()
# t1.join()
# t2.join()
# t3.join()
# print(time.time()-start)
with ThreadPoolExecutor(max_workers=5) as executor:
    f1 = [executor.submit(func_1, num) for num in range(1,6)]


print(time.time()-start)
# with ThreadPoolExecutor(max_workers=2) as executor:
#     f1 = executor.submit(func_1())
#     f2 = executor.submit(func_2())



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint

