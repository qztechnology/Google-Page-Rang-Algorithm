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
    
    for page in corpus.keys():
        page_counter.update({page: 0})
        
    for page in corpus.keys():
        page_rank.update({page: 0})
       
    # Sampling cycle     
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
            
            # Increase page counter
            page_counter[next_page] += 1
            
            # Calculate PR
            pr = page_counter[next_page] / n
            new_record = {next_page: pr} #TODO: check why i cannot put directly the key:value in the dictionary
            page_rank.update(new_record)

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
    links = {}
    pr = {}
    n_pages = len(corpus)
    first_cycle = 0
    
    initial_page_rank = 1 / n_pages
    pr_random_page = (1 - damping_factor) / n_pages #TODO: check this: (damping_factor/n_pages)
    
    for page in corpus:
        pr.update({page: initial_page_rank})
        
    # Pages iterations
    exit_range = float('inf')
    
    while exit_range > 0.001: 

        for page in corpus:
            n_links = len(corpus[page])
            page_links = {page: n_links}
            links.update(page_links)
            page_rank_previous = 0
            page_rank = 0
            pr_i = initial_page_rank
            sum_links = 0 # PR(i) / NumLinks(i)

            # PR(i) calculation
            for i in corpus[page]:
                print(f'page: {page} - link to {page}: {len(corpus[page])} - i: {i} - links of "i": {corpus[i]} - NumLinks(i): {len(corpus[i])}') 
                num_links_i = len(corpus[i])


                
                if num_links_i == 0:
                    if first_cycle == 0:
                        sum_links += initial_page_rank / n_pages
                        first_cycle += 1
                    else:
                        sum_links += pr[i] / n_pages
                elif num_links_i > 0:
                    if first_cycle == 0:
                        sum_links += initial_page_rank / num_links_i
                        first_cycle += 1
                    else:
                        sum_links += pr_i / num_links_i
                        
            # Get PageRank for a specific page and pages that links to it
            page_rank += pr_random_page + damping_factor * sum_links
            
            # Store PageRank for each page
            pr.update({page: page_rank})
            
            # Exit conditions 
            exit_range = abs(page_rank_previous - page_rank)
            page_rank_previous = page_rank

            print(f'pr: {pr}')

    return pr
    
    


if __name__ == "__main__":
    main()
