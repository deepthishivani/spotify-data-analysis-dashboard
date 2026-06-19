"""
Project Configuration
Spotify Data Analysis Dashboard
"""

# Project metadata
PROJECT_NAME = "spotify-data-analysis-dashboard"
VERSION = "1.0.0"
AUTHOR = "Deepthi Shivani"
DESCRIPTION = "Python data analytics project exploring Spotify music trends using Pandas and NumPy"

# Data file paths
DATA_INPUT_FILE = "spotify_tracks.csv"
DATA_OUTPUT_FILE = "spotify_tracks_analyzed.csv"
VISUALIZATIONS_DIR = "visualizations"

# Expected columns in dataset
REQUIRED_COLUMNS = [
    'name',
    'artists',
    'release_date',
    'popularity',
    'duration_ms'
]

# Optional audio feature columns
AUDIO_FEATURES = [
    'energy',
    'danceability',
    'valence',
    'acousticness',
    'instrumentalness',
    'liveness',
    'speechiness'
]

# Analysis parameters
MIN_TRACKS_FOR_ARTIST_ANALYSIS = 3  # Minimum tracks to include artist in performance metrics
POPULARITY_BINS = [0, 20, 40, 60, 80, 100]  # For popularity tier categorization
POPULARITY_LABELS = ['Very Low', 'Low', 'Medium', 'High', 'Very High']

# Visualization settings
DPI = 300  # Resolution for saved charts
FIGURE_SIZE_SINGLE = (14, 8)
FIGURE_SIZE_DOUBLE = (16, 6)
FIGURE_SIZE_SQUARE = (12, 8)
COLORMAP_CONTINUOUS = 'viridis'  # For continuous data
COLORMAP_CATEGORICAL = 'Set2'    # For categorical data

# Statistical thresholds
WEAK_CORRELATION_THRESHOLD = 0.3
MODERATE_CORRELATION_THRESHOLD = 0.5
STRONG_CORRELATION_THRESHOLD = 0.7

print(f"✓ Configuration loaded: {PROJECT_NAME} v{VERSION}")
