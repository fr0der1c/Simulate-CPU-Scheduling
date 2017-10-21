import sys
import threading
import time
from PyQt5.QtWidgets import QApplication, QMainWindow
import mainwindow
from PCB import PCB
from pool import JobPool, TerminatedPool, WaitingList
from table_control import TableControl

JOB_POOL_LOCK = threading.Lock()
WAITING_LIST_LOCK = threading.Lock()
used_PIDs = set()

# Demo Parameter
num_waiting_max = 3
mode = 'priority'

# Waiting time for clearer show
CPU_PROCESS_TIME = 0.1

# Add priority each tern
PRIORITY_ADD_EACH_TERN = 0.5

job_pool = JobPool()

waiting_list = WaitingList(scheduling_mode='priority', max=num_waiting_max)

terminated_pool = TerminatedPool()

app = QApplication(sys.argv)
UI_main_window = mainwindow.Ui_MainWindow()
window = QMainWindow()
UI_main_window.setupUi(window)

job_pool_table_control = TableControl(table=UI_main_window.JobPoolTable,
                                      content_each_line=['pid',
                                                         'name',
                                                         'status',
                                                         'priority',
                                                         'required_time'])

running_table_control = TableControl(table=UI_main_window.RunningTable,
                                     content_each_line=['pid',
                                                        'name',
                                                        'status',
                                                        'priority',
                                                        'required_time',
                                                        'address'])

terminated_table_control = TableControl(table=UI_main_window.TerminatedTable,
                                        content_each_line=['pid', 'name'])


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


def slotStartButton():
    global num_waiting_max
    num_waiting_max = UI_main_window.DaoshuBox.value()
    waiting_list.max = UI_main_window.DaoshuBox.value()

    # Create CPU thread
    st_scheduling_thread = threading.Thread(target=short_term_scheduling_thread,
                                            args=(mode, waiting_list))
    lt_scheduling = threading.Thread(target=long_term_scheduling_thread,
                                     args=(mode, waiting_list, job_pool))
    st_scheduling_thread.start()
    lt_scheduling.start()


def slotGenerateJobButton():
    for i in range(UI_main_window.RandomCountBox.value()):
        random_process = PCB.random()
        job_pool.add(random_process)


def slotAddJobButton():
    job_pool.add(PCB(PCB.generate_pid(),
                     UI_main_window.AddJobNameEdit.text(),
                     UI_main_window.AddJobPriorityEdit.text(),
                     UI_main_window.AddJobTimeEdit.text()))


def slotMaxWaitingChanged():
    waiting_list.max = UI_main_window.DaoshuBox.value()


# Set table width
UI_main_window.JobPoolTable.setColumnWidth(0, 50)
UI_main_window.RunningTable.setColumnWidth(0, 50)
UI_main_window.SuspendTable.setColumnWidth(0, 50)

# Stretch last column of the table
# UI_main_window.JobPoolTable.horizontalHeader().setStretchLastSection(True)
# UI_main_window.JobPoolTable.horizontalHeader().setStretchLastSection(True)
# UI_main_window.TerminatedTable.horizontalHeader().setStretchLastSection(True)
# UI_main_window.RunningTable.horizontalHeader().setStretchLastSection(True)
# UI_main_window.SuspendTable.horizontalHeader().setStretchLastSection(True)

# Connect slots
UI_main_window.StartButton.clicked.connect(slotStartButton)
UI_main_window.GenerateJobButton.clicked.connect(slotGenerateJobButton)
UI_main_window.AddJobButton.clicked.connect(slotAddJobButton)
UI_main_window.DaoshuBox.valueChanged.connect(slotMaxWaitingChanged)
# UI_main_window.JobPoolTable.currentCellChanged(0,0).connect(JobPoolTableControl.checkbox_changed)

if __name__ == '__main__':
    window.show()
    exit(app.exec_())
