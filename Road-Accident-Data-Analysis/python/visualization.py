import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_visualizations():
    input_path = '../dataset/processed/accident_cleaned.csv'
    visuals_dir = '../visuals/'
    
    print("Starting visualization process...")
    
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: {input_path} not found.")
        return

    sns.set_theme(style="darkgrid")
    plt.rcParams.update({'figure.figsize': (10, 6), 'font.size': 12})
    
    # 1. Accidents by Region
    if 'region' in df.columns:
        plt.figure()
        top_regions = df['region'].value_counts().head(10)
        sns.barplot(x=top_regions.values, y=top_regions.index, palette='viridis')
        plt.title('Top 10 High-Risk Regions (UK Districts)', fontsize=16, fontweight='bold')
        plt.xlabel('Number of Accidents', fontsize=12)
        plt.ylabel('Region', fontsize=12)
        plt.tight_layout()
        plt.savefig(os.path.join(visuals_dir, 'python_charts/01_accidents_by_region.png'), dpi=300)
        plt.close()

    # 2. Accident Severity
    if 'accident_severity' in df.columns:
        plt.figure()
        sns.countplot(data=df, x='accident_severity', palette='rocket')
        plt.title('Accident Severity Distribution (1=Fatal, 2=Serious, 3=Minor)', fontsize=16, fontweight='bold')
        plt.xlabel('Severity Level', fontsize=12)
        plt.ylabel('Count', fontsize=12)
        plt.tight_layout()
        plt.savefig(os.path.join(visuals_dir, 'python_charts/02_accidents_by_severity.png'), dpi=300)
        plt.close()

    # 3. Monthly Trend
    if 'month' in df.columns:
        plt.figure()
        months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        monthly_counts = df['month'].value_counts().reindex(months_order).fillna(0)
        sns.lineplot(x=monthly_counts.index, y=monthly_counts.values, marker='o', color='crimson', linewidth=2)
        plt.title('Monthly Accident Trends', fontsize=16, fontweight='bold')
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Number of Accidents', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(visuals_dir, 'python_charts/03_monthly_trend.png'), dpi=300)
        plt.close()

    # 4. Day of Week Trend
    if 'day_of_week_extracted' in df.columns:
        plt.figure()
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_counts = df['day_of_week_extracted'].value_counts().reindex(days_order).fillna(0)
        sns.barplot(x=day_counts.index, y=day_counts.values, palette='coolwarm')
        plt.title('Accidents by Day of the Week', fontsize=16, fontweight='bold')
        plt.xlabel('Day of Week', fontsize=12)
        plt.ylabel('Number of Accidents', fontsize=12)
        plt.tight_layout()
        plt.savefig(os.path.join(visuals_dir, 'python_charts/04_accidents_by_day_of_week.png'), dpi=300)
        plt.close()

    # Note: vehicle type visualization skipped as it's missing from the raw dataset.

    print(f"Visualizations saved successfully to {visuals_dir}")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    create_visualizations()
