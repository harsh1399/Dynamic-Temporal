import requests
import json
import re
with open("sports_league_new.txt", "r") as f:
    text = f.read()
    titles = text.split("\n")
    f.close()
links = dict()

def get_edit_history(page_title, start_date = None, end_date = None):
    # Initialize an empty list to store the revisions
    revisions = []
    
    # Set the base URL for the API request
    api_url = "https://en.wikipedia.org/w/api.php"
    
    # Set the parameters for the API request
    if (start_date and end_date):
        params = {
            "action": "query",
            "titles": page_title,
            "rvstart":start_date,
            "rvend":end_date,
            "format": "json",
            "prop": "revisions",
            "rvlimit": "500",
            "rvdir": "newer"
        }

    else:
        params = {
            "action": "query",
            "titles": page_title,
            "format": "json",
            "prop": "revisions",
            "rvlimit": "500",
        }
    
    # Set a flag to indicate whether there are more revisions to retrieve
    more_revisions = True
    
    while more_revisions:
        # Make the API request
        response = requests.get(api_url, params=params)
        
        # Get the data from the response
        data = response.json()
        
        # Extract the revisions from the data
        page_id = list(data["query"]["pages"].keys())[0]
        try:
            page_revisions = data["query"]["pages"][page_id]["revisions"]
            
            # Add the revisions to the list
            revisions.extend(page_revisions)
        except:
            pass
        #cont = re.search('<continue rvcontinue="([^"]+)"', data)
        # Check if there are more revisions to retrieve
        if "continue" in data:
            # Update the rvcontinue parameter for the next request
            params["rvcontinue"] = data["continue"]["rvcontinue"]
        else:
            # Set the flag to False to stop the loop
            more_revisions = False
    
    # Return the list of revisions
    return revisions


# for title in titles:
#     links[title] = get_edit_history(title)


# with open(f"link.json", "a", encoding="utf-8") as f:
#     json.dump(links, f, indent=4)