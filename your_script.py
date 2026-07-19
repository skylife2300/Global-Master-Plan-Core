import os
import sys
import json
import subprocess
import re
import requests

# GitHub Secrets 비밀 금고에서 보안 주소를 메모리로 Bypass 호출
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
UPWORK_RSS_URL = os.getenv('UPWORK_RSS_URL', "https://upwork.com")
STATE_FILE = "last_sales_state.json"

# 🔥 [비즈니스 코어] 프리랜서들이 치트킷/가이드를 결제할 당신의 검로드 상품 판매 주소
GUMROAD_STORE_URL = "https://your_://gumroad.com"

def run_global_sniper():
    # 금고가 열리지 않았을 때를 대비한 최소한의 예외 방어선
    if not WEBHOOK_URL:
        return
        
    # 상태 파일 로드 및 초기화
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
        # User-Agent 위장 및 네트워크 커넥션 바이패스
        cmd = f'curl -s -L --max-time 15 -H "Accept: text/html,application/xhtml+xml,application/xml" -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "{UPWORK_RSS_URL}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        raw_xml = result.stdout
        
        # 업워크 RSS 피드에서 최신 일감 정보 추출
        item_content = re.findall(r'<item>(.*?)</item>', raw_xml, re.DOTALL)
        if not item_content:
            return
            
        title = re.findall(r'<title>(.*?)</title>', item_content[0])
        link = re.findall(r'<link>(.*?)</link>', item_content[0])
        
        title_str = title[0] if title else "🚨 [글로벌 실시간 일감 포획!]"
        link_str = link[0] if link else ""
        
        # 중복 알림을 완벽히 차단하고 새로운 일감일 때만 격발
        if link_str and link_str != state.get("last_job_link", ""):
            
            # 🔥 프리랜서의 지갑을 열게 만드는 고도화된 그로스해킹 디스코드 카드 
            discord_msg = {
                'embeds': [{
                    'title': f'🎯 **New High-Value Job Detected!**',
                    'description': (
                        f"**Job Title:** {title_str}\n\n"
                        "💡 *수많은 인도/동유럽 경쟁자들을 제치고 이 일감을 100% 수주하고 싶으신가요? "
                        "구글 AI가 분석한 상위 1% 프리랜서 전용 맞춤 제안서 템플릿과 자동화 무기를 지금 즉시 장착하세요.*"
                    ),
                    'url': link_str,
                    'color': 5814783,
                    'fields': [
                        {
                            'name': '💵 [초고속 프리패스] 수주 확률 99% 치트킷 다운로드',
                            'value': f'[👉 지금 검로드(Gumroad)에서 즉시 받기]({GUMROAD_STORE_URL})',
                            'inline': False
                        }
                    ],
                    'footer': {
                        'text': 'Global Sniper Auto Run Engine | Powered by Google AI'
                    }
                }]
            }
            
            # 디스코드 채널로 폭격
            requests.post(WEBHOOK_URL, json=discord_msg, timeout=10)
            
            # 전역 상태 갱신
            state["last_job_link"] = link_str
            state["total_captured"] = state.get("total_captured", 0) + 1
            
            with open(STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=4)
    except:
        pass

# 구매자의 성공 웹훅 격발 시 소스코드 제어 및 10% 후불 정산 추적망
def report_royalty_to_architect(job_budget, buyer_id):
    royalty_fee = job_budget * 0.10
    architect_webhook = os.getenv('DISCORD_WEBHOOK_URL')
    if not architect_webhook:
        return
    payload = {
        "content": f"🔥 [로컬 IP 대여 승전보] 구매자({buyer_id})가 {job_budget}달러 프로젝트 수주 성공! 청구 로열티: {royalty_fee}달러. 정산 대기."
    }
    requests.post(architect_webhook, json=payload)

if __name__ == "__main__":
    run_global_sniper()
