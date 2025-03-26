import glob
import json
import time
import pandas as pd
import csv
from datetime import datetime

def main():
    print("Starting convert")
    start_time = time.perf_counter()
    all_rows = []

    # Process every file matching the pattern "Streaming_History*.json"
    for filename in glob.glob("Streaming_History*.json"):
        print(f"Processing file: {filename}")
        with open(filename, "r", encoding="utf8") as f:
            try:
                # Each file is assumed to be a JSON array of records.
                data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error reading {filename}: {e}")
                continue

        for record in data:
            try:
                ms_played = int(record.get("ms_played", 0))
            except (ValueError, TypeError):
                ms_played = 0

            # Skip records with less than 30 seconds played
            if ms_played < 30000:
                continue

            # Extract mandatory fields

            # Track (mandatory)
            track = (record.get("master_metadata_track_name") or "").strip()
            if not track:
                continue

            # Artist (mandatory) – using the album artist field as a proxy
            artist = (record.get("master_metadata_album_artist_name") or "").strip()
            if not artist:
                continue

            # Optional fields:
            album = (record.get("master_metadata_album_album_name") or "").strip()

            # Timestamp: convert from e.g. "2023-08-05T01:26:10Z" to "YYYY-MM-DD HH:MM:SS"
            ts_raw = (record.get("ts") or "").strip()
            timestamp = ""
            if ts_raw:
                try:
                    if ts_raw.endswith("Z"):
                        dt = datetime.strptime(ts_raw, "%Y-%m-%dT%H:%M:%SZ")
                    else:
                        dt = datetime.fromisoformat(ts_raw)
                    timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    timestamp = ts_raw  # Fallback if parsing fails

            # Album artist (optional); in many cases it's the same as artist
            album_artist = (record.get("master_metadata_album_artist_name") or "").strip()

            # Duration in seconds (ms_played is in milliseconds)
            duration = str(ms_played // 1000)

            # Append the row in the required order:
            # "{artist}", "{track}", "{album}", "{timestamp}", "{album artist}", "{duration}"
            all_rows.append([artist, track, album, timestamp, album_artist, duration])

    # Create a DataFrame from the collected rows.
    df = pd.DataFrame(all_rows, columns=["artist", "track", "album", "timestamp", "album_artist", "duration"])
    # Write to CSV with all fields quoted and no header row.
    df.to_csv("output.csv", index=False, header=False, quoting=csv.QUOTE_ALL)

    elapsed = time.perf_counter() - start_time
    print(f"Convert finished in {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()
