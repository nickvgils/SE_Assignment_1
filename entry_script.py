import csv
import sys
import trace_logic

import os


def write_output_file(trace):
    '''
    Writes a dummy output file using the python csv writer, update this 
    to accept as parameter the found trace links. 
    '''
    # ADD \ up-front
    with open('output/links.csv', 'w') as csvfile:

        writer = csv.writer(csvfile, delimiter=",",
                            quotechar="\"", quoting=csv.QUOTE_MINIMAL)

        fieldnames = ["id", "links"]

        writer.writerow(fieldnames)

        for highReq in trace:
            lowReq = ','.join(highReq[1])
            writer.writerow([highReq[0], lowReq])

            #writer.writerow(["UC1", "L1, L34, L5"])
            #riter.writerow(["UC2", "L5, L4"])


if __name__ == "__main__":
    '''
    Entry point for the script
    '''
    if len(sys.argv) < 2:
        print("Please provide an argument to indicate which matcher should be used")
        exit(1)

    match_type = 0

    try:
        match_type = int(sys.argv[1])
    except ValueError as e:
        print("Match type provided is not a valid number")
        exit(1)

    print(f"Hello world, running with matchtype {match_type}!")

    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

    # Read input low-level requirements and count them (ignore header line).
    # ADD \ up-front
    with open("input/low.csv", "r") as inputfile:
        print(
            f"There are {len(inputfile.readlines()) - 1} low-level requirements")

    '''
    This is where you should implement the trace level logic as discussed in the 
    assignment on Canvas. Please ensure that you take care to deliver clean,
    modular, and well-commented code.
    '''
    trace = trace_logic.getTrace(match_type)

    write_output_file(trace)

    print("Output written")
