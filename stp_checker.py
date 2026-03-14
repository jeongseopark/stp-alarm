import requests
from bs4 import BeautifulSoup
import telegram
import asyncio
import os

# 깃허브 Secrets에 저장한 값을 불러옵니다.
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

URLS = {
    "SBB 공식홈": "https://www.sbb.ch/en/leisure-holidays/inspiration/international-guests/swiss-travel-pass.html",
    "클룩(Klook)": "https://www.klook.com/ko/activity/1130-swiss-travel-pass/"
}

async def send_msg(text):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=text)

def check():
    results = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    for name, url in URLS.items():
        try:
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            text = soup.get_text().lower()
            # 1등석(1st class)과 할인 관련 키워드 감시
            if "1st class" in text and ("promotion" in text or "sale" in text or "discount" in text or "할인" in text):
                results.append(f"✅ [{name}] 1등석 할인 가능성 감지! 확인: {url}")
        except:
            print(f"{name} 접속 실패")
    return results

async def main():
    found = check()
    if found:
        await send_msg("🚨 STP 특가 알림! 🚨\n\n" + "\n".join(found))
    else:
        print("아직 할인 정보가 없습니다.")

if __name__ == "__main__":
    asyncio.run(main())
