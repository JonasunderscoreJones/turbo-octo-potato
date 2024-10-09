'''Fetch the monthly comeback/debut/release pages on kprofiles.com'''
import datetime
import requests
import dotenv
import spotipy
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import top_lib

dotenv.load_dotenv()

WORKING_DIR = os.getenv('WORKING_DIR')


def get_links():
    '''Get the links to the monthly comeback/debut/release pages on kprofiles.com
    
    Returns: a list of links to the monthly comeback/debut/release pages on kprofiles.com'''
    links = []

    # Starting month and year
    start_date = datetime.date(2020, 3, 1)

    # End month and year
    end_date = datetime.date.today().replace(day=1)
    end_date = end_date.replace(month=end_date.month + 1) if end_date.month != 12 \
        else end_date.replace(year=end_date.year + 1, month=1)
    current_date = start_date
    while current_date <= end_date:
        # Construct the URL based on the current month and year
        links.append(f"https://kprofiles.com/{current_date.strftime('%B').lower() }" + \
                     f"-{current_date.year}-comebacks-debuts-releases/")

        # Move to the next month
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)

    return links

def check_link_extensions(link, comeback_compilation):
    '''Check if the link is valid
    
    link: the link to check
    comeback_compilation: the text of the kprofiles comeback compilation page
    
    Returns: the link if it is valid, None if it is not'''
    if link in comeback_compilation:
        return link
    link_base = link.copy()
    if link.replace("-debuts-releases", "") in comeback_compilation:
        link = link.replace("-debuts-releases", "")
    elif link.replace("-comebacks-debuts-releases", "") in comeback_compilation:
        link = link.replace("-comebacks-debuts-releases", "")
    elif link.replace("-comebacks-debuts-releases", "-kpop") in comeback_compilation:
        link = link.replace("-comebacks-debuts-releases", "-kpop")
    elif link[:-1] + "-2/" in comeback_compilation:
        link = link[:-1] + "-2/" # WHY IS OCTOBER 2020 THE ONLY MONTH WITH A -2
    elif link.replace("-comebacks-debuts-releases",
                      "-kpop-comebacks-debuts-releases") in comeback_compilation:
        link = link.replace("-comebacks-debuts-releases", "-kpop-comebacks-debuts-releases")
    elif link.replace("-comebacks-debuts-releases", "-kpop-comebacks") in comeback_compilation:
        link = link.replace("-comebacks-debuts-releases", "-kpop-comebacks")
    if link != link_base:
        return link
    print("Link not found: " + link)


def filter_valid_links(links):
    '''Filter out invalid links
    
    links: the list of links to filter
    
    Returns: a list of valid links'''
    valid_links = []
    compilation_link = "https://kprofiles.com/comebacks/page/"
    comeback_compilation = ""
    for i in range(1, 100):
        request = requests.get(compilation_link + str(i))
        if request.status_code == 200:
            comeback_compilation += request.text
        else:
            break

    for link in links:
        is_valid = check_link_extensions(link, comeback_compilation)
        if is_valid:
            valid_links.append(is_valid)

    return valid_links

def fetch_site(link):
    '''Fetch the site from the given link

    link: the link to fetch

    Returns: the text of the site'''
    #check if file already exists
    if os.path.isfile(WORKING_DIR + "/kprofiles/" + link.split("/")[-2] + ".html") \
        and not FORCE_REFRESH:
        # read from file
        with open(WORKING_DIR + "/kprofiles/" + link.split("/")[-2] + ".html", "r") as file:
            return file.read()
    request = requests.get(link)
    if request.status_code == 200:
        # save to file
        with open(WORKING_DIR + "/kprofiles/" + link.split("/")[-2] + ".html", "w") as file:
            file.write(request.text)
        return request.text

def fetch_handler(links):
    '''Fetch the sites from the given links

    links: the links to fetch

    Returns: a list of the text of the sites'''
    data = []
    progress_bar = top_lib.Progressbar(total=len(links))
    progress_bar.print(0)
    try:
        os.makedirs(WORKING_DIR + "/kprofiles/", exist_ok=True)
    except OSError:
        print(f"Creation of the directory {WORKING_DIR}/kprofiles/ failed.")
        sys.exit(1)
    for link in links:
        data.append(fetch_site(link))
        progress_bar.print(links.index(link) + 1)
    return data


if __name__ == '__main__':
    # launch args
    FORCE_REFRESH = "-f" in sys.argv

    print("Fetching kprofiles.com... (This may take a while, kprofiles is slow...)")
    links = get_links()
    valid_links = filter_valid_links(links)
    data = fetch_handler(valid_links)
