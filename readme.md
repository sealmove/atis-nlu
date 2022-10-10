# Introduction
This project uses ATIS, a well-known airplane ticket reservation system dataset. The goal is to extract information from human messages, represent it in a machine-readable format, and then build a system that uses this information.

# Outline
The project includes the following:
- A collection of jupyter notebooks to demonstrate the techniques used for building the NLP pipelines
- A jupyter notebooks which showcases how to cleanse data to adjust it to the application's needs
- An end-to-end NLU system to demonstrate a practical end result

## NLP Techniques
The notebooks are split into the following 5 chapters:

0. Introduce and explore ATIS dataset

1. Extract the named entities with two different methods:
    - with spaCy Matcher
    - by walking on the dependency tree

2. Determine the intent of the user utterance using various techniques:
    - by extracting the verbs and their direct objects
    - by using wordlists
    - by walking on the dependency tree

3. Match keywords to synonyms:
    - from a synonyms list to detect semantic similarity
    - with word vector-based semantic similarity methods

4. Generate a semantic representation

## Data Engineering
The following datasets are used to compile a sqlite database:
- [Kaggle: flight data.csv](https://www.kaggle.com/datasets/polartech/flight-data-with-1-million-or-more-records)
- [OpenFlights: airports-extended.dat](https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports-extended.dat)

## End-to-end System
An airlines information application which searches a database with queries written in plain english.
