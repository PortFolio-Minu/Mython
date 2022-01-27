import os
from threading import Thread
import time

def _check_usage_of_cpu_and_memory():
    while True:
        pid = os.getpid()
        py  = psutil.Process(pid)
        
        cpu_usage   = os.popen("ps aux | grep " + str(pid) + " | grep -v grep | awk '{print $3}'").read()
        cpu_usage   = cpu_usage.replace("\n","")
        
        memory_usage  = round(py.memory_info()[0] /2.**30, 2)
        
        print("cpu usage\t\t:", cpu_usage, "%")
        print("memory usage\t\t:", memory_usage, "%")

        print("Test")
        time.sleep(2)

if __name__ == "__main__":
    count = 10
    th1 = Thread(target=_check_usage_of_cpu_and_memory, args=())
    
    th1.start()
    th1.join()

    while True :
        count = count*count
        if (count > 100000000000):
            count = 10

