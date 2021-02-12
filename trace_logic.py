from requirements import Requirements
from numpy import dot
from numpy.linalg import norm

import math


def getTrace(match_type):

    # Parse high/low CSV file into an 'Requirements' object
    requirements = Requirements()

    # Enrich highCsv and lowCsv requirements with its vector representation
    getVectorRepresentation(requirements)

    # Create similarity matrix with highCsv and lowCsv vector representations
    getSimilarityMatrix(requirements, match_type)

    return requirements


def getVectorRepresentation(csv):
    '''
    For each requirement, enrich the object with its vector representation
        For each word in the master vocabulary, count the frequency with respect to the tokens
            if frequency != 0, construct tf * idf
    '''
    requirements = csv.highRequirements + csv.lowRequirements

    print("Getting vector representation...")
    for requirement in requirements:
        for word in csv.masterVocabulary:
            result = requirement.tokens.count(word)

            # If word does appear in requirement tokens
            if result != 0:
                count = 0

                # Construct tf * idf
                for requirement2 in requirements:
                    containsMv = requirement2.tokens.count(word) > 0
                    if containsMv:
                        count += 1

                idf = math.log(len(requirements)/count, 2)
                result = result*idf

             # Save vector representation in 'requirement' object
            requirement.vectorRepr.append(result)


def getSimilarityMatrix(csv, match_type):
    '''
    Create two-dimensional array and compute the angle between 'H' high-level (row) and 'L' low-level (column) vector representations
    '''
    print("Calculating similarity matrix...")
    for i in range(len(csv.highRequirements)):
        yList = []
        highestSimScore = 0.0

        for j in range(len(csv.lowRequirements)):
            angle = angle_between(
                csv.highRequirements[i].vectorRepr, csv.lowRequirements[j].vectorRepr)

            if angle != 0:
                if match_type == 0:
                    yList.append(csv.lowRequirements[j].id)
                elif match_type == 1 and angle > 0.25:
                    yList.append(csv.lowRequirements[j].id)
                elif match_type == 2 and angle >= highestSimScore:
                    highestSimScore = angle

        if match_type == 2:
            for j in range(len(csv.lowRequirements)):
                angle = angle_between(
                    csv.highRequirements[i].vectorRepr, csv.lowRequirements[j].vectorRepr)
                if angle >= (0.67*highestSimScore):
                    yList.append(csv.lowRequirements[j].id)

        csv.similarityMatrix.append((csv.highRequirements[i].id, yList))


def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2':: """
    return dot(v1, v2)/(norm(v1)*norm(v2))
