import datetime, requests, dotenv, os, sys
import top_lib

dotenv.load_dotenv()

WORKING_DIR = os.getenv('WORKING_DIR')


def getLinks():
    links = []

    # Starting month and year
    start_date = datetime.date(2020, 3, 1)

    # End month and year
    end_date = datetime.date.today().replace(day=1)
    end_date = end_date.replace(month=end_date.month + 1) if end_date.month != 12 else end_date.replace(year=end_date.year + 1, month=1)
    current_date = start_date
    while current_date <= end_date:
        # Construct the URL based on the current month and year
        links.append(f"https://kprofiles.com/{current_date.strftime('%B').lower()}-{current_date.year}-comebacks-debuts-releases/")
        
        # Move to the next month
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)
        
    return links

def checkLinkExtensions(link, comeback_compilation):
    if link in comeback_compilation:
        return link
    elif link.replace("-debuts-releases", "") in comeback_compilation:
        return link.replace("-debuts-releases", "")
    elif link.replace("-comebacks-debuts-releases", "") in comeback_compilation:
        return link.replace("-comebacks-debuts-releases", "")
    elif link.replace("-comebacks-debuts-releases", "-kpop") in comeback_compilation:
        return link.replace("-comebacks-debuts-releases", "-kpop")
    elif link[:-1] + "-2/" in comeback_compilation:
        return link[:-1] + "-2/" # WHY IS OCTOBER 2020 THE ONLY MONTH WITH A -2
    elif link.replace("-comebacks-debuts-releases", "-kpop-comebacks-debuts-releases") in comeback_compilation:
        return link.replace("-comebacks-debuts-releases", "-kpop-comebacks-debuts-releases")
    elif link.replace("-comebacks-debuts-releases", "-kpop-comebacks") in comeback_compilation:
        return link.replace("-comebacks-debuts-releases", "-kpop-comebacks")
    print("Link not found: " + link)
    

def filterValidLinks(links):
    # valid_links = []
    # for link in links:
    #     if requests.get(link).status_code == 200:
    #         valid_links.append(link)
    #     else:
    #         print(requests.get(link).status_code)
    # return valid_links
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
        is_valid = checkLinkExtensions(link, comeback_compilation)
        if is_valid:
            valid_links.append(is_valid)
    
    return valid_links

def fetchSite(link):
    #check if file already exists
    if os.path.isfile(WORKING_DIR + "/kprofiles/" + link.split("/")[-2] + ".html") and not FORCE_REFRESH:
        # read from file
        with open(WORKING_DIR + "/kprofiles/" + link.split("/")[-2] + ".html", "r") as file:
            return file.read()
    request = requests.get(link)
    if request.status_code == 200:
        # save to file
        with open(WORKING_DIR + "/kprofiles/" + link.split("/")[-2] + ".html", "w") as file:
            file.write(request.text)
        return request.text

def fetchHandler(links):
    data = []
    bar = top_lib.Progressbar(total=len(links))
    bar.print(0)
    try:
        os.makedirs(WORKING_DIR + "/kprofiles/", exist_ok=True)
    except OSError:
        OSError("Creation of the directory %s failed" % WORKING_DIR + "/kprofiles/")
    for link in links:
        data.append(fetchSite(link))
        bar.print(links.index(link) + 1)
    return data

def stripText():
    pass


if __name__ == '__main__':
    # launch args
    FORCE_REFRESH = True if "-f" in sys.argv else False

    print("Fetching kprofiles.com... (This may take a while, kprofiles is slow...)")
    links = getLinks()
    valid_links = filterValidLinks(links)
    data = fetchHandler(valid_links)
