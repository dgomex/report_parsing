import argparse
import os
import shutil
from src.report_parser.report_parser import ReportParser

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process report files in a directory.")
    parser.add_argument('--reports_path', type=str, required=True, help='Path to the directory containing report files')
    parser.add_argument('--output_path', type=str, required=False, help='Path to the directory to save processed files')
    parser.add_argument('--persist_kv', action='store_true', help='Flag to persist key-value pairs')
    args = parser.parse_args()

    reports_path = args.reports_path
    output_path = args.output_path
    persist_kv = args.persist_kv
    processed_dir = os.path.join(reports_path, 'files_processed')
    os.makedirs(processed_dir, exist_ok=True)

    for filename in os.listdir(reports_path):
        file_path = os.path.join(reports_path, filename)
        if os.path.isfile(file_path) and not filename.startswith('.') and filename != 'files_processed':
            try:
                ReportParser(file_path).process_file(output_dir=output_path, is_kv_persisted=persist_kv)
                shutil.move(file_path, os.path.join(processed_dir, filename))
                print(f"Processed and moved: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")