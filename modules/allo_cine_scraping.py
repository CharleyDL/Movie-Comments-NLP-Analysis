#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Tuesday 20 Dec. 2022
# ==============================================================================
# Script Scrapping the Allocine website (Movie comment + note by viewers)
# then save it on dataframe + csv
# ==============================================================================


import pandas as pd
import requests

from bs4 import BeautifulSoup
from tqdm import tqdm




class Allo_Cine:
    """Class to scrap the Allocine website"""
    def __init__(self, movie_number:int, nb_pages:int) -> None:
        """
        Constructor Allo_Cine
        @Params:
            movie_number    - required  : int (number after 'fichefilm-' in the url)
            nb_page         - required  : int (number of commentary pages)
        """
        self.movie_number = movie_number
        self.nb_pages = nb_pages


    def get_all_pages(self) -> list:
        """
        Get all url page of comments
        @Params:
            movie_number    - required  : int (number after 'fichefilm-' in the url)
            nb_page         - required  : int (number of commentary pages)
        """

        urls = []
        page_number = 1

        for page in range(self.nb_pages):
            page = f"""https://www.allocine.fr/film/fichefilm-{self.movie_number}/critiques/spectateurs/?page={page_number}"""
            page_number += 1
            urls.append(page)

        return urls


    def scrape(self) -> bool:
        """
        Scrap the note and comment for each viewers
        @Params:
            movie_number    - required  : int (number after 'fichefilm-' in the url)
            nb_page         - required  : int (number of commentary pages)
        """

        #**** USER-AGENT HEADER ****#
        HEADER = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)\
                                  AppleWebKit/537.36 (KHTML, like Gecko)\
                                  Chrome/44.0.2403.157 Safari/537.36',
                   'Accept-Language': 'fr-FR'
                  })

        result_notes = []
        result_comments = []

        try:
            # Get all pages
            urls = Allo_Cine.get_all_pages(self)

            # Iterate for each url and show a progress bar(tqdm)
            for url in tqdm(urls):
                # Initiate the page with each url
                webpage = requests.get(url, headers=HEADER)
                soup = BeautifulSoup(webpage.content, "html.parser")

                # Get Review Card
                review_card = soup.find_all("div", class_='hred review-card cf')
                #print(len(review_card))

                # Iterate into review_card
                for review in review_card:
                    # Scrap the note and the comment
                    note = review.select('span.stareval-note')[0].text
                    comment = review.select('div.content-txt')[0].text

                    # Print to check the result
                    #print(note)
                    #print(comment)

                    # Save in a list for a csv backup
                    result_notes.append(note)
                    result_comments.append(comment)

            # Create the DataFrame to transform it on CSV
            viewers_critic_movies = pd.DataFrame({'Note': result_notes, 'Comment': result_comments})
            viewers_critic_movies.to_csv('../data/viewers_critic_movies.csv', mode='a', index=False, header=False)

            return True

        except AttributeError as e:
            print(f"Error 'class Allo_Cine - def scrape' : {e}")
            return False




# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
    movie_number = int(input("numéro du fichefilm (barre de recherche) : "))
    nb_pages = int(input("nombre de pages commentaires : "))

    movie_critic = Allo_Cine(movie_number, nb_pages)
    Allo_Cine.scrape(movie_critic)