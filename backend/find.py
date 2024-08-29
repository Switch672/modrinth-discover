import pymongo

def find(mongoclient, slug, project_type='mod'):

    tags = mongoclient["tags"]
    mods = tags[project_type+'s']

    print(mods)

    project = mods.find_one({'slug':slug})
    print(project)
    projects = mods.find({'tags': { '$in':project['tags']}})

    suggested_projects = []

    for i in projects:
        
        suggested_projects.append(i['slug'])

    print(suggested_projects)
    return suggested_projects



mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")

find(mongoclient, 'fabulously-optimized', 'modpack')