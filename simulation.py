import mainwindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget
from PyQt5 import QtCore, QtGui
import random
import time
import threading
import functools
import name_generator
from termcolor import cprint

MODE = 'priority'  # priority is the only available choice
CPU_PROCESS_TIME = 0.04  # Waiting time for clearer show
PRIORITY_ADD_EACH_TERN = 0.5  # Add priority each tern
PRIORITY_MAX = 10  # Limit job's max priority to avoid too big priority
AGING_TABLE = [0.1, 0.1, 0.2, 0.4, 0.4, 0.5, 1.0, 1.0, 1.5, 1.5, 2.0, 2.5, 3.0, 3.5, 3.8]
COLOR_MEMORY = QtGui.QColor(12, 249, 20)
COLOR_USED_MEMORY = QtGui.QColor(255, 152, 0)
TOTAL_MEM = 122
MEM_OS_TAKE = 20  # How much memory would operating system take


def mutex_lock(fun):
    """
    Mutex lock decorator for pools

    :param fun: function to decorate
    :return: wrapped function
    """

    @functools.wraps(fun)
    def wrapper(*args):
        # print("%s acquire" % args[0].lock)
        args[0].lock.acquire()
        value = fun(*args)
        # print("%s release" % args[0].lock)
        args[0].lock.release()
        return value

    return wrapper


class PCB(object):
    def __init__(self, pid, name="process", priority=1, required_time=200):
        self.pid = pid
        self.name = name if name else "process"
        self.priority = priority if priority else 1
        self.required_time = required_time if required_time else 200
        self.status = 'new'
        self.address = hex(id(self))
        self.age = 0
        self.required_memory = random.randint(1, 10)
        self.allocated_memory_start = None

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

    @staticmethod
    def random():
        """
        Generate a random job

        :return: a random job object
        """
        pid = random.randint(1, 10000)
        # Avoid duplicated PID
        while pid in used_PIDs:
            pid = random.randint(1, 10000)
        name = name_generator.gen_one_word_digit(lowercase=False)
        priority = random.randint(1, 7)
        required_time = random.randint(200, 1000)
        used_PIDs.add(pid)
        return PCB(pid, name, priority, required_time)

    @staticmethod
    def generate_pid():
        """
        Generate a random PID number

        :return: an unique int number
        """
        pid = random.randint(1, 10000)
        # Avoid duplicated PID
        while pid in used_PIDs:
            pid = random.randint(1, 10000)
        return pid


class Pool(QtCore.QObject):
    refreshTableSignal = QtCore.pyqtSignal("QString", PCB, "QString")
    editTableSignal = QtCore.pyqtSignal("QString", int, int, "QString")
    running_label_change_signal = QtCore.pyqtSignal("QString")

    def __init__(self):
        super().__init__()
        self._pool = []

        # Set table controller and mutex lock for each pool
        if type(self).__name__ == 'JobPool':
            self.table_controller = "job_pool_table_control"
            self.lock = JOB_POOL_LOCK
        elif type(self).__name__ == 'ReadyPool':
            self.table_controller = "ready_table_control"
            self.lock = READY_POOL_LOCK
        elif type(self).__name__ == 'SuspendPool':
            self.table_controller = "suspend_table_control"
            self.lock = SUSPEND_POOL_LOCK
        elif type(self).__name__ == 'TerminatedPool':
            self.table_controller = "terminated_table_control"
            self.lock = TERMINATED_POOL_LOCK

    def __str__(self):
        print("<{1} Pool ({0})>".format(len(self._pool), type(self).__name__))
        for job in self._pool:
            print(job)
        print('')
        return ""

    def __repr__(self):
        return "<PCB Pool ({0})>:{1}".format(len(self._pool), [job for job in self._pool])

    def connectSignal(self):
        self.refreshTableSignal.connect(UI_main_window.slotTableRefresh)
        self.editTableSignal.connect(UI_main_window.slotTableEdit)
        self.running_label_change_signal.connect(UI_main_window.slotChangeRunningLabel)

    @mutex_lock
    def add(self, job):
        """
        Add a job to pool

        :param job: Job to add
        :return: none
        """
        if isinstance(job, PCB):
            self._pool.append(job)

            # Change job's status
            if type(self).__name__ == 'TerminatedPool':
                job.status = 'terminated'
            elif type(self).__name__ == 'ReadyPool':
                job.status = 'ready'
            elif type(self).__name__ == 'SuspendPool':
                job.status = 'suspend'

            self.refreshTableSignal.emit(self.table_controller, job, "append")  # Append to table widget

    @property
    @mutex_lock
    def num(self):
        """
        Get number of items in pool

        :return: length of pool
        """
        return len(self._pool)

    def item(self, pid):
        """
        Get a item for specific PID

        :param pid: PID of item
        :return: An item of specified PID
        """
        for item in self._pool:
            if item.pid == int(pid):
                return item
        return None

    @mutex_lock
    def remove(self, identifier):
        """
        Remove a job
        :param identifier: job's pid or PCB
        :return: none
        """
        for each in self._pool:
            if isinstance(identifier, PCB):
                if each.pid == identifier.pid:
                    to_return = each
                    self.refreshTableSignal.emit(self.table_controller, identifier, "remove")
                    self._pool.remove(each)
                    return to_return
            elif isinstance(identifier, int):
                if each.pid == int(identifier):
                    to_return = each
                    self.refreshTableSignal.emit(self.table_controller, self.item(identifier), "remove")
                    self._pool.remove(each)
                    return to_return


class JobPool(Pool):
    @mutex_lock
    def pop(self):
        """
        Get the first job and remove it from job pool
        """
        if self._pool:
            job = self._pool.pop(0)
            self.refreshTableSignal.emit("job_pool_table_control", job, "remove")
            return job

    @mutex_lock
    def get(self):
        if self._pool:
            return self._pool[0]


class TerminatedPool(Pool):
    pass


class SuspendPool(Pool):
    pass


class ReadyPool(Pool):
    def __init__(self, scheduling_mode='priority', max=5):
        super().__init__()
        self.scheduling_mode = scheduling_mode
        self.max = max
        self.suspended_count = 0

    def __repr__(self):
        return self.__str__()

    @mutex_lock
    def get(self):
        """
        Schedule a job for CPU to process

        :return: a job in pool
        """
        if self.scheduling_mode == 'priority':
            self._pool = sorted(self._pool, key=lambda item: item.priority)
        return self._pool[0]

    def minus_time(self, job):
        """
        Minus a job's required_time and sync to table widget

        :param job: A job to minus its time
        :return: none
        """
        job.status = 'ready'
        if job.required_time >= 40:
            job.required_time -= 40
        else:
            job.required_time = 0

        # Update table widget
        self.editTableSignal.emit("ready_table_control", job.pid, 4, str(job.required_time))
        self.editTableSignal.emit("ready_table_control", job.pid, 2, "ready")

        # Need to be terminated
        if job.required_time == 0:
            cprint('{0} terminated'.format(job.name), color='red')
            self.remove(job.pid)  # remove job from waiting list
            memory.free(job.required_memory, job.allocated_memory_start)  # free memory
            terminated_pool.add(job)  # add to terminated pool
            if len(self._pool) == 0:
                self.running_label_change_signal.emit("")

    def change_priority(self, job):
        """
        Actively adjust job's priority

        :param job: Job running this time
        :return: none
        """
        job.age = 0
        if job.priority < PRIORITY_MAX:
            job.priority += PRIORITY_ADD_EACH_TERN
        self.editTableSignal.emit("ready_table_control", job.pid, 3, str(job.priority))
        self.editTableSignal.emit("ready_table_control", job.pid, 2, "running")
        self.running_label_change_signal.emit(job.name)

        # Change other job's age
        for process in self._pool:
            if process.pid != job.pid:
                if process.age < len(AGING_TABLE) - 1:
                    process.age += 1
                if process.priority - AGING_TABLE[process.age] >= 0:
                    process.priority -= AGING_TABLE[process.age]
                    self.editTableSignal.emit("ready_table_control", process.pid, 3, str(process.priority))

    def suspend(self, job):
        """
        Suspend a process

        :param job: job to suspend
        :return: none
        """
        self.remove(job)
        self.suspended_count += 1

    def resume(self, job):
        """
        Resume a suspended job

        :param job: job to resume
        :return: none
        """
        self.add(job)
        self.suspended_count -= 1

    @property
    def count(self):
        """
        :return: number of jobs that could be scheduled
        """
        return self.max - self.suspended_count


class TableController(object):
    def __init__(self, table, content_each_line):
        self.table = table
        self.content_each_line = content_each_line
        self.table.itemClicked.connect(self.itemClickedSlot)

        # Set different mutex lock for different QTableWidget
        if type(self).__name__ == 'JobPoolTableController':
            self.lock = JOB_POOL_TABLE_LOCK
        elif type(self).__name__ == 'ReadyTableController':
            self.lock = READY_TABLE_LOCK
        elif type(self).__name__ == 'SuspendTableController':
            self.lock = SUSPEND_TABLE_LOCK
        elif type(self).__name__ == 'TerminatedTableController':
            self.lock = TERMINATED_TABLE_LOCK

    @mutex_lock
    def append(self, process):
        """
        Append a row to table widget

        :param process: process to append to widget
        :return: none
        """
        self.table.setRowCount(self.table.rowCount() + 1)
        for j in range(0, len(self.content_each_line)):
            content = eval('process.' + self.content_each_line[j])
            if j == 3:
                # Special for priority column
                item = QTableWidgetItem(str("%.2f" % float(content)))
            elif j == 7:
                item = QTableWidgetItem(str(hex(content)))
            else:
                item = QTableWidgetItem(str(content))
            self.table.setItem(self.table.rowCount() - 1, j, item)  # Add item to table
            self.table.scrollToItem(item)  # Scroll to item

    @mutex_lock
    def remove(self, process):
        """
        Remove a row in table widget

        :param process: process to remove from table widget
        :return: none
        """
        for i in range(0, self.table.rowCount()):
            if self.table.item(i, 0).text() == str(process.pid):
                # Move rows after me
                if i < self.table.rowCount() - 1:
                    for j in range(i, self.table.rowCount() - 1):
                        for k in range(0, len(self.content_each_line)):
                            self.table.setItem(j, k, QTableWidgetItem(self.table.item(j + 1, k).text()))
                break

        self.table.setRowCount(self.table.rowCount() - 1)  # row count - 1

    @mutex_lock
    def edit(self, process_id, column, new_text):
        """
        Edit a item and change its background color to yellow

        :param process_id: PID of process
        :param column: column to edit
        :param new_text: new text of QTableWidgetItem
        :return: none
        """

        for i in range(0, self.table.rowCount()):
            if self.table.item(i, 0).text() == str(process_id):
                if column == 3:
                    new_text = "%.2f" % float(new_text)
                new_item = QTableWidgetItem(new_text)
                new_item.setBackground(QtGui.QColor(252, 222, 156))
                self.table.setItem(i, column, new_item)

    def itemClickedSlot(self, item):
        """
        Slot for suspending and resuming process

        :param item: QTableWidgetItem clicked
        """
        if type(self).__name__ == 'ReadyTableController':
            if item.column() == 0 and self.table.item(item.row(), 2).text() == "ready":
                print("Suspend %s" % self.table.item(item.row(), 0).text())
                process = ready_pool.item(self.table.item(item.row(), 0).text())
                print(process)
                ready_pool.suspend(process)
                suspend_pool.add(process)
        elif type(self).__name__ == 'SuspendTableController':
            if item.column() == 0:
                print("Resume %s" % self.table.item(item.row(), 0).text())
                process = suspend_pool.item(self.table.item(item.row(), 0).text())
                suspend_pool.remove(process)
                ready_pool.resume(process)


class JobPoolTableController(TableController):
    pass


class ReadyTableController(TableController):
    pass


class SuspendTableController(TableController):
    pass


class TerminatedTableController(TableController):
    pass


class Memory(QtCore.QObject):
    memory_edit_signal = QtCore.pyqtSignal("QString", int)

    def __init__(self, table):
        super().__init__()
        self.table = table
        self.lock = threading.Lock()
        self.free_mem = [{"start": 0, "length": TOTAL_MEM}]
        self.memory_edit_signal.connect(UI_main_window.slotMemoryTableEdit)

        # Init table widget
        for i in range(0, TOTAL_MEM):
            self.table.setRowCount(self.table.rowCount() + 1)
            item = QTableWidgetItem(" ")
            item.setBackground(COLOR_MEMORY)
            self.table.setItem(self.table.rowCount() - 1, 0, item)

    @mutex_lock
    def allocate(self, mem_need):
        """
        Allocate memory for a process

        :return: Starting address or "Failure"
        """
        for each_free_mem in self.free_mem:
            if each_free_mem["length"] >= mem_need:
                # Edit table widget
                for each_location in range(each_free_mem["start"], each_free_mem["start"] + mem_need):
                    self._edit_table_widget("allocate", each_location)

                each_free_mem["length"] -= mem_need
                each_free_mem["start"] += mem_need
                if each_free_mem["length"] == 0:
                    self.free_mem.remove(each_free_mem)
                return each_free_mem["start"] - mem_need
        return "Failure"

    @mutex_lock
    def free(self, mem_length, mem_start):
        """
        Free memory for a process

        :return: None
        """
        # Free memory on right bar
        for each_location in range(mem_start, mem_start + mem_length):
            self._edit_table_widget("free", each_location)
        # Free memory in free_mem list
        self.free_mem.append({"start": mem_start, "length": mem_length})
        while True:
            if_combined = False
            for mem1 in self.free_mem:
                for mem2 in self.free_mem:
                    if mem1["start"] + mem1["length"] == mem2["start"]:
                        mem1["length"] += mem2["length"]
                        self.free_mem.remove(mem2)
                        if_combined = True
            if not if_combined:
                break

    def _edit_table_widget(self, operation, location):
        self.memory_edit_signal.emit(operation, location)


class MainWindow(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)

        # Set table width
        self.JobPoolTable.setColumnWidth(0, 50)
        self.ReadyTable.setColumnWidth(0, 50)
        self.SuspendTable.setColumnWidth(0, 50)
        self.initial_width = self.width()

        # Settings for right bar
        self.setFixedWidth(1100)  # hide bar on the right
        self.rightBarWidget.setShowGrid(False)
        self.rightBarWidget.verticalHeader().setDefaultSectionSize(5)

        # Stretch last column of the table
        self.TerminatedTable.horizontalHeader().setStretchLastSection(True)
        self.ReadyTable.horizontalHeader().setStretchLastSection(True)
        self.SuspendTable.horizontalHeader().setStretchLastSection(True)

        # Connect slots
        self.StartButton.clicked.connect(self.slotStartButton)
        self.GenerateJobButton.clicked.connect(self.slotGenerateJobButton)
        self.AddJobButton.clicked.connect(self.slotAddJobButton)
        self.DaoshuBox.valueChanged.connect(self.slotMaxWaitingChanged)

    def slotStartButton(self):
        ready_pool.max = self.DaoshuBox.value()
        self.StartButton.setDisabled(True)
        self.StartButton.setText("正在运行")

        # Create thread
        st_scheduling_thread = threading.Thread(target=short_term_scheduling_thread,
                                                args=(MODE, ready_pool))
        lt_scheduling_thread = threading.Thread(target=long_term_scheduling_thread,
                                                args=(MODE, ready_pool, job_pool))

        memory.allocate(MEM_OS_TAKE)

        # Start thread
        st_scheduling_thread.start()
        lt_scheduling_thread.start()

        # Show memory bar
        self.setFixedWidth(self.initial_width)

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
        ready_pool.max = self.DaoshuBox.value()

    @QtCore.pyqtSlot("QString", PCB, "QString")
    def slotTableRefresh(self, controller_name, process, operation):
        if operation == "append":
            eval(controller_name + ".append(process)")
        elif operation == "remove":
            eval(controller_name + ".remove(process)")

    @QtCore.pyqtSlot("QString", int, int, "QString")
    def slotTableEdit(self, controller_name, pid, column, new_text):
        eval(controller_name + ".edit(pid, column, new_text)")

    @QtCore.pyqtSlot("QString", int)
    def slotMemoryTableEdit(self, operation, location):
        print(operation, location)
        memory.table.item(location, 0).setBackground(
            COLOR_USED_MEMORY if operation == "allocate" else COLOR_MEMORY)

    @QtCore.pyqtSlot("QString")
    def slotChangeRunningLabel(self, process_name):
        if process_name:
            self.NowRunningLabel.setText("Running %s" % process_name)
        else:
            self.NowRunningLabel.setText(" ")


def short_term_scheduling_thread(mode, ready_pl):
    """
    Thread for CPU scheduling

    :param mode: Scheduling mode
    :param ready_pl: ready pool
    """
    while True:
        if ready_pl.num > 0:
            processing_job = ready_pl.get()
            processing_job.status = 'running'
            if mode == 'priority':
                print('Running {0}...'.format(processing_job.name))
                ready_pl.change_priority(processing_job)
                time.sleep(CPU_PROCESS_TIME)  # Sleep just for show
                ready_pl.minus_time(processing_job)

        time.sleep(0.001)


def long_term_scheduling_thread(mode, ready_pl, job_pl):
    """
    # Thread for long term scheduling

    :param mode: mode for scheduling
    :param ready_pl: ready pool object
    :param job_pl: job pool object
    """
    while True:
        if ready_pl.num < ready_pl.count:
            job = job_pl.pop()
            if job:
                mem = memory.allocate(job.required_memory)
                if mem == "Failure":
                    job_pl.add(job)
                else:
                    ready_pl.add(job)
                    job.allocated_memory_start = mem
        time.sleep(0.001)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    UI_main_window = MainWindow()

    JOB_POOL_LOCK = threading.Lock()
    JOB_POOL_TABLE_LOCK = threading.Lock()
    READY_POOL_LOCK = threading.Lock()
    READY_TABLE_LOCK = threading.Lock()
    SUSPEND_POOL_LOCK = threading.Lock()
    SUSPEND_TABLE_LOCK = threading.Lock()
    TERMINATED_POOL_LOCK = threading.Lock()
    TERMINATED_TABLE_LOCK = threading.Lock()

    used_PIDs = set()

    # Create table controller
    job_pool_table_control = JobPoolTableController(table=UI_main_window.JobPoolTable,
                                                    content_each_line=['pid',
                                                                       'name',
                                                                       'status',
                                                                       'priority',
                                                                       'required_time',
                                                                       'required_memory'])
    ready_table_control = ReadyTableController(table=UI_main_window.ReadyTable,
                                               content_each_line=['pid',
                                                                  'name',
                                                                  'status',
                                                                  'priority',
                                                                  'required_time',
                                                                  'address',
                                                                  'required_memory',
                                                                  'allocated_memory_start'])
    suspend_table_control = SuspendTableController(table=UI_main_window.SuspendTable,
                                                   content_each_line=['pid',
                                                                      'name',
                                                                      'status',
                                                                      'priority',
                                                                      'required_time',
                                                                      'address',
                                                                      'required_memory',
                                                                      'allocated_memory_start'])
    terminated_table_control = TerminatedTableController(table=UI_main_window.TerminatedTable,
                                                         content_each_line=['pid', 'name'])

    # Create pool instances and memory
    job_pool = JobPool()
    ready_pool = ReadyPool(scheduling_mode=MODE, max=5)
    terminated_pool = TerminatedPool()
    suspend_pool = SuspendPool()
    memory = Memory(UI_main_window.rightBarWidget)

    # Connect signals
    job_pool.connectSignal()
    ready_pool.connectSignal()
    terminated_pool.connectSignal()
    suspend_pool.connectSignal()

    # Show main window
    UI_main_window.show()
    exit(app.exec_())
