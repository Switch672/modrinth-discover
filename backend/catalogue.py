import requests
import math
from time import sleep
import enchant

def analyze(text, default_tags=[], min=5):

    dictionary = enchant.Dict("en_US")

    text += ' '
    allowed_chars = 'abcdefghijklmnopqrstuvwxyz'
    ignore_list = ["even","want","different","like","used","the","add","also","visit","we","using","sure","make","game","greatly","minecraft","this","mod","work","like","use","","mods","i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
    occurences = {}
    word = ''
    common = []

    for i in range(len(text)):

        if text[i] == ' ' or i == range(len(text)):

            if occurences.get(word):

                occurences.update({word: occurences.get(word)+1})
            else:

                occurences.update({word: 1})

            word = ''

            pass
        elif not text[i].lower() in allowed_chars:

            pass
        else:

            word += text[i].lower()
    
    for i in occurences:

        if occurences[i] > min-1 and not i in ignore_list and dictionary.check(i):

            common.append(i)

    for i in default_tags:
        
        common.append(i)
    
    return common

def catalogue(count, offset=0, project_type='mod'):

    limit = 10
    projects = []
    h = offset

    for i in range(math.ceil(count/10)):

        search = requests.get('https://api.modrinth.com/v2/search?facets=[["project_type:'+project_type+'"]]',params={'limit':limit,'offset':h})

        for j in range(len(search.json()['hits'])):

            slug = search.json()['hits'][j]['slug']
            project = requests.get('https://api.modrinth.com/v2/project/'+slug)
            id = project.json()['id']

            text_to_search = ''
            text_to_search += project.json()['title']
            text_to_search += project.json()['body']
            text_to_search += project.json()['description']

            h += 1

            projects.append({'_id':id,'slug':slug,'tags':analyze(text_to_search)})
            print({'_id':id,'slug':slug,'tags':len(analyze(text_to_search))})

            sleep(0.3)

    return projects

def catalogue_one(slug, project_type='mod'):

    print(slug)
    project = requests.get('https://api.modrinth.com/v2/project/'+slug)
    id = project.json()['id']

    text_to_search = ''
    text_to_search += project.json()['title']
    text_to_search += project.json()['body']
    text_to_search += project.json()['description']

    return {'_id':id,'slug':slug,'tags':analyze(text_to_search)}

def catalogue_and_save(mongoclient, slug, count=10, offset=0, project_type='mod'):

    print(mongoclient)

    tags = mongoclient["tags"]
    mods = tags[project_type+'s']
    projects = []

    if count > 1:
        
        projects = catalogue(count, offset, project_type)
    elif count == 1:

        projects.append(catalogue_one(slug, project_type))

    for i in projects:
        
        if mods.find_one({'_id':i['_id']}):

            mods.update_one({'_id':i['_id']}, {'$set':i})
        else:

            mods.insert_one(i)