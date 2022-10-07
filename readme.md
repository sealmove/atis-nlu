# Introduction
This project uses ATIS, a well-known airplane ticket reservation system dataset. The goal is to extract information from human messages, represent it in a machine-readable format, and then build a system that uses this information.

# Outline
The project includes the following:
- An end-to-end NLU system to demonstrate a practical end result
- A collection of jupyter notebooks to demonstrate the techniques used for building the NLP pipelines

The notebooks are split into the following 4 chapters:

1. Extract the named entities with two different methods:
    - with spaCy Matcher
    - by walking on the dependency tree

2. Determine the intent of the user utterance with three different methods:
    - by extracting the verbs and their direct objects
    - by using wordlists
    - by walking on the dependency tree

3. Match keywords:
    - to synonyms from a synonyms list to detect semantic similarity
    - with word vector-based semantic similarity methods

4. Generate a semantic representation