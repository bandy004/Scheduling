import random
import copy
import datetime as dt
from utils import hours


class RandomSolver:
    def __init__(self, scheduler, repeat) -> None:
        self.original = scheduler
        self.scheduler = None
        self.bestSch = {}
        self.result = []
        self.best = dt.timedelta(hours=100000)
        self.repeat = repeat

    def solve(self):
        for i in range(self.repeat):
            # copy.deepcopy(self.original)
            self.scheduler = self.original.clone(self.original)
            task = self.selectTask()
            while(task):
                res_position = self.selectResource(task)
                self.plan(task, res_position)
                task = self.selectTask()

            def getEnd(res):
                if(len(res.tasks) == 0):
                    return self.scheduler.start
                else:
                    return res.tasks[len(res.tasks)-1].end

            self.scheduler.makespan = max(
                [getEnd(res) for res in self.scheduler.resources.values()]) - self.scheduler.start

            if(self.best > self.scheduler.makespan):
                self.bestSch = {
                    'makespan': self.scheduler.makespan,
                    'Tasks': [task.serialize() for task in self.scheduler.tasks.values()],
                    'Resources': [res.serialize() for res in self.scheduler.resources.values()]}
                self.best = self.scheduler.makespan

            self.result.append({'id': i, 'makespan': hours(
                self.scheduler.makespan)})

        return self.bestSch, self.result

    def selectTask(self):
        taskList = [t for t in self.scheduler.tasks.values()
                    if t.resource == None]
        if(len(taskList) > 0):
            return taskList[random.randint(0, len(taskList)-1)]
        else:
            return False

    def selectResource(self, task):
        return self.scheduler.resources[random.randint(1, len(self.scheduler.resources))]

    def plan(self, task, resource_position):
        resource_position.addTaskToEnd(task)
