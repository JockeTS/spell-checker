# Spell Checker

## Description
A spell checking website built with **Flask**. It uses a **Trie** data structure consisting of nodes to store a dictionary of English words. Each node represents a letter and recursion is used to traverse them.

The Trie object is created from a text file whenever the user navigates to one of the main routes. 
It includes several methods:

* Checking if it contains a specific word
* Listing all its words alphabetically
* Removing a specific word
* Searching words with a certain prefix or suffix
* Giving spelling suggestions based on input

## Quick Start
* git clone https://github.com/JockeTS/spell-checker.git
* cd spell-checker/
* python3 app.py
* navigate to: http://127.0.0.1:5000