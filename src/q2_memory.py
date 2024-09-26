from typing import List, Tuple
import pandas as pd
import emoji

def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Analyze Twitter data to count emojis for the top 10 emojis.
    
    Args:
    file_path (str): Path to file containing Twitter data.
    
    Returns:
    List[Tuple[str, int]]: Top 10 days with most emojis and their emoji counts
    """
    
    chunks = pd.read_json(file_path, lines=True, chunksize=10000)
    
    dfs = []
    
    for chunk in chunks:
        emojis_list = chunk['content'].apply(extract_emojis).explode()
        emojis_count = emojis_list.to_frame(name='emoji').groupby('emoji').size().reset_index(name='count')
        dfs.append(emojis_count)
    
    all_counts = pd.concat(dfs)
    final_counts = all_counts.groupby('emoji')['count'].sum().reset_index()
    top_10_days = final_counts.sort_values('count', ascending=False).head(10)    
    
    return [(row['emoji'], int(row['count'])) for _, row in top_10_days.iterrows()]

def extract_emojis(text: str) -> list:
    """Get emojis in a given text."""
    return [x for x in text if x in emoji.EMOJI_DATA]
