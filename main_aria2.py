import urllib.parse
import json
import aria2p
import time
import subprocess
import requests
import sys

def get_json_data(keyword):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://thepiratebay.org'
    }
    url = f"https://apibay.org/q.php?q={keyword}&cat="
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.RequestException:
        return None

def generate_magnet_link(info_hash, name):
    magnet = f"magnet:?xt=urn:btih:{info_hash}"

    encoded_name = urllib.parse.quote(name, safe='')
    magnet += f"&dn={encoded_name}"

    trackers = [
        'udp://tracker.opentrackr.org:1337',
        'udp://open.stealth.si:80/announce',
        'udp://tracker.torrent.eu.org:451/announce',
        'udp://tracker.bittor.pw:1337/announce',
        'udp://public.popcorn-tracker.org:6969/announce',
        'udp://tracker.dler.org:6969/announce',
        'udp://exodus.desync.com:6969',
        'udp://open.demonii.com:1337/announce',
        'udp://glotorrents.pw:6969/announce',
        'udp://tracker.coppersurfer.tk:6969',
        'udp://torrent.gresille.org:80/announce',
        'udp://p4p.arenabg.com:1337',
        'udp://tracker.internetwarriors.net:1337'
    ]

    for tracker in trackers:
        encoded_tracker = urllib.parse.quote(tracker, safe='')
        magnet += f"&tr={encoded_tracker}"

    return magnet

print("Welcome to my tool!")
print("This tool will help you download torrent files using Aria2c and the Pirate Bay API.")
keyword = input("Type your search keyword: ")

results = get_json_data(keyword)

if not results or results[0].get('id') == '0':
    print("No torrents found.")
    sys.exit(0)

torrent_info = results[0]
final_link = generate_magnet_link(torrent_info["info_hash"], torrent_info["name"])

print(f"\nMagnet link:\n{final_link}")
print("\nStarting download...")

aria_process = subprocess.Popen(
    ['aria2c', '--enable-rpc', '--rpc-listen-all=true', '--rpc-allow-origin-all'],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
time.sleep(3)

try:
    aria2 = aria2p.API(aria2p.Client(host="http://localhost", port=6800, secret=""))
    download = aria2.add_magnet(final_link)
    print(f"Download started with GID: {download.gid}")

    while True:
        time.sleep(1)
        download.update()

        if download.has_failed:
            print(f"\nDownload failed: {download.error_message}")
            sys.exit(1)

        # Follow chained downloads (e.g. magnet metadata → actual torrent)
        if download.followed_by_ids:
            new_gid = download.followed_by_ids[0]
            download = aria2.get_download(new_gid)
            print(f"\nMetadata ready. Switching to file download (GID: {download.gid})...")
            continue

        if download.is_complete:
            break

        print(f"Progress: {download.progress_string()} | Speed: {download.download_speed_string()}", end='\r')

    print("\nDownload complete!")
finally:
    aria_process.terminate()