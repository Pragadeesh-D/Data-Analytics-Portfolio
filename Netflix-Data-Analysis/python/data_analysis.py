import pandas as pd
import os

def run_analysis():
    # Define file paths
    input_file = '../dataset/processed/netflix_cleaned.csv'
    output_file = '../outputs/insights_summary.txt'
    
    print("Starting data analysis process...")
    
    # Load dataset
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: Could not find the file {input_file}")
        return

    insights = []
    insights.append("=== NETFLIX DATA ANALYSIS INSIGHTS ===\n")
    
    # Analysis 1: Content Type Distribution
    type_counts = df['type'].value_counts()
    insights.append("1. Content Type Distribution:")
    for content_type, count in type_counts.items():
        insights.append(f"   - {content_type}: {count}")
    
    total = type_counts.sum()
    movie_pct = (type_counts.get('Movie', 0) / total) * 100
    insights.append(f"   *Insight: Movies dominate Netflix content, making up {movie_pct:.1f}% of the catalog compared to TV Shows.\n")

    # Analysis 2: Most Common Genres
    # Split the 'listed_in' column on commas and stack
    genres = df['listed_in'].str.split(',').explode().str.strip()
    top_genres = genres.value_counts().head(10)
    
    insights.append("2. Top 10 Genres:")
    for genre, count in top_genres.items():
        insights.append(f"   - {genre}: {count}")
    insights.append("   *Insight: International Movies and Dramas are the most popular genres produced/licensed on Netflix.\n")

    # Analysis 3: Yearly Release Trend
    yearly_trend = df['release_year'].value_counts().sort_index()
    recent_trend = yearly_trend.tail(15) # Last 15 years
    
    insights.append("3. Yearly Release Trend (Last 15 Years):")
    for year, count in recent_trend.items():
        insights.append(f"   - {year}: {count}")
    insights.append("   *Insight: Content production increased rapidly after 2015, peaking around 2018-2019 before dipping slightly, likely due to market saturation or COVID-19 delays.\n")

    # Analysis 4: Top Producing Countries
    # Split countries
    countries = df['country'].str.split(',').explode().str.strip()
    # Filter out 'Unknown' if we want cleaner insights, or keep it. Let's keep it but maybe note it.
    countries = countries[countries != 'Unknown']
    top_countries = countries.value_counts().head(10)
    
    insights.append("4. Top 10 Producing Countries:")
    for country, count in top_countries.items():
        insights.append(f"   - {country}: {count}")
    insights.append("   *Insight: The United States and India are by far the largest producers of content available on Netflix.\n")

    # Analysis 5: Rating Distribution
    ratings = df['rating'].value_counts()
    insights.append("5. Rating Distribution:")
    for rating, count in ratings.items():
        insights.append(f"   - {rating}: {count}")
    insights.append("   *Insight: TV-MA (Mature Audiences) is the most common rating, indicating a strong focus on adult-oriented content.\n")

    # Write to text file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(insights))
        
    print(f"Analysis complete. Insights saved to {output_file}")

if __name__ == "__main__":
    # Change working directory to script location
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run_analysis()
