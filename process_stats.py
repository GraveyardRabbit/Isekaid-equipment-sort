import pandas as pd
from collections import Counter

# Read the CSV file
df = pd.read_csv('equipment.csv')

def process_stats(stats):
    if not isinstance(stats, str):
        return "N/A"  # Handle missing or non-string values
    
    stats_list = stats.split(', ')
    counter = Counter(stats_list)
    
    # Check if all counts are the same
    counts = list(counter.values())
    if len(set(counts)) == 1 and len(counter) == 1:
        most_common_stat = list(counter.keys())[0].split(':')[0]
        return f"pure {most_common_stat}"
    
    # Check if all stat names are different
    if len(counter) == len(stats_list):
        all_counts_sorted = sorted(counts, reverse=True)
        return f"{'/'.join(map(str, all_counts_sorted))} mixed"
    
    # Find the highest count
    highest_count = max(counter.values())
    
    # Find all stats with the highest count
    most_common_stats = [stat.split(':')[0] for stat, count in counter.items() if count == highest_count]
    
    # Extract all counts, including the highest ones
    all_counts = [count for stat, count in counter.items()]
    all_counts_sorted = sorted(all_counts, reverse=True)

     # Convert "attack" to "strength" if needed
    most_common_stats = [stat if stat != "attack" else "strength" for stat in most_common_stats]
    
    # Join the counts with '/' and append the most common stats
    result = f"{'/'.join(map(str, all_counts_sorted))} {', '.join(most_common_stats)}"
    
    return result

# Apply the function to the stats column (assuming it's the 3rd column, i.e., column C)
df['Processed Stats'] = df.iloc[:, 2].apply(process_stats)

# Save the updated DataFrame back to a CSV with the result in a new column
output_file = 'equipment_processed.csv'
df.to_csv(output_file, index=False)

print(f"Processed data has been saved to {output_file}")

#run python process_stats.py
