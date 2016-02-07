# Adri, Anne, Maj
# visualization.py


def fillDict():
    count = 1
    twentyFour = {}
    while count <= 24:
        twentyFour[count] = 0
        count += 1
    return twentyFour
    
dayDict = fillDict()

def mostCommonTimes(email,filename):
    for entry in fromTextToPickle(email,filename)['last_visit_time']:
        for key in dayDict:
            if key == int(entry.split('T')[1].split('.')[0].split(':')[0]):
                dayDict[key] += 1
    return dayDict
