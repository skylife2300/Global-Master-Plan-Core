import os
import json
import re
import requests
import subprocess

WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
UPWORK_RSS_URL = os.getenv('UPWORK_RSS_URL', "https://upwork.com")
# 1. 아키텍트의 검로드 상품 판매 주소 주입
GUMROAD_STORE_URL = "https://your_://gumroad.com" 

def run_global_sniper():
    if not WEBHOOK_URL:
        return
        
    try:
        # User-Agent 및 헤더 위장으로 업워크 보안망 우회 및 RSS 데이터 수집
        cmd = f'curl -s -L --max-time 15 -H "Accept: text/html,application/xhtml+xml,application/xml" -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "{UPWORK_RSS_URL}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        raw_xml = result.stdout
        
        item_content = re.findall(r'<item>(.*?)</item>', raw_xml, re.DOTALL)
        if not item_content:
            return
            
        # 최신 일감의 제목과 링크, 설명 파싱
        title = re.findall(r'<title>(.*?)</title>', item_content[0])
        link = re.findall(r'<link>(.*?)</link>', item_content[0])
        
        title_str = title[0] if title else "새로운 글로벌 일감 포획"
        link_str = link[0] if link else ""
        
        if link_str:
            # 2. 프리랜서를 검로드 결제로 유도하는 디스코드 스나이퍼 카드 구성
            discord_msg = {
                'embeds': [{
                    'title': f'🚨 **[글로벌 스나이퍼] {title_str}**',
                    'description': (
                        "🎯 **방금 전 세계 최고가 일감이 등록되었습니다!**\n"
                        "인도, 동유럽 경쟁자들을 제치고 이 일감을 100% 수주하고 싶으신가요?\n\n"
                        "👇 **아래 치트킷을 구매하고 1분 만에 제안서를 발송하세요!**"
                    ),
                    'url': link_str,
                    'color': 5814783,
                    'fields': [
                        {
                            'name': '💵 [초고속 프리패스] 수주 확률 99% 무기 장착',
                            'value': f'[👉 즉시 치트킷 다운로드 (Gumroad)]({GUMROAD_STORE_URL})',
                            'inline': False
                        }
                    ],
                    'footer': {
                        'text': 'Global Sniper Auto Run Engine | Powered by Google AI'
                    }
                }]
            }
            # 발송 격발
            requests.post(WEBHOOK_URL, json=discord_msg, timeout=10)
            
    except Exception as e:
        pass

if __name__ == "__main__":
    run_global_sniper()
