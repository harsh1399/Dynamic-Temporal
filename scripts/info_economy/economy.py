import re
from functions import *
redundant = ['image', 'alt', 'caption', 'show-medals', 'module', 'updated', 'url', 'work', 'child', 'image_size','country'
             ,'currency','group','url','title']

interesting_keys = ['gdp','gdp rank','growth','per capita','per capita rank','sectors','poverty','gini','hdi','labor','unemployment',
                    'FDI','debt','balance','revenue','expenses','population','inflation','occupations','average gross salary',
                    'average net salary','exports','export-partners','imports','import-partners','import-goods','export-goods',
                    'gross external debt','debt','revenue','expenses','reserves']

timeline_keys = ['birth_date', 'medaltemplates', 'years', 'clubs', 'nationalteams']

final_timeline_keys = ['medaltemplates', 'clubs', 'years', 'nationalteams']

def squashMod(json_dict, key):
    # Nickname and height
    if key in ['nickname', 'height', 'birth_place', 'weight']:
        json_dict[key] = re.sub('url(.*)', '', json_dict[key])
        json_dict[key] = re.sub('https(.*)', '', json_dict[key])
        json_dict[key] = re.sub('title(.*)', '', json_dict[key])

    # Name and fullname
        if key in ['name', 'full_name']:
            json_dict[key] = re.sub("post-nominals","",json_dict[key])

def clubAddendum(json_dict):
    club_lst = []    
    for i in range(1,18):
        if f'years{i}' in json_dict.keys():
            club_lst.append(i)

    lst = {}
    for num in club_lst:
        try:
            lst[json_dict[f'team{num}']] = json_dict[f'years{num}']
        except:
            pass
                
        try:
            del json_dict[f'team{num}']
        except:
            pass
        
        try:
            del json_dict[f'years{num}']
        except:
            pass
        
    if lst:
        json_dict['clubs'] = lst

def ntAddendum(json_dict):
    nt_lst = []    
    for i in range(1,18):
        if f'nationalyears{i}' in json_dict.keys():
            nt_lst.append(i)

    lst = {}
    for num in nt_lst:
        try:
            lst[json_dict[f'nationalteam{num}']] = json_dict[f'nationalyears{num}']
        except:
            pass
                
        try:
            del json_dict[f'nationalteam{num}']
        except:
            pass
        
        try:
            del json_dict[f'nationalyears{num}']
        except:
            pass
        
    if lst:
        json_dict['nationalteams'] = lst