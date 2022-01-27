import psutil
import time
import multiprocessing

def child(all_pid):
    all_pid[multiprocessing.current_process().pid] = 'child'
    while True:
        dum = (10**5 + 3**21)**50

def main():
    all_pid = multiprocessing.Manager().dict()
    all_pid[multiprocessing.current_process().pid] = 'main'
    cp = multiprocessing.Process(target=child, args=(all_pid,))
    cp.start()
    while True:
        info = dict()
        for pid, name in all_pid.items():
            cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
            info[name] = cpu_usage
        print(info)
        time.sleep(1)

if __name__=='__main__':
    main()