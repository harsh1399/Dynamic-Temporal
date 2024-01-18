from driver import driver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import re

import json
import dateparser
from functions import *
from economy import *
from constants import XPATH, history_limit
from api import titles, get_edit_history
import csv
players = []
links = dict()
for uu, page_title in enumerate(titles):
    try:
        global_lst = []
        championship_years = {}
        birth_date = ''
        json_dict = dict()
        raw_dict = dict()
        history_page = f"https://en.wikipedia.org/w/index.php?title={page_title}&action=history"
        driver.get(history_page)
        inter_links = driver.find_elements(By.PARTIAL_LINK_TEXT,", ")
        link = inter_links[0]
        url = link.get_attribute('href')+'&action=raw'
        driver.get(url)
        page = replace_newlines(remove_comments(driver.find_element(By.XPATH,XPATH).text))
        temp = replace_special(re.findall('(?<=\{\{Infobox)(.*)',replace_newlines(page))[0])
        # Figuring out where }} ends to mark end of infobox
        i=2
        infobox = ''
        for char in temp:
            if (i==0):
                break
            infobox = infobox + char
            if char=='{':
                i = i+1
            elif char=='}':
                i = i-1
        processed_text = replace_tabs(infobox+' | ')
        pt = replace_t(infobox)
        keys = re.findall("\|\s*[a-zA-Z]+_*[a-zA-Z]*\s*=",infobox)
        #re.findall('\^(.*?)ZXC', processed_text)
        '''
        for key_value in keys:
            try:
                key = key_value.split('=')[0]
                value = '='.join(key_value.split('=')[1:])
                if value.strip() == '':
                    key = key_value.split(': ')[0]
                    value = ': '.join(key_value.split(':')[1:])
                if value.strip() == '':
                    key = key_value.split('=')[0]
                    value = '='.join(key_value.split('=')[1:])
                # Do i need these strips??
                key = key.strip()
                raw_dict[key] = value        
                if key == 'birth_date':
                    parsed_code = parse(value)
                    date_template = parsed_code.filter_templates()[0]
                    try:
                        birth_date = birth_date + date_template.get(1).value.strip() + '-' 
                    except:
                        pass
                    try:
                        birth_date = birth_date + date_template.get(2).value.strip() + '-' 
                    except:
                        pass
                    try:
                        birth_date = birth_date + date_template.get(3).value.strip() + '-'
                    except:
                        pass
                    try:
                        birth_date = birth_date + date_template.get(4).value.strip()
                    except:
                        pass
                elif 'established_date' in key:
                    parsed_code = parse(value)
                    date_template = parsed_code.filter_templates()[0]
                    json_dict[key] = ''
                    try:
                        json_dict[key] = json_dict[key] + date_template.get(1).value.strip() + '-' 
                    except:
                        pass
                    try:
                        json_dict[key] = json_dict[key] + date_template.get(2).value.strip() + '-' 
                    except:
                        pass
                    try:
                        json_dict[key] = json_dict[key] + date_template.get(3).value.strip() + '-'
                    except:
                        pass
                    try:
                        json_dict[key] = json_dict[key] + date_template.get(4).value.strip()
                    except:
                        pass
                    if(json_dict[key][-1] == '-'):
                        json_dict[key] = json_dict[key][:-1]
                else:
                    json_dict[key] = clean(value)
                keyMod(json_dict, key)
                modify(json_dict,key)

            except:
                continue

        # Post Modification Cleaning
        for key in json_dict:
            if type(json_dict[key]) is str:
                json_dict[key] = post_clean(json_dict[key])
            elif type(json_dict[key]) is list:
                json_dict[key] = [post_clean(a) for a in json_dict[key]]
                
        # Removing empty slots
        remove = []
        for key in json_dict.keys():
            try:
                if(json_dict[key].strip() == ''):
                    remove.append(key)
            except:
                pass
        for key in remove:
            json_dict.pop(key)

        # Removing redundant slots
        for key in redundant:
            try:
                json_dict.pop(key)
            except:
                pass
    
        # subdivisionAddendum(json_dict)
        # establishedAddendum(json_dict)
        # leadersAddendum(json_dict)
        # seatAddendum(json_dict)
        # blanksAddendum(json_dict)

        try:
            if birth_date:
                json_dict['birth_date'] = birth_date[:-1]
        except:
            pass    

        try:
            if global_lst:
                json_dict['medaltemplates'] = global_lst
        except:
            pass

        try:
            if championship_years:
                json_dict['WorldOpenresult'] = championship_years
        except:
            pass
        '''
        imp_keys = []
        for key in keys:
            key = key[1:-1]
            if key not in redundant:
                imp_keys.append(key)

        timelines = re.findall("\d\d\d\d", infobox)
        final_timelines = []
        # for ele in range(2005, 2024):
        for ele in timelines:
            if (int(ele) <= 2023) and (int(ele) >= 2005):
                # final_timelines.append(str(ele))
                final_timelines.append(ele)
                
        final_timelines = list(set(final_timelines))

        # print(final_timelines)
        links[page_title] = []
        for ele in final_timelines:
            date = dateparser.parse(ele)
            start = date.replace(month=1, day = 1).strftime("%Y%m%d") + '000000'
            end = date.replace(month=12, day = 31).strftime("%Y%m%d") + '000000'
            try:
                revisions = get_edit_history(page_title, start, end)
                links[page_title]  = links[page_title]+ revisions
            except:
                pass
        print(len(links[page_title]))
        links[page_title] = [d for i, d in enumerate(links[page_title]) if d not in links[page_title][:i]]
        links[page_title] = sorted(links[page_title], key = lambda x: x['timestamp'])
        # print(len(links[page_title]))
        # final_dict = {}
        # final_dict['name'] = page_title
        # final_dict['total_timelines'] = len(final_timelines)
        # final_dict['total_keys'] = len(imp_keys)
        # final_dict['revisions'] = len(links[page_title])
        # players.append(final_dict)

    except:
        pass

# links = dict(sorted(links.items(), key=lambda item: len(item[1]), reverse=True))
# links = {key: links[key] for key in list(links)[:history_limit]}

# file = open('cyclist_player.csv','w')
# writer = csv.writer(file)
# writer.writerow(['Name', 'total_timelines', 'total_keys','revisions'])
# for player in players:
#     writer.writerow(player.values())
# file.close()

with open(f"link_timeline.json", "w", encoding="utf-8") as f:
    json.dump(links, f, indent=4)
    f.close()