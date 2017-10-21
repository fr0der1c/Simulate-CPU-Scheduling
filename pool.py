from termcolor import cprint

from diaodu import job_pool_table_control, terminated_table_control, running_table_control, terminated_pool
from PCB import PCB


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
            job_pool_table_control.append(job)
        elif type(self).__name__ == 'TerminatedPool':
            terminated_table_control.append(job)


class JobPool(Pool):
    def __init__(self):
        super().__init__()

    # Get the first job and remove it from job pool
    def get(self):
        if self._pool:
            job = self._pool.pop(0)
            job.status = "ready"
            running_table_control.append(job)
            job_pool_table_control.pop(job)
            return job
        else:
            return


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
                cprint('{0} terminated'.format(each.name), color='red')
                terminated_pool.add(each)

    # Tell how many items in waiting list
    def num(self):
        return len(self._pool)