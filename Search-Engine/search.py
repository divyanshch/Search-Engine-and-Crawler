import sys

from whoosh import highlight
from whoosh import qparser
from whoosh.index import open_dir
from whoosh.scoring import TF_IDF, BM25F

search_input = sys.argv[1]
search_type = sys.argv[2]
operation_type = sys.argv[3]

if search_input.endswith(","):
    search_input = search_input[:-1]
if search_type.endswith(","):
    search_type = search_type[:-1]
if(operation_type =="AND"):
    op_type = qparser.AndGroup
elif(operation_type=="OR"):
    op_type = qparser.OrGroup
else:
    op_type = qparser.AndGroup

dirname = "indexdir"
ix = open_dir(dirname)
qp = qparser.MultifieldParser(['content', 'path', 'title', 'head1', 'head2', 'head3', 'head4'], ix.schema,
                              group=op_type)
qp.add_plugin(qparser.PlusMinusPlugin)
query = qp.parse(search_input)
# print(query)
if search_type == "BM25":
    w = BM25F(B=0.75, K1=1.5)
elif search_type == "TFIDF":
    w = TF_IDF()
else:
    w = BM25F(B=0.75, K1=1.5,)
with ix.searcher(weighting=w) as searcher:
    results = searcher.search(query, terms=True)
    results.fragmenter = highlight.ContextFragmenter(maxchars=50, surround=50, )
    # print(list(searcher.lexicon("content")))
    found_doc_num = results.scored_length()
    run_time = results.runtime
#  -------------------------------for html use---------------------------------
    if found_doc_num == 0:
        final_top_output = "<h1> Sorry " + str(found_doc_num) + " Search Results Found.</h1>" \
            "<h5>Search Results for "+search_input+" using "+search_type+" (" + str(run_time) + " seconds)</h5><br>"

    else:
        final_top_output = "<h1> Top " + str(found_doc_num) + " Search Results </h1>" \
            "<h5>Search Results for "+search_input+" using "+search_type +" Ranking and "+ operation_type+\
                           " operation to score (" + str(run_time) + " seconds)</h5><br>"
    print(final_top_output)
    if results:
        for hit in results:
            snip = "<p>" + hit.highlights('content', top=2) + "</p>"
            path = hit['path']
            title = "<h4><a href=\"" + path + "\">" + hit['title'] + "</a></h4>"
            path = "<a href=\"" + path + "\">" + path + "</a>"
            score = hit.score
            score = "<p>" + path + "&nbsp &nbsp &nbsp(Score: " + str(score) + ")</p>"
            print(title, score, '\n', snip, "<br>")

#------------------------------for non html use-------------------------------------------------------------
    # if found_doc_num == 0:
    #     final_top_output = "Sorry " + str(found_doc_num) + " Search Results Found." \
    #         "Search Results for "+search_input+" using "+search_type+" (" + str(run_time) + " seconds)\n"
    #
    # else:
    #     final_top_output = "Top " + str(found_doc_num) + " Search Results" \
    #         "Search Results for "+search_input+" using "+search_type +" Ranking and "+ operation_type+\
    #                        " operation to score (" + str(run_time) + " seconds)"
    # print(final_top_output)
    # if results:
    #     for hit in results:
    #         snip = hit.highlights('content', top=2)
    #         path = hit['path']
    #         title = hit['title']
    #         score = hit.score
    #         score = path + "   (Score: " + str(score) + ")"
    #         print(str(title.encode('utf-8')), '\n', str(score.encode('utf-8')), '\n', snip, "\n")
            # print(list(searcher.lexicon("path")))

