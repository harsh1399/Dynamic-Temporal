import re
from functions import *
redundant = ['image','upright','fullname','short name','founded','nickname', 'alt', 'caption', 'website','image_size','url','title','micronation','loctext','map_width'
    ,'map_caption','logo','logo_size','logo_alt','logo_caption','screenshot','screenshot_size','screenshot_alt','collapsible','collapsibletext','background','caption','company_type',
             'type','language','language_count','language_footnote','traded_as','founded','dissolved','predecessor','successor','headquarters','location_city','location_country',
             'country_of_origin','area_srved','author','founder','industry','international','parent','url','ipv6','advertising','commercial','registration','launch_date',
             'current_status','native_clients','programming_language','issn','eissn','oclc','footnotes']

interesting_keys = ['name','locations','owner','editor','chairman','chairperson','president','CEO','MD','GM','key_people','products','services','revenue','operating_income',
                    'net_income','assets','equity','employees','divisions','subsidiaries','num_users']

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