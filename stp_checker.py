import requests
from bs4 import BeautifulSoup
import telegram
import asyncio
import os

# 깃허브 Secrets 환경변수
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

# 감시할 사이트 리스트 (2024 최신 주소 반영)
URLS = {
    "SBB(공식)": "https://www.sbb.ch/en/offers/swiss-travel-pass",
    "클룩(Klook)": "https://www.klook.com/ko/activity/11366-swiss-travel-rail-pass/",
    "마이리얼트립": "https://experiences.myrealtrip.com/products/3852623"
}

# 잡고 싶은 할인 키워드 (영어/한국어 믹스)
PROMO_KEYWORDS = ['promotion', 'special offer', 'free days', 'discount', '할인', '특가', '얼리버드', '프로모션', '쿠폰']

async def send_msg(text):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=text)

def check_promotions():
    results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    for name, url in URLS.items():
        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code != 200:
                continue
                
            soup = BeautifulSoup(res.text, 'html.parser')
            text = soup.get_text().lower()
            
            # 1. 어떤 좌석 등급이 언급되었는지 확인
            found_classes = []
            if "1st class" in text or "1등석" in text or "first class" in text:
                found_classes.append("1등석")
            if "2nd class" in text or "2등석" in text or "second class" in text:
                found_classes.append("2등석")
                
            # 2. 좌석 등급이 하나라도 확인되었고, 프로모션 키워드가 있는지 확인
            if found_classes:
                found_keywords = [kw for kw in PROMO_KEYWORDS if kw in text]
                
                if found_keywords:
                    class_str = " 및 ".join(found_classes)
                    kw_str = ", ".join(found_keywords)
                    results.append(f"🎯 [{name}] {class_str} 특가 의심!\n- 감지된 단어: {kw_str}\n- 링크: {url}")
        except Exception as e:
            print(f"{name} 크롤링 중 에러: {e}")
            
    return results

async def main():
    alerts = check_promotions()
    
    if alerts:
        final_message = "🚨 스위스 트래블 패스(STP) 감시망 작동! 🚨\n\n" + "\n\n".join(alerts)
        await send_msg(final_message)
    else:
        print("현재 새로운 프로모션 키워드가 발견되지 않았습니다.")

if __name__ == "__main__":
    asyncio.run(main())
