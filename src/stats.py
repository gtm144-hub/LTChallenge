import csv
from datetime import datetime
from memory_profiler import memory_usage
from google.cloud import storage
from q1_memory import q1_memory
from q2_memory import q2_memory
from q3_memory import q3_memory
import time
import io
import os
import tempfile


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

    mem_row = [function.__name__, datetime.now().isoformat(), f"{avg_memory:.4f}", f"{max_memory:.4f}"]
    blob = bucket.blob(mem_name)

    if blob.exists():
        existing_csv = blob.download_as_text()
        csv_data = io.StringIO(existing_csv)
        csv_reader = csv.reader(csv_data)
        rows = list(csv_reader)
        blob.delete()
    else:
        rows = [['function', 'datetime', 'avg_memory_usage', 'max_memory_usage']]

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

def efficiency_update_csv_in_gcs(function, bucket_name, file_name, eff_name):
    
    temp_file_path = get_file_path(bucket_name, file_name)
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    start_time = time.time()
    mem_usage = memory_usage((function, (temp_file_path,), {}))
    total_time = time.time() - start_time

    eff_row = [function.__name__, datetime.now().isoformat(), f"{total_time:.4f}"]
    blob = bucket.blob(eff_name)

    if blob.exists():
        existing_csv = blob.download_as_text()
        csv_data = io.StringIO(existing_csv)
        csv_reader = csv.reader(csv_data)
        rows = list(csv_reader)
        blob.delete()
    else:
        rows = [['function', 'datetime', 'total_time']]

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

if __name__ == '__main__':
    bucket_name = 'test_jobs144'
    file_name = 'lt/farmers-protest-tweets-2021-2-4.json'
    mem_name = 'lt/results/memory_result.csv'
    eff_name = 'lt/results/efficiency_result.csv'

    memory_update_csv_in_gcs(q1_memory, bucket_name, file_name, mem_name)
    efficiency_update_csv_in_gcs(q1_memory, bucket_name, file_name, eff_name)
