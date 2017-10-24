import mainwindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QCheckBox
from PyQt5 import QtCore
from PyQt5 import QtGui
import random
import time
import threading
import name_generator
from termcolor import cprint

JOB_POOL_LOCK = threading.Lock()
WAITING_LIST_LOCK = threading.Lock()
used_PIDs = set()

mode = 'priority'

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
        self.operation = 'suspend'

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
        while pid in used_PIDs:
            pid = random.randint(1, 10000)
        name = name_generator.gen_one_word_digit(lowercase=False)
        priority = random.randint(1, 7)
        required_time = random.randint(200, 1000)
        used_PIDs.add(pid)
        return PCB(pid, name, priority, required_time)

    # Generate a PID
    @staticmethod
    def generate_pid():
        pid = random.randint(1, 10000)
        # Avoid duplicated PID
        while pid in used_PIDs:
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
            # Append to pool
            self._pool.append(job)

            # Change job's status
            if type(self).__name__ == 'TerminatedPool':
                job.status = 'terminated'
            elif type(self).__name__ == 'WaitingList':
                job.status = 'ready'

            # Append to table widget
            if type(self).__name__ == 'JobPool':
                job_pool_table_control.append(job)
            elif type(self).__name__ == 'TerminatedPool':
                terminated_table_control.append(job)
            elif type(self).__name__ == 'WaitingList':
                running_table_control.append(job)


class JobPool(Pool):
    # Get the first job and remove it from job pool
    def pop(self):
        if self._pool:
            job = self._pool.pop(0)
            # job_pool_table_control.remove(job)
            return job


class TerminatedPool(Pool):
    pass


class WaitingList(Pool):
    def __init__(self, scheduling_mode='priority', max=5):
        super().__init__()
        self.scheduling_mode = scheduling_mode
        self.max = max

    def __repr__(self):
        return self.__str__()

    # Get a job for CPU to process
    def get(self):
        if self.scheduling_mode == 'priority':
            # If using priority, sort waiting list using priority of each job
            self._pool = sorted(self._pool, key=lambda item: item.priority)
        return self._pool[0]

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
                cprint('{0} terminated'.format(each.name), color='red')
                terminated_pool.add(each)

    # Tell how many items in waiting list
    def num(self):
        return len(self._pool)


# Create pools instances
job_pool = JobPool()
waiting_list = WaitingList(scheduling_mode='priority', max=5)
terminated_pool = TerminatedPool()


class TableControl(object):
    def __init__(self, table, content_each_line):
        self.table = table
        self.content_each_line = content_each_line

    def append(self, process):
        running_table_control_lock.acquire()

        print(self.table.rowCount())

        self.table.setRowCount(self.table.rowCount() + 1)

        for j in range(0, len(self.content_each_line)):
            item = QTableWidgetItem(str(eval('process.' + self.content_each_line[j])))

            # Add item to table
            self.table.setItem(self.table.rowCount() - 1,
                               j,
                               item)

            # Scroll to item
            self.table.scrollToItem(item)

        running_table_control_lock.release()

    def remove(self, process):
        pass
        """
        
                for i in range(0, self.table.rowCount()-1):
            if self.table.item(i, 0).text() == str(process.pid):
                print("hey")
                # Clear this row
                for j in range(0, len(self.content_each_line)):
                    pass
                    #print(self.table.itemAt(i, j))

                #time.sleep(1)

                
                # Move rows after me
                if i < self.table.rowCount() - 1:
                    for j in range(i + 1, self.table.rowCount()):
                        for k in range(0, len(self.content_each_line)):
                            self.table.setItem(i, j, QTableWidgetItem(self.table.item(i + 1, j).text()))
                

        """


class MainWindow(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        # Set table width
        self.JobPoolTable.setColumnWidth(0, 50)
        self.RunningTable.setColumnWidth(0, 50)
        self.SuspendTable.setColumnWidth(0, 50)

        # Stretch last column of the table
        # UI_main_window.JobPoolTable.horizontalHeader().setStretchLastSection(True)
        self.TerminatedTable.horizontalHeader().setStretchLastSection(True)
        self.RunningTable.horizontalHeader().setStretchLastSection(True)
        self.SuspendTable.horizontalHeader().setStretchLastSection(True)

        # Connect slots
        self.StartButton.clicked.connect(self.slotStartButton)
        self.GenerateJobButton.clicked.connect(self.slotGenerateJobButton)
        self.AddJobButton.clicked.connect(self.slotAddJobButton)
        self.DaoshuBox.valueChanged.connect(self.slotMaxWaitingChanged)
        # UI_main_window.JobPoolTable.currentCellChanged(0,0).connect(JobPoolTableControl.checkbox_changed)

    def slotStartButton(self):
        waiting_list.max = self.DaoshuBox.value()
        running_table_control.append(PCB(123, "123", 1, 55))

        # Create thread
        st_scheduling_thread = threading.Thread(target=short_term_scheduling_thread,
                                                args=(mode, waiting_list))
        lt_scheduling = threading.Thread(target=long_term_scheduling_thread,
                                         args=(mode, waiting_list, job_pool))

        # Start thread
        st_scheduling_thread.start()
        lt_scheduling.start()

    def slotGenerateJobButton(self):
        for i in range(self.RandomCountBox.value()):
            random_process = PCB.random()
            job_pool.add(random_process)

    def slotAddJobButton(self):
        job_pool.add(PCB(PCB.generate_pid(),
                         self.AddJobNameEdit.text(),
                         self.AddJobPriorityEdit.text(),
                         self.AddJobTimeEdit.text()))

    def slotMaxWaitingChanged(self):
        waiting_list.max = self.DaoshuBox.value()


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
            job = job_pool.pop()
            waiting_list.add(job)
            WAITING_LIST_LOCK.release()

        time.sleep(0.01)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    UI_main_window = MainWindow()
    UI_main_window.show()

    job_pool_table_control = TableControl(table=UI_main_window.JobPoolTable,
                                          content_each_line=['pid',
                                                             'name',
                                                             'status',
                                                             'priority',
                                                             'required_time'])
    job_pool_table_control_lock = threading.Lock()

    running_table_control = TableControl(table=UI_main_window.RunningTable,
                                         content_each_line=['pid',
                                                            'name',
                                                            'status',
                                                            'priority',
                                                            'required_time',
                                                            'address',
                                                            'operation'])
    running_table_control_lock = threading.Lock()

    terminated_table_control = TableControl(table=UI_main_window.TerminatedTable,
                                            content_each_line=['pid', 'name'])
    terminated_table_control_lock = threading.Lock()

    exit(app.exec_())
