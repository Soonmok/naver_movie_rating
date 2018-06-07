#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import os
import re
import argparse

# Parser declaration
args = argparse.ArgumentParser()
args.add_argument("--maxcode", type=int, default=100000)
args.add_argument("--maxpage", type=int, default=500)
config = args.parse_args()

# 크롤링할때 html태그가 딸려오는데 그것을 지워주는 역할을 하는 함수
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = cleantext.strip()
    cleantext = cleantext.replace('\n     ','').replace('\n','')
    cleantext = cleantext.replace('\t\t\t\t\t\t\t',' ')
    cleantext = cleantext.replace('.',' ')
    cleantext = cleantext.replace('>',' ')
    cleantext = cleantext.replace('<',' ')
    return cleantext

# 주어진 path에 해당하는 html 정보를 가져와서 cleanhtml함수로 깨끗히 하여 반환하는 함수

def get_cleanhtml(html_path, html_type = 'html'):
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    
    cleaned_data = []
    if html_type == 'html':
        data = soup.select(html_path)
        for datum in data:
            datum = cleanhtml(str(datum))
            cleaned_data.append(datum)
        return cleaned_data
    else:
        data = soup.select(html_path)
        for datum in data:
            datum = cleanhtml(str(datum['src']))
            cleaned_data.append(datum)
        return cleaned_data

# Initialize variables
all_data_dict = []
data_dict = {}
id=0

# python파일의 위치
BASE_DIR = os.path.dirname(os.path.abspath("/home/iron/Project/crawling_python/data"))

# Turn around and crawl!
# range: 10000 ~ maxcode (The number of Movie)
for step,page_numbers in enumerate(range(10000, config.maxcode)):
    
    # Runs from page 1 to maxpage (The number of page per movie)
    for i in range(1, config.maxpage):
        req = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=' + str(page_numbers) + "&type=after&page=" + str(i))

        max_page = get_cleanhtml('.paging .pg_next em')
        text_data = get_cleanhtml('.score_result .score_reple p')
        score_data = get_cleanhtml('.score_result .star_score em')
        
        if not score_data and not text_data:
            break

        else:
            for text,score in zip(text_data, score_data):
                data_dict['comment_text'] = text
                data_dict['score'] = score
                id += 1
                all_data_dict.append(data_dict)
                
                #with open('./movie_score.json', 'a+', encoding='utf8') as json_file:
                #    json.dump(all_data_dict, json_file, ensure_ascii=False,indent=4)
                #all_data_dict = []
                
                if not os.path.isfile('./movie_score.json'):
                    with open('./movie_score.json', 'w+', encoding='utf8') as json_file:
                        json.dump(all_data_dict, json_file, ensure_ascii=False, indent=4)
                else:
                    with open('./movie_score.json', encoding='utf8') as json_file:
                        values = json.load(json_file)
                        values.extend(all_data_dict)
                    with open('./movie_score.json', mode='w', encoding='utf8') as json_file:
                        json_file.write(json.dumps(values, ensure_ascii=False, indent=4))
                all_data_dict=[]

            # If there is no next button, exit.
            print(step," 저장된 데이터 수 :",id)
            if max_page==[]:
                break


#with open('./movie_score.json', encoding='utf8') as json_file:
#    values = json.load(json_file)
   # json_file.write(json.dumps(values, ensure_ascii=False, indent=4))
   # print(values)
