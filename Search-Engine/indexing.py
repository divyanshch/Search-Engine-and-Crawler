import os
import os.path
import os.path

from bs4 import BeautifulSoup
from whoosh.fields import *
from whoosh.index import create_in
#
folder_to_index = sys.argv[1]

# folder_to_index = "test3"
dirname = "indexdir"

if not folder_to_index.startswith("/"):
    folder_to_index = "/" + folder_to_index

if not os.path.isdir(os.getcwd()+folder_to_index):
    print(folder_to_index[1:] + " does not exist.")
    exit(1)


schema = Schema(
    path=NGRAM(minsize=4, maxsize=11, stored=True, sortable=True),  # ID: indexes the entire field as a single unit
    title=TEXT(field_boost=2.0, stored=True, phrase=True, sortable=True),
    # False parsing gets term frequency, stemming is not allowed for titles and titles are boosted
    content=TEXT(analyzer=analysis.StemmingAnalyzer(), stored=True, phrase=True, sortable=True),
    head1=TEXT(field_boost=1.75, stored=False, phrase=True, sortable=True),
    head2=TEXT(field_boost=1.5, stored=False, phrase=True, sortable=True),
    head3=TEXT(field_boost=1.25, stored=False, phrase=True, sortable=True),
    head4=TEXT(field_boost=1.10, stored=False, phrase=True, sortable=True),
)

if not os.path.exists(dirname):
    os.mkdir(dirname)

ix = create_in(dirname, schema)
writer = ix.writer()
path = os.getcwd()
path += folder_to_index
number_indexed = 1
for filename in os.listdir(path):
    print_filename = str(filename.encode('utf-8'))
    if print_filename[0:2] == "b\'" and print_filename.endswith("\'"):
        print_filename = print_filename[2:-1]

    print("indexing: "+print_filename)
    print("indexed number: "+str(number_indexed))
    number_indexed += 1
    f = open(path + "\\" + filename, 'r')
    content = f.read()
    soup = BeautifulSoup(content, 'html.parser')  # variable to call beautifulsoup(variable of the source code)
    for script in soup.find_all('script'):
        script.extract()
    for style in soup.find_all('style'):
        style.extract()
    final_head1 = ""
    final_head2 = ""
    final_head3 = ""
    final_head4 = ""
    final_p_tag = ""
    for h in soup.find_all('h1'):
        final_head1 += h.text
    for h in soup.find_all('h2'):
        final_head2 += h.text
    for h in soup.find_all('h3'):
        final_head3 += h.text
    for h in soup.find_all('h4'):
        final_head4 += h.text
    for para in soup.find_all('p'):
        final_p_tag += para.text

    link = soup.find('page_url', href=True) #special page_url tag created to store the url of page
    try:
        writer.add_document(path=link['href'], title=filename[:-4], head1=final_head1, head2=final_head2,
                            head3=final_head3, head4=final_head4, content=final_p_tag,)
    except:
        writer.add_document(path=u'None', title=filename[:-4], head1=final_head1, head2=final_head2,
                            head3=final_head3, head4=final_head4, content=final_p_tag,)
print("Committing please wait...")
writer.commit()
print("Finished")



