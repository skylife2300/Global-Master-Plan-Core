import os
import sys
import json
import subprocess
import re
import requests

# GitHub Secrets 비밀 금고에서 보안 주소를 메모리로 Bypass 호출 (평문 노출 0%)
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
STATE_FILE = "last_sales_state.json"
UPWORK_RSS_URL = os.getenv('UPWORK_RSS_URL', "https://upwork.com")

def run_global_sniper():
    # 금고가 열리지 않았을 때를 대비한 최소한의 예외 방어선
    if not WEBHOOK_URL:
        return
        
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
