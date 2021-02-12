import csv


def getEvaluation(requirements):
    # Open csv file and loop through rows
    output = "output/links.csv"
    input = "input/links.csv"

    # store all the low-level requirement id's
    lowIds = []
    for lr in requirements.lowRequirements:
        lowIds.append(lr.id)

    tp = tn = fp = fn = 0
    with open(output, "r") as outputfile:
        with open(input, "r") as inputfile:
            csv_dict_reader_output = csv.DictReader(outputfile)
            csv_dict_reader_input = csv.DictReader(inputfile)
            for o, i in zip(csv_dict_reader_output, csv_dict_reader_input):
                toolOut = o['links'].split(",")
                toolIn = i['links'].split(",")

                # confusion matrix
                for id in lowIds:
                    if any(id in s for s in toolOut):
                        if any(id in s for s in toolIn):
                            tp += 1
                        else:
                            fp += 1
                    else:
                        if any(id in s for s in toolIn):
                            fn += 1
                        else:
                            tn += 1

    print('True Positives: ' + str(tp) + ', True Negatives:' + str(tn) +
          ", False Positives: " + str(fp) + ", False Negatives " + str(fn))

    # Recall, Precision and F-measure
    recall = tp / (tp + fn)
    precision = tp / (tp + fp)
    fMeasure = (2 * precision * recall) / (precision + recall)
    print('Recall: ' + str(recall) + ", precision: " +
          str(precision) + ", fMeasure: " + str(fMeasure))
