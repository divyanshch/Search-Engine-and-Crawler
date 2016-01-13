# Search-Engine-and-Crawler
Python based search engine and crawler. Search engine uses Whoosh and the crawler uses Beautiful-soup 
##Crawler
#####- Overview:

>This program takes in a particular seed and scans that webpage for any links. 
It then appends those links onto a queue and continues to pop and append until one of the given parameters is reached. 
The main parameters are number of pages to be crawled, and the depth of the pages to crawl. 
With a little additional code, another parameter may be added to get certain amount of data. 

>The duplication of urls is handled by a loop that checks if the URL is already present in the previously visited queue. 
If it is not then the both the urls list and the visited list gets the new URL appended to them. 

>To check for duplication of the material on the site even more the sites are organized by titles. 
If the title is the same then the program checks if the two files have the same size/amount of data, if they do the file is left alone. 
If they are different, the new file gets the title and an increasing number attached to it as the title of the file. 
This organizes and keeps the duplicate material out of the program. 

>The program outputs the URL of the webpage it is crawling, the depth of the pages crawled, the number of pages crawled and the total size of the repository. 
With a little adjustment to the code, the total size of the repository can be used as a parameter to decide when to stop crawling.
The program displays this for every webpage crawled. 

#####- Architecture
>Architecturally the program goes starts with one URL, and puts it in a queue of URLS and visited. 
Then the program checks if the directory that the user has provided with exists, if it does not exist the program makes that directory and switches current directory to it. 
This is to place all the HTML documents in a text file to place into the proper directory.
The queue then takes that urls [0] and process the source code to use for the BeautifulSoup library. 
The BeautifulSoup library is there to make it easier to parse through HTML code. 
Then the program checks for all the ‘href’ tags and appends them to both the urls and visited lists while following the parameters.
In this case, the parameters can be increased to get a better result. 
To improve performance the program excluded addition of pdf and jpg files from the lists.
This allows the program to not look at the code, as the code is not encoded properly for windows.
While doing this the HTML code for each of the urls [0] is being inputted into a text file with the title of the URL.
If the title is not provided the title is replaced with “no title” followed by an appropriate number to keep identifications clear.

>To keep track of the depth, a list is used. The list contains the length of the visited urls. 
The idea of making this list is based on a binary search tree.
As one page is scanned all its links are on depth 1, and all the links picked up from scanning from depth 1 are on depth 2.
This led to the design of using the length of visited urls and pages visited to keep a count on the depth. 

>To start at depth 0 any links in the visited are going to belong to depth 1. 
Therefore, the size of that would be the amount of links that were collected from the first URL. 
This leads to the program knowing that depth 1 will be at the number of links are in the visited list. 
After the depth 1 is complete, the program gets the length again which now indicates the size of depth 2.
This is done continuously to update the amount of pages needed to be parsed in order to go through the depths.

