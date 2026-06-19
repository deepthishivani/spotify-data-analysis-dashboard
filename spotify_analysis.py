"""
Spotify Data Analysis - Main Analysis Pipeline
Explores music trends, artist patterns, and audio feature correlations
using Pandas, NumPy, and statistical methods.
"""

import pandas as pd
import numpy as np
import warnings
from collections import Counter
import os

warnings.filterwarnings('ignore')

class SpotifyAnalyzer:
    def __init__(self, data_path):
        """Initialize analyzer with dataset path"""
        self.df = None
        self.data_path = data_path
        self.load_data()
    
    def load_data(self):
        """Load and validate dataset"""
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"✓ Dataset loaded: {self.df.shape[0]} tracks, {self.df.shape[1]} features")
            return self.df
        except FileNotFoundError:
            print(f"✗ Error: Dataset not found at {self.data_path}")
            raise
    
    def basic_statistics(self):
        """Generate basic statistical summary"""
        print("\n" + "="*60)
        print("BASIC STATISTICS")
        print("="*60)
        
        print(f"\nDataset Shape: {self.df.shape}")
        print(f"Date Range: {self.df['release_date'].min()} to {self.df['release_date'].max()}")
        print(f"Missing Values:\n{self.df.isnull().sum()}")
        
        # Numeric column statistics
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        print(f"\nNumeric Summary:\n{self.df[numeric_cols].describe()}")
        
        return self.df.describe()
    
    def popularity_analysis(self):
        """Analyze track popularity patterns"""
        print("\n" + "="*60)
        print("POPULARITY ANALYSIS")
        print("="*60)
        
        popularity = self.df['popularity']
        
        insights = {
            'mean_popularity': popularity.mean(),
            'median_popularity': popularity.median(),
            'std_popularity': popularity.std(),
            'min_popularity': popularity.min(),
            'max_popularity': popularity.max(),
            'top_quartile': popularity.quantile(0.75)
        }
        
        for key, val in insights.items():
            print(f"{key.replace('_', ' ').title()}: {val:.2f}")
        
        # Popularity distribution
        bins = [0, 20, 40, 60, 80, 100]
        self.df['popularity_tier'] = pd.cut(self.df['popularity'], bins=bins, 
                                            labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
        
        print(f"\nPopularity Distribution:\n{self.df['popularity_tier'].value_counts().sort_index()}")
        
        return insights
    
    def temporal_trends(self):
        """Analyze trends over time"""
        print("\n" + "="*60)
        print("TEMPORAL TRENDS")
        print("="*60)
        
        # Parse release_date
        self.df['release_year'] = pd.to_datetime(self.df['release_date']).dt.year
        
        # Tracks released per year
        yearly_counts = self.df['release_year'].value_counts().sort_index()
        print(f"\nTracks Released by Year (Last 10 Years):\n{yearly_counts.tail(10)}")
        
        # Average popularity over time
        yearly_popularity = self.df.groupby('release_year')['popularity'].agg(['mean', 'median', 'count'])
        print(f"\nAverage Popularity by Year (Last 5 Years):\n{yearly_popularity.tail(5)}")
        
        return yearly_popularity
    
    def artist_analysis(self):
        """Analyze top artists and artist patterns"""
        print("\n" + "="*60)
        print("ARTIST ANALYSIS")
        print("="*60)
        
        # Top artists by track count
        top_artists = self.df['artists'].value_counts().head(15)
        print(f"\nTop 15 Artists by Track Count:\n{top_artists}")
        
        # Average popularity by artist (top 20)
        artist_stats = self.df.groupby('artists').agg({
            'popularity': ['mean', 'max', 'count'],
            'duration_ms': 'mean'
        }).round(2)
        artist_stats.columns = ['avg_popularity', 'peak_popularity', 'track_count', 'avg_duration']
        artist_stats = artist_stats.sort_values('track_count', ascending=False).head(20)
        
        print(f"\nTop Artists Performance Metrics:\n{artist_stats}")
        
        return artist_stats
    
    def audio_features_analysis(self):
        """Analyze audio features and their relationships"""
        print("\n" + "="*60)
        print("AUDIO FEATURES ANALYSIS")
        print("="*60)
        
        audio_features = ['energy', 'danceability', 'valence', 'acousticness', 
                         'instrumentalness', 'liveness', 'speechiness']
        
        available_features = [f for f in audio_features if f in self.df.columns]
        
        print(f"\nAudio Feature Statistics (0-1 scale):")
        feature_stats = self.df[available_features].describe().round(3)
        print(feature_stats)
        
        # Correlation analysis
        print(f"\nFeature Correlations with Popularity:")
        correlations = {}
        for feature in available_features:
            corr = self.df[feature].corr(self.df['popularity'])
            correlations[feature] = corr
            print(f"  {feature.capitalize():20s}: {corr:7.3f}")
        
        # Sorted by correlation strength
        sorted_corr = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)
        print(f"\nFeatures Ranked by Popularity Impact:")
        for feature, corr in sorted_corr:
            direction = "↑" if corr > 0 else "↓"
            print(f"  {direction} {feature.capitalize():20s}: {abs(corr):.3f}")
        
        return correlations
    
    def energy_danceability_clusters(self):
        """Segment tracks by energy and danceability"""
        print("\n" + "="*60)
        print("TRACK SEGMENTATION (Energy × Danceability)")
        print("="*60)
        
        if 'energy' not in self.df.columns or 'danceability' not in self.df.columns:
            print("Energy/Danceability data not available")
            return None
        
        # Create quadrants
        energy_med = self.df['energy'].median()
        dance_med = self.df['danceability'].median()
        
        def classify_track(row):
            if row['energy'] >= energy_med and row['danceability'] >= dance_med:
                return 'High Energy, Danceable'
            elif row['energy'] >= energy_med and row['danceability'] < dance_med:
                return 'High Energy, Not Danceable'
            elif row['energy'] < energy_med and row['danceability'] >= dance_med:
                return 'Low Energy, Danceable'
            else:
                return 'Low Energy, Not Danceable'
        
        self.df['track_type'] = self.df.apply(classify_track, axis=1)
        
        print(f"\nTrack Distribution:\n{self.df['track_type'].value_counts()}")
        
        print(f"\nAverage Popularity by Type:")
        type_popularity = self.df.groupby('track_type')['popularity'].agg(['mean', 'median', 'count']).round(2)
        print(type_popularity)
        
        return self.df['track_type'].value_counts()
    
    def duration_analysis(self):
        """Analyze song duration patterns"""
        print("\n" + "="*60)
        print("DURATION ANALYSIS")
        print("="*60)
        
        self.df['duration_min'] = self.df['duration_ms'] / 60000  # Convert to minutes
        
        print(f"\nDuration Statistics (minutes):")
        duration_stats = self.df['duration_min'].describe().round(2)
        print(duration_stats)
        
        # Correlation with popularity
        duration_corr = self.df['duration_min'].corr(self.df['popularity'])
        print(f"\nDuration-Popularity Correlation: {duration_corr:.3f}")
        
        # Optimal duration band
        duration_bins = [0, 2, 3, 4, 5, 10]
        self.df['duration_band'] = pd.cut(self.df['duration_min'], bins=duration_bins)
        
        print(f"\nPopularity by Duration Band:")
        duration_band_pop = self.df.groupby('duration_band', observed=True)['popularity'].agg(['mean', 'count']).round(2)
        print(duration_band_pop)
        
        return self.df['duration_min'].describe()
    
    def valence_acousticness_patterns(self):
        """Analyze mood (valence) and acoustic characteristics"""
        print("\n" + "="*60)
        print("MOOD & ACOUSTIC PATTERNS")
        print("="*60)
        
        if 'valence' not in self.df.columns or 'acousticness' not in self.df.columns:
            print("Valence/Acousticness data not available")
            return None
        
        valence_corr = self.df['valence'].corr(self.df['popularity'])
        acoustic_corr = self.df['acousticness'].corr(self.df['popularity'])
        
        print(f"\nValence (Happiness) ↔ Popularity: {valence_corr:.3f}")
        print(f"Acousticness ↔ Popularity: {acoustic_corr:.3f}")
        
        # Segment by valence
        self.df['mood'] = pd.cut(self.df['valence'], bins=3, labels=['Dark', 'Neutral', 'Happy'])
        
        print(f"\nPopularity by Mood Profile:")
        mood_stats = self.df.groupby('mood', observed=True)['popularity'].agg(['mean', 'median', 'count']).round(2)
        print(mood_stats)
        
        return {
            'valence_corr': valence_corr,
            'acousticness_corr': acoustic_corr
        }
    
    def generate_summary_report(self):
        """Generate executive summary"""
        print("\n" + "="*70)
        print("EXECUTIVE SUMMARY - KEY INSIGHTS")
        print("="*70)
        
        insights = [
            f"Dataset contains {self.df.shape[0]:,} tracks spanning {self.df['release_year'].min():.0f}-{self.df['release_year'].max():.0f}",
            f"Average track popularity: {self.df['popularity'].mean():.1f}/100",
            f"Most common artist: {self.df['artists'].mode()[0]} ({self.df['artists'].value_counts().iloc[0]} tracks)",
            f"Average track duration: {self.df['duration_min'].mean():.1f} minutes",
            f"Most popular track: '{self.df.loc[self.df['popularity'].idxmax(), 'name']}' ({self.df['popularity'].max()}/100)",
            f"Least popular track: '{self.df.loc[self.df['popularity'].idxmin(), 'name']}' ({self.df['popularity'].min()}/100)",
        ]
        
        if 'energy' in self.df.columns:
            insights.append(f"Average energy level: {self.df['energy'].mean():.2f}/1.0")
        if 'danceability' in self.df.columns:
            insights.append(f"Average danceability: {self.df['danceability'].mean():.2f}/1.0")
        
        for i, insight in enumerate(insights, 1):
            print(f"{i}. {insight}")
        
        print("\n" + "="*70)
    
    def run_full_analysis(self):
        """Execute complete analysis pipeline"""
        print("\n" + "╔" + "="*68 + "╗")
        print("║" + " "*15 + "SPOTIFY DATA ANALYSIS DASHBOARD" + " "*21 + "║")
        print("╚" + "="*68 + "╝\n")
        
        self.basic_statistics()
        self.popularity_analysis()
        self.temporal_trends()
        self.artist_analysis()
        self.audio_features_analysis()
        self.energy_danceability_clusters()
        self.duration_analysis()
        self.valence_acousticness_patterns()
        self.generate_summary_report()
        
        print("\n✓ Analysis Complete\n")
        
        return self.df


if __name__ == "__main__":
    # Path to your dataset (download from Kaggle)
    data_file = "spotify_tracks.csv"
    
    # Run analysis
    analyzer = SpotifyAnalyzer(data_file)
    analyzed_df = analyzer.run_full_analysis()
    
    # Save enriched dataset with new features
    analyzed_df.to_csv("spotify_tracks_analyzed.csv", index=False)
    print("Analyzed dataset saved as 'spotify_tracks_analyzed.csv'")
