from typing import List, Tuple, Generator
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
    
    def process_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
        emojis_series = chunk['content'].apply(extract_emojis).explode() # Intente reducir memoria con sparse o category pero no baja 
        return emojis_series.value_counts().reset_index(name='count')

    def chunk_generator():
        for chunk in pd.read_json(file_path, lines=True, chunksize=4000): # Miminimizamos el numero de lineas en cada batch da resultado
            yield process_chunk(chunk)

    emoji_counts = pd.concat(chunk_generator(), ignore_index=True)
    
    final_counts = emoji_counts.groupby('content')['count'].sum().reset_index()
    top_10_days = final_counts.sort_values('count', ascending=False).head(10)

    return list(zip(top_10_days['content'], top_10_days['count'].astype(int)))

def extract_emojis(text: str) -> list:
    """Get emojis in a given text."""
    return [x for x in text if x in emoji.EMOJI_DATA]
