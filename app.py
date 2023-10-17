import json
import sys
import os
from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Ayush-Jef'

class SearchForm(FlaskForm):
    search = StringField("Enter your search terms:")
    submit = SubmitField("Search")

TF_IDF_map = None
document_links = None
document_names = None
document = None

def process_query(query, TF_IDF_map, document_links, document_names, document):
    query = query.lower().split()
    potential_documents = {}
    results = []

    ans = []

    try:
        for word in query:
            if word in TF_IDF_map:
                for index in TF_IDF_map[word]:
                    if index in potential_documents:
                        potential_documents[index] += TF_IDF_map[word][index]
                    else:
                        potential_documents[index] = TF_IDF_map[word][index]

        potential_documents = sorted(potential_documents.items(), key=lambda x: x[1], reverse=True)

        for index, score in potential_documents:
            index = int(index)
            results.append(str(document_links[index]) + "*" + str(document_names[index]))
            ans.append([
                str(document_links[index]),
                str(document_names[index])
            ])
    except Exception as e:
        print(e)
        return jsonify(error="Error processing the query")

    results = list(set(results))

    # ans = sorted(ans, key =lambda item : item[0], reverse = True)

    # # Prepare the JSON response
    # output_data = {
    #     'results': results
    # }

    # return jsonify(output_data)
    return ans

@app.route("/", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    ans = []
    q_terms = []
    if form.validate_on_submit():
        query = form.search.data
        q_terms = [term.lower() for term in query.strip().split()]
        ans = process_query(query, TF_IDF_map, document_links, document_names, document)[:20]

    if len(q_terms) != 0:
        search_triggered = True
    else:
        search_triggered = False

    return render_template('index.html', form=form, results=ans, search_triggered=search_triggered)

if __name__ == '__main__':
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(current_dir)
        output_file = os.path.join(current_dir, 'output.json')
        doc_file = os.path.join(current_dir, 'doc.json')
        links_file = os.path.join(current_dir, 'links.json')
        names_file = os.path.join(current_dir, 'names.json')

        with open(output_file, 'r') as file:
            TF_IDF_map = json.load(file)

        with open(doc_file, 'r') as file:
            document = json.load(file)

        with open(links_file, 'r') as file:
            document_links = json.load(file)

        with open(names_file, 'r') as file:
            document_names = json.load(file)
    except Exception as e:
        print(e)
        exit()

    app.run(debug=True)
