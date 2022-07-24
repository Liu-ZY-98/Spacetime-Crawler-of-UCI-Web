import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

crawledURLs = set()

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation requred.
    links = []
    crawled = False
    content = []


    urlListFile = open('URLlistfile.txt', 'a')
    urlContentFile = open('URLcontentfile.txt', 'a')
    urlContentNumFile = open('URLcontentNumfile.txt', 'a')
    relatedURLFile = open('nextURLfile.txt', 'a')

    checkURL = url
    if url[-1] == '/':
        checkURL = url[:-1]
    if checkURL in crawledURLs:
        crawled = True
    elif checkURL not in crawledURLs:
        crawledURLs.add(checkURL)

    # from the reference website, the status between 200 and 202 are good for crawling.
    if crawled == False and is_valid(url) and resp.status >= 200 and resp.status <= 202:
        urlListFile.write(url + '\n')

        html_doc = resp.raw_response.content
        soup = BeautifulSoup(html_doc, 'html.parser')

        text = soup.get_text().split()
        for word in text:
            if word.isalnum():
                content.append(word)
        urlContentFile.write(url + '\n' + str(content) + '\n')
        urlContentNumFile.write(url + '\n' + str(len(content)) + '\n')
        for link in soup.find_all('a'):
            urlLink = link.get('href')
            links.append(urlLink)
            relatedURLFile.write(str(urlLink) + '\n')
    urlListFile.close()
    urlContentFile.close()
    urlContentNumFile.close()
    relatedURLFile.close()

    return links



def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False

        netloc = parsed.netloc

        if netloc == 'wics.ics.uci.edu' and '/events' in parsed.path:
            return False

        netlocList = netloc.split('.')
        if len(netlocList) >= 4:
            netloc = '.'.join(netlocList[1:])

        if (netloc not in ['ics.uci.edu', 'cs.uci.edu', 'informatics.uci.edu', 'stat.uci.edu']) and \
                (netloc != 'today.uci.edu' or '/department/information_computer_sciences/' in parsed.path):
            return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise