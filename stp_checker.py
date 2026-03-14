async def main():
    found = check()
    # 테스트를 위해 할인이 없어도 알림을 보내게 수정합니다
    if not found:
        await send_msg("🤖 봇이 정상 작동 중입니다! 현재는 STP 1등석 할인 정보가 없습니다.")
    else:
        await send_msg("🚨 STP 특가 알림! 🚨\n\n" + "\n".join(found))
