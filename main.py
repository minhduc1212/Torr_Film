import urllib.parse
import json
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


json_data = get_json_data("dune")[0]

torrent_info = json_data

# Gọi hàm để tạo link
final_link = generate_magnet_link(torrent_info["info_hash"], torrent_info["name"])

print("Link Magnet của bạn là:\n")
print(final_link)