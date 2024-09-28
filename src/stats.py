import csv
from datetime import datetime
from memory_profiler import memory_usage
from google.cloud import storage
from q1_memory import q1_memory
from q2_memory import q2_memory
from q3_memory import q3_memory
from q1_time import q1_time
from q2_time import q2_time
from q3_time import q3_time
import pandas as pd
import time
import io
import os
import tempfile

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../sa.json"

def get_file_path(bucket_name, file_name):
    
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    file_blob = bucket.blob(file_name)

    # Create a temporary file
    _, temp_local_filename = tempfile.mkstemp()

    # Download the file to the temporary file
    file_blob.download_to_filename(temp_local_filename)

    return temp_local_filename


def memory_update_csv_in_gcs(function, bucket_name, file_name, mem_name):
    
    temp_file_path = get_file_path(bucket_name, file_name)
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    #Profile the function
    mem_usage = memory_usage((function, (temp_file_path,), {}))
    avg_memory = sum(mem_usage) / len(mem_usage)
    max_memory = max(mem_usage)

    mem_row = [function.__name__, int(datetime.utcnow().timestamp()), f"{avg_memory:.4f}", f"{max_memory:.4f}"]
    blob = bucket.blob(mem_name)

    if blob.exists():
        existing_csv = blob.download_as_text()
        csv_data = io.StringIO(existing_csv)
        csv_reader = csv.reader(csv_data)
        rows = list(csv_reader)
        
        df = pd.DataFrame(rows[1:], columns=rows[0])
        filtered_df = df[df['function'] == function.__name__].sort_values(by='timestamp').iloc[-1]
        
        if float(filtered_df['avg_memory_usage']) <= avg_memory and float(filtered_df['max_memory_usage']) <= max_memory: return False
        
        blob.delete()
    else:
        rows = [['function', 'timestamp', 'avg_memory_usage', 'max_memory_usage']]

    # Add new row
    rows.append(mem_row)
    
    # Prepare updated CSV data
    updated_csv = io.StringIO()
    csv_writer = csv.writer(updated_csv)
    csv_writer.writerows(rows)
    
    # Upload updated CSV to GCS
    blob.upload_from_string(updated_csv.getvalue(), content_type='text/csv')

    print(f"CSV updated and uploaded to gs://{bucket_name}/{mem_name}")
    print(mem_row)

    return True

def efficiency_update_csv_in_gcs(function, bucket_name, file_name, eff_name):
    
    temp_file_path = get_file_path(bucket_name, file_name)
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    start_time = time.time()
    mem_usage = memory_usage((function, (temp_file_path,), {}))
    total_time = time.time() - start_time

    eff_row = [function.__name__, int(datetime.utcnow().timestamp()), f"{total_time:.4f}"]
    blob = bucket.blob(eff_name)

    if blob.exists():
        existing_csv = blob.download_as_text()
        csv_data = io.StringIO(existing_csv)
        csv_reader = csv.reader(csv_data)
        rows = list(csv_reader)

        df = pd.DataFrame(rows[1:], columns=rows[0])
        filtered_df = df[df['function'] == function.__name__].sort_values(by='timestamp').iloc[-1]
        
        if float(filtered_df['total_time']) <= total_time: return False
        
        blob.delete()
    else:
        rows = [['function', 'timestamp', 'total_time']]

    # Add new row
    rows.append(eff_row)
    
    # Prepare updated CSV data
    updated_csv = io.StringIO()
    csv_writer = csv.writer(updated_csv)
    csv_writer.writerows(rows)
    
    # Upload updated CSV to GCS
    blob.upload_from_string(updated_csv.getvalue(), content_type='text/csv')

    print(f"CSV updated and uploaded to gs://{bucket_name}/{eff_name}")
    print(eff_row)

    return True

if __name__ == '__main__':
    bucket_name = 'test_jobs144'
    file_name = 'lt/farmers-protest-tweets-2021-2-4.json'
    #file_name = 'lt/twitter_test.json'
    mem_name = 'lt/results/memory_result.csv'
    eff_name = 'lt/results/efficiency_result.csv'

    is_q1_mem = memory_update_csv_in_gcs(q1_memory, bucket_name, file_name, mem_name)
    is_q2_mem = memory_update_csv_in_gcs(q2_memory, bucket_name, file_name, mem_name)
    is_q3_mem = memory_update_csv_in_gcs(q3_memory, bucket_name, file_name, mem_name)
    
    is_q1_eff = efficiency_update_csv_in_gcs(q1_time, bucket_name, file_name, eff_name)
    is_q2_eff = efficiency_update_csv_in_gcs(q2_time, bucket_name, file_name, eff_name)
    is_q3_eff = efficiency_update_csv_in_gcs(q3_time, bucket_name, file_name, eff_name)

    bool_list = [is_q1_mem, is_q2_mem, is_q3_mem,
                is_q1_eff, is_q2_mem, is_q3_eff]

    assert not all(value is False for value in bool_list), "AssertionError: Optimization metrics should improve not decrease."
