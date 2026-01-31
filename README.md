# Restaurant Review Scraper and Analyzer

This project scrapes restaurant reviews from OpenTable, analyzes the reviews using AI, and provides visual insights and competitor comparisons. It includes data collection via Selenium, AI-based review categorization using Anthropic Claude, and interactive visualization via a Flask web app.

## Features

### Scraping Restaurant Reviews
- Uses Selenium to scrape restaurant reviews from OpenTable.
- Collects:
  - Reviewer name, city, total reviews
  - Review content
  - Ratings: overall, food, service, ambience
  - Review date
- Automatically handles pagination to scrape multiple pages.

### AI-based Review Analysis
- Processes scraped reviews with Anthropic Claude API.
- Extracts and categorizes:
  - Food-related comments (taste, presentation, quality, etc.)
  - Staff-related comments (speed, politeness, professionalism, etc.)
- Stores results in a structured JSON format.

### Data Visualization
- Uses pandas and matplotlib to visualize review trends over time.
- Compares competitor restaurants by overall rating trends.
- Generates line charts showing performance comparison.

### Interactive Web Dashboard
- Built using Flask.
- Displays reviews with food and staff analysis.
- Supports search/filter by keywords in food or staff comments.
- Includes competitor analysis module to visualize rating trends.

## Installation

Clone the repository:

```bash
git clone https://github.com/shireenfatimakhilji/restaurant-review-analyzer.git
cd restaurant-review-analyzer
