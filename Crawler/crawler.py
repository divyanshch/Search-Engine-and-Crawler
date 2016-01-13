import requests
from bs4 import BeautifulSoup
import urllib.parse
import os.path
import sys

url = sys.argv[1]  # url to start from
iterate = int(sys.argv[2])
depth_to_go = int(sys.argv[3])  # depth to go for
directory = sys.argv[4]  # directory name
if not url.startswith("http"):
    url = "http://" + url



# max_pages is the number of pages to crawl

def trade_spider(max_pages):  # function(maximum number of pages to call variable)
    page = 1

    urls = [url]
    visited = [url]
    title_number = 0  # this is to make sure no two files are named the same way
    if not os.path.isdir(directory):  # check if the directory exists
        os.mkdir(directory)  # if it doesnt then make it
    os.chdir(directory)  # then change directory to that folder

    dsize = 0  # makes the amount of depth already crawled 0
    depth = [dsize]
    # this checks if pg < max pg, the depth is < depth_to_go, and that urls are still available
    while page <= max_pages and depth_to_go >= dsize and len(urls) > 0:
        try:
            try:
                source_code = requests.get(urls[0])  # variable = requests.get(url)
                html = source_code.text  # get source code of page
                soup = BeautifulSoup(html, 'html.parser')  # variable to call beautifulsoup(variable of the source code)
            except:
                print(urls[0])

            try:
                name = soup.title.string  # removes all the uncessary things from title
                name = name.replace("\n", "")
                name = name.replace("\r", "")
                name = name.replace("\t", "")
                name = name.replace("|", "")
                name = name.replace(":", "")
                name = name.strip(' ')
            except:
                name = "no title " + str(title_number)  # if not title provided give a no title with number title
                title_number += 1

            num = 1
            name = "{0}.txt".format(name)  # adds the .txt to the end of the name
            try:
                if not os.path.isfile(name):  # if the file doesn't exist makes it
                    fo = open(name, "w")

                    fo.write('<page_url href=\"' + urls[0] + '\"></page_url>\n' + html)
                    fo.close()

                    size = os.stat(name)
                    size = size.st_size

                    if size2 == 0:
                        os.remove(name)
                else:  # if it does exists checks if it's the same file
                    new_name = name[:name.find(".")]
                    new_name = str(num) + ".txt"
                    fo = open(new_name, "w")
                    fo.write(html)
                    fo.close()

                    size = os.stat(name)
                    size = size.st_size

                    size2 = os.stat(new_name)
                    size2 = size2.st_size

                    if size == size2:
                        os.remove(new_name)
                    if size2 == 0:
                        os.remove(new_name)
                print(urls[0])
                for link in soup.findAll('a', href=True):
                    link['href'] = urllib.parse.urljoin(urls[0], link['href'])
                    if link['href'] not in visited:  # if the link is not in visited then it appends it to urls and visited
                        if '.pdf' not in link['href'] and '.jpg' not in link['href']:#makes sure no jpg or pdfs pass
                            urls.append(link['href'])
                            visited.append(link['href'])
            except:
                print("Can not encode file: " + urls[0])
        except:
            print("Error: Encoding")

        print("depth:", dsize)
        print("iterations:", page, "pages")
        urls.pop(0)

        if page >= depth[dsize]:
            depth.append(len(visited))
            dsize += 1

        page += 1
        # prints the amount of data collected in GB
        size_of_directory = get_tree_size(os.curdir) / 1000000000
        print(round(size_of_directory, 5), "GB")
        print('\n')



def get_tree_size(path):
    """Return total size of files in given path and subdirs."""
    total = 0
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            total += get_tree_size(entry.path)
        else:
            total += entry.stat(follow_symlinks=False).st_size
    return total


trade_spider(iterate)
