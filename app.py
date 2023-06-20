from flask import Flask, jsonify
import math
import os
import re

from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

vocab_path = r"TFIDF implementation\tf-idf\vocab1.txt"
idf_values_path= r"TFIDF implementation\tf-idf\idf-values1.txt"
documents_path= r"TFIDF implementation\tf-idf\documents1.txt"
inverted_index_path= r"TFIDF implementation\tf-idf\inverted-index1.txt"

"""
#absolute path in os.join format
script_dir = os.path.dirname(os.path.abspath(__file__))
vocab_path = os.path.join(script_dir, 'TFIDF implementation', 'tf-idf', 'vocab1.txt')
idf_values_path = os.path.join(script_dir, 'TFIDF implementation', 'tf-idf', 'idf-values1.txt')
documents_path = os.path.join(script_dir, 'TFIDF implementation', 'tf-idf', 'documents1.txt')
inverted_index_path = os.path.join(script_dir, 'TFIDF implementation', 'tf-idf', 'inverted-index1.txt')
"""

#index file to a dictionary
indexdict = {}
with open("Leetcodescrapped\Qdata\index.txt",'r') as f:
        lines = f.readlines()

        for line_number, line_text in enumerate(lines, start=1):
          indexdict[line_number] = line_text.strip()

    
def preprocess_string(input_string):
    processed_string = input_string.lower().replace(" ", "-")
    processed_string = re.sub(r'\b\d+\.\s*', '', processed_string)  # Remove leading numbers and dot with trailing whitespace
    isplit_string = processed_string.lstrip("-")
    return isplit_string

def create_link(index_line):
    base_url = "https://leetcode.com/problems/"
    link = base_url + index_line.replace("-", "-")
    return link
  
def load_vocab():
    vocab = {}
    with open(vocab_path, 'r',encoding='utf-8') as f:
        vocab_terms = f.readlines()
    with open(idf_values_path, 'r') as f:
        idf_values = f.readlines()
    
    for (term,idf_value) in zip(vocab_terms, idf_values):
        vocab[term.strip()] = int(idf_value.strip())
    
    return vocab

def load_documents():
    documents = []
    with open(documents_path, 'r',encoding='utf-8') as f:
        documents = f.readlines()
    documents = [document.strip().split() for document in documents]

    return documents

def load_inverted_index():
    inverted_index = {}
    with open(inverted_index_path, 'r',encoding='utf-8') as f:
        inverted_index_terms = f.readlines()

    for row_num in range(0,len(inverted_index_terms),2):
        term = inverted_index_terms[row_num].strip()
        documents = inverted_index_terms[row_num+1].strip().split()
        inverted_index[term] = documents
    
    return inverted_index



vocab_idf_values = load_vocab()
documents = load_documents()
inverted_index = load_inverted_index()


def get_tf_dictionary(term):
    tf_values = {}
    if term in inverted_index:
        for document in inverted_index[term]:
            if document not in tf_values:
                tf_values[document] = 1
            else:
                tf_values[document] += 1
                
    for document in tf_values:
        tf_values[document] /= len(documents[int(document)])
    
    return tf_values

def get_idf_value(term):
    return math.log(len(documents)/vocab_idf_values[term])

def calculate_sorted_order_of_documents(query_terms):
    potential_documents = {}
    question_links = []  # New list to store the question links

    for term in query_terms:
        if term not in vocab_idf_values or vocab_idf_values[term] == 0:
            print("Sorry, We do not have questions containing the keyword you entered!")
            return []
        tf_values_by_document = get_tf_dictionary(term)
        idf_value = get_idf_value(term)
        for document in tf_values_by_document:
            if document not in potential_documents:
                potential_documents[document] = tf_values_by_document[document] * idf_value
            potential_documents[document] += tf_values_by_document[document] * idf_value

    # Divide by the length of the query terms
    for document in potential_documents:
        potential_documents[document] /= len(query_terms)

    potential_documents = dict(sorted(potential_documents.items(), key=lambda item: item[1], reverse=True))

    for document_index in potential_documents:
        line_text = indexdict[int(document_index)+1]
        line_updated = preprocess_string(line_text)
        question_link = create_link(line_updated)
        question_links.append(question_link)  # Append the question link to the list

    return question_links[:20:] # Return the list of question links

# -------------------Flask Work--------------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = '1606Shinoy'
#query_string = input('Enter your query: ')
#query_terms = [term.lower() for term in query_string.strip().split()]

# print(query_terms)
# print(calc_docs_sorted_order(query_terms)[0])
# print(len(calc_docs_sorted_order(query_terms)))


class SearchForm(FlaskForm):
    search = StringField('Enter your search term')
    submit = SubmitField('Search')


@app.route("/<query>", methods=['POST'])
def return_links(query):
    q_terms = [term.lower() for term in query.strip().split()]
    return jsonify(calculate_sorted_order_of_documents(q_terms)[:20])

@app.route("/", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        query = form.search.data
        q_terms = [term.lower() for term in query.strip().split()]
        results = calculate_sorted_order_of_documents(q_terms)[:20]
    return render_template('index.html', form=form, results=results)

"""
@app.route("/<query>")
def return_links(query):
    q_terms = [term.lower() for term in query.strip().split()]
    return jsonify(calculate_sorted_order_of_documents(q_terms)[:20:])


@app.route("/", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        query = form.search.data
        q_terms = [term.lower() for term in query.strip().split()]
        results = calculate_sorted_order_of_documents(q_terms)[:20:]
    return render_template('index.html', form=form, results=results)
"""
if __name__ == "__main__":
    app.run(debug=True,use_reloader = True,port = 8001)