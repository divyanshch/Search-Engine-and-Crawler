# Search-Engine-and-Crawler
Python based search engine and crawler. Search engine uses Whoosh and the crawler uses Beautiful-soup to process the information.
##Crawler
Use the crawler to gather html source code files starting with a certain seed. 
The html souce code is stored in a certain folder with the title of the website being the name of the file.

- The first paramater when running the program is the seed (the url you want to start to crawl from).
- Second the number of pages to crawl. 
- Third number of hops away from the original seed.
- Fourth the output directory name to store all the html source code.

##### Overview:

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

## Search engine
##### Overview:
>We used Whoosh, an open source Python library, to build our search engine. 
Whoosh provides full-indexing and searching library. 
It provides several indexing and searching functions that allow us to quickly learn and utilize. 
The main difference from Whoosh and Lucene is that Lucene is built in Java, but Whoosh is built in pure Python. 
The two systems provide similar functionalities. 

>Our search engine contains several different parts, indexing, and query parsing, and searching.
Before we start using Whoosh, we need to define the schema for the index that lists the fields in the index. 
In our schema, we index the entire field as a single unit. 
We also have stemming and using stop words in our index to eliminate useless, extra index and save time and memory space. 
However, to avoid accidently deleting important words, we separate the title and give the title more weight to emphasize the importance of it. 

>After we define our schema, we call the function create_in() from Whoosh to create our index. 
In our index, other than common fields such as title, we also the URL link of each of the documents parsed.
This is done by making adding a special tag when crawling to make the first line of the text file of the html contains the URL. 
In the end of indexing, we call the writer function to write the index into our database.
Before we call the writer functions, all index are free to be changed, but after writer function starts to commit, we are making our final step to finish indexing. 
This can be modified or improved to extend the indexing than start from scratch every time.

>With our index, we can do search by parsing the input query keywords and matching the keywords with our index.
In our search engine, we parse the query keywords by calling the QueryParser function from Whoosh. 
The QueryParser helps parsing the inputted keywords and allow us to pass everything into a searcher. 
The searcher would take in the parsed query and searching methods that we define. 

>In our search engine, we apply two different methods to the search algorithm. 
The first one is BM25, which we used as our default-searching algorithm. 
The reason we pick this is that BM25 returns better, more accurate results the most other algorithm. 
Through calculating the relation of each word between the query and the documents, we can find the most relevant results in a shorter time.
We also use TFIDF, term frequency over inverse document frequency, as our search algorithm. 
TFIDF is a basic searching algorithm that returns the results faster than other searching algorithm.
Even though the relevancy ranking of the result from TFIDF is not as accurate as BM25, it is faster.

>Another functionality that is included is the ability to give keywords in the query more or less weight.
Another added functionality is using keywords in search like AND or OR or NOT to further simplify the search. 
Also included is the option to choose simply which parsing function to use whether it be AND or OR. 
This is to give the user fast way to change inputs. 

>For the website, we write the base skeleton structure first in html. 
We first define the main searching box and result page. 
We then define the css to apply background image and design to our website and make it perfect. 
After we make our search box for the website, we change the html file to a php file in order to make a dynamic webpage.
The user input would be directly passed in to a conditional loop and call the Python file of the searcher.
When inputting the search query, the user can also select either BM25 or TFIDF as the searching method.
The default searching method will be BM25. When the searcher finishes searching through the index, it will send the top N results to the website and the website will then print out the top N results of the search and a snippet of each result on the same page. 
The N is calculated by the query program and displays the number of results the program was able to find, maxing out at 10.
Note the user input query and search type will appear on the hyperlink of the website so the user can double check. 

