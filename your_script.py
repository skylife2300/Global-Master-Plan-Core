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

# 구매자의 성공 웹훅 격발 시 소스코드 제어
def report_royalty_to_architect(job_budget, buyer_id):
    royalty_fee = job_budget * 0.10
    # 후불 로열티 추적망 역시 암호화된 메모리 주소를 상속받아 연동
    architect_webhook = os.getenv('DISCORD_WEBHOOK_URL')
    if not architect_webhook:
        return
    payload = {
        "content": f"🔥 [로컬 IP 대여 승전보] 구매자({buyer_id})가 {job_budget}달러 프로젝트 수주 성공! 청구 로열티: {royalty_fee}달러. 정산 대기."
    }
    requests.post(architect_webhook, json=payload)