
class ConstraintSolver:
    pass

    def createVariables(self):
        # for each task : start, end
        # for each task-res: presense@res, start@res, end@res, interval(optional)
        # makespan
        pass

    def postConstraints(self):
        # for each task: start = one of the start@res, end = one of the end@res
        # for each task: only one resource is used => sum(presense@res) = 1
        # for each res: nooverlap all intervals
        # for each res: t1->t2 on res : t2.start >= t1.end + offset(t1, t2) : provided both t1 and t2 are present
        # for each res: either t1->t2 holds or t2->t1 holds

        pass

    def addObjective(self):
        # minimize makespan
        pass

    def solve(self):
        # create variables
        # create constraints
        # create objective
        # solve
        # post process
        pass

    def processSolution(self):
        #create task json
        pass
