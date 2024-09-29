from typing import List, Tuple
import multiprocessing as mp
from functools import partial
import pandas as pd
import emoji

def q2_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Analyze Twitter data to count emojis for the top 10 emojis.
    
    Args:
    file_path (str): Path to file containing Twitter data.
    
    Returns:
    List[Tuple[str, int]]: Top 10 days with most emojis and their emoji counts
    """
    
    chunks = pd.read_json(file_path, lines=True, chunksize=2000) # Reducimos el tamano de las particiones sin sobrepasarnos para reducir el small file problems
    
    num_cores = mp.cpu_count()
    
    with mp.Pool(num_cores) as pool:
        dfs = pool.map(process_chunk, chunks) #Procesaremos chunks en paralelo
    
    all_counts = pd.concat(dfs)
    final_counts = all_counts.groupby('emoji')['count'].sum().reset_index()
    top_10_days = final_counts.sort_values('count', ascending=False).head(10)
    
    return list(zip(top_10_days['emoji'], top_10_days['count'].astype(int)))

def extract_emojis(text: str) -> list:
    """Get emojis in a given text."""
    return [x for x in text if x in emoji.EMOJI_DATA]

def process_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
    emojis_list = chunk['content'].apply(extract_emojis).explode()
    return emojis_list.to_frame(name='emoji').groupby('emoji').size().reset_index(name='count')
