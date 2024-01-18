import re
from functions import *
redundant = ['image','image_upright','fullname','short name','founded','nickname', 'image_alt', 'caption', 'website','image_size','url','title','honorific_prefix','latin_name',
             'honorific_suffix','native_name','native_name_lang','landscape','birth_name','birth_date','birth_place','death_date','death_place','death_cause','other_name',
             'resting_place','resting_place_coordinates','other_name','siglum','pronounce','citizenship','nationality','patrons','thesis_title','thesis_url','former_name',
             'thesis_year','doctoral_advisors','academic_advisors','author_abbrev_bot','author_abbrev_zoo','parents','father','mother','relatives','signature','signature_type',
             'signature_alt','footnotes','motto','motto_lang','mottoeng','top_free_label','top_free','type','established','closed','founder','parent','accreditation','affiliation',
             'religion_affiliation','academic_affiliation','address','city','state','province','country','postalcode','coordinates','campus_type','language',
             'free_label','free','colors','sports_nickname','sporting_affiliations','mascot','sports_free_label','sports_free','website','logo','logo_size','logo_upright',
             'logo_alt','embedded','pushpin_map','pushpin_label_position','map_size','pushpin_map_caption','footnotes','image_name']

interesting_keys = ['name','endowment','budget','officer_in_charge','chair','chairman','chairperson','visitor','chancellor','president','vice_president','superintendent',
                    'vice_chancellor','provost','rector','principal','director','dean','head_label','head','academic_staff','total_staff','students','undergrad',
                    'postgrad','doctoral','other_students','campus_size']

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