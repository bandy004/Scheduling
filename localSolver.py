from math import floor
from os import read
import random
import datetime as dt
from utils import hours


class LocalSolver:
    def __init__(self, scheduler, repeat, n_swaps) -> None:
        self.original = scheduler
        self.scheduler = None
        self.bestSch = {}
        self.result = []
        self.best = dt.timedelta(hours=100000)
        self.repeat = repeat
        self.nswaps = n_swaps

    def solve(self):
        self.scheduler = self.original.clone(self.original)
        self.scheduler.createRandomSolution()
        for i in range(self.repeat):
            # copy.deepcopy(self.original)
            fromRes = self.getFromResource()
            fromPos = self.getFromPosition(fromRes)
            toRes = self.getToResource()
            toPos = self.getToPosition(toRes, fromRes.tasks[fromPos])

            self.relocate(fromRes,
                          fromPos,
                          toRes,
                          toPos)

            self.scheduler.updateKPIs()

            if(self.best > self.scheduler.makespan):
                self.bestSch = {
                    'makespan': self.scheduler.makespan,
                    'Tasks': [task.serialize() for task in self.scheduler.tasks.values()],
                    'Resources': [res.serialize() for res in self.scheduler.resources.values()]}
                self.best = self.scheduler.makespan
                # self.result.append({'id': i, 'makespan': hours(
                #     self.scheduler.makespan)})

            self.result.append({'id': i, 'makespan': hours(
                self.scheduler.makespan)})

        return self.bestSch, self.result

    def getFromResource(self):
        # fromResSet = [
        #     res for res in self.scheduler.resources.values() if len(res.tasks) > 0]
        # fromRes = fromResSet[random.randint(0, len(fromResSet)-1)]
        # fromRes = max(
        #     [res.utilization for res in self.scheduler.resources.values()])
        sortedResource = sorted(
            self.scheduler.resources.items(), key=lambda x: x[1].utilization)
        fromRes = sortedResource[len(sortedResource)-1]
        return fromRes[1]

    def getToResource(self):
        # toRes = random.randint(1, len(self.scheduler.resources))
        sortedResource = sorted(
            self.scheduler.resources.items(), key=lambda x: x[1].utilization)
        toRes = sortedResource[0]
        return toRes[1]

    def getFromPosition(self, res):
        res.tasks.sort(key=lambda t: t.offset)
        maxIndex = len(res.tasks)-1
        minIndex = maxIndex - floor(maxIndex/2)
        fromPosIndex = random.randint(minIndex, maxIndex)

        return fromPosIndex

    def getToPosition(self, res, task):
        toSet = [
            target for target in res.tasks if target.color == task.color]
        toPos = 0
        if(len(toSet) > 0):
            toPosIndex = random.randint(0, len(toSet)-1)
            toPos = res.tasks.index(toSet[toPosIndex])

        #     if (len(self.scheduler.resources[toRes].tasks) > 0):
        #         toPos = random.randint(
        #             0, len(self.scheduler.resources[toRes].tasks)-1)

        return toPos

    def relocate(self, fromRes, fromPos, toRes, toPos):
        task = fromRes.tasks.pop(fromPos)
        toRes.tasks.insert(toPos, task)
        task.resource = toRes
        fromRes.propagateFrom(0)
        toRes.propagateFrom(0)
        # print("Move", task.name, "from ", fromRes.name, "pos",
        #       fromPos, "to ", toRes.name, " pos", toPos)

    def unplan(self, task):
        return None

    def plan(self, task, resource, beforeTask):
        return None
