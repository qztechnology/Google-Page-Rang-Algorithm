import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 5 #10000 TODO: set 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    
    #------------ TEST AREA -------------#
    #page = "2.html"
    #print(transition_model(corpus, page, DAMPING))
    #------------- END TEST AREA -------------#
    
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
        

def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    n_pages = len(corpus)
    n_page_links = len(corpus[page])
    
    # Transition model function
    _transition_model = dict()
    
    # Random page probability
    p_random_page = (1 - damping_factor)/n_pages
    _transition_model[page] = round(p_random_page, 4)
    
    # Random link probability
    p_random_link = round(damping_factor / n_page_links, 4)
    
    # Check the probability based on the current page
    for p in corpus:
        if p not in corpus[page]:
            _transition_model[p] = p_random_page
        elif p == page:
            _transition_model[p] = p_random_page
        else:
            _transition_model[p] = p_random_link + p_random_page
            
    return _transition_model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    # Ensure n is at least 1
    if n < 1:
        n = 1
        
    page_counter = {}
    tm_1 = 0
    next_page = ""
    pr = 0
    
    n_pages = len(corpus)
            
    counter = 1
    while counter <= n:
        
        # The first page is random
        if counter == 1:
            # Choose the first page
            page = random.choice(list(corpus.keys()))
            page_counter.setdefault(page, 1)
            print(f"First random page: {page}")
            tm_1 = transition_model(corpus, page, damping_factor)
            
            # Get the new page based on the PR's
            pages = list(tm_1.keys())
            values = list(tm_1.values())
            next_page = random.choices(pages, weights=values, k=1)[0]
            print(f"tm_1: {tm_1}")
            
            page_counter.setdefault(next_page, 1)
        
            print(f"page_counter 1: {page_counter}")
        
        else:
            if counter >= 2:
                tm = transition_model(corpus, next_page, damping_factor)
                
                # Get the new page based on the new PR's
                pages = list(tm.keys())
                values = list(tm.values())
                next_page = random.choices(pages, weights=values, k=1)[0]
                print(f"next_page: {next_page}")
                print(f"tm: {tm}")
                page_counter.setdefault(next_page)
                
                # Increase page counter
                if page_counter[next_page] == None:
                    cnt = 1
                else:
                    cnt = page_counter[next_page]
                    cnt += 1 
                
                page_counter[next_page] = cnt
                print(f"page counter: {page_counter}")
            
                    
        counter += 1
        
            
def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
