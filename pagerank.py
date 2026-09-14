import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000 #10000 TODO: set 10000


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
    tm = {}
    
    # Random page probability
    p_random_page = (1 - damping_factor) / n_pages
    tm[page] = p_random_page
    
    # Random link probability
    if n_page_links != 0: p_random_link = damping_factor / n_page_links
    
    # Check the probability based on the current page
    for p in corpus:
        if p not in corpus[page]:
            tm[p] = p_random_page
        elif p == page:
            tm[p] = p_random_page
        else:
            tm[p] = p_random_link + p_random_page
            
    return tm


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
        
    # Initializzations
    page_counter = {}
    tm = {}
    next_page = ""
    pr = 0
    page_rank = {}
    
    n_pages = len(corpus)
    
    for page in corpus.keys():
        page_counter.update({page: 0})
        
    for page in corpus.keys():
        page_rank.update({page: 0})
        
    print(f"page counter: {page_counter}")
            
    counter = 1
    while counter <= n:
        
        # The first page is random
        if counter == 1:
            
            # Choose the first page
            first_page = random.choice(list(corpus.keys()))
            page_counter[first_page] += 1

            tm = transition_model(corpus, first_page, damping_factor)
            
            # Get the next page based on the current transition model
            pages = list(tm.keys())
            values = list(tm.values())
            next_page = random.choices(pages, weights=values, k=1)[0]
      
        elif counter >= 2:
            
            tm = transition_model(corpus, next_page, damping_factor)
            
            # Get the new page based on the new PR's
            pages = list(tm.keys())
            values = list(tm.values())
            next_page = random.choices(pages, weights=values, k=1)[0]
            
            print(f"next_page: {next_page}")
            print(f"tm: {tm}")
            print(f"page counter 2: {page_counter}")
            
            # Increase page counter
            page_counter[next_page] += 1
            
            # Calculate PR
            pr = page_counter[next_page] / n
            new_record = {next_page: pr}
            page_rank.update(new_record)
            
            
            print(f"page counter: {page_counter}")
            print(f"new_record: {new_record}")
            print(f"page_rank: {page_rank}")
        else:
            raise ("Counter Error")
                      
        counter += 1
        
    return dict(sorted(page_rank.items()))
        
            
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
