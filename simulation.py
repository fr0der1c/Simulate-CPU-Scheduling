import mainwindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget
from PyQt5 import QtCore, QtGui
import random
import time
import threading
import name_generator
from termcolor import cprint

JOB_POOL_LOCK = threading.Lock()
READY_POOL_LOCK = threading.Lock()

JOB_POOL_TABLE_LOCK = threading.Lock()
READY_TABLE_LOCK = threading.Lock()
SUSPEND_TABLE_LOCK = threading.Lock()
TERMINATED_TABLE_LOCK = threading.Lock()

used_PIDs = set()

MODE = 'priority'  # priority is the only available choice
CPU_PROCESS_TIME = 0.5  # Waiting time for clearer show
AGING_TABLE = [0.1, 0.1, 0.2, 0.4, 0.4, 0.5, 1.0, 1.0, 1.5, 1.5, 2.0, 2.5, 3.0, 3.5, 3.8]
PRIORITY_ADD_EACH_TERN = 0.5  # Add priority each tern
PRIORITY_MAX = 10  # Limit job's max priority to avoid too big priority


class PCB(object):
    def __init__(self, pid, name="process", priority=1, required_time=200):
        self.pid = pid
        if name:
            self.name = name
        else:
            self.name = "process"
        if priority:
            self.priority = priority
        else:
            self.priority = 1
        if required_time:
            self.required_time = required_time
        else:
            self.required_time = 200
        self.status = 'new'
        self.address = hex(id(self))
        self.age = 0

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


class Pool(QtCore.QObject):
    refreshTableSignal = QtCore.pyqtSignal("QString", PCB, "QString")
    editTableSignal = QtCore.pyqtSignal("QString", int, int, "QString")
    running_label_change_signal = QtCore.pyqtSignal("QString")

    def __init__(self):
        super().__init__()
        self._pool = []
        if type(self).__name__ == 'JobPool':
            self.table_controller = "job_pool_table_control"
        elif type(self).__name__ == 'TerminatedPool':
            self.table_controller = "terminated_table_control"
        elif type(self).__name__ == 'ReadyPool':
            self.table_controller = "ready_table_control"
        elif type(self).__name__ == 'SuspendPool':
            self.table_controller = "suspend_table_control"

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

    # Add a job to pool
    def add(self, job):
        if isinstance(job, PCB):
            self._pool.append(job)

            # Change job's status
            if type(self).__name__ == 'TerminatedPool':
                job.status = 'terminated'
            elif type(self).__name__ == 'ReadyPool':
                job.status = 'ready'
            elif type(self).__name__ == 'SuspendPool':
                job.status = 'suspend'

            # Append to table widget
            self.refreshTableSignal.emit(self.table_controller, job, "append")

    # Tell how many items in waiting list
    def num(self):
        return len(self._pool)

    # return a item for specific PID
    def item(self, pid):
        for item in self._pool:
            if item.pid == int(pid):
                return item
        return None

    # Remove a job
    def remove(self, identifier):
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
    # Get the first job and remove it from job pool
    def pop(self):
        if self._pool:
            job = self._pool.pop(0)
            self.refreshTableSignal.emit("job_pool_table_control", job, "remove")
            return job


class TerminatedPool(Pool):
    pass


class SuspendPool(Pool):
    pass


class ReadyPool(Pool):
    def __init__(self, scheduling_mode='priority', max=5):
        super().__init__()
        self.scheduling_mode = scheduling_mode
        self.max = max

    def __repr__(self):
        return self.__str__()

    # Schedule a job for CPU to process
    def get(self):
        if self.scheduling_mode == 'priority':
            # If using priority, sort waiting list using priority of each job
            self._pool = sorted(self._pool, key=lambda item: item.priority)
        return self._pool[0]

    # Minus a job's required_time and sync to table widget
    def minus_time(self, job):
        if job.required_time >= 40:
            job.required_time -= 40
            job.status = 'ready'
        else:
            # Required time of this job is less than quantum time
            job.required_time = 0
            job.status = 'ready'

        # Update table
        self.editTableSignal.emit("ready_table_control", job.pid, 4, str(job.required_time))
        self.editTableSignal.emit("ready_table_control", job.pid, 2, "ready")

        # Need to be terminated
        if job.required_time == 0:
            self.remove(job.pid)  # remove job from waiting list
            cprint('{0} terminated'.format(job.name), color='red')
            terminated_pool.add(job)  # add to terminated pool
            if len(self._pool) == 0:
                self.running_label_change_signal.emit("")

    # Actively adjust job's priority
    def change_priority(self, job):
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


class TableController(object):
    def __init__(self, table, content_each_line):
        self.table = table
        self.content_each_line = content_each_line
        self.table.itemClicked.connect(self.itemClickedSlot)
        if type(self).__name__ == 'JobPoolTableController':
            self.lock = JOB_POOL_TABLE_LOCK
        elif type(self).__name__ == 'ReadyTableController':
            self.lock = READY_TABLE_LOCK
        elif type(self).__name__ == 'SuspendTableController':
            self.lock = SUSPEND_TABLE_LOCK
        elif type(self).__name__ == 'TerminatedTableController':
            self.lock = TERMINATED_TABLE_LOCK

    # Append a row to table widget
    def append(self, process):
        self.lock.acquire()
        self.table.setRowCount(self.table.rowCount() + 1)
        for j in range(0, len(self.content_each_line)):
            if j == 3:
                # Special for priority column
                item = QTableWidgetItem(str("%.2f" % float(eval('process.' + self.content_each_line[j]))))
            else:
                item = QTableWidgetItem(str(eval('process.' + self.content_each_line[j])))
            self.table.setItem(self.table.rowCount() - 1, j, item)  # Add item to table
            self.table.scrollToItem(item)  # Scroll to item
        self.lock.release()

    # Remove a row in table widget
    def remove(self, process):
        self.lock.acquire()
        for i in range(0, self.table.rowCount()):
            if self.table.item(i, 0).text() == str(process.pid):
                # Move rows after me
                if i < self.table.rowCount() - 1:
                    for j in range(i, self.table.rowCount() - 1):
                        for k in range(0, len(self.content_each_line)):
                            self.table.setItem(j, k, QTableWidgetItem(self.table.item(j + 1, k).text()))
                break

        self.table.setRowCount(self.table.rowCount() - 1)  # row count - 1
        self.lock.release()

    # Edit a item and change its background color to yellow
    def edit(self, process_id, column, new_text):
        self.lock.acquire()
        for i in range(0, self.table.rowCount()):
            if self.table.item(i, 0).text() == str(process_id):
                if column == 3:
                    new_text = "%.2f" % float(new_text)
                new_item = QTableWidgetItem(new_text)
                new_item.setBackground(QtGui.QColor(252, 222, 156))
                self.table.setItem(i, column, new_item)
        self.lock.release()

    # Slot for suspending and resuming process
    def itemClickedSlot(self, item):
        if type(self).__name__ == 'ReadyTableController':
            if item.column() == 0 and self.table.item(item.row(), 2).text() == "ready":
                print("Suspend %s" % self.table.item(item.row(), 0).text())
                process = ready_pool.item(self.table.item(item.row(), 0).text())
                print(process)
                ready_pool.remove(process)
                suspend_pool.add(process)
        elif type(self).__name__ == 'SuspendTableController':
            if item.column() == 0:
                print("Resume %s" % self.table.item(item.row(), 0).text())
                process = suspend_pool.item(self.table.item(item.row(), 0).text())
                suspend_pool.remove(process)
                ready_pool.add(process)


class JobPoolTableController(TableController):
    pass


class ReadyTableController(TableController):
    pass


class SuspendTableController(TableController):
    pass


class TerminatedTableController(TableController):
    pass


class MainWindow(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)

        # Set table width
        self.JobPoolTable.setColumnWidth(0, 50)
        self.ReadyTable.setColumnWidth(0, 50)
        self.SuspendTable.setColumnWidth(0, 50)

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
        lt_scheduling = threading.Thread(target=long_term_scheduling_thread,
                                         args=(MODE, ready_pool, job_pool))

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

    @QtCore.pyqtSlot("QString")
    def slotChangeRunningLabel(self, process_name):
        if process_name:
            self.NowRunningLabel.setText("Running %s" % process_name)
        else:
            self.NowRunningLabel.setText(" ")


# CPU scheduling Thread
def short_term_scheduling_thread(mode, waiting_list):
    while True:
        # Get a job from waiting list
        if waiting_list.num() > 0:
            READY_POOL_LOCK.acquire()
            processing_job = waiting_list.get()
            READY_POOL_LOCK.release()
            processing_job.status = 'running'

            if mode == 'priority':
                print('Running {0}...'.format(processing_job.name))
                waiting_list.change_priority(processing_job)
                time.sleep(CPU_PROCESS_TIME)  # Sleep just for show
                waiting_list.minus_time(processing_job)

        time.sleep(0.001)


# Advanced scheduling
def long_term_scheduling_thread(mode, waiting_list, job_pool):
    while True:
        # If waiting list isn't full, transfer job from job poll to waiting list
        if waiting_list.num() < waiting_list.max:
            READY_POOL_LOCK.acquire()
            job = job_pool.pop()
            waiting_list.add(job)
            READY_POOL_LOCK.release()

        time.sleep(0.001)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    UI_main_window = MainWindow()

    # Create table controller
    job_pool_table_control = JobPoolTableController(table=UI_main_window.JobPoolTable,
                                                    content_each_line=['pid',
                                                                       'name',
                                                                       'status',
                                                                       'priority',
                                                                       'required_time'])
    ready_table_control = ReadyTableController(table=UI_main_window.ReadyTable,
                                               content_each_line=['pid',
                                                                  'name',
                                                                  'status',
                                                                  'priority',
                                                                  'required_time',
                                                                  'address'])
    suspend_table_control = SuspendTableController(table=UI_main_window.SuspendTable,
                                                   content_each_line=['pid',
                                                                      'name',
                                                                      'status',
                                                                      'priority',
                                                                      'required_time',
                                                                      'address'])
    terminated_table_control = TerminatedTableController(table=UI_main_window.TerminatedTable,
                                                         content_each_line=['pid', 'name'])

    # Create pool instances
    job_pool = JobPool()
    ready_pool = ReadyPool(scheduling_mode=MODE, max=5)
    terminated_pool = TerminatedPool()
    suspend_pool = SuspendPool()

    # Connect signals
    job_pool.connectSignal()
    ready_pool.connectSignal()
    terminated_pool.connectSignal()
    suspend_pool.connectSignal()

    # Show main window
    UI_main_window.show()
    exit(app.exec_())
