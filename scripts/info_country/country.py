import re
from functions import *
redundant = ['image','upright','fullname','short name','founded','nickname', 'alt', 'caption', 'website','image_size','url','title','micronation','loctext','map_width','map_caption',
             'conventional_long_name','native_name','image_flag','alt_flag','flag_border','image_flag2','alt_flag2','flag2_border','image_coat','symbol_width','motto',
             'alt_coat','symbol_type','national_motto','englishmotto','national_anthem','royal_anthem','other_symbol_type','other_symbol','alt_symbol','text_symbol_type',
             'image_map','loctext','alt_map','map_caption','image_map_size','image_map2','alt_map2','map_caption2','image_map2_size','capital','coordinates','government_type',
             'legislature','upper_house','lower_house','sovereignty_note','established_event1','established_date1','established_event2','established_date2','text_symbol',
             'established_event13','established_date13','area_footnote','area_label','area_label2','area_data2','Gini_ref','HDI_ref','currency','currency_code',
             'time_zone','utc_offset','time_zone_DST','utc_offset_DST','DST_note','antipodes','date_format','drives_on','cctld','iso3166code','org_type','membership_type',
             'calling_code','patron_saint','image_map3','alt_map3','footnote_a','footnote_b','footnote_h','footnotes','admin_center_type','established','established_event9',
             'established_date9','official_website','era','status_text','empire','event_start','date_start','year_start','event_end','date_end','year_end','year_exile_start',
             'year_exile_end','event1','date_event1','event2','date_event2','event3','date_event3','event4','date_event4','event5','date_event5','event6','date_event6',
             'event_pre','date_pre','event_post','date_post','p1','flag_p1','image_p1','p2','flag_p2','p3','flag_p3','p4','flag_p4','p5','flag_p5','s1','flag_s1','image_s1',
             's2','flag_s2','s3','flag_s3','s4','flag_s4','s5','flag_s5','image_flag','flag_alt','image_flag2','flag_alt2','flag','flag2','flag_type','flag2_type',
             'image_coat','coa_size','coat_alt','symbol_type','symbol_type_article','image_map','image_map_size','image_map_alt','image_map_caption','image_map2','image_map2_size',
             'image_map2_alt','image_map2_caption','capital','capital_exile','common_languages','house1','type_house1','house2','type_house2']

interesting_keys = ['common_name','status','largest_city','largest_settlement_type','largest_settlement','official_languages','national_languages','regional_languages',
                    'ethnic_groups','ethnic_groups_year','religion','religion_year','leader_title1','leader_name1','leader_title2','leader_name2','leader_title14','leader_name14',
                    'sovereignty_type','area_rank','area','area_km2','area_sq_mi','percent_water','population_estimate','population_estimate_rank','population_estimate_year',
                    'population_census','population_census_year','population_density_km2','population_density_sq_mi','population_density_rank','nummembers',
                    'GDP_PPP','GDP_PPP_rank','GDP_PPP_year','GDP_PPP_per_capita','GDP_PPP_per_capita_rank','GDP_nominal','GDP_nominal_rank','GDP_nominal_year',
                    'GDP_nominal_per_capita','GDP_nominal_per_capita_rank','Gini','Gini_rank','Gini_year','HDI_year','HDI','HDI_change','HDI_rank','membership','admin_center',
                    'leader1','leader2','leader3','leader4','leader21','title_leader','representative1','representative2','representative3','representative4',
                    'representative5','year_representative1','year_representative2','year_representative3','year_representative4','year_representative5','title_representative',
                    'deputy1','deputy2','deputy3','deputy4','year_deputy1','year_deputy2','year_deputy3','year_deputy4','title_deputy','legislature','stat_year1','stat_area1',
                    'stat_pop1','stat_year2','stat_area2','stat_pop2','stat_year3','stat_area3','stat_pop3','stat_year4','stat_area4','stat_pop4','stat_year5','stat_area5','stat_pop5',
                    'today']

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