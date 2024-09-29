from typing import List, Tuple
import pandas as pd
import re

def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Analyze Twitter data to find the top 10 count user names mentions
    
    Args:
    file_path (str): Path to file containing Twitter data.
    
    Returns:
    List[Tuple[str, int]]: Top 10 with most user names mentions
    """
    
    def chunk_generator():
        for chunk in pd.read_json(file_path, lines=True, chunksize=4000): # Miminimizamos el numero de lineas en cada batch da resultado
            yield process_chunk(chunk)
    
#    for chunk in chunks:
#        user_list = chunk['content'].apply(extract_user_mentions).explode()
#        users_count = user_list.to_frame(name='user_name').groupby('user_name').size().reset_index(name='count')
#        dfs.append(users_count)
    
    all_counts = pd.concat(chunk_generator(), ignore_index=True)
    final_counts = all_counts.groupby('user_name')['count'].sum().reset_index()
    top_10_days = final_counts.sort_values('count', ascending=False).head(10)    
    
    return [(row['user_name'], int(row['count'])) for _, row in top_10_days.iterrows()]

def process_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
    user_list = chunk['content'].apply(extract_user_mentions).explode()
    return user_list.to_frame(name='user_name').groupby('user_name').size().reset_index(name='count')

def extract_user_mentions(text: str) -> list:
    """Get user mentions in a given text."""
    return re.findall(r'@(\w+)', text)
