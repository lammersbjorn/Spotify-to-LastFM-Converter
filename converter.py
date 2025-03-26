import glob
import json
import time
import pandas as pd

def main():
    print("Starting convert\n")
    start_time = time.perf_counter()
    all_rows = []

    # This will find all files whose names start with "Streaming_History" and end with .json.
    for filename in glob.glob("Streaming_History*.json"):
        print(f"Processing file: {filename}")
        with open(filename, "r", encoding="utf8") as f:
            try:
                # Each file is assumed to contain a JSON array of records.
                data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error loading JSON from {filename}: {e}")
                continue

        # Process each record in the JSON data.
        for record in data:
            try:
                ms_played = int(record.get("ms_played", 0))
            except (ValueError, TypeError):
                ms_played = 0

            # Only include records with at least 30,000 ms played.
            if ms_played >= 30000:
                # Extract the timestamp, artist name, and track name.
                ts = record.get("ts", "").strip()
                artist = record.get("master_metadata_album_artist_name", "").strip()
                track = record.get("master_metadata_track_name", "").strip()

                # Append a row with the desired fields.
                all_rows.append([ts, artist, track])

    # Create a DataFrame from the collected records.
    # You can change the list of column names or remove the header in the CSV output as needed.
    df = pd.DataFrame(all_rows, columns=["Timestamp", "Artist", "Track"])

    # Write the combined data to output.csv.
    # Set header=False if you do not want a header row in your CSV.
    df.to_csv('output.csv', index=False, header=False)

    elapsed_time = time.perf_counter() - start_time
    print(f"\nConvert finished in {elapsed_time:.2f} seconds.")

if __name__ == '__main__':
    main()
