import praw
import dotenv
import os
import markdown
import re
import json
import time

dotenv.load_dotenv()

def fetch_main_reddit_wiki_page(subreddit_name, page_name):

    try:
        # fetch the main wiki page with all the links to the monthly pages
        subreddit = reddit.subreddit(subreddit_name)
        wiki_page = subreddit.wiki[f"{page_name}"]
        content = wiki_page.content_md  # Markdown content

        content.splitlines()

        wiki_links = []

        # parse the wiki page for the links to the monthly pages
        for line in content.splitlines():
            if line.startswith("###"):
                wiki_links.append(line.split("(")[1].replace(")", "").replace(f"https://www.reddit.com/r/{subreddit_name}/wiki/", ""))


        return wiki_links

    # if there's an error fetching the wiki page, return None
    except praw.exceptions.PRAWException as e:
        print(f"Error fetching Reddit wiki page: {e}")
        return None


def convert_monthly_content_to_json(content, year, month):
    json_data = []

    time_not_provided = ["2017-04", "2017-03"]

    day = "0th"

    for line in content.splitlines():
        # break the loop before OSTs are parsed
        if "#OST" in line:
            break
        try:
            # split the line into parts from the table columns
            parts = line.split("|")
            # remove the first element, which is always empty string
            parts.pop(0)
            if year + "-" + month in time_not_provided:
                # add a new element in between the 1st and 2nd element
                # for these months, the time of release is not provided
                parts.insert(1, "")
            # if the list is not 7 elements long, append an empty string
            # in this case, no song links were provided
            if len(parts) != 7:
                parts.append("")
            # autocomplete the day for the entries below the first of the day
            # as the day is only provided for the first entry of each day
            if parts[0] == "":
                parts[0] = day
            # if the day is provided, save it for the next entry
            day = parts[0]
            # if the time is not provided, replace it with "--:--"
            if parts[1] == "" or parts[1] == "?":
                parts[1] = "--:--"
            # if the text is surrounded by asterisks, remove them
            # this is used to mark the text as bold in the wiki
            if parts[2].startswith("*") and parts[2].endswith("*"):
                parts[2] = parts[2][1:-1]
            if parts[3].startswith("*") and parts[3].endswith("*"):
                parts[3] = parts[3][1:-1]
            if parts[4].startswith("*") and parts[4].endswith("*"):
                parts[4] = parts[4][1:-1]
            if parts[5].startswith("*") and parts[5].endswith("*"):
                parts[5] = parts[5][1:-1]
            if parts[6].startswith("*") and parts[6].endswith("*"):
                parts[6] = parts[6][1:-1]
            # get the link from the markdown syntax
            parts[5] = markdown.markdown(parts[5])
            link_pattern = re.compile(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"', re.IGNORECASE)
            parts[5] = link_pattern.search(parts[5])
            if parts[5]:
                parts[5] = parts[5].group(1)
                if parts[5].startswith("/"):
                    parts[5] = "https://www.reddit.com" + parts[5]

            if parts[6] != "":
                parts[6] = parts[6].split(" / ")
                links = []
                for link in parts[6]:
                    link = markdown.markdown(link)
                    link = link_pattern.search(link)
                    if link:
                        link = link.group(1)
                    links.append(link)
                parts[6] = links
                if parts[-1] == "":
                    parts.pop(-1)
            else:
                parts[6] = []
            
            reddit = parts.pop(5)
            if reddit != "":
                parts[5].append(reddit)
            
            parts[0] = parts[0].replace('th', '').replace('st', '').replace('nd', '').replace('rd', '')
            
            json_entry = {
                "date": f"{year}-{month}-{parts[0]}",
                "time": parts[1],
                "artist": parts[2],
                "title": parts[3],
                "album": parts[4],
                "links": parts[5]
            }

            
            json_data.append(json_entry)
            #print(json_entry)
        except Exception as e:
            if not line.startswith("|"):
                continue
            else:
                print("[IGNORED] Error parsing line: '" + line + "'")
                print(e)

    print(f"Found {len(json_data)} entries in {year}-{month}.")
    return json_data



def fetch_monthly_page(wiki_link, subreddit_name):
    try:
        subreddit = reddit.subreddit(subreddit_name)
        wiki_page = subreddit.wiki[f"{wiki_link}"].content_md

        wiki_page = wiki_page[wiki_page.find("|--|--|"):]
        wiki_page = wiki_page[wiki_page.find("\n") + 1:]
        #wiki_page = wiki_page[:wiki_page.find("\n\n")]

        year = wiki_link.split('/')[1]
        month = wiki_link.split('/')[2]

        month = month.replace("january", "01")
        month = month.replace("february", "02")
        month = month.replace("march", "03")
        month = month.replace("april", "04")
        month = month.replace("may", "05")
        month = month.replace("june", "06")
        month = month.replace("july", "07")
        month = month.replace("august", "08")
        month = month.replace("september", "09")
        month = month.replace("october", "10")
        month = month.replace("november", "11")
        month = month.replace("december", "12")

        return convert_monthly_content_to_json(wiki_page, year, month)

    except praw.exceptions.PRAWException as e:
        print(f"Error fetching Reddit wiki page: {e}")
        return None


# Example usage:
subreddit_name = "kpop"
wiki_page_name = "upcoming-releases/archive"

reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT')
    )
try:
        subreddit = reddit.subreddit(subreddit_name)
except praw.exceptions.PRAWException as e:
        print(f"Error fetching subreddit: {e}")

content = fetch_main_reddit_wiki_page(subreddit_name, wiki_page_name)

if content:

    json_data = []

    for wiki_link in content:

        print("Fetching monthly page: " + wiki_link)
            
        try:
            json_data += fetch_monthly_page(wiki_link, subreddit_name)
        except Exception as e:
            # write json_data to file
            with open(f"{subreddit_name}_upcoming_releases-CANCELED.json", "w") as f:
                f.write(json.dumps(json_data, indent=4))
            print("Error fetching monthly page: " + wiki_link)
            print(e)
            exit(1)

        print("Parsed monthly page: " + wiki_link)

        time.sleep(2)

    # save json_data to file
    with open(f"{subreddit_name}_upcoming_releases.json", "w") as f:
        f.write(json.dumps(json_data, indent=4))
    
    print("Fetched", len(json_data), "entries.")
