import glob
import json
import time
import pandas as pd

def main():
    print("Starting convert\n")
    start_time = time.perf_counter()
    all_rows = []

    # Process all JSON files starting with "Streaming_History"
    for filename in glob.glob("Streaming_History*.json"):
        print(f"Processing file: {filename}")
        with open(filename, "r", encoding="utf8") as f:
            try:
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

            # Only include records with at least 30000ms played.
            if ms_played >= 30000:
                # Use (record.get(KEY) or "") to ensure a default empty string for None values.
                ts = (record.get("ts") or "").strip()
                artist = (record.get("master_metadata_album_artist_name") or "").strip()
                track = (record.get("master_metadata_track_name") or "").strip()

                all_rows.append([ts, artist, track])

    # Create a DataFrame from the collected rows.
    df = pd.DataFrame(all_rows, columns=["Timestamp", "Artist", "Track"])

    # Write to CSV; set header=False if you prefer no header row.
    df.to_csv('output.csv', index=False, header=False)

    elapsed_time = time.perf_counter() - start_time
    print(f"\nConvert finished in {elapsed_time:.2f} seconds.")

if __name__ == '__main__':
    main()
