#!/usr/bin/env python3
""" Main module """

import traceback
import os
import re
from flask import Flask, render_template, request, redirect, url_for, session
from src.trie import Trie
from src.errors import SearchMiss

app = Flask(__name__)
app.secret_key = re.sub(r"[^a-z\d]", "", os.path.realpath(__file__))

@app.route("/")
def main():
    """ Main route. """

    return redirect(url_for('index'))

def init():
    """ Init stuff. """

    if session.get("helper") is None:
        session["helper"] = "init"

    if session.get("curr_dict") is None:
        session["curr_dict"] = app.static_folder + "/dictionary.txt"

    Trie.default_dict = session["curr_dict"]

    if session.get("message") is None:
        session["message"] = ""

    if session.get("removed_words") is None:
        session["removed_words"] = []

    if session.get("prefix_results") is None:
        session["prefix_results"] = []

    if session.get("cs_results") is None:
        session["cs_results"] = []

    if session.get("suffix_results") is None:
        session["suffix_results"] = []

@app.route("/index")
def index():
    """ Starting place. """
    init()

    return render_template("index.html")

# Check Word
@app.route("/check-word")
def check_word():
    """ Check if current dictionary has a specific word (form). """
    init()

    message = session["message"]
    session["message"] = ""

    return render_template("check-word.html", message=message)

@app.route("/check-word-post", methods=["POST"])
def check_word_post():
    """ Check if current dictionary has a specific word (post). """

    word = request.form.get("fword").lower()

    if word:
        trie = Trie.create_from_file()
        remove_words(trie)

        try:
            trie.has_word(word)
            session["message"] = f"'{word}' is in dictionary."
        except SearchMiss:
            session["message"] = f"'{word}' is not in dictionary."

    return redirect(url_for('check_word'))

# List Words
@app.route("/list-words")
def list_words():
    """ List all words in current dictionary. """
    init()

    trie = Trie.create_from_file()
    remove_words(trie)

    word_list = trie.get_all_words()
    word_list.sort()

    return render_template("list-words.html", word_list=word_list)

# Remove Word
@app.route("/remove-word")
def remove_word():
    """ Add a word to list of removed words (form). """
    init()

    message = session["message"]
    session["message"] = ""

    return render_template("remove-word.html", message=message)

@app.route("/remove-word-post", methods=["POST"])
def remove_word_post():
    """ Add a word to list of removed words (post). """

    word = request.form.get("fword").lower()

    if word:
        # Add word to list if removed words if not already in list
        if word not in session["removed_words"]:

            # Check that the dictionary has the word
            trie = Trie.create_from_file()

            try:
                trie.has_word(word)
                session["removed_words"].append(word)
                session["message"] = f"'{word}' was removed from dictionary."
            except SearchMiss:
                session["message"] = f"'{word}' is not in dictionary."
        else:
            session["message"] = f"'{word}' has already been removed."

    return redirect(url_for('remove_word'))

# Prefix Search
@app.route("/prefix-search")
def prefix_search():
    """ Find all words matching prefix (form). """
    init()

    if session["prefix_results"]:
        prefix = session["prefix_results"][0]
        matches = session["prefix_results"][1:]
        #matches.sort()

        session["prefix_results"] = []

        return render_template("prefix-search.html", prefix=prefix, matches=matches)

    message = session["message"]
    session["message"] = ""

    return render_template("prefix-search.html", message=message)

@app.route("/prefix-search-post", methods=["POST"])
def prefix_search_post():
    """ Find all words matching prefix (post). """

    session["helper"] = "psp"

    prefix = request.form.get("fpre").lower()

    if prefix:
        trie = Trie.create_from_file()
        remove_words(trie)

        for word in trie.prefix_search(prefix):
            session["prefix_results"].append(word)

        if len(session["prefix_results"]) > 0:
            session["prefix_results"].insert(0, prefix)
        else:
            session["message"] = f"No results for '{prefix}'."

    return redirect(url_for('prefix_search'))

# Correct Spelling
@app.route("/correct-spelling")
def correct_spelling():
    """ Get suggestions for wrongly spelled words (form). """
    init()

    if session["cs_results"]:
        fword = session["cs_results"][0]
        suggs = session["cs_results"][1:]

        session["cs_results"] = []

        return render_template("correct-spelling.html", fword=fword, suggs=suggs)

    message = session["message"]
    session["message"] = ""

    return render_template("correct-spelling.html", message=message)

@app.route("/correct-spelling-post", methods=["POST"])
def correct_spelling_post():
    """ Get suggestions for wrongly spelled words (post). """

    session["helper"] = "cs"

    fword = request.form.get("fword").lower()

    if fword:
        trie = Trie.create_from_file()
        remove_words(trie)

        for word in trie.correct_spelling(fword):
            session["cs_results"].append(word)

        if len(session["cs_results"]) > 0:
            session["cs_results"].insert(0, fword)
        else:
            session["message"] = f"No suggestions available for '{fword}'."

    return redirect(url_for('correct_spelling'))

# Suffix Search
@app.route("/suffix-search")
def suffix_search():
    """ Find all words matching suffix (form). """
    init()

    if session["suffix_results"]:
        suffix = session["suffix_results"][0]
        matches = session["suffix_results"][1:]

        session["suffix_results"] = []

        return render_template("suffix-search.html", suffix=suffix, matches=matches)

    message = session["message"]
    session["message"] = ""

    return render_template("suffix-search.html", message=message)

@app.route("/suffix-search-post", methods=["POST"])
def suffix_search_post():
    """ Find all words matching suffix (post). """

    session["helper"] = "ssp"

    suffix = request.form.get("fsuf").lower()

    if suffix:
        trie = Trie.create_from_file()
        remove_words(trie)

        for word in trie.suffix_search(suffix):
            session["suffix_results"].append(word)

        if len(session["suffix_results"]) > 0:
            session["suffix_results"].insert(0, suffix)
        else:
            session["message"] = f"No results for '{suffix}'."

    return redirect(url_for('suffix_search'))

@app.route("/change-dict")
def change_dict():
    """ Change dictionary (form). """
    init()

    message = session["message"]
    session["message"] = ""

    #dicts = ["tiny_dictionary.txt", "dictionary.txt"]
    dicts = ["tiny_frequency.txt", "frequency.txt"]

    #selected = Trie.default_dict.split("/")[-1]
    selected = Trie.default_dict.rsplit('/', maxsplit=1)[-1]

    return render_template("change-dict.html", message=message, dicts=dicts, selected=selected)

@app.route("/change-dict-post", methods=["POST"])
def change_dict_post():
    """ Change dictionary (post). """

    session["helper"] = "cdp"

    new_dct = request.form.get("dicts")

    #if new_dct != Trie.default_dict.split("/")[-1]:

    #if new_dct != Trie.default_dict.rsplit('/', maxsplit=1)[-1]:
    if new_dct != session["curr_dict"].rsplit('/', maxsplit=1)[-1]:

        # Trie.default_dict = app.static_folder + "/" + new_dct

        session["curr_dict"] = app.static_folder + "/" + new_dct

        session["removed_words"] = []

        session["message"] = f"Dictionary changed to '{new_dct}'"

    return redirect(url_for('change_dict'))

@app.route("/reset")
def reset():
    """ Route for reset session """
    init()

    # Drop all sesh vars
    _ = [session.pop(key) for key in list(session.keys())]

    # Re-init sesh vars
    init()

    return redirect(url_for('main'))

def remove_words(trie):
    """ Remove words stored in session from trie. """

    for removed_word in session["removed_words"]:
        trie.remove_word(removed_word)

@app.errorhandler(404)
def page_not_found(e):
    """ * """
    #pylint: disable=unused-argument
    return "hej, 404 error"

@app.errorhandler(500)
def internal_server_error(e):
    """ * """
    #pylint: disable=unused-argument
    return traceback.format_exc()

if __name__=="__main__":
    app.run(debug=True)
