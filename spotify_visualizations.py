"""
Spotify Data Visualization Module
Creates publication-quality visualizations for insights presentation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings

warnings.filterwarnings('ignore')

class SpotifyVisualizer:
    def __init__(self, df, output_dir="visualizations"):
        """Initialize visualizer with dataframe"""
        self.df = df
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        import os
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Set style for professional-looking plots
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (14, 8)
        plt.rcParams['font.size'] = 10
    
    def save_plot(self, name):
        """Save plot with timestamp"""
        filepath = f"{self.output_dir}/{name}.png"
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {filepath}")
        plt.close()
    
    def popularity_distribution(self):
        """Visualize popularity distribution with statistics"""
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        # Histogram with KDE
        axes[0].hist(self.df['popularity'], bins=30, alpha=0.7, color='#1DB954', edgecolor='black')
        axes[0].axvline(self.df['popularity'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {self.df["popularity"].mean():.1f}')
        axes[0].axvline(self.df['popularity'].median(), color='orange', linestyle='--', linewidth=2, label=f'Median: {self.df["popularity"].median():.1f}')
        axes[0].set_xlabel('Popularity Score', fontsize=11, fontweight='bold')
        axes[0].set_ylabel('Number of Tracks', fontsize=11, fontweight='bold')
        axes[0].set_title('Popularity Distribution', fontsize=13, fontweight='bold')
        axes[0].legend()
        axes[0].grid(alpha=0.3)
        
        # Box plot by decade
        self.df['decade'] = (self.df['release_year'] // 10 * 10).astype(str)
        sns.boxplot(data=self.df, x='decade', y='popularity', ax=axes[1], palette='Set2')
        axes[1].set_xlabel('Decade', fontsize=11, fontweight='bold')
        axes[1].set_ylabel('Popularity Score', fontsize=11, fontweight='bold')
        axes[1].set_title('Popularity Trends by Decade', fontsize=13, fontweight='bold')
        axes[1].grid(alpha=0.3, axis='y')
        
        self.save_plot('01_popularity_distribution')
    
    def temporal_trends(self):
        """Visualize temporal trends in music releases and popularity"""
        fig, axes = plt.subplots(2, 1, figsize=(15, 10))
        
        # Tracks released per year
        yearly_data = self.df.groupby('release_year').size()
        axes[0].plot(yearly_data.index, yearly_data.values, marker='o', linewidth=2.5, 
                    markersize=6, color='#1DB954')
        axes[0].fill_between(yearly_data.index, yearly_data.values, alpha=0.3, color='#1DB954')
        axes[0].set_xlabel('Year', fontsize=11, fontweight='bold')
        axes[0].set_ylabel('Number of Tracks', fontsize=11, fontweight='bold')
        axes[0].set_title('Track Releases Over Time', fontsize=13, fontweight='bold')
        axes[0].grid(alpha=0.3)
        
        # Average popularity over time
        yearly_pop = self.df.groupby('release_year')['popularity'].mean()
        axes[1].plot(yearly_pop.index, yearly_pop.values, marker='s', linewidth=2.5, 
                    markersize=6, color='#FF6B6B')
        axes[1].fill_between(yearly_pop.index, yearly_pop.values, alpha=0.3, color='#FF6B6B')
        axes[1].set_xlabel('Year', fontsize=11, fontweight='bold')
        axes[1].set_ylabel('Average Popularity', fontsize=11, fontweight='bold')
        axes[1].set_title('Average Popularity Trend', fontsize=13, fontweight='bold')
        axes[1].set_ylim([self.df['popularity'].min() - 5, self.df['popularity'].max() + 5])
        axes[1].grid(alpha=0.3)
        
        self.save_plot('02_temporal_trends')
    
    def top_artists(self):
        """Visualize top artists by track count and popularity"""
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Top artists by count
        top_artists_count = self.df['artists'].value_counts().head(12)
        axes[0].barh(range(len(top_artists_count)), top_artists_count.values, color='#1DB954')
        axes[0].set_yticks(range(len(top_artists_count)))
        axes[0].set_yticklabels(top_artists_count.index, fontsize=9)
        axes[0].set_xlabel('Number of Tracks', fontsize=11, fontweight='bold')
        axes[0].set_title('Top 12 Artists by Track Count', fontsize=13, fontweight='bold')
        axes[0].grid(alpha=0.3, axis='x')
        axes[0].invert_yaxis()
        
        # Top artists by average popularity
        artist_pop = self.df.groupby('artists').agg({'popularity': 'mean', 'name': 'count'})
        artist_pop = artist_pop[artist_pop['name'] >= 3].sort_values('popularity', ascending=False).head(12)
        
        colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(artist_pop)))
        axes[1].barh(range(len(artist_pop)), artist_pop['popularity'].values, color=colors)
        axes[1].set_yticks(range(len(artist_pop)))
        axes[1].set_yticklabels(artist_pop.index, fontsize=9)
        axes[1].set_xlabel('Average Popularity', fontsize=11, fontweight='bold')
        axes[1].set_title('Top 12 Artists by Avg. Popularity (min. 3 tracks)', fontsize=13, fontweight='bold')
        axes[1].set_xlim([0, 100])
        axes[1].grid(alpha=0.3, axis='x')
        axes[1].invert_yaxis()
        
        self.save_plot('03_top_artists')
    
    def audio_features_heatmap(self):
        """Create correlation heatmap for audio features"""
        audio_features = ['energy', 'danceability', 'valence', 'acousticness', 
                         'instrumentalness', 'liveness', 'speechiness', 'popularity']
        available_features = [f for f in audio_features if f in self.df.columns]
        
        corr_matrix = self.df[available_features].corr()
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                   square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                   vmin=-1, vmax=1)
        plt.title('Audio Features Correlation Matrix', fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        
        self.save_plot('04_audio_features_heatmap')
    
    def energy_danceability_scatter(self):
        """Scatter plot of energy vs danceability colored by popularity"""
        if 'energy' not in self.df.columns or 'danceability' not in self.df.columns:
            print("Energy/Danceability data not available")
            return
        
        plt.figure(figsize=(12, 8))
        scatter = plt.scatter(self.df['energy'], self.df['danceability'], 
                             c=self.df['popularity'], cmap='viridis', 
                             s=80, alpha=0.6, edgecolors='black', linewidth=0.5)
        
        plt.xlabel('Energy (0-1)', fontsize=12, fontweight='bold')
        plt.ylabel('Danceability (0-1)', fontsize=12, fontweight='bold')
        plt.title('Energy vs Danceability (colored by Popularity)', fontsize=14, fontweight='bold')
        
        cbar = plt.colorbar(scatter, label='Popularity')
        cbar.set_label('Popularity Score', fontsize=11, fontweight='bold')
        
        # Add quadrant lines
        plt.axhline(y=self.df['danceability'].median(), color='red', linestyle='--', 
                   alpha=0.5, linewidth=1.5, label='Median Danceability')
        plt.axvline(x=self.df['energy'].median(), color='blue', linestyle='--', 
                   alpha=0.5, linewidth=1.5, label='Median Energy')
        
        plt.legend(loc='upper left')
        plt.grid(alpha=0.3)
        
        self.save_plot('05_energy_danceability')
    
    def valence_mood_analysis(self):
        """Visualize valence (mood) patterns"""
        if 'valence' not in self.df.columns:
            print("Valence data not available")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        # Valence distribution
        axes[0].hist(self.df['valence'], bins=30, color='#FF6B6B', alpha=0.7, edgecolor='black')
        axes[0].axvline(self.df['valence'].mean(), color='darkred', linestyle='--', 
                       linewidth=2, label=f'Mean: {self.df["valence"].mean():.2f}')
        axes[0].set_xlabel('Valence (0=Sad, 1=Happy)', fontsize=11, fontweight='bold')
        axes[0].set_ylabel('Number of Tracks', fontsize=11, fontweight='bold')
        axes[0].set_title('Mood Distribution (Valence)', fontsize=13, fontweight='bold')
        axes[0].legend()
        axes[0].grid(alpha=0.3)
        
        # Valence vs Popularity
        axes[1].scatter(self.df['valence'], self.df['popularity'], alpha=0.5, s=50, color='#1DB954')
        
        # Add trend line
        z = np.polyfit(self.df['valence'], self.df['popularity'], 1)
        p = np.poly1d(z)
        axes[1].plot(self.df['valence'].sort_values(), p(self.df['valence'].sort_values()), 
                    "r--", linewidth=2, label=f'Trend (r={self.df["valence"].corr(self.df["popularity"]):.3f})')
        
        axes[1].set_xlabel('Valence (0=Sad, 1=Happy)', fontsize=11, fontweight='bold')
        axes[1].set_ylabel('Popularity', fontsize=11, fontweight='bold')
        axes[1].set_title('Valence vs Popularity', fontsize=13, fontweight='bold')
        axes[1].legend()
        axes[1].grid(alpha=0.3)
        
        self.save_plot('06_valence_mood')
    
    def duration_analysis(self):
        """Visualize duration patterns"""
        self.df['duration_min'] = self.df['duration_ms'] / 60000
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        # Duration distribution
        axes[0].hist(self.df['duration_min'], bins=30, color='#4ECDC4', alpha=0.7, edgecolor='black')
        axes[0].axvline(self.df['duration_min'].mean(), color='darkblue', linestyle='--', 
                       linewidth=2, label=f'Mean: {self.df["duration_min"].mean():.2f} min')
        axes[0].set_xlabel('Duration (minutes)', fontsize=11, fontweight='bold')
        axes[0].set_ylabel('Number of Tracks', fontsize=11, fontweight='bold')
        axes[0].set_title('Song Duration Distribution', fontsize=13, fontweight='bold')
        axes[0].legend()
        axes[0].grid(alpha=0.3)
        
        # Duration vs Popularity
        axes[1].scatter(self.df['duration_min'], self.df['popularity'], alpha=0.5, s=50, color='#FF6B6B')
        
        # Add trend line
        z = np.polyfit(self.df['duration_min'], self.df['popularity'], 1)
        p = np.poly1d(z)
        axes[1].plot(self.df['duration_min'].sort_values(), p(self.df['duration_min'].sort_values()), 
                    "b--", linewidth=2, label=f'Trend (r={self.df["duration_min"].corr(self.df["popularity"]):.3f})')
        
        axes[1].set_xlabel('Duration (minutes)', fontsize=11, fontweight='bold')
        axes[1].set_ylabel('Popularity', fontsize=11, fontweight='bold')
        axes[1].set_title('Duration vs Popularity', fontsize=13, fontweight='bold')
        axes[1].legend()
        axes[1].grid(alpha=0.3)
        
        self.save_plot('07_duration_analysis')
    
    def acousticness_analysis(self):
        """Visualize acoustic vs electric characteristics"""
        if 'acousticness' not in self.df.columns:
            print("Acousticness data not available")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        # Acousticness distribution
        axes[0].hist(self.df['acousticness'], bins=30, color='#F38181', alpha=0.7, edgecolor='black')
        axes[0].axvline(self.df['acousticness'].mean(), color='darkred', linestyle='--', 
                       linewidth=2, label=f'Mean: {self.df["acousticness"].mean():.2f}')
        axes[0].set_xlabel('Acousticness (0=Electric, 1=Acoustic)', fontsize=11, fontweight='bold')
        axes[0].set_ylabel('Number of Tracks', fontsize=11, fontweight='bold')
        axes[0].set_title('Acousticness Distribution', fontsize=13, fontweight='bold')
        axes[0].legend()
        axes[0].grid(alpha=0.3)
        
        # Acousticness vs Popularity
        axes[1].scatter(self.df['acousticness'], self.df['popularity'], alpha=0.5, s=50, color='#AA96DA')
        
        # Add trend line
        z = np.polyfit(self.df['acousticness'], self.df['popularity'], 1)
        p = np.poly1d(z)
        axes[1].plot(self.df['acousticness'].sort_values(), p(self.df['acousticness'].sort_values()), 
                    "r--", linewidth=2, label=f'Trend (r={self.df["acousticness"].corr(self.df["popularity"]):.3f})')
        
        axes[1].set_xlabel('Acousticness (0=Electric, 1=Acoustic)', fontsize=11, fontweight='bold')
        axes[1].set_ylabel('Popularity', fontsize=11, fontweight='bold')
        axes[1].set_title('Acousticness vs Popularity', fontsize=13, fontweight='bold')
        axes[1].legend()
        axes[1].grid(alpha=0.3)
        
        self.save_plot('08_acousticness_analysis')
    
    def generate_all_visualizations(self):
        """Generate all visualizations"""
        print("\n" + "="*60)
        print("GENERATING VISUALIZATIONS")
        print("="*60)
        
        visualizations = [
            ('Popularity Distribution', self.popularity_distribution),
            ('Temporal Trends', self.temporal_trends),
            ('Top Artists', self.top_artists),
            ('Audio Features Heatmap', self.audio_features_heatmap),
            ('Energy vs Danceability', self.energy_danceability_scatter),
            ('Valence (Mood) Analysis', self.valence_mood_analysis),
            ('Duration Analysis', self.duration_analysis),
            ('Acousticness Analysis', self.acousticness_analysis),
        ]
        
        for name, func in visualizations:
            try:
                print(f"\n→ Generating {name}...")
                func()
            except Exception as e:
                print(f"  ⚠ Could not generate {name}: {str(e)}")
        
        print("\n" + "="*60)
        print(f"✓ All visualizations saved to '{self.output_dir}' folder")
        print("="*60)


if __name__ == "__main__":
    # Load analyzed data
    df = pd.read_csv("spotify_tracks_analyzed.csv")
    
    # Generate visualizations
    visualizer = SpotifyVisualizer(df, output_dir="visualizations")
    visualizer.generate_all_visualizations()
