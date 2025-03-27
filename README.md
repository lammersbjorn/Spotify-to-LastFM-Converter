# Spotify to LastFM

Converts your Spotify streaming history JSON files into a CSV format suitable for importing into Universal Scrobbler, allowing you to add it to your Last.fm profile.

## Prerequisites

1.  **Spotify Data Request:** Request your personal Spotify data in the data rights and privacy settings. Instructions can be found here: [https://www.spotify.com/account/privacy/](https://www.spotify.com/account/privacy/) (availability may vary by region).

2.  **Python 3.6+:** Ensure you have Python 3.6 or a later version installed.

## Installation

1.  **Clone the repository (or download the script):**  Download the `converter.py` script and place it in a directory of your choice.

2.  **Install Dependencies:**  Navigate to the directory containing the script in your terminal and run:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Place JSON Files:** Put all the `Streaming_History*.json` files from your Spotify data export in the same directory as the `converter.py` script.

2.  **Run the Conversion:**  Open a terminal, navigate to the script's directory, and run the script.  You can customize the minimum playback time using the `--threshold` argument:

    ```bash
    python converter.py --threshold 30000
    ```

    *   `--threshold`:  Specifies the minimum play time in milliseconds for a song to be included in the output. The default value is 30000 (30 seconds).

3.  **Output File:**  The script will generate a file named `output.csv` in the same directory. This file contains your Spotify history in a format suitable for Universal Scrobbler.

4.  **Process Multiple Files:** The script automatically processes all files matching the pattern `Streaming_History*.json` in the directory.  No need to rename or move files individually.

## Importing into Last.fm via Universal Scrobbler

1.  **Universal Scrobbler:** Go to [https://universalscrobbler.com](https://universalscrobbler.com/).

2.  **Manual Scrobbling:** Choose "Scrobble manually in bulk".

3.  **Connect Last.fm:** Connect your Last.fm profile.

4.  **Premium Subscription:** You'll need a premium subscription for Universal Scrobbler (approximately \$1 per month). One month should be sufficient for a one-time import.

5.  **Copy and Paste:** Copy the contents of the `output.csv` file into the bulk scrobbler.

6.  **Scrobble:** Submit the scrobbles. Be aware of the daily limit (approximately 2800 scrobbles).

## Optional: Album Attribution

The imported songs won't automatically be attributed to their respective albums. To solve this, you can upgrade to a Last.fm Pro subscription and follow the steps described here: [https://github.com/RudeySH/lastfm-bulk-edit](https://github.com/RudeySH/lastfm-bulk-edit)

