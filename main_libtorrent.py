import urllib.parse
import libtorrent as lt
import json
import time
import requests

def get_json_data(keyword):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://thepiratebay.org'
    }
    url = f"https://apibay.org/q.php?q={keyword}&cat="
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def generate_magnet_link(info_hash, name): 
    magnet = f"magnet:?xt=urn:btih:{info_hash}"
    
    #encode name
    encoded_name = urllib.parse.quote(name, safe='')
    magnet += f"&dn={encoded_name}"
    
    #trackers list
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
print("Type your search keyword: ")
keyword = input()
json_data = get_json_data(keyword)[0]

print("Type the path to save the downloaded file (e.g., C:/Downloads/): ")
save_path = input()

torrent_info = json_data

#Create magnet link
final_link = generate_magnet_link(torrent_info["info_hash"], torrent_info["name"])

print("Link Magnet của bạn là:\n")
print(final_link)
print("Download started...")


#create session
ses = lt.session({'listen_interfaces': '0.0.0.0:6881'})

# Analyze magnet link
params = lt.parse_magnet_uri(final_link)
params["save_path"] = save_path

#start session
handle = ses.add_torrent(params)
while not handle.has_metadata():
    time.sleep(1)
    
#start download
while not handle.is_seed(): # Chạy cho đến khi tải xong (chuyển sang chế độ seed)
    s = handle.status()
    
    # Tính toán thông số
    progress = s.progress * 100
    download_speed = s.download_rate / 1000  # Chuyển đổi sang kB/s
    peers = s.num_peers
    
    print(f"Tiến độ: {progress:.2f}% | Tốc độ: {download_speed:.1f} kB/s | Peers: {peers}", end='\r')
    time.sleep(1)