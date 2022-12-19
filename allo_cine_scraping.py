#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Monday 19 Dec. 2022
# ==============================================================================
# Script Scrapping the Allociné website : Movie comments + note by viewers
# ==============================================================================

import mysql.connector as mysqlco
import pandas as pd
import requests

from bs4 import BeautifulSoup
from mysql.connector import Error


config = {
            "host" : "localhost",
            "user" : "root",
            "password" : "example",
            "auth_plugin" : "mysql_native_password",
            "port" : "3307",
            "database" : "allocine"
         }


#**** CLASS ****#
class Allo_Cine:
    """Class to scrap the Allocine website"""

    #**** USER-AGENT HEADER ****#
    HEADER = ({'User-Agent':
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
               'Accept-Language': 'fr-FR'
             })


    def get_all_pages() -> list:
        """Get all url page of comments"""
        urls = []
        page_number = 1

        for page in range(667):
            page = f"""https://www.allocine.fr/film/fichefilm-61282/critiques/spectateurs/?page={page_number}"""
            page_number += 1
            urls.append(page)

        return urls


    def scrape() -> bool:
        """Scrap the note and comment for each viewers"""

        #**** USER-AGENT HEADER ****#
        HEADER = ({'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Accept-Language': 'fr-FR'})

        result_notes = []
        result_comments = []

        try:
            # Open the connection to the database
            db = mysqlco.connect(**config)
            cursor = db.cursor()

            # Get all pages
            urls = Allo_Cine.get_all_pages()

            for url in urls:
                # Initiate the page with each url
                webpage = requests.get(url, headers=HEADER)
                soup = BeautifulSoup(webpage.content, "html.parser")

                # Get Review Card
                review_card = soup.find_all("div", class_='hred review-card cf')
                #print(len(review_card))

                # Iterate into review_card
                for review in review_card:
                    # Scrap the note
                    note = review.select('span.stareval-note')[0].text

                    # Scrap the comment
                    comment = review.select('div.content-txt')[0].text
                    comment = comment.replace('"', "'" ) # replace les "" par une single

                    # Print to check the result
                    #print(note)
                    #print(comment)

                    # Save in a list for a csv backup
                    result_notes.append(note)
                    result_comments.append(comment)

                    # Insert in the database
                    sql = f"""
                           INSERT INTO avatar (note_viewer, comment_viewer)
                           VALUES ("{note}", "{comment}")
                           ON DUPLICATE KEY UPDATE note_viewer = "{note}",
                                                comment_viewer = "{comment}";
                           """
                    cursor.execute(sql)
                    db.commit()

            avatar_viewers_df = pd.DataFrame({'Note': result_notes, 'Comment': result_comments})
            avatar_viewers_df.to_csv('avatar_viewers_df.csv')

            return True

        except AttributeError as e:
            print(f"Error 'class Allo_Cine - def scrape' : {e}")
            return False

        finally:
            if db.is_connected():
                db.close
                cursor.close()




# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
    Allo_Cine.scrape()