"""
Telegram 多账号自动签到工具
"""
import os
import sys
import asyncio
import logging
from typing import Any

import yaml
from telethon import TelegramClient
from telethon.sessions import StringSession

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger("telethon").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def load_config() -> dict[str, Any]:
    """加载配置，优先使用环境变量，其次使用配置文件"""
    config_str = os.getenv("TG_CONFIG")
    if config_str:
        logger.info("从环境变量 TG_CONFIG 加载配置")
        return yaml.safe_load(config_str)

    config_path = "config.yaml"
    if os.path.exists(config_path):
        logger.info(f"从文件 {config_path} 加载配置")
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    logger.error("未找到配置文件，请设置 TG_CONFIG 环境变量或创建 config.yaml")
    sys.exit(1)


async def run_account(account: dict) -> None:
    """执行单个账号的任务"""
    api_id = account.get("api_id")
    api_hash = account.get("api_hash")
    session = account.get("session", "")
    tasks = account.get("tasks", [])

    if not api_id or not api_hash:
        logger.error("账号配置缺少 api_id 或 api_hash")
        return
    if not session:
        logger.warning("跳过无效账号配置（缺少 session）")
        return

    async with TelegramClient(StringSession(session), int(api_id), api_hash) as client:
        me = await client.get_me()
        logger.info(f"登录账号: {me.first_name} (ID: {me.id})")

        for task in tasks:
            bot = task.get("bot", "")
            message = task.get("message", "")
            if not bot or not message:
                continue
            try:
                await client.send_message(bot, message)
                logger.info(f"  -> 发送给 {bot}: {message[:30]}...")
            except Exception as e:
                logger.error(f"  -> 发送给 {bot} 失败: {e}")


async def main() -> None:
    config = load_config()
    accounts = config.get("accounts", [])

    if not accounts:
        logger.warning("配置中没有账号")
        return

    for i, account in enumerate(accounts):
        logger.info(f"开始处理账号 {i + 1}/{len(accounts)}...")
        await run_account(account)

    logger.info("所有账号任务执行完成")


if __name__ == "__main__":
    asyncio.run(main())
