import json
from pprint import pprint

with open("movie_score.json", encoding='utf-8') as f:
    data = json.loads(f.read())

for review in data:
    pprint(review)
