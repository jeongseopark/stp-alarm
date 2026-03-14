import requests
import telegram
import asyncio
import os

# 1. 정보 가져오기
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

async def main():
    # 2. 봇 객체 생성
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    
    # 3. 테스트 메시지 강제 발송
    print("메시지 발송 시도 중...")
    try:
        await bot.send_message(chat_id=CHAT_ID, text="🔔 테스트 알림: 봇과 깃허브가 연결되었습니다!")
        print("발송 성공!")
    except Exception as e:
        print(f"발송 실패 에러: {e}")

if __name__ == "__main__":
    asyncio.run(main())
