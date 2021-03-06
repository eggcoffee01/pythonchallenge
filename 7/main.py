import requests
import json
from flask import Flask, render_template, request

app = Flask(__name__)

url = 'http://hn.algolia.com/api/v1'

popular = f'{url}/search?tags=story'

new = f"{url}/search_by_date?tags=story"

newDB = []
popDB = []

def new_update():
    new_result = requests.get(new)
    new_json = new_result.json()
    for json in new_json["hits"]:
        title = json.get('title')
        id = json.get('objectID')
        link = json.get('url')
        points = json.get('points')
        author = json.get('author')
        comments = json.get('num_comments')
        newDB.append({"title": title, "id": id, "link": link, "points": points, "author": author, "comments": comments})

def popular_update():
    pop_result = requests.get(popular)
    pop_json = pop_result.json()
    for json in pop_json["hits"]:
        title = json.get('title')
        id = json.get('objectID')
        link = json.get('url')
        points = json.get('points')
        author = json.get('author')
        comments = json.get('num_comments')
        popDB.append({"title": title, "id": id, "link": link, "points": points, "author": author, "comments": comments})

@app.route('/')
def home():
    searchword = request.args.get('order_by', 'popular')
    if searchword:
        if searchword == "new":
            db = newDB
            if db:
                pass
            else:
                new_update()
            return render_template("index.html", first_tag="a", second_tag="strong", first_href="href=/?order_by=popular", db=db)
        else:
            db = popDB
            if db:
                pass
            else:
                popular_update()
            return render_template("index.html", first_tag="strong", second_tag="a", second_href="href=/?order_by=new", db=db)

@app.route('/<id>')
def description(id):
    id_url = f'{url}/items/{id}'
    id_result = requests.get(id_url)
    id_json = id_result.json()
    title = id_json["title"]
    points = id_json["points"]
    author = id_json["author"]
    link = id_json["url"]
    id_comments = []
    for child in id_json["children"]:
        comments_author = child['author']
        text = child["text"]
        child_dict = {"author": comments_author, "text": text}
        id_comments.append(child_dict)
    return render_template("detail.html", title=title, points=points, author=author, link=link, db=id_comments)



app.run()