# -----------------------------------------------------------------------------
# Organization - Universidad de La Laguna
# Author - Hugo Fernández Solís
# Date - 16/12/2021
#
# File - evaluator.py
# Brief - Contains the functions to evaluate files.
# -----------------------------------------------------------------------------

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from math import log


# Calculates the inverse document frequency of all the words in the past document.
def inverse_document_frequency(document: list[str], matrix: list[list[str]]) -> dict[str]:
    idf: dict[str] = dict[str]()
    for term in document:
        if term not in idf:
            idf[term] = log(len(matrix) / document_frequency(term, matrix))
    return idf


# Calculates the term frequency of all the words in the past document.
def term_frequency(document: list[str]) -> dict[str]:
    tf: dict[str] = dict[str]()
    for term in document:
        if term in tf:
            tf[term] += 1
        else:
            tf[term] = 1
    for term in document:
        tf[term] /= len(document)

    return tf


# Calculates the document frequency of the passed term in the matrix of documents.
def document_frequency(term: str, matrix: list[list[str]]) -> int:
    count: int = 0
    for document in matrix:
        for word in document:
            if word == term:
                count += 1
    return count


# Calculates the tf-idf of the passed term in the matrix of documents.
def tf_idf(document: list[str], tf: dict[str], idf: dict[str]) -> dict[str]:
    w: dict[str] = dict[str]()
    for term in document:
        if term not in w:
            w[term] = tf[term] * idf[term]
    return w


# Removes all the stopwords of the english alfabet from the text.
def remove_stopwords(line: str) -> list[str]:
    filtered_sentence: list[str] = list[str]()
    for term in word_tokenize(line):
        if term not in set(stopwords.words('english')):
            filtered_sentence.append(term)
    return filtered_sentence



def calculate_similarity(w: list[dict[str]]) -> list[list[int]]:
    result: list[list[int]] = list[list[int]]()
    for original_document in w:
        original: list[int] = list(original_document.values())
        values: list[int]() = list[int]()
        for compared_document in w:
            sim: int = 0
            compared: list[int] = list(compared_document.values())
            if len(original) > len(compared):
                for i in range(len(compared)):
                    sim += compared[i] * original[i]
            else:
                for i in range(len(original)):
                    sim += compared[i] * original[i]
            values.append(sim)
        result.append(values)
    return result