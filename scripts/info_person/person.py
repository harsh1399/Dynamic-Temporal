import re
from functions import *
redundant = ['image','upright','fullname','short name','founded','nickname', 'alt', 'caption', 'website','image_size','url','title','birth_name','birth_date','birth_place',
             'death_date','death_place','nationality','other_names','honorific_prefix','honorific_suffix','image_upright','landscape','native_name','native_name_lang',
             'pronunciation','baptised','disappeared_date','disappeared_place','disappeared_status','death_cause','resting_place','resting_place_coordinates','burial_place',
             'burial_coordinates','monuments','nationality','other_names','siglum','citizenship','image_upright',
             'body_discovered','years_active','era','agent','style','height','television','title','term','predecessor',
             'successor','criminal_status','parents','mother','father','relatives','family','callsign','website',
             'module','module2','module3','module4','module5','module6','signature','signature_type','signature_size','signature_alt',
             'footnotes']

interesting_keys = ['name','education','alma_mater','occupation','employer','organization','known_for','notable_works',
                    'party','otherparty','movement','opponents','boards','criminal_charges','criminal_penalty',
                    'spouse','partner','children','awards']

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