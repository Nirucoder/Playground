import requests
import pandas as pd
# Step 1: Define API endpoints
endpoints = {
    "planet": "https://data-vortex-api.onrender.com/round1/earth_planet",
    "climate": "https://data-vortex-api.onrender.com/round1/earth_climate",
    "soil": "https://data-vortex-api.onrender.com/round1/earth_soil"
}
# Step 2: Fetch and store in dictionary of DataFrames
dfs = {}
for name, url in endpoints.items():
    response = requests.get(url)
    data = response.json()
    response.raise_for_status()  
    df = pd.json_normalize(data)
    df["source"] = name   # add label column
    dfs[name] = df
# Step 3: Merge into a single dataset
unified_df = pd.concat(dfs.values(), axis=1)
unified_df = unified_df.dropna(how="any")
# Step 5: Save to CSV
unified_df.to_csv(r"D:\SRM EXTRA\earth_unified_clean.csv", index=False)
df = pd.read_csv(r"D:\SRM EXTRA//earth_unified_clean.csv")
numeric_df=df.select_dtypes(include='number')
mins=numeric_df.min()
maxs=numeric_df.max()
extremes=pd.DataFrame({'min':mins,'max':maxs})
endpoints_round3 = {
   "planets": "https://data-vortex-api.onrender.com/round3/planets",
    "biosphere": "https://data-vortex-api.onrender.com/round3/biosphere",
    "energy_sources": "https://data-vortex-api.onrender.com/round3/energy_sources",
    "climate": "https://data-vortex-api.onrender.com/round3/climate",
    "soil": "https://data-vortex-api.onrender.com/round3/soil",
    "habitability_scores": "https://data-vortex-api.onrender.com/round3/habitability_scores",
    "colonization_history": "https://data-vortex-api.onrender.com/round3/colonization_history"

}

dfs_round3 = {}
for name, url in endpoints_round3.items():
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        df = pd.json_normalize(data)
        df["source"] = name
        dfs_round3[name] = df
    except requests.RequestException as e:
        print(f"Error fetching {name}: {e}")
        dfs_round3[name] = pd.DataFrame()

# Unify data
unified_planets_df = dfs_round3["planets"].copy()
for name, df in dfs_round3.items():
    if name != "planets":
        unified_planets_df = unified_planets_df.merge(df, on="planet_id", how="outer", suffixes=("", f"_{name}"))

unified_planets_df = unified_planets_df.dropna(subset=["planet_id"], how="any")

# Aggregate averages (no exclusions)
numeric_cols = unified_planets_df.select_dtypes(include='number').columns.tolist()
group_key = "planet_name" if "planet_name" in unified_planets_df.columns else "planet_id"
planet_averages = unified_planets_df.groupby(group_key)[numeric_cols].mean().reset_index()

# Load Earth ranges (all numeric features)
earth_df = pd.read_csv("earth_unified_clean.csv")  # Update path if needed
earth_numeric = earth_df.select_dtypes(include='number')
earth_ranges = pd.DataFrame({'min': earth_numeric.min(), 'max': earth_numeric.max()})
relevant_features = [col for col in planet_averages.columns if col in earth_ranges.index]
earth_ranges = earth_ranges.loc[relevant_features]
print("Shared features:", relevant_features)

# Score planets
def check_within_range(row, ranges):
    score = 0
    matches = {}
    weights = {
        'avg_temp_c': 2,
        'vegetation_index': 2,

    }
    default_weight = 1
    for feature in ranges.index:
        if feature in row.index and pd.notna(row[feature]):
            value = row[feature]
            min_val, max_val = ranges.loc[feature]
            weight = weights.get(feature, default_weight)
            if min_val <= value <= max_val:
                score += weight
                matches[feature] = f"Yes ({weight} points)"
            else:
                matches[feature] = f"No ({weight} points)"
        else:
            matches[feature] = "Missing"
    return pd.Series([score, matches])

results = []
for _, row in planet_averages.iterrows():
    score_series = check_within_range(row, earth_ranges)
    result_row = row.copy()
    result_row["score"] = score_series[0]
    result_row["matches"] = score_series[1]
    results.append(result_row)

results_df = pd.DataFrame(results)

# Rank and print
if not results_df.empty:
    ranked_df = results_df.sort_values(by="score", ascending=False).reset_index(drop=True)
    ranked_df["rank"] = ranked_df.index + 1
    name_col = "planet_name" if "planet_name" in ranked_df.columns else "planet_id"
    print("\nRanked Planets by Habitability Score:")
    print(ranked_df[[name_col, "score", "rank"]].to_string(index=False))
    
    non_earth_df = ranked_df[ranked_df[name_col] != "Earth"] if name_col == "planet_name" else ranked_df[ranked_df["planet_id"] != 1]
    if not non_earth_df.empty:
        if len(non_earth_df) > 1:
            next_best_planet = non_earth_df.iloc[1]
            print(f"\nNext Best Habitable Planet: {next_best_planet[name_col]} (Score: {next_best_planet['score']})")
        else:
            print("\nOnly one non-Earth planet found; no 'next best' available.")
    else:
        print("\nNo non-Earth planets found.")
    
    top_planet = ranked_df.iloc[0]
    print("\nDetailed Matches for Top Planet:")
    matches_df = pd.DataFrame(list(top_planet["matches"].items()), columns=["Feature", "Within Range?"])
    print(matches_df.to_string(index=False))

# Save CSVs
unified_planets_df.to_csv(r"D:\SRM EXTRA\\resourceless_unified.csv", index=False)

print("\nSaved Round 2 data as 'planets_round3_unified.csv'")

if not results_df.empty:
    ranked_df.to_csv(r"D:\SRM EXTRA\\resouceless.csv", index=False)
    print("\nSaved ranked planet data as 'ranked_planets_habitability.csv'")