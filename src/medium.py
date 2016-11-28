from src.models.posts import Post
import requests
import json
import unidecode

def get_posts(x):
    result = requests.get('https://medium.com/@matthewedanwoo/latest?format=json')
    result_content = result.content[16:]
    medium_json = json.loads(result_content)
    posts = medium_json['payload']['references']['Post'].keys()
    latest_posts = posts[:x]
    posts_content = []
    i = x-1
    while i >= 0:
        title = medium_json['payload']['references']['Post'][latest_posts[i]]['title']
        title = unidecode.unidecode(title)
        url = medium_json['payload']['references']['Post'][latest_posts[i]]['uniqueSlug']
        subtitle = medium_json['payload']['references']['Post'][latest_posts[i]]['virtuals']['snippet']
        subtitle = unidecode.unidecode(subtitle)
        reading_time = medium_json['payload']['references']['Post'][latest_posts[i]]['virtuals']['readingTime']
        posts_content.append(Post(title=title, url=url, subtitle=subtitle, reading_time=reading_time).json())
        i -= 1
    return bot_post_json(x,posts_content)

def bot_post_json(x, posts_content):
    i = 0
    post_header = {
                    "messages": [
                        {
                    "attachment": {
                      "type": "template",
                      "payload": {
                        "template_type": "generic",
                        "elements": []
                      }
                    }
                }
            ]
    }
    while i < x:
        post = {
                "title": posts_content[i]['title'],
                "subtitle": posts_content[i]['subtitle'],
                "buttons": [
                    {
                        "type": "web_url",
                        "url": posts_content[i]['url'],
                        "title": "Read More"
                    }
                ]
            }
        post_header['messages'][0]['attachment']['payload']['elements'].append(post)
        i += 1
    return post_header













