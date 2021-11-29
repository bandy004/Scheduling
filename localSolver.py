import random
import datetime as dt
from utils import hours


class LocalSolver:
    def __init__(self, scheduler, repeat) -> None:
        self.original = scheduler
        self.scheduler = None
        self.bestSch = {}
        self.result = []
        self.best = dt.timedelta(hours=100000)
        self.repeat = repeat

    def solve(self):
        initialSolution = self.original
        for i in range(self.repeat):
            # copy.deepcopy(self.original)
            pairToSwap = self.getSwap()
            # task unplan from resource
            # for each resource remember the position
            # plan to the task to resources

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

    def selectSwap(self):
        taskList = [t for t in self.scheduler.tasks.values()
                    if t.resource != None]
        if(len(taskList) > 0):
            return taskList[random.randint(0, len(taskList)-1)]
        else:
            return False

    def unplan(self, task):
        return None

    def plan(self, task, resource, beforeTask):
        return None
