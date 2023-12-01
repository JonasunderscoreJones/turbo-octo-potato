import praw

def fetch_main_reddit_wiki_page(subreddit_name, page_name):

    try:
        subreddit = reddit.subreddit(subreddit_name)
        wiki_page = subreddit.wiki[f"{page_name}"]
        content = wiki_page.content_md  # Markdown content

        content.splitlines()

        wiki_links = []

        for line in content.splitlines():
            if line.startswith("###"):
                wiki_links.append(line.split("(")[1].replace(")", "").replace(f"https://www.reddit.com/r/{subreddit_name}/wiki/", ""))


        return wiki_links

    except praw.exceptions.PRAWException as e:
        print(f"Error fetching Reddit wiki page: {e}")
        return None


def convert_monthly_content_to_json(content, year, month):
    json_data = []

    day = 0

    for line in content.splitlines():
        parts = line.split("|")
        parts.pop(0)
        print(parts)


def fetch_monthly_page(wiki_link, subreddit_name):
    try:
        subreddit = reddit.subreddit(subreddit_name)
        wiki_page = subreddit.wiki[f"{wiki_link}"].content_md

        wiki_page = wiki_page[wiki_page.find("|--|--|"):]
        wiki_page = wiki_page[wiki_page.find("\n") + 1:]
        wiki_page = wiki_page[:wiki_page.find("\n\n")]

        convert_monthly_content_to_json(wiki_page, 2021, 1)
        exit()

        return wiki_page

    except praw.exceptions.PRAWException as e:
        print(f"Error fetching Reddit wiki page: {e}")
        return None


# Example usage:
subreddit_name = "kpop"
wiki_page_name = "upcoming-releases/archive"

reddit = praw.Reddit(
        client_id='6X31S2XAmGulAhMbASXJtw',
        client_secret='L9pUKAKFMvkA0hbIVsdZBdV43frTSg',
        user_agent='KProfilesFetch/1.0 by u/Jonas_Jones_',
    )
try:
        subreddit = reddit.subreddit(subreddit_name)
except praw.exceptions.PRAWException as e:
        print(f"Error fetching subreddit: {e}")

content = fetch_main_reddit_wiki_page(subreddit_name, wiki_page_name)

if content:

    print(fetch_monthly_page(content[1], subreddit_name))
