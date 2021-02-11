from requirements import Requirements
from numpy import dot
from numpy.linalg import norm

import math


def getTrace(match_type):

    # Parse high/low CSV file into an 'Requirements' object
    highCsv = Requirements("high")
    lowCsv = Requirements("low")

    masterVocabulary = highCsv.vocabulary + lowCsv.vocabulary

    getVectorRepresentations(
        highCsv.requirements, highCsv.requirements + lowCsv.requirements, masterVocabulary)

    getVectorRepresentations(
        lowCsv.requirements, highCsv.requirements + lowCsv.requirements, masterVocabulary)

    similarityMatrix = getSimilarityMatrix(
        highCsv.requirements, lowCsv.requirements, match_type)

    return similarityMatrix


def getVectorRepresentations(requirements, allRequirements, masterVocabulary):

    print("Getting vector representation...")
    for requirement in requirements:
        vectorRepr = []
        for mv in masterVocabulary:
            result = requirement.text.count(mv)

            if result != 0:
                count = 0

                for allRequirement in allRequirements:
                    containsMv = allRequirement.text.count(mv) > 0
                    if containsMv:
                        count += 1

                idf = math.log(len(allRequirements)/count, 2)
                result = result*idf

            vectorRepr.append(result)
        requirement.vectorRepr = vectorRepr

    return requirements


def getSimilarityMatrix(highRequirements, lowRequirements, match_type):
    fullList = []

    print("Calculating similarity matrix...")
    for i in range(len(highRequirements)):
        yList = []
        highestSimScore = 0.0

        for j in range(len(lowRequirements)):
            angle = angle_between(
                highRequirements[i].vectorRepr, lowRequirements[j].vectorRepr)

            if angle != 0:
                if match_type == 0:
                    yList.append(lowRequirements[j].id)
                elif match_type == 1 and angle > 0.25:
                    yList.append(lowRequirements[j].id)
                elif match_type == 2 and angle >= highestSimScore:
                    highestSimScore = angle

        if match_type == 2:
            for j in range(len(lowRequirements)):
                angle = angle_between(
                    highRequirements[i].vectorRepr, lowRequirements[j].vectorRepr)
                if angle >= (0.67*highestSimScore):
                    yList.append(lowRequirements[j].id)

        fullList.append((highRequirements[i].id, yList))

    return fullList


def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::
    """
    return dot(v1, v2)/(norm(v1)*norm(v2))
