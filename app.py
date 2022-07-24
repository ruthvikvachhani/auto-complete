import csv
import os

from flask import Flask, jsonify, request
app = Flask(__name__)

FILE = os.environ.get("FILE", "test_data_sample.csv")


with open(FILE) as f:
    reader = csv.reader(f)
    terms = [row[0] for row in reader if len(row[0])>=3]



def filter(name,query):
    quer = query.lower() 
    name = name.lower()
    if quer in name:
        if name.startswith(quer):
            return 1
        else:
            return 0
    return -1



def name_list(name_dict):

    name_lst = []
    for i in name_dict:
        temp = {}
        temp['name'] = i
        name_lst.append(temp)
    return name_lst




@app.route('/process_search')
def gen_search_json():
    query = request.args.get("q", '')
    results = [{"name" : "This is invalid, just to demo AJAX call is working"}]  
    if len(query)>=3:
        # must be list of dicts: [{"name": "foo"}, {"name": "bar"}]
        dist={0:[],1:[]}

        for i in terms[1:]:
            temp = filter(i,query)
            if temp>=0:
                dist[temp].append(i)


        # your logic goes here!
        results=[]
        dist[0].sort(key=lambda val:len(val))
        dist[1].sort(key=lambda val:len(val))

        results.extend(name_list(dist[1]))
        results.extend(name_list(dist[0]))
        

    resp = jsonify(results=results[:10])  # top 10 results
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == "__main__":
    app.run(debug=True)