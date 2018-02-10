import NODE
import MODEL
import math
from random import randint


nodeList = []
distancesMatrix = []
locatedModelList = []


numberOfTurn = 50
sizeOfPopulation = 100
pmedian = 10
numberOfNodes = 76
probabilityOfMutation = 10


# Initial Part Methods
def readTxtFiles():

    #   acording to amountOfNodes paramater readTxtFiles method will run for 76 or 51 Nodes
    Xfile = "x" + str(numberOfNodes) + ".txt"
    Yfile = "y" + str(numberOfNodes) + ".txt"
    DemandFile = "dem" + str(numberOfNodes) + ".txt"
    counter = 0;

    #   Open Xfile and CREATE a Node object as default then get it's X coordinates and indexes from Xfile
    with open(Xfile, 'r') as f:
        for line in f:
            n = NODE.Node()     #   Node is crated here as X, Y, index and demand variables as None
            for i in line.split():
                if counter % 2 is 0:
                    n.index = i     # set index of the current Node
                else:
                    n.x = i     # set X coordinate of the current Node
                counter+=1
            nodeList.append(n)
    f.close()

    #   Open Yfile then get it's Y coordinate from Yfile for already created Nodes in nodeList[]
    k=0
    with open(Yfile, 'r') as f:
        for line in f:
            for i in line.split():
                if counter % 2 is not 0:
                    nodeList[k].y = i       # set Y coordinate of the current Node
                counter+=1
            k+=1
    f.close()

    #   Open demandfile then get it's demand from DemandFile for already created Nodes in nodeList[]
    k = 0
    with open(DemandFile, 'r') as f:
        for line in f:
            for i in line.split():
                if counter % 2 is not 0:
                    nodeList[k].demand = i      # set demand of the current Node
                counter += 1
            k += 1
    f.close()

def distanceMatrix():
    #   for each Node calculate the distance to the other Nodes
    for i in range(len(nodeList)):      #   hold current Node
        tmp = []
        for j in range(len(nodeList)):  #   pass throughout the list and calculate distance to the current Node
            distance = math.sqrt(((int(nodeList[i].x) - int(nodeList[j].x)) ** 2) + ((int(nodeList[i].y) - int(nodeList[j].y)) ** 2))
            tmp.append(format(distance, '.2f'))     # format is used for significant digits like '30.68'
        distancesMatrix.append(tmp)

def firstTrial():
    #   create LocatedModels and add them into populationArray[]
    for i in range(sizeOfPopulation):
        locatedModel = MODEL.LocatedModel(numberOfNodes)      #   create default locatedModel

        #   define 1 chromosomes in DNA of current locatedModel randomly untill ones is equal to the pmedian
        counter = 0
        while counter < pmedian:
            randomIndex = randint(0, len(locatedModel.DNA) - 1)
            if (locatedModel.DNA[randomIndex] is not 1):
                locatedModel.DNA[randomIndex] = 1
                counter += 1

        FitnessLevelFinder(locatedModel)        #   calculate fitness value for the current locatedModel
        locatedModelList.append(locatedModel)     #   after all of properties of the current locatedModel have been defined add into locatedModelList[]

def FitnessLevelFinder(locatedModel):
    sum = 0
    candidates = locatedModel.getOnes()      #   get opened Node indexes which is based on 1 chromosomes in DNA of the locatedModel

    for i in range(len(locatedModel.DNA)):
        if (locatedModel.DNA[i] is 0):
            closestCandidateDistance = getClosestCandidateDistance(i, locatedModel, candidates[0])  #  candidates[0] is used as reference to find closest Candidate Node
            sum = sum + (float(nodeList[i].demand) * float(closestCandidateDistance))

        locatedModel.fitness = format(sum, '.2f')

def getClosestCandidateDistance(demandNodeIndex, locatedModel,referenceCandidate):

    closestDistance = distancesMatrix[demandNodeIndex][referenceCandidate]     # assume referenceCandidate value as closestDistance at the beginning

    #   search whether there is any closer candidate Node to the current demand Node
    for i in locatedModel.getOnes():
        if ((float(distancesMatrix[demandNodeIndex][i]) - float(closestDistance) < 0)):
            closestDistance = distancesMatrix[demandNodeIndex][i]

    return closestDistance


# Iterations Methods
def elimination():

    protectedPercentage = (sizeOfPopulation * 30) / 100         # first 30% of generation will be saved
    startRemovingIndex = sizeOfPopulation - protectedPercentage  # last 30% of generation will be removed


    #   remove last 30% of locatedModelList[]
    for i in range(sizeOfPopulation - 1, (startRemovingIndex - 1), -1):      #   start from LAST index and remove locatedModel backwards (solution of index out of boundry issue)
        locatedModelList.remove(locatedModelList[i])


    populationAfterElection = len(locatedModelList)   # get current population after removing last 30%

    # randomly remove last 40% of elected generation
    for i in range(populationAfterElection - 1, protectedPercentage, -1):
        r = randint(0,1)
        if (r is 0):
            locatedModelList.remove(locatedModelList[i])

    reproduce()   #  reproduce the generation with new baby locatedModels

def reproduce():

    currentPopulation = len(locatedModelList)

    #   start from current population and reproduce baby till current population is equal to the 'population' parameter
    for i in range(currentPopulation, sizeOfPopulation):
        dad = locatedModelList[randint(0, currentPopulation - 1)]       # choose a dad randomly from current population
        mom = locatedModelList[randint(0, currentPopulation - 1)]       # choose a mom randomly from current population
        while dad is mom:
            mom = locatedModelList[randint(0, currentPopulation - 1)]

        locatedModelList.append(newLocatedModel(dad, mom))     # after get the new baby add it into populationArray[]

def newLocatedModel(dad, mom):

    baby = MODEL.LocatedModel(numberOfNodes)      # create a default  baby

    #   UNIFORM CROSSOVER chromosomes are chosen radomly form dad and mom
    for i in range(len(baby.DNA)):
        randomChromosome = randint(0,1)
        if randomChromosome is 0:
            baby.DNA[i] = dad.DNA[i]
        else:
            baby.DNA[i] = mom.DNA[i]


    #   In this part fix amount of ones in DNA if there are more or less than pmedian
    onesIndexes = baby.getOnes()

    difference = pmedian - len(onesIndexes) # difference<0 means number of ones more than pmedian so we need to remove some ones randomly
    if difference < 0:
        for i in range(abs(difference)):
            r = randint(0, len(onesIndexes)-1)
            randomDnaIndex = onesIndexes[r]
            baby.DNA[randomDnaIndex] = 0
            onesIndexes.remove(onesIndexes[r])
    elif difference > 0:
        dnaLength = len(baby.DNA)
        i = 0
        while i is not difference:
            randomDnaIndex = randint(0, dnaLength - 1)
            if (baby.DNA[randomDnaIndex] is 0):
                baby.DNA[randomDnaIndex] = 1
                i += 1
    else:
        pass

    mutation(baby)      #   check mutation factor for baby

    FitnessLevelFinder(baby)    #   get fitness value of baby

    return baby

def  mutation(baby):

    onesIndexes = baby.getOnes()

    mutationFactor = randint(0, 100)    # check mutation 10% probability

    if mutationFactor < probabilityOfMutation:     # if mutationFactor less than 10 then turn one of the 1s into 0 and vice versa
        muttationChromosome = onesIndexes[randint(0,len(onesIndexes)-1)]
        baby.DNA[muttationChromosome] = 0

        randomChromosome = randint(0, len(baby.DNA) - 1)

        # check if random chromosome is 1 then choose another one till chosen chromosome is 0 to turn into 1
        while baby.DNA[randomChromosome] is 1:
            if baby.DNA[randomChromosome] is 0:
                break
            randomChromosome = randint(0, len(baby.DNA) - 1)

        baby.DNA[randomChromosome] = 1


#---------HELPER FUNCTIONS TO SORT GENERATIONS by QuickSort Algorithm-----------
def quickSort(alist):
   quickSortHelper(alist,0,len(alist)-1)

def quickSortHelper(alist,first,last):
   if first<last:

       splitpoint = partition(alist,first,last)

       quickSortHelper(alist,first,splitpoint-1)
       quickSortHelper(alist,splitpoint+1,last)

def partition(alist,first,last):
   pivotvalue = alist[first].fitness

   leftmark = first+1
   rightmark = last

   done = False
   while not done:

       while leftmark <= rightmark and alist[leftmark].fitness <= pivotvalue:
           leftmark = leftmark + 1

       while alist[rightmark].fitness >= pivotvalue and rightmark >= leftmark:
           rightmark = rightmark -1

       if rightmark < leftmark:
           done = True
       else:
           temp = alist[leftmark]
           alist[leftmark] = alist[rightmark]
           alist[rightmark] = temp

   temp = alist[first]
   alist[first] = alist[rightmark]
   alist[rightmark] = temp


   return rightmark



def printFirstTurn():
    print "\n\n_*_  The Best Fitness Value AT THE BEGINNING: " + str(locatedModelList[0].fitness) + "  _*_"
    print "--LocatedModel Info--"
    locatedModelList[0].toString()

def printResults():
    print "\n\n_*_  The Best Fitness Value AT THE END: " + str(locatedModelList[0].fitness) + "  _*_"
    print "--LocatedModel Info--"
    locatedModelList[0].toString()


def main():

    #----Process Preparation----#
    readTxtFiles() #bir node icin x,y demand okur, bu nodeu nodelist'e ekler
    distanceMatrix() #node listteki her bir nodeun diger nodelara olan uzakliklarini tutar
    firstTrial() #populasyon kadar locatedmodel yaratilir(DNAsi hazirlanir ve fitness hesaplanir), locatedmodellist'e eklenir

    quickSort(locatedModelList) #ilk neslin en iyi fitness degerli locatedmodelini ekrana basmak icin sort ettik
    printFirstTurn()

    # ----Process----#
    for i in range(numberOfTurn): #sort, remove, reproduce
        quickSort(locatedModelList)   # sort locatedModels by their fitness values in locatedModelList[]
        elimination()
        #print  "Generation: " + str(i+1) + " \tbest fitness: " + str(locatedModelList[0].fitness)


    printResults()


if __name__ == '__main__':
    main()