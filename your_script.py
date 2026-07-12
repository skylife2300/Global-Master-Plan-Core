import os
import sys
import json
import subprocess
import re
import requests

WEBHOOK_URL = 'https://discordapp.com'
STATE_FILE = "last_sales_state.json"
UPWORK_RSS_URL = os.getenv('UPWORK_RSS_URL', "https://upwork.com")

def run_global_sniper():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                state = json.load(f)
        except:
            state = {"last_job_link": "", "total_captured": 0, "system_locked": False}
    else:
        state = {"last_job_link": "", "total_captured": 0, "system_locked": False}
        
    if state.get("system_locked", False): 
        return
        
    try:
        cmd = f'curl -s -L --max-time 15 -H "Accept: text/html,application/xhtml+xml,application/xml" -A "Mozilla/5.0" "{UPWORK_RSS_URL}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        raw_xml = result.stdout
        
        item_content = re.findall(r'<item>(.*?)</item>', raw_xml, re.DOTALL)
        link = re.findall(r'<link>(.*?)</link>', item_content[0]) if item_content else []
        link = link[0] if link else ""
        
        if link and link != state.get("last_job_link", ""):
            discord_msg = {
                'embeds': [{
                    'title': '🚨 **[마스터플랜] 글로벌 실시간 일감 포획!**',
                    'description': 'Bypass Connection Successful.',
                    'url': link,
                    'color': 5814783
                }]
            }
            requests.post(WEBHOOK_URL, json=discord_msg, timeout=10)
            state["last_job_link"] = link
            with open(STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=4)
    except:
        pass

if __name__ == "__main__":
    run_global_sniper()
