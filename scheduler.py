import datetime as dt
import random
from localSolver import LocalSolver
from randomSolver import RandomSolver
import copy
from utils import hours


class Task:
    def __init__(self, schedule, id, duration, color) -> None:
        self.id = id
        self.name = 'Task-'+str(id)
        self.duration = dt.timedelta(hours=duration)
        self.color = color
        self.start = schedule.start
        self.end = self.start + self.duration
        self.resource = None
        self.offset = 0

    def serialize(self):
        obj = {}
        res_name = "N/A"
        if(self.resource):
            res_name = self.resource.name
        obj['Task'] = self.name
        obj['Start'] = self.start  # .strftime("%Y-%m-%d %H")
        obj['Finish'] = self.end  # .strftime("%Y-%m-%d %H")
        obj['Resource'] = res_name
        obj['Duration'] = str(self.duration)
        obj['Color'] = self.color
        return obj

    def updateStart(self, prevEnd, offset):
        self.start = prevEnd + dt.timedelta(hours=offset)
        self.offset = offset
        self.end = self.start + self.duration


class Resource:
    def __init__(self, scheduler, id, color) -> None:
        self.id = id
        self.name = 'Machine-'+str(id)
        self.tasks = []
        self.scheduler = scheduler
        self.utilization = 0.0
        self.color = color

    def addTaskToEnd(self, task):
        task.resource = self
        self.tasks.append(task)
        self.propagateFrom(len(self.tasks)-1)
        # if(len(self.tasks) > 0):
        #     lastTask = self.tasks[len(self.tasks)-1]
        #     offset = self.scheduler.color_setup_matrix[lastTask.color][task.color]
        #     task.updateStart(lastTask.end + dt.timedelta(hours=offset))
        # self.tasks.append(task)

    def getLength(self):
        if(len(self.tasks) == 0):
            return self.scheduler.start
        else:
            return self.tasks[len(self.tasks)-1].end

    def propagateFrom(self, pos):
        for i in range(pos, len(self.tasks)):
            task = self.tasks[i]
            end = self.scheduler.start
            offset = 0
            if(i > 0):
                lastTask = self.tasks[i-1]
                offset = self.scheduler.color_setup_matrix[lastTask.color][task.color]
                end = lastTask.end
            task.updateStart(end, offset)

    def calcUtilization(self):
        self.utilization = sum(
            [hours(x.duration) for x in self.tasks])/hours(self.scheduler.makespan)*100
        makespan = self.getLength() - self.scheduler.start
        self.utilization = 0
        if(hours(makespan) > 0):
            self.utilization = hours(
                makespan)/hours(self.scheduler.makespan)*100

    def serialize(self):
        # self.calcUtilization()
        obj = {}
        obj['Resource'] = self.name
        obj['ID'] = self.id
        obj['Utilization'] = self.utilization
        obj['Allocation'] = len(self.tasks)
        obj['Color'] = self.color
        return obj


class Scheduler:
    ''' Scheduler presents a scheduling problem with tasks, resources, setup constraint.'''

    def __init__(self, n_tasks, n_res, colors, color_setup, depndency_density, task_duration_range) -> None:
        self.n_tasks = n_tasks
        self.n_res = n_res
        self.colors = colors
        self.task_duration_range = task_duration_range
        self.durationList = []
        for i in range(self.task_duration_range[0], self.task_duration_range[1]):
            self.durationList.append(i)
        self.dep_density = depndency_density
        self.color_setup_matrix = color_setup
        self.start = dt.datetime.today().replace(hour=0, minute=0, second=0)

        self.tasks = {}
        self.resources = {}
        self.taskDependencies = {}

        self.makespan = 0

    @classmethod
    def clone(cls, other_schedule) -> None:
        ins = cls(other_schedule.n_tasks, other_schedule.n_res, other_schedule.colors,
                  other_schedule.color_setup_matrix, other_schedule.dep_density,  other_schedule.task_duration_range)

        ins.tasks = {}
        for t in other_schedule.tasks:
            task = other_schedule.tasks[t]
            ins.tasks[task.id] = Task(
                ins, task.id, hours(task.duration), task.color)

        ins.resources = {}
        for r in other_schedule.resources:
            res = other_schedule.resources[r]
            ins.resources[res.id] = Resource(ins, res.id, res.color)

        return ins

    def createProblem(self):
        self.createTasks()
        self.createResources()
        self.createDependencies()

    def solveProblem(self, strategy, repeat):
        solver = RandomSolver(self, repeat)
        if(strategy == 'Local'):
            solver = LocalSolver(self, repeat, 2)
        return solver.solve()

    def createRandomSolution(self):
        solver = RandomSolver(self, 0)
        solver.createRandomSolution()

    def createTasks(self):
        for i in range(0, self.n_tasks):
            colorIndex = i % len(self.colors)
            durationIndex = i % len(self.durationList)
            # task = Task(self, i+1, random.randint(self.task_duration_range[0], self.task_duration_range[1]),
            #             self.colors[random.randint(0, len(self.colors)-1)])
            task = Task(
                self, i+1, self.durationList[durationIndex], self.colors[colorIndex])
            self.tasks[task.id] = task

    def createResources(self):
        for i in range(0, self.n_res):
            res = Resource(
                self, i+1, self.colors[i])
            self.resources[res.id] = res

    def createDependencies(self):
        pass

    def updateKPIs(self):
        self.makespan = max(
            [res.getLength() for res in self.resources.values()]) - self.start

        self.updateResourceUtilization()

    def updateResourceUtilization(self):
        for r in self.resources:
            self.resources[r].calcUtilization()
