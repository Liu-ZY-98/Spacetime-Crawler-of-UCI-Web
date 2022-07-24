import operator
from urllib.parse import urlparse

def uniquePage(URLlist):
    solution = open('Solution.txt', 'a')
    solution.write('1. ')
    unique = set()
    for url in URLlist:
        unique.add(url)
    solution.write('The number of unique pages is ' + str(len(unique)) + '\n')
    solution.close()

def longestPage(URLcontentNumList):
    solution = open('Solution.txt', 'a')
    solution.write('2. ')

    longest = 0
    longest_page = ''

    for length in range(1, len(URLcontentNumList), 2):
        if int(URLcontentNumList[length]) > longest:
            longest = int(URLcontentNumList[length])
            longest_page = URLcontentNumList[length - 1]

    solution.write('The longest page is ' + longest_page + 'with ' + str(longest) + ' words.' + '\n')
    solution.close()


def commonWords(URLcontentList):
    stopwords = []
    stopwordsFile = open('stopwords.txt', 'r')
    for line in stopwordsFile:
        stopwords.append(line.rstrip())
    stopwordsFile.close()

    solution = open('Solution.txt', 'a')
    solution.write('3. The 50 most common words are: \n')

    wordNumDict = dict()
    for URLcontents in URLcontentList[1::2]:
        contents = URLcontents.split(',')
        for content in contents:
            word = content.lower().strip().replace("'", '')
            if word in stopwords:
                continue
            if word in wordNumDict:
                wordNumDict[word] += 1
            else:
                wordNumDict[word] = 1

    mostCommonList = []
    for num in range(0,50):
        mostCommon = max(wordNumDict.items(), key = operator.itemgetter(1))[0]
        mostCommonList.append(mostCommon)
        wordNumDict[mostCommon] = 0
    for word in mostCommonList:
        solution.write(word + '\n')
    solution.close()


def subdomain(URLlist):
    solution = open('Solution.txt', 'a')
    solution.write('4. \n')
    subdomainDict = dict()
    for url in URLlist:
        parsed = urlparse(url)
        netloc = parsed.netloc
        netlocList = netloc.split('.')
        subdomain = ''
        if len(netlocList) >= 4:
            subdomain = '.'.join(netlocList[1:])
        if subdomain == 'ics.uci.edu':
            if netloc in subdomainDict:
                subdomainDict[netloc] += 1
            else:
                subdomainDict[netloc] = 1

    solution.write('Subdomain num = ' + str(len(subdomainDict)) + '\n')
    for key, value in subdomainDict.items():
        solution.write(key + ' ' + str(value) + '\n')
    solution.close()

if __name__ == '__main__':
    urlListFile = open('URLlistfile.txt', 'r')
    urlContentFile = open('URLcontentfile.txt', 'r')
    urlContentNumFile = open('URLcontentNumfile.txt', 'r')

    URLlist = []
    URLcontentList = []
    URLcontentNumList = []

    for line in urlListFile:
        URLlist.append(line)

    for line in urlContentFile:
        URLcontentList.append(line)

    for line in urlContentNumFile:
        URLcontentNumList.append(line)

    uniquePage(URLlist)
    longestPage(URLcontentNumList)
    commonWords(URLcontentList)
    subdomain(URLlist)

    urlListFile.close()
    urlContentFile.close()
    urlContentNumFile.close()