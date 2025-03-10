"""Functions for scraping and sentiment analysis"""

import requests

def scrape_amazon(url):
    """Scrape reviews from Amazon"""
    return ["Amazon review 1", "Amazon review 2"]

def scrape_flipkart(url):
    """Scrape reviews from Flipkart"""
    return ["Flipkart review 1", "Flipkart review 2"]

def scrape_myntra(url):
    """Scrape reviews from Myntra"""
    return ["Myntra review 1", "Myntra review 2"]

def analyze_sentiment(reviews):
    """Perform sentiment analysis"""
    return {"positive": 70, "negative": 30, "summary": "Mostly positive reviews"}
