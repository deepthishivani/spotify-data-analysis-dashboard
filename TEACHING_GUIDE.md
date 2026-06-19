# 📚 Code Walkthrough & Teaching Guide

This document explains every component of the Spotify Data Analysis project so you can answer **any** interview question.

---

## Table of Contents
1. [Data Loading & Validation](#1-data-loading--validation)
2. [Basic Statistics](#2-basic-statistics)
3. [Popularity Analysis](#3-popularity-analysis)
4. [Temporal Trends](#4-temporal-trends)
5. [Artist Analysis](#5-artist-analysis)
6. [Audio Features Analysis](#6-audio-features-analysis)
7. [Track Segmentation](#7-track-segmentation)
8. [Duration Analysis](#8-duration-analysis)
9. [Mood & Acoustic Patterns](#9-mood--acoustic-patterns)
10. [Visualization Pipeline](#10-visualization-pipeline)

---

## 1. Data Loading & Validation

### The Problem
CSV files can be unreliable: missing columns, corrupted rows, wrong data types. We need to validate before analysis.

### The Code
```python
def load_data(self):
    """Load and validate dataset"""
    try:
        self.df = pd.read_csv(self.data_path)
        print(f"✓ Dataset loaded: {self.df.shape[0]} tracks, {self.df.shape[1]} features")
        return self.df
    except FileNotFoundError:
        print(f"✗ Error: Dataset not found at {self.data_path}")
        raise
```

### What's Happening
- `pd.read_csv()`: Reads CSV into a Pandas DataFrame (2D table)
- `self.df.shape[0]`: Number of rows (tracks)
- `self.df.shape[1]`: Number of columns (features)
- `try/except`: Catches errors gracefully

### Interview Questions You Can Answer

**Q: How do you handle missing files?**  
A: "I use try/except to catch FileNotFoundError. If the file is missing, the error message tells you the exact path it's looking for, making debugging easy."

**Q: What if the CSV is corrupted?**  
A: "Pandas automatically handles common issues. For severe corruption, I could use `error_bad_lines='skip'` parameter to skip corrupted rows."

**Q: What does `self.df` mean?**  
A: "It's an instance variable—stores the DataFrame at the object level so all methods can access it. Similar to a class variable."

---

## 2. Basic Statistics

### The Problem
We need to understand what we're dealing with before doing complex analysis.

### The Code
```python
def basic_statistics(self):
    """Generate basic statistical summary"""
    print(f"\nDataset Shape: {self.df.shape}")
    print(f"Date Range: {self.df['release_date'].min()} to {self.df['release_date'].max()}")
    print(f"Missing Values:\n{self.df.isnull().sum()}")
    
    numeric_cols = self.df.select_dtypes(include=[np.number]).columns
    print(f"\nNumeric Summary:\n{self.df[numeric_cols].describe()}")
```

### What's Happening

**Dataset Shape:**
```python
self.df.shape  # Returns (10000, 18) for 10k tracks with 18 columns
```

**Date Range:**
```python
self.df['release_date'].min()  # Earliest release date
self.df['release_date'].max()  # Latest release date
```

**Missing Values:**
```python
self.df.isnull().sum()
# Returns:
# name              0
# artists           0
# release_date      150
# popularity        0
# ... etc
```

**Numeric Columns:**
```python
select_dtypes(include=[np.number])  # Filters to only numeric columns
describe()  # Returns mean, std, min, max, quartiles
```

### Interview Questions

**Q: How do you identify numeric vs. categorical columns?**  
A: "Using `select_dtypes()` with `include=[np.number]` for numeric, or `include=['object']` for categorical (strings)."

**Q: What does `isnull()` do?**  
A: "Creates a boolean mask showing True where data is missing (NaN). `.sum()` counts the True values."

**Q: What's the difference between `.min()` and `.minmax()`?**  
A: "`.min()` gives the minimum value. There's no `.minmax()`—use `.min()` and `.max()` separately or `.describe()` for both plus stats."

---

## 3. Popularity Analysis

### The Problem
We need to understand how popularity is distributed and segment tracks by popularity level.

### The Code
```python
def popularity_analysis(self):
    popularity = self.df['popularity']
    
    insights = {
        'mean_popularity': popularity.mean(),
        'median_popularity': popularity.median(),
        'std_popularity': popularity.std(),
        'min_popularity': popularity.min(),
        'max_popularity': popularity.max(),
        'top_quartile': popularity.quantile(0.75)
    }
    
    bins = [0, 20, 40, 60, 80, 100]
    self.df['popularity_tier'] = pd.cut(self.df['popularity'], bins=bins, 
                                        labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
```

### What's Happening

**Extracting Column:**
```python
popularity = self.df['popularity']  # Creates a Series (1D array of values)
```

**Statistical Metrics:**
```python
popularity.mean()      # Average: sum / count
popularity.median()    # Middle value (50th percentile)
popularity.std()       # Standard deviation: how spread out data is
popularity.quantile(0.75)  # 75th percentile: value below which 75% of data falls
```

**Binning (Categorization):**
```python
bins = [0, 20, 40, 60, 80, 100]  # Boundaries
labels = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
pd.cut(data, bins=bins, labels=labels)
```

This creates bins:
- Very Low: 0–20
- Low: 20–40
- Medium: 40–60
- High: 60–80
- Very High: 80–100

### Interview Questions

**Q: What's the difference between mean and median?**  
A: "Mean is the average (sum/count). Median is the middle value. With outliers, median is more robust. For popularity, if a few mega-hit tracks exist, median better represents typical tracks."

**Q: How does `pd.cut()` differ from `pd.qcut()`?**  
A: "`.cut()` uses fixed bin edges (0, 20, 40, ...). `.qcut()` uses quantiles (equal count per bin). Use `.cut()` for business categories, `.qcut()` for equal-sized groups."

**Q: Why store popularity_tier as a new column?**  
A: "It's feature engineering. Now I can group by popularity_tier later, like `df.groupby('popularity_tier')['artists'].count()`"

---

## 4. Temporal Trends

### The Problem
Music trends change over time. We need to see if there are patterns.

### The Code
```python
def temporal_trends(self):
    self.df['release_year'] = pd.to_datetime(self.df['release_date']).dt.year
    
    yearly_counts = self.df['release_year'].value_counts().sort_index()
    print(f"\nTracks Released by Year (Last 10 Years):\n{yearly_counts.tail(10)}")
    
    yearly_popularity = self.df.groupby('release_year')['popularity'].agg(['mean', 'median', 'count'])
    print(f"\nAverage Popularity by Year (Last 5 Years):\n{yearly_popularity.tail(5)}")
```

### What's Happening

**Extracting Year:**
```python
pd.to_datetime(self.df['release_date'])  # Converts string "2020-03-15" to datetime object
.dt.year                                 # Extracts just the year: 2020
```

**Counting by Year:**
```python
self.df['release_year'].value_counts()   # Counts: how many tracks per year
.sort_index()                            # Sorts by year (chronological)
```

**Grouping & Aggregation:**
```python
self.df.groupby('release_year')['popularity'].agg(['mean', 'median', 'count'])
# Groups by year, then for each year calculates:
# - mean: average popularity
# - median: median popularity  
# - count: number of tracks

# Returns:
#              mean  median  count
# release_year
# 2015         60.5    62.0   850
# 2016         58.2    59.0   920
# ...
```

### Interview Questions

**Q: Why use `.tail(10)` instead of printing everything?**  
A: "Large datasets have too much output. `.tail(10)` shows the last 10 entries. `.head(10)` shows first 10. Better for readability and finding recent trends."

**Q: What does `.agg(['mean', 'median', 'count'])` do exactly?**  
A: "It applies multiple aggregation functions simultaneously. For each group, it calculates mean, median, and count. Efficient than doing three separate operations."

**Q: How would you handle missing dates?**  
A: "Use `pd.to_datetime(..., errors='coerce')` to convert unparseable dates to NaT (Not a Time). Then filter with `.dropna()` or `.fillna()`."

---

## 5. Artist Analysis

### The Problem
Who are the most successful artists? Do popular artists make more tracks?

### The Code
```python
def artist_analysis(self):
    top_artists = self.df['artists'].value_counts().head(15)
    
    artist_stats = self.df.groupby('artists').agg({
        'popularity': ['mean', 'max', 'count'],
        'duration_ms': 'mean'
    }).round(2)
    artist_stats.columns = ['avg_popularity', 'peak_popularity', 'track_count', 'avg_duration']
    artist_stats = artist_stats.sort_values('track_count', ascending=False).head(20)
```

### What's Happening

**Top Artists by Track Count:**
```python
self.df['artists'].value_counts().head(15)
# artist_name    count
# Taylor Swift   350
# Drake          320
# The Beatles    280
# ...
```

**Multi-Level Aggregation:**
```python
df.groupby('artists').agg({
    'popularity': ['mean', 'max', 'count'],    # 3 stats for popularity column
    'duration_ms': 'mean'                      # 1 stat for duration column
})
# Returns:
#                popularity       duration_ms
#                mean   max count  mean
# artist_name
# Taylor Swift   75.2   95  350    210000
# Drake          72.1   98  320    215000
```

**Renaming Multi-Level Columns:**
```python
artist_stats.columns = ['avg_popularity', 'peak_popularity', 'track_count', 'avg_duration']
# Before: MultiIndex with nested names
# After: Simple column names
```

**Sorting & Filtering:**
```python
artist_stats.sort_values('track_count', ascending=False)  # Most tracks first
.head(20)                                                  # Top 20 only
```

### Interview Questions

**Q: What's the difference between `.agg()` and `.apply()`?**  
A: "`.agg()` applies built-in functions (mean, max, sum). `.apply()` applies custom functions. For simple stats, `.agg()` is faster."

**Q: How do you handle artists with multiple spellings or missing names?**  
A: "You'd preprocess: `df['artists'].str.lower().str.strip()` to normalize. Handle missing with `.fillna('Unknown')`."

**Q: Why use `round(2)` on the aggregation?**  
A: "It rounds all numeric results to 2 decimal places. Cleaner output, easier to read. `round(2)` means 2 decimals: 75.23"

---

## 6. Audio Features Analysis

### The Problem
Which audio characteristics predict popularity? Is loud music more popular? Are happy songs more successful?

### The Code
```python
def audio_features_analysis(self):
    audio_features = ['energy', 'danceability', 'valence', 'acousticness', 
                     'instrumentalness', 'liveness', 'speechiness']
    available_features = [f for f in audio_features if f in self.df.columns]
    
    correlations = {}
    for feature in available_features:
        corr = self.df[feature].corr(self.df['popularity'])
        correlations[feature] = corr
```

### What's Happening

**List Comprehension:**
```python
available_features = [f for f in audio_features if f in self.df.columns]
# Filters to only features that exist in the dataset
# Avoids errors if some columns are missing
```

**Correlation Calculation:**
```python
self.df['energy'].corr(self.df['popularity'])
# Pearson correlation coefficient: -1.0 to 1.0
# -1.0: perfect negative correlation (more energy = less popular)
#  0.0: no correlation (independent)
#  1.0: perfect positive correlation (more energy = more popular)
```

**Building Correlation Dictionary:**
```python
correlations = {}
for feature in available_features:
    corr = self.df[feature].corr(self.df['popularity'])
    correlations[feature] = corr
# Result:
# {'energy': 0.12, 'danceability': 0.08, 'valence': 0.15, ...}
```

**Sorting by Correlation Strength:**
```python
sorted_corr = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)
# abs(x[1]): absolute value (ignores sign)
# reverse=True: largest first
# Result: Features ranked by impact magnitude
```

### Interview Questions

**Q: What does Pearson correlation mean exactly?**  
A: "It measures linear relationship between two variables (−1 to 1). 0.5 means moderate positive: as one increases, other tends to increase. For this data, correlations < 0.3 are weak."

**Q: Why use `abs()` for sorting?**  
A: "Because −0.8 (strong negative) is just as important as 0.8 (strong positive). We care about magnitude, not direction."

**Q: Can correlation predict causation?**  
A: "No. Correlation ≠ causation. High energy might correlate with popularity, but maybe popular artists choose energetic songs, not vice versa. Need experiments to prove cause."

**Q: What if a feature is missing for some tracks?**  
A: "`.corr()` automatically ignores NaN values. By default it uses `skipna=True`. Alternatively, you could impute missing values with mean/median first."

---

## 7. Track Segmentation

### The Problem
Not all tracks are the same. Can we group them by characteristics? What segment is most popular?

### The Code
```python
def energy_danceability_clusters(self):
    energy_med = self.df['energy'].median()
    dance_med = self.df['danceability'].median()
    
    def classify_track(row):
        if row['energy'] >= energy_med and row['danceability'] >= dance_med:
            return 'High Energy, Danceable'
        elif row['energy'] >= energy_med and row['danceability'] < dance_med:
            return 'High Energy, Not Danceable'
        # ... etc
    
    self.df['track_type'] = self.df.apply(classify_track, axis=1)
```

### What's Happening

**Finding Medians:**
```python
energy_med = self.df['energy'].median()  # Middle value for energy
dance_med = self.df['danceability'].median()  # Middle value for danceability
# Each divides the feature into "high" and "low" halves
```

**Defining Classification Function:**
```python
def classify_track(row):
    if row['energy'] >= energy_med and row['danceability'] >= dance_med:
        return 'High Energy, Danceable'
    # ... other conditions
    else:
        return 'Low Energy, Not Danceable'

# This creates a 2×2 matrix:
#                    Danceable      Not Danceable
# High Energy        Quadrant 1     Quadrant 2
# Low Energy         Quadrant 3     Quadrant 4
```

**Applying to Each Row:**
```python
self.df.apply(classify_track, axis=1)
# axis=1: apply function to each row
# axis=0: apply function to each column
# Returns Series of classifications
```

**Creating New Column:**
```python
self.df['track_type'] = ...  # Adds new column with track type
```

### Interview Questions

**Q: What's the difference between `apply()` and `map()`?**  
A: "`.apply()` works on Series or DataFrames. `.map()` works only on Series. For row-by-row operations, `.apply(..., axis=1)` is standard."

**Q: Is using medians for clustering optimal?**  
A: "It's simple and interpretable, but not optimal statistically. For production, you'd use K-means clustering. For interviews, explaining the business logic (4 track types) matters more."

**Q: How would you handle missing energy/danceability values?**  
A: "Fill with mean/median first: `df['energy'].fillna(df['energy'].mean())`"

---

## 8. Duration Analysis

### The Problem
Do shorter songs get more plays? Is there an optimal length?

### The Code
```python
def duration_analysis(self):
    self.df['duration_min'] = self.df['duration_ms'] / 60000
    
    duration_corr = self.df['duration_min'].corr(self.df['popularity'])
    
    duration_bins = [0, 2, 3, 4, 5, 10]
    self.df['duration_band'] = pd.cut(self.df['duration_min'], bins=duration_bins)
    
    duration_band_pop = self.df.groupby('duration_band', observed=True)['popularity'].agg(['mean', 'count'])
```

### What's Happening

**Converting Units:**
```python
self.df['duration_min'] = self.df['duration_ms'] / 60000
# Spotify stores duration in milliseconds
# 1 minute = 60,000 milliseconds
# Divide to convert to minutes (more readable)
```

**Correlation with Popularity:**
```python
duration_corr = self.df['duration_min'].corr(self.df['popularity'])
# Typically r ≈ 0.05 to 0.15 (weak positive)
# Meaning: slightly longer songs tend to be slightly more popular
```

**Binning Into Duration Bands:**
```python
bins = [0, 2, 3, 4, 5, 10]  # 0–2 min, 2–3 min, 3–4 min, 4–5 min, 5–10 min
pd.cut(duration_min, bins=bins)  # Assigns each song to a bin
```

**Popularity by Duration Band:**
```python
groupby('duration_band', observed=True)['popularity'].agg(['mean', 'count'])
# observed=True: only show bins that have data (skip empty bins)
# Returns: average popularity and track count per duration band
```

### Interview Questions

**Q: Why convert to minutes instead of using milliseconds?**  
A: "Interpretability. 180000 ms is harder to understand than 3 minutes. Also reduces numerical scale, sometimes helps with computations."

**Q: What does `observed=True` do?**  
A: "By default, `.groupby()` shows all categories even if empty. `observed=True` shows only categories with data. Cleaner output."

**Q: How would you find the optimal duration?**  
A: "Look at which duration_band has highest mean popularity. Or fit a curve (polynomial regression) to find the peak mathematically."

---

## 9. Mood & Acoustic Patterns

### The Problem
Do happy, upbeat songs do better? Are acoustic songs less popular?

### The Code
```python
def valence_acousticness_patterns(self):
    valence_corr = self.df['valence'].corr(self.df['popularity'])
    acoustic_corr = self.df['acousticness'].corr(self.df['popularity'])
    
    self.df['mood'] = pd.cut(self.df['valence'], bins=3, labels=['Dark', 'Neutral', 'Happy'])
    
    mood_stats = self.df.groupby('mood', observed=True)['popularity'].agg(['mean', 'median', 'count'])
```

### What's Happening

**Correlations:**
```python
# Valence: 0 = sad, 1 = happy
# Acousticness: 0 = electric, 1 = acoustic
# Both typically have weak correlations (< 0.2) with popularity
```

**Creating Mood Categories:**
```python
pd.cut(valence, bins=3, labels=['Dark', 'Neutral', 'Happy'])
# bins=3: divides valence into 3 equal-width bins
# [0.0–0.33: Dark, 0.33–0.66: Neutral, 0.66–1.0: Happy]
```

**Mood Popularity Stats:**
```python
groupby('mood')['popularity'].agg(['mean', 'median', 'count'])
# Shows: Is happy music more popular? By how much?
```

### Interview Questions

**Q: What's valence exactly?**  
A: "Spotify's measure of musical positiveness. 0 = minor key, sad, angry. 1 = major key, happy, cheerful. Derived from audio analysis algorithms."

**Q: Why would acousticness NOT predict popularity?**  
A: "Genre and context matter more. Acoustic folk songs are different from acoustic pop. Both can be popular in their niche. Raw acoustic value ≠ success."

**Q: How is mood calculated? Is it always accurate?**  
A: "Spotify uses audio feature algorithms (not lyrics). Sometimes inaccurate—a sad song with upbeat tempo gets high valence. But good enough for trends."

---

## 10. Visualization Pipeline

### The Problem
Numbers are hard to understand. Charts tell the story faster.

### Key Visualization Techniques

**Histogram (Distribution):**
```python
plt.hist(data, bins=30, alpha=0.7, color='#1DB954', edgecolor='black')
# bins=30: number of bars
# alpha=0.7: transparency (0=invisible, 1=opaque)
# Shows: How many tracks fall into each popularity range?
```

**Line Plot (Trends):**
```python
plt.plot(years, popularity, marker='o', linewidth=2.5)
# marker='o': circles at data points
# Shows: How does popularity change over time?
```

**Scatter Plot (Relationships):**
```python
plt.scatter(energy, popularity, c=popularity, cmap='viridis', s=80)
# c=popularity: color intensity based on popularity
# s=80: size of dots
# Shows: Is there a relationship between energy and popularity?
```

**Heatmap (Correlations):**
```python
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
# annot=True: show correlation values
# coolwarm: blue (negative) to red (positive)
# Shows: Which features are related?
```

**Box Plot (Distribution by Category):**
```python
sns.boxplot(data=df, x='decade', y='popularity', palette='Set2')
# Shows: How does popularity vary by decade?
# Box = 50% of data, whiskers = outliers
```

### Interview Questions

**Q: Why use `alpha=0.7` in histograms?**  
A: "Transparency makes overlapping bars visible. Shows density: darker areas = more data."

**Q: How do you choose number of bins for a histogram?**  
A: "Rule of thumb: `bins = sqrt(n)` or `bins = log2(n)`. Too few: lose detail. Too many: too noisy. Experiment and see what looks right."

**Q: What's the difference between `plt` and `sns`?**  
A: "Matplotlib (`plt`) is basic plotting. Seaborn (`sns`) builds on matplotlib with statistical visuals and prettier defaults. Use seaborn for most things."

**Q: Why save visualizations as PNG, not PDF?**  
A: "PNG works everywhere (GitHub, websites). PDF is for printing. PNG at 300 DPI is high quality and web-friendly."

---

## Complete Workflow Summary

```
1. Load Data (spotify_analysis.py)
   ↓
2. Validate (check shape, missing values)
   ↓
3. Feature Engineering (create release_year, duration_min, popularity_tier, etc.)
   ↓
4. Univariate Analysis (look at each column alone)
   - Popularity distribution
   - Temporal trends
   - Artist rankings
   ↓
5. Bivariate Analysis (look at relationships)
   - Correlations (audio features ↔ popularity)
   - Scatter plots
   - Segmentation
   ↓
6. Multivariate Analysis (complex patterns)
   - Mood + acoustic patterns
   - Energy × danceability clustering
   ↓
7. Visualization (spotify_visualizations.py)
   - Create 8 publication-quality charts
   - Save to visualizations/ folder
   ↓
8. Report (Executive summary & key findings)
```

---

## Interview Preparation Checklist

### Understand Each Method
- [ ] Can explain `load_data()` in 2 sentences
- [ ] Can explain `popularity_analysis()` and why we bin popularity
- [ ] Can explain `temporal_trends()` and what year-over-year shows
- [ ] Can explain `artist_analysis()` and multi-level aggregation
- [ ] Can explain `audio_features_analysis()` and correlation interpretation
- [ ] Can explain `energy_danceability_clusters()` and 2×2 segmentation
- [ ] Can explain `duration_analysis()` and optimal duration logic
- [ ] Can explain visualization choices (histogram vs. scatter, etc.)

### Know These Concepts
- [ ] Pearson correlation (-1 to 1)
- [ ] Mean vs. median
- [ ] Standard deviation
- [ ] Quantiles (25th, 50th, 75th percentile)
- [ ] GroupBy + aggregation
- [ ] `.apply()` vs. `.agg()`
- [ ] Binning (`.cut()`) vs. Quantile binning (`.qcut()`)
- [ ] Why correlation ≠ causation

### Practice Explanations
- [ ] "What does this project do?" (30 seconds)
- [ ] "Walk me through your most complex analysis" (2 minutes)
- [ ] "What was your biggest finding?" (1 minute)
- [ ] "How would you improve this?" (2 minutes)
- [ ] "Can you explain this specific line of code?" (1 minute)

### Be Ready to Code
- [ ] Modify an existing analysis
- [ ] Add a new feature column
- [ ] Create a new visualization
- [ ] Fix a bug in the code
- [ ] Explain time complexity (O(n) for most operations)

---

## Final Tips

1. **Test Everything**: Run the code locally multiple times. Understand output.
2. **Modify & Experiment**: Change bins, add new features, try new visualizations.
3. **Read Documentation**: Look up Pandas/NumPy docs when confused.
4. **Ask "Why?"**: For every line, ask why that choice was made.
5. **Teach Someone Else**: Explaining to friends cements understanding.
6. **Practice Interviews**: Record yourself explaining the project. Watch back.

---

**You got this.** Go run `python3 spotify_analysis.py` and start exploring. 🎵
