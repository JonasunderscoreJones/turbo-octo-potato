import dotenv, os, re, datetime
import html as html_lib

dotenv.load_dotenv()

# Load the environment variables
WORKING_DIR = os.getenv('WORKING_DIR')

# Read file .working/kprofiles/march-2020-comebacks-debuts-releases.html
with open(os.path.join(WORKING_DIR, "kprofiles", "march-2020-comebacks-debuts-releases.html"), "r") as f:
    html = f.read()

def stripText(html, date:datetime.date=None):
    # remove the script and style sections
    script_pattern = re.compile('<script.*?</script>', re.DOTALL)
    style_pattern = re.compile('<style.*?</style>', re.DOTALL)
    text = re.sub(script_pattern, "", html)
    text = re.sub(style_pattern, "", text)
    text = html_lib.unescape(text)
    if html.startswith("<!DOCTYPE html>"):
        return text
    lines = text.split("•")

    if date:
        result = []
    else:
        result = ""

    for line in lines:
        print(line)
        print(lines)
        line = line.replace("<strong>", "").replace("</strong>", "").replace("<span>", "").replace("</span>", "").replace("<br/>", "")
        if "[Comeback]" in line:
            line = line.split("[Comeback]")[0] + "[Comeback]"
        elif "[Debut]" in line:
            line = line.split("[Debut]")[0] + "[Debut]"
        elif "[Release]" in line:
            line = line.split("[Release]")[0] + "[Release]"
        elif "[Solo Debut]" in line:
            line = line.split("[Solo Debut]")[0] + "[Debut]"
        elif "[Solo Release]" in line:
            line = line.split("[Solo Release]")[0] + "[Release]"
        elif "[Pre-Debut Release]" in line:
            line = line.split("[Pre-Debut Release]")[0] + "[Pre-Debut Release]"
        elif "[Pre-Single Release]" in line:
            line = line.split("[Pre-Single Release]")[0] + "[Pre-Debut Release]"
        elif "[Japanese Comeback]" in line:
            line = line.split("[Japanese Comeback]")[0] + "[Japanese Comeback]"
        elif "[Japanese Debut]" in line:
            line = line.split("[Japanese Debut]")[0] + "[Japanese Debut]"
        elif "[Project Release]" in line:
            line = line.split("[Project Release]")[0] + "[Release]"
        elif "[Pre-Release Single]" in line:
            line = line.split("[Pre-Release Single]")[0] + "[Pre-Release]"
        elif "[Comeback Single]" in line:
            line = line.split("[Comeback Single]")[0] + "[Comeback]"
        elif "[Collab Release]" in line:
            line = line.split("[Collab Release]")[0] + "[Release]"
        elif "[Comeback Full Album]" in line:
            line = line.split("[Comeback Full Album]")[0] + "[Comeback]"
        elif "[Special Release]" in line:
            line = line.split("[Special Release]")[0] + "[Release]"
        elif "[Collab]" in line:
            line = line.split("[Collab]")[0] + "[Release]"
        elif "[Mixtape]" in line:
            line = line.split("[Mixtape]")[0] + "[Mixtape]"
        elif "[Japan Release]" in line:
            line = line.split("[Japan Release]")[0] + "[Japanese Release]"
        elif "[Single Release]" in line:
            line = line.split("[Single Release]")[0] + "[Release]"
        line = line.replace("\n", "").replace("&#8216;", "").replace("&#8217;", "")
        if date and not line == "" and not line == " ":
            print(line)
            artist_title = line.split("[")[0].strip()
            artist = artist_title.split("|")[0].strip()
            title = artist_title.split("|")[1].strip().replace("‘", "").replace("’", "")
            release_type = line.split("[")[1].split("]")[0].strip()
            line = (str(date), artist, title, release_type)
            result.append(line)
            for i in ["\n", " ", ""]:
                try:
                    result.remove(i)
                except ValueError:
                    pass
        else:
            result += line + "\n"
    return result

def formatDate(date:datetime.date):
    formatted_date = "{} {}".format(date.strftime("%B"), date.day)
    if 10 <= date.day % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(date.day % 10, 'th')
    formatted_date += suffix
    return formatted_date

def extract_between_strings(main_string, string1, string2):
    start_index = main_string.find(string1)
    end_index = main_string.find(string2)
    
    # Check if both strings are found in the main string
    if start_index != -1 and end_index != -1:
        # Extract the characters between string1 and string2
        extracted_text = main_string[start_index + len(string1):end_index]
        return extracted_text
    else:
        # If either string1 or string2 is not found, return None or an empty string
        return None

def increaseDateDay(date:datetime.date):
    return date + datetime.timedelta(days=1)


def do_dates(html, date:datetime.date):
    result = []
    this_date = formatDate(date)
    this_string = None
    this_this_date = None
    for i in range(0, 46):
        this_date = formatDate(date)
        date = increaseDateDay(date)
        date_str = formatDate(date)
        extract = extract_between_strings(html, this_date, date_str)
        if this_string:
            extract = extract_between_strings(html, this_string, date_str)
        if not extract:
                this_string = this_date
                this_this_date = date
                continue
        this_string = None
        #print("---------------------------------------------------")
        #print(this_date)
        this_this_date = date if this_this_date == None else this_this_date
        result += stripText(extract, this_this_date)
        this_this_date = None
    return result

result = do_dates(stripText(html), datetime.date(2020, 2, 15))
for i in result:
    print(i)
print(len(result))

#save output to file .working/kprofiles/march-2020-comebacks-debuts-releases.txt
with open(os.path.join(WORKING_DIR, "kprofiles", "may-2020-comebacks-debuts-releases.txt"), "w") as f:
    f.write(stripText(html))
