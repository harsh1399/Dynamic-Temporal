import re
from functions import *
redundant = ['image','upright','fullname','short name','founded','nickname', 'alt', 'caption', 'website','image_size','url','title','honorific_prefix','imagesize','image2',
             'honorific_suffix','native_name','native_name_lang','landscape','birth_name','birth_date','birth_place','death_date','death_place','death_cause','image_upright2',
             'resting_place','resting_place_coordinates','other_name','siglum','pronounce','citizenship','nationality','patrons','thesis_title','thesis_url','imagesize2',
             'thesis_year','doctoral_advisors','academic_advisors','author_abbrev_bot','author_abbrev_zoo','parents','father','mother','relatives','signature','signature_type',
             'signature_alt','footnotes','native_name','native_name_a','native_name_r','country','logo','logo_size','logo_border','logo_alt','image_size','image_border',
             'organization','purpose','firstflight','firstcrewed','lastflight','launchsite','image_alt','motto','school','founder','custom_label','custom','foundation'
             'uncrewvehicle','crewvehicle','capacity','launcher','ceased publication','ceased_publication','relaunched','publishing_city','publishing_country',
             'circulation_date','circulation_ref','sister newspapers','sister_newspapers','ISSN','eISSN','oclc','RNI','website','free','alt2','caption2',
             'established','dissolved','location','coordinates','type','appealsto','appealsfrom','language','website','chiefjudgetitle','chiefjudgetitle2','chiefjudgetitle3',
             'division_map','division_map_upright','division_map_size','division_map_alt','division_caption']

interesting_keys = ['court_name','jurisdiction','authority','terms','positions','budget','tribunal-type','chiefjudgename','termstart','termend','termend2',
                    'chiefjudgename2','termstart2','termend3','chiefjudgename3','termstart3']

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