
class LocatedModel():
    def __init__(self,rng):
        self.fitness = 0.0
        self.DNA = [0 for i in range(rng)]

    def toString(self):
        ones = self.getOnes()
        print "Fitness: " + str(self.fitness)
        print "Candidates = {",
        for i in ones:
            print i + 1,
        print "}",
        print "\tpmedian: " + str(len(self.getOnes()))
        print self.DNA

    def getOnes(self):
        onesIndexes = []
        for i in range(len(self.DNA)):
            if self.DNA[i] is 1:
                onesIndexes.append(i)
        return onesIndexes

