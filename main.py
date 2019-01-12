#!/usr/bin/env python

# The goal is to predict the rating of an application based on the following factors:
# - The keywords in the title (convert this to a numeric value of indicator of strength)
# - The keywords in the description (as above)
from future_builtins import map

from collections import Counter
from itertools import chain
import json
import nltk
import numpy
import string
import sys
import play_scraper

class ListingUtils(object):

    def __init__(self):

        return None

    def search_listings(self, query):
        """
        Search and return the application ID's of the apps that are returned
        for the given query.
        """
        applications = []

        # Make API request here and parse the id's here.
        query_result_json = play_scraper.search(query, page=1)

        for result in query_result_json:
            applications.append({
                'application_id': result['app_id'],
                'rating': float(result['score']),
                'title': result['title'],
                'summary': result['description']
            })

        return applications

    def fetch_listing(self, application_id, short_description):
        listing_data = play_scraper.details(application_id)
        # Fetch the listing and save the following: Title, Short Description,
        # Rating, Number of ratings, Description.
        listing_json = {
            'application_id': application_id,
            'title': listing_data['title'],
            'summary': short_description,
            'description': listing_data['description'],
            'editors_choice': listing_data['editors_choice'],
            'rating': float(listing_data['score']),
            'total_reviews': listing_data['reviews'],
            'histogram': listing_data['histogram'],
            'installs': listing_data['installs']
        }
    
        return listing_json

    def keywords(self, description):
        tokens = [token for token in nltk.word_tokenize(description)]
        # Remove punctuation
        stripped = [token.encode('utf8').lower().translate(None, string.punctuation) for token in tokens]
        words = [word for word in stripped if word.isalpha()]
        # Filter out stop words
        stop_words = set(nltk.corpus.stopwords.words('english'))

        words = [w for w in words if not w in stop_words]
    
        return Counter(words).most_common(10)

    def rating(self, app):

        app['histogram']
    
class ListingAnalysis(object):

    def __init__(self):
        self._listing_utils = ListingUtils()

        return None

    def query(self, query):

        # Here we want to map a listing to a value and a collection of keywords.
        # This data will then be analysed to suggested keywords which other apps
        # are using.
        listings = self._listing_utils.search_listings(query)

        print 'Listing size: ' + str(len(listings))

        # Lets filter out the listings which have a low rating -- these are not
        # useful. This hueristic can be adjusted to, for example, filter on
        # short descriptions.
        listings = [l for l in listings if l['rating'] >= 4.1]

        print 'Filtered listing size: ' + str(len(listings))

        # Now we want to query each of these listings and fetch their more
        # "full" details.
        listings = [self._listing_utils.fetch_listing(l['application_id'], l['summary']) for l in listings]

        print 'Finding keywords.'

        for listing in listings:
            listing['title_keywords'] = self._listing_utils.keywords(listing['title'])
            listing['description_keywords'] = self._listing_utils.keywords(listing['description'])

        print 'Assigning values.'

        # Compute average installs so we can normalize -- +1 if above or equal,
        # -1 if below.
        total_histogram = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for listing in listings:
            for key in listing['histogram'].keys():
                if total_histogram.has_key(key):
                    total_histogram[key] += listing['histogram'][key]

        total_ratings = sum(total_histogram.values())
        average_rating = numpy.dot(total_histogram.keys(), total_histogram.values()) / total_ratings

        print 'Average rating is', average_rating

        return None

    def assign_value(self, listings):

        return None


if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print 'Invalid args -- Try \'./main.py "Facebook"\''
        exit()

    ListingAnalysis().query(sys.argv[1])