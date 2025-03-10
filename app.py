"""Flask Web App for Review Sentiment Analysis"""

print("Starting Flask app...")

import os
import flask
import requests
from flask import Flask, request, jsonify, render_template
from rq.job import Job
from redis_resc import redis_conn, redis_queue
from functions import scrape_amazon, scrape_flipkart, scrape_myntra, analyze_sentiment

app = Flask(__name__)

@app.route("/")
def home():
    """Render the homepage."""
    return render_template("index.html")

@app.route("/enqueue", methods=["POST"])
def enqueue():
    """Process URL and collect reviews from all three sites."""
    data = request.json
    product_url = data.get("url")

    if not product_url:
        return jsonify({"error": "No URL provided"}), 400

    # Enqueue jobs for all three retailers
    job_amazon = redis_queue.enqueue(scrape_amazon, product_url, job_timeout=500)
    job_flipkart = redis_queue.enqueue(scrape_flipkart, product_url, job_timeout=500)
    job_myntra = redis_queue.enqueue(scrape_myntra, product_url, job_timeout=500)

    return jsonify({"amazon_job_id": job_amazon.id, "flipkart_job_id": job_flipkart.id, "myntra_job_id": job_myntra.id})

@app.route("/results", methods=["GET"])
def get_results():
    """Fetch results for all three jobs and analyze sentiment."""
    job_ids = request.args.getlist("job_id")
    reviews = []

    for job_id in job_ids:
        job = Job.fetch(job_id, connection=redis_conn)
        if job.result:
            reviews.extend(job.result)

    # Perform sentiment analysis
    sentiment_summary = analyze_sentiment(reviews)

    return jsonify({"reviews": reviews, "summary": sentiment_summary})

if __name__ == "__main__":
    print("Running Flask server...")
    app.run(debug=True)
