import os
import signal
from subprocess import Popen, PIPE
from sys import stdout

class Process(object):
    def __init__(self, proc_info):
        self.user = proc_info[0] if len(proc_info) > 0 else ''
        self.pid = proc_info[1] if len(proc_info) > 1 else ''
        self.cpu = proc_info[2] if len(proc_info) > 2 else ''
        self.mem = proc_info[3] if len(proc_info) > 3 else ''
        self.vsz = proc_info[4] if len(proc_info) > 4 else ''
        self.rss = proc_info[5] if len(proc_info) > 5 else ''
        self.tty = proc_info[6] if len(proc_info) > 6 else ''
        self.stat = proc_info[7] if len(proc_info) > 7 else ''
        self.start = proc_info[8] if len(proc_info) > 8 else ''
        self.time = proc_info[9] if len(proc_info) > 9 else ''
        self.cmd = proc_info[10] if len(proc_info) > 10 else ''
        
    def to_str(self):
        return '%s %s %s' % (self.user, self.pid, self.cmd)

    def name(self):
        return '%s' % self.cmd

    def procid(self):
        return '%s' % self.pid

    @staticmethod
    def kill_logger(key_pid):
        stdout.write("\n\nDo you want to stop this process: y/n ?")
        response = input()
        if response.lower() == "y":
            os.kill(int(key_pid), signal.SIGILL)
        else:
            pass

    @staticmethod
    def get_process_list():
        process_list = []
        sub_process = Popen(['tasklist', '/fo', 'csv', '/v'], shell=True, stdout=PIPE)
        sub_process.stdout.readline()
        for line in sub_process.stdout:
            proc_info = [x.strip('"') for x in line.decode().split(',')]
            process_list.append(Process(proc_info))
        return process_list

if __name__ == "__main__":
    process_list = Process.get_process_list()
    stdout.write('Reading Process list...\n')
    process_cmd = []
    process_pid = []
    l1 = ["logkey", "keylog", "keysniff", "kisni", "lkl", "ttyrpld", "uber", "vlogger"]
    record = 0
    flag = 1
    for process in process_list:
        process_cmd.append(process.name())
        process_pid.append(process.procid())

    for x in process_cmd:
        for y in l1:
            if x.lower().find(y.lower()) > -1:
                stdout.write("KeyLogger Detected: \nThe following process may be a key logger: \n\n\t" + process_pid[record] + " ---> " + x)
                Process.kill_logger(process_pid[record])
                flag = 0
        record += 1

    if flag:
        print("No Keylogger Detected")

