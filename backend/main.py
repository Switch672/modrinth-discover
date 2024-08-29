import pymongo
import catalogue
import find
from flask import Flask, request

mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")

app = Flask(__name__)

@app.route("/related/")
def related():

    slug = str(request.args.get('slug'))
    type = str(request.args.get('type'))

    catalogue.catalogue_and_save(mongoclient, slug, 1, project_type=type)

    return find.find(mongoclient, slug, type)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)