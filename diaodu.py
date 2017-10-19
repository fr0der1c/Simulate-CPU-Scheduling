import mainwindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QCheckBox
import random
import time
import threading
import name_generator
from termcolor import cprint

JOB_POOL_LOCK = threading.Lock()
WAITING_LIST_LOCK = threading.Lock()
PIDs = set()

# Waiting time for clearer show
CPU_PROCESS_TIME = 0.1

# Add priority each tern
PRIORITY_ADD_EACH_TERN = 0.5


class PCB(object):
    def __init__(self, pid, name, priority, required_time):
        self.pid = pid
        self.name = name
        self.priority = priority
        self.required_time = required_time
        self.status = 'new'
        self.address = hex(id(self))

    def __str__(self):
        cprint("<PCB {0} {2}[{1}]> priority:".format(str(self.pid),
                                                     str(self.status),
                                                     self.name), end='')
        cprint("{0}".format(str(self.priority)), color='red', end='')
        cprint(" need_time:{0} address:{1}".format(str(self.required_time), self.address), end='')
        return ''

    def __repr__(self):
        return "<PCB {0} {3}[{1}]> priority:{2} need_time:{4}".format(str(self.pid),
                                                                      str(self.status),
                                                                      str(self.priority),
                                                                      self.name,
                                                                      str(self.required_time))

    # Get a random job
    @staticmethod
    def random():
        pid = random.randint(1, 10000)
        # Avoid duplicated PID
        while pid in PIDs:
            pid = random.randint(1, 10000)
        name = name_generator.gen_one_word_digit(lowercase=False)
        priority = random.randint(1, 7)
        required_time = random.randint(200, 1000)
        PIDs.add(pid)
        return PCB(pid, name, priority, required_time)

    # Generate a PID
    @staticmethod
    def generate_pid():
        pid = random.randint(1, 10000)
        # Avoid duplicated PID
        while pid in PIDs:
            pid = random.randint(1, 10000)
        return pid


class Pool(object):
    def __init__(self):
        self._pool = []

    def __str__(self):
        print("<{1} Pool ({0})>".format(len(self._pool), type(self).__name__))
        for job in self._pool:
            print(job)
        print('')
        return ""

    def __repr__(self):
        return "<PCB Pool ({0})>:{1}".format(len(self._pool), [job for job in self._pool])

    # Add a job to job pool
    def add(self, job):
        if isinstance(job, PCB):
            self._pool.append(job)
        if type(self).__name__ == 'JobPool':
            JobPoolTableControl.append(job)


class JobPool(Pool):
    def __init__(self):
        super().__init__()

    # Get the first job and remove it from job pool
    def get(self):
        if self._pool:
            return self._pool.pop(0)
        else:
            return


class WaitingList(Pool):
    def __init__(self, scheduling_mode='priority', max=5):
        super().__init__()
        self.scheduling_mode = 'priority' if scheduling_mode == 'priority' else 'time_slice'
        self.max = max

    def __repr__(self):
        return self.__str__()

    # Get a job for CPU to process
    def get(self):
        if self.scheduling_mode == 'priority':
            # If using priority, sort waiting list using priority of each job
            self._pool = sorted(self._pool, key=lambda item: item.priority)
        return self._pool[0]

    # Add a job
    def add(self, job):
        if isinstance(job, PCB):
            self._pool.append(job)
            job.status = 'ready'

    # Remove a job
    def pop(self, job):
        for each in self._pool:
            if each.generate_pid == job.generate_pid:
                self._pool.remove(each)

    # Remove terminated job
    def remove_terminated(self):
        for each in self._pool:
            if each.required_time == 0:
                self.pop(each)
                each.status = 'terminated'
                print('{0} terminated'.format(each.name))
                terminated_pool.add(each)

    # Tell how many items in waiting list
    def num(self):
        return len(self._pool)


class TerminatedPool(Pool):
    pass


terminated_pool = TerminatedPool()


# CPU scheduling Thread
def short_term_scheduling_thread(mode, waiting_list):
    while True:
        # Get a job from waiting list
        if waiting_list.num() > 0:
            WAITING_LIST_LOCK.acquire()
            processing_job = waiting_list.get()
            WAITING_LIST_LOCK.release()
            processing_job.status = 'running'

            if mode == 'priority':
                # Priority mode
                print('Running {0}...'.format(processing_job.name))
                # Actively adjust job's priority
                processing_job.priority += PRIORITY_ADD_EACH_TERN

                # Just for show
                time.sleep(CPU_PROCESS_TIME)

                if processing_job.required_time >= 40:
                    print('Running {0}...'.format(processing_job.name))
                    processing_job.required_time -= 40
                    processing_job.status = 'ready'
                else:
                    # Required time of this job is less than quantum time
                    print('Running {0}...'.format(processing_job.name))
                    processing_job.required_time = 0
                    processing_job.status = 'ready'

        time.sleep(0.01)


# Advanced scheduling
def long_term_scheduling_thread(mode, waiting_list, job_pool):
    while True:
        # Remove terminated jobs
        waiting_list.remove_terminated()

        # If waiting list isn't full, transfer job from job poll to waiting list
        if waiting_list.num() < waiting_list.max:
            WAITING_LIST_LOCK.acquire()
            waiting_list.add(job_pool.get())
            WAITING_LIST_LOCK.release()

        time.sleep(0.01)


app = QApplication(sys.argv)
UI_main_window = mainwindow.Ui_MainWindow()
window = QMainWindow()
UI_main_window.setupUi(window)

# Demo Parameter
num_job_to_create = 5
num_waiting_max = 3
mode = 'priority'

# Create job_pool
job_pool = JobPool()

# Create waiting list
waiting_list = WaitingList(scheduling_mode='priority', max=num_waiting_max)
for _ in range(num_waiting_max):
    waiting_list.add(job_pool.get())
print("Waiting list:")
print(waiting_list)

"""
# Create CPU thread
st_scheduling_thread = threading.Thread(target=short_term_scheduling_thread,
                                        args=(mode, waiting_list))
lt_scheduling = threading.Thread(target=long_term_scheduling_thread,
                                 args=(mode, waiting_list, job_pool))
st_scheduling_thread.start()
lt_scheduling.start()
st_scheduling_thread.join()
lt_scheduling.join()
"""


class TableControl(object):
    @staticmethod
    def append_to_table(table, content_each_line, process):
        table.setRowCount(table.rowCount() + 1)
        check_box_item = QTableWidgetItem()
        check_box_item.setCheckState(2)
        table.setItem(table.rowCount() - 1, 0, check_box_item)
        for j in range(0, len(content_each_line)):
            item = QTableWidgetItem(str(eval('process.' + content_each_line[j])))
            table.setItem(table.rowCount() - 1,
                          j + 1,
                          item)


class JobPoolTableControl(TableControl):
    content_each_line = ['pid', 'name', 'status', 'priority', 'required_time']

    @staticmethod
    def append(process):
        TableControl.append_to_table(UI_main_window.JobPoolTable, JobPoolTableControl.content_each_line, process)


def slotStartButton():
    item = QTableWidgetItem("haha")
    UI_main_window.JobPoolTable.setRowCount(2)
    UI_main_window.JobPoolTable.setItem(1, 1, item)
    print("re")


def slotGenerateJobButton():
    for i in range(UI_main_window.RandomCountBox.value()):
        random_process = PCB.random()
        job_pool.add(random_process)

    print("Inited job_pool:")
    print(job_pool)


def slotAddJobButton():
    job_pool.add(PCB(PCB.generate_pid(),
                     UI_main_window.AddJobNameEdit.text(),
                     UI_main_window.AddJobPriorityEdit.text(),
                     UI_main_window.AddJobTimeEdit.text()))


# Set table width
UI_main_window.JobPoolTable.setColumnWidth(0, 30)
UI_main_window.RunningTable.setColumnWidth(0, 30)
UI_main_window.SuspendTable.setColumnWidth(0, 30)

# Stretch last column of the table
UI_main_window.JobPoolTable.horizontalHeader().setStretchLastSection(True)
UI_main_window.TerminatedTable.horizontalHeader().setStretchLastSection(True)

# Connect slots
UI_main_window.StartButton.clicked.connect(slotStartButton)
UI_main_window.GenerateJobButton.clicked.connect(slotGenerateJobButton)
UI_main_window.AddJobButton.clicked.connect(slotAddJobButton)

if __name__ == '__main__':
    window.show()
    exit(app.exec_())
