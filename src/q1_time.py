from typing import List, Tuple
from datetime import datetime
import multiprocessing as mp
from functools import partial
import pandas as pd


def process_chunk(chunk):
        chunk['date'] = pd.to_datetime(chunk['date']).dt.date
        chunk['user'] = chunk['user'].apply(lambda x: x['username'])
        return chunk.groupby(['user', 'date']).size().reset_index(name='count')

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    Analyze Twitter data to find the top 10 days with most tweets.

    Args:
    file_path (str): Path to file containing Twitter data.

    Returns:
     List[Tuple[datetime.date, str]]: Top 10 days with most tweets and users with most tweets
    """

    chunks = pd.read_json(file_path, lines=True, chunksize=2000) # Reducimos el tamano de las particiones sin sobrepasarnos para reducir el small file problems
    
    num_cores = mp.cpu_count()
    
    with mp.Pool(num_cores) as pool:
        dfs = pool.map(process_chunk, chunks)
    
    all_chunk_counts = pd.concat(dfs)
    final_counts = all_chunk_counts.groupby('date')['count'].sum().reset_index()
    top_10_days = final_counts.sort_values('count', ascending=False).head(10)

    ch = pd.merge(top_10_days['date'], all_chunk_counts, on='date', how='left')
    final_counts = ch.groupby(['user', 'date'])['count'].sum().reset_index()
    final_counts['row_number'] = final_counts.groupby('date')['count'].rank(method='first', ascending=False).astype(int)
    
    df = final_counts[final_counts['row_number'] == 1]
    
    return list(zip(df['date'], df['user'])) 
