import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_visualizations():
    input_file = '../dataset/processed/netflix_cleaned.csv'
    visuals_dir = '../visuals/'
    
    print("Starting visualization process...")
    
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}")
        return

    # Set professional style
    sns.set_theme(style="darkgrid")
    plt.rcParams.update({'figure.figsize': (10, 6), 'font.size': 12})
    
    # 1. Content Type Distribution (Countplot)
    plt.figure()
    ax = sns.countplot(data=df, x='type', palette='Set2')
    plt.title('Content Type Distribution on Netflix', fontsize=16, fontweight='bold')
    plt.xlabel('Content Type', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.0f'), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha = 'center', va = 'center', 
                    xytext = (0, 9), 
                    textcoords = 'offset points')
    plt.tight_layout()
    plt.savefig(os.path.join(visuals_dir, 'content_type_distribution.png'), dpi=300)
    plt.close()

    # 2. Top Genres (Bar Plot)
    plt.figure(figsize=(12, 6))
    genres = df['listed_in'].str.split(',').explode().str.strip()
    top_genres = genres.value_counts().head(10)
    sns.barplot(y=top_genres.index, x=top_genres.values, palette='viridis')
    plt.title('Top 10 Most Common Genres on Netflix', fontsize=16, fontweight='bold')
    plt.xlabel('Count', fontsize=12)
    plt.ylabel('Genre', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(visuals_dir, 'top_genres.png'), dpi=300)
    plt.close()

    # 3. Yearly Release Trend (Line Plot)
    plt.figure(figsize=(12, 6))
    yearly_trend = df['release_year'].value_counts().sort_index()
    # Let's focus on 2000 onwards for a cleaner trend
    recent_trend = yearly_trend[yearly_trend.index >= 2000]
    sns.lineplot(x=recent_trend.index, y=recent_trend.values, marker='o', color='crimson', linewidth=2)
    plt.title('Netflix Content Release Trend (2000 - Present)', fontsize=16, fontweight='bold')
    plt.xlabel('Release Year', fontsize=12)
    plt.ylabel('Number of Titles', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(visuals_dir, 'yearly_release_trend.png'), dpi=300)
    plt.close()

    # 4. Top Countries (Bar Plot)
    plt.figure(figsize=(12, 6))
    countries = df['country'].str.split(',').explode().str.strip()
    countries = countries[countries != 'Unknown']
    top_countries = countries.value_counts().head(10)
    sns.barplot(x=top_countries.values, y=top_countries.index, palette='mako')
    plt.title('Top 10 Content Producing Countries', fontsize=16, fontweight='bold')
    plt.xlabel('Number of Titles', fontsize=12)
    plt.ylabel('Country', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(visuals_dir, 'top_countries.png'), dpi=300)
    plt.close()

    # 5. Rating Distribution (Bar Plot)
    plt.figure(figsize=(12, 6))
    ratings_order = df['rating'].value_counts().index
    sns.countplot(data=df, x='rating', order=ratings_order, palette='rocket')
    plt.title('Distribution of Content Ratings', fontsize=16, fontweight='bold')
    plt.xlabel('Rating', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(visuals_dir, 'rating_distribution.png'), dpi=300)
    plt.close()

    print(f"Visualizations successfully saved to {visuals_dir}")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    create_visualizations()
