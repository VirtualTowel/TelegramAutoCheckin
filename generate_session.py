"""
生成 Telethon StringSession 的工具
运行: uv run python generate_session.py
"""
import asyncio

from telethon import TelegramClient
from telethon.sessions import StringSession


async def main():
    api_id = input("请输入 API ID: ").strip()
    api_hash = input("请输入 API Hash: ").strip()

    async with TelegramClient(StringSession(), int(api_id), api_hash) as client:
        print("\n" + "=" * 60)
        print("StringSession 生成成功！")
        print("=" * 60)
        print(client.session.save())
        print("=" * 60)
        print("\n请将此字符串保存到 config.yaml 或 GitHub Secrets 中")


if __name__ == "__main__":
    asyncio.run(main())
