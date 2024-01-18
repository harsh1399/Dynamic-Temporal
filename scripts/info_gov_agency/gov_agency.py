import re
from functions import *
redundant = ['image','upright','fullname','short name','founded','nickname', 'alt', 'caption', 'website','image_size','url','title','native_name','native_name_a',
             'native_name_r','type','seal','seal_size','seal_caption','seal_alt','logo','logo_size','logo_caption','logo_alt','image','image_size','image_caption',
             'image_alt','formed','preceding1','preceding2','dissolved','superseding1','superseding2','agency_type','jurisdiction','status','headquarters',
             'coordinates','motto','parent_department','parent_agency','parent_agency_type','child1_agency','child2_agency','keydocument1','website','agency_id','map',
             'map_size','map_caption','map_alt','footnotes','embed']

interesting_keys = ['name','employees','budget','minister_type','minister1_name','minister1_pfo','deputyminister_type','deputyminister1_name',
                    'deputyminister1_pfo','deputyminister2_name','deputyminister2_pfo','chief1_name','chief1_position','chief2_name','chief2_position']

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