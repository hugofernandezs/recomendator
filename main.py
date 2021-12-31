# -----------------------------------------------------------------------------
# Organization - Universidad de La Laguna
# Author - Hugo Fernández Solís
# Date - 16/12/2021
#
# File - main.py
# Brief - Initializes the recommendation system.
# -----------------------------------------------------------------------------

import argparse
import re

import evaluator as ev


# Evaluates the arguments and starts the execution.
def main():
    # Parses the arguments
    ps: argparse.ArgumentParser = argparse.ArgumentParser()
    ps.add_argument("-f", "--file", required=True)

    # Preprocesses the text.
    filename = ps.parse_args().file
    file = open(filename, "r")
    matrix: list[list[str]] = list[list[str]]()
    line: str = file.readline()
    while len(line) > 0:
        matrix.append(ev.remove_stopwords(re.sub(r'[^\w]', ' ', line).lower()))
        line = file.readline()

    # Evaluates the documents.
    tf: list[dict[str]] = list[dict[str]]()
    idf: list[dict[str]] = list[dict[str]]()
    w: list[dict[str]] = list[dict[str]]()
    for document in matrix:
        document_tf: dict[str] = ev.term_frequency(document)
        document_idf: dict[str] = ev.inverse_document_frequency(document, matrix)
        document_w: dict[str] = ev.tf_idf(document, document_tf, document_idf)
        tf.append(document_tf)
        idf.append(document_idf)
        w.append(document_w)

    # Prints the results.
    filename = filename.split('\\')[-1]
    print("\n")
    print(f"    Content Based Recommendation - {filename}      ".center(120, "#"))
    print("")
    trm = "Term_freq"
    doc = "Doc_freq"
    res = "tf + idf"
    for i in range(len(matrix)):
        print(f"    Article {i+1}    ".center(40, "-"))
        print("")
        print("{:>20}{:>10}{:>10}".format(trm, doc, res))
        for key, value in tf[i].items():
            print("{:<14}{}{:>10}{:>10}".format(key, "{:.2f}".format(value),
                                                "{:.2f}".format(idf[i][key]),
                                                "{:.2f}".format(w[i][key])))
        print("\n")

    cosine: list[list[int]] = ev.calculate_similarity(w)
    print("")
    print(f"    Cosine relation    ".center(40, "-"))
    print("")
    for i in range(len(cosine)):
        for j in range(len(cosine[i])):
            if j != i:
                print(f"cos(A{i+1}, A{j+1}) = {cosine[i][j]}")
    print("")


# Starts the program.
main()
