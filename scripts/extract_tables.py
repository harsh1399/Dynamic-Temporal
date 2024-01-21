import jellyfish
import os
import json

number_of_changing_keys = 3
# fuzzy_hash_match = 80  ##100 full match
jaro_lower_bound = 0.25
jaro_upper_bound = 0.85
minimum_number_of_tables = 5

important_keys = ['name','captain','test_captain','od_captain','t20i_captain','1captain','2captain','coach','test_coach','od_coach','chairman','batting_coach',
                  'bowling_coach','fielding_coach','overseas','overseas1','overseas2','owner','ceo','manager','adviser','num_titles',
                  'title1','title1wins','title2','title2wins','title3','title3wins','title4','title4wins','title5','title5wins','title6','title6wins',
                  'title7','title7wins','title8','title8wins','sheffield','frc_wins','t20_wins','ipl_wins','clt20_wins','bpl_wins','psl_wins','WCL_division',
                  'test_rank','test_rank_best','odi_rank','odi_rank_best','t20i_rank','t20i_rank_best','wodi_rank','wodi_rank_best','wt20i_rank','wt20i_rank_best',
                  'num_tests','test_record','num_tests_this_year','test_record_this_year','wtc_apps','num_odis','odi_record','num_odis_this_year',
                  'odi_record_this_year','wc_apps','num_t20is','t20i_record','num_t20is_this_year','t20i_record_this_year','wt20_apps','wcq_apps','wcq_best',
                  'wt20q_apps','wt20q_best','num_wtests','wtest_record','num_wtests_this_year','wtest_record_this_year','num_wodis','wodi_record',
                  'num_wodis_this_year','wodi_record_this_year','wwc_apps','wwc_best','num_wt20is','num_wt20is_this_year','wt20i_record_this_year','wwt20_apps',
                  'wwt20_best']

folders_path = "scripts//info_cricket_team//infoboxes//cricket_team"

folders = os.listdir(folders_path)
bad_data = 0
less_than_two_file = []
for folder in folders:
    if folder == "json_compare_logging.txt" or folder == "good_folders.txt":
        continue
    if folder!="India_national_cricket_team":
        continue
    print(folder)
    folder_path = os.path.join(folders_path, folder)
    files = os.listdir(folder_path)
    files_int = []
    for filename in files:
        if filename != "logs.txt" and filename != f"{folder}.json":
            filen = int(filename.split(".")[0])
            files_int.append(filen)
    files_int.sort()

    if len(files_int) < 2:
        less_than_two_file.append(folder)
        continue
    final_json = {}
    first = 0
    second = 1

    while second < len(files_int):
        with open(f"{folder_path}/{files_int[first]}.json", 'r', encoding="utf-8") as f:
            try:
                data_first = json.load(f)
            except:
                print(first)
        with open(f"{folder_path}/{files_int[second]}.json", 'r', encoding="utf-8") as f:
            try:
                data_second = json.load(f)
            except:
                print(second)
        first_keys = data_first.keys()
        second_keys = data_second.keys()
        number_of_keys = min(len(first_keys), len(second_keys))
        count = 0
        count1 = 0
        js = {}
        for key in second_keys:
            if key in first_keys and key in important_keys:
                if not isinstance(data_first[key], list) and not isinstance(data_second[key], list):
                    similarity = jellyfish.jaro_winkler_similarity(data_first[key], data_second[key])
                    if similarity < jaro_upper_bound and similarity > jaro_lower_bound:
                        count += 1
                    # h1 = ssdeep.hash(data_first[key])
                    # h2 = ssdeep.hash(data_second[key])
                    # fuzzy_val = ssdeep.compare(h1,h2)
                    # if fuzzy_val < fuzzy_hash_match:
                    #     count += 1
                count1 += 1
            elif key not in first_keys and key in important_keys:
                count += 1
        if count >= (0.1 * number_of_changing_keys) * number_of_keys:
            for key in data_first:
                if key in important_keys:
                    js[key] = data_first[key]
            if len(js) != 0:
                final_json[data_first["DATE_TIME"]] = js
            first = second
            second += 1
        else:
            if count1 == 0:
                first = second
                second += 1
            else:
                second += 1
    if len(final_json) >= minimum_number_of_tables:
        with open(f"{folders_path}/good_folders.txt", 'a') as f:
            f.write(f"{folder}\n")
        with open(f"{folder_path}/{folder}.json", 'w') as f:
            json.dump(final_json, f)
    else:
        with open(f"{folders_path}/json_compare_logging.txt", 'a') as f:
            f.write(f"{folder}\n")
        bad_data += 1

print(f"folders having non usable timelines {bad_data}")