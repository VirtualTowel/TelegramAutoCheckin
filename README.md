# Telegram 多账号自动签到工具

基于 `Telethon` 的 Telegram 多账号自动签到/任务执行工具，支持 GitHub Actions 定时运行。

## 功能特性

- 支持多账号独立配置（每个账号有不同的 `api_id`、`api_hash`、`session`）
- 单个账号可向多个 Bot 发送不同消息
- 自动标记 bot 回复为已读
- 支持 GitHub Actions 定时执行
- 本地配置文件 + 环境变量双模式

## 配置文件格式

复制 `config.yaml.example` 为 `config.yaml`：

```yaml
accounts:
  - api_id: 12345
    api_hash: "your_api_hash"
    session: "YOUR_STRING_SESSION_1"
    tasks:
      - bot: "@bot_username"
        message: "/start"
      - bot: "@another_bot"
        message: "/checkin"

  - api_id: 67890
    api_hash: "another_api_hash"
    session: "YOUR_STRING_SESSION_2"
    tasks:
      - bot: "@third_bot"
        message: "/daily"
```

## 获取 StringSession

运行以下命令生成 StringSession：

```bash
uv run python generate_session.py
```

按提示输入 `api_id`、`api_hash`、手机号和验证码。

## 本地运行

```bash
# 设置环境变量
export API_ID=your_api_id
export API_HASH=your_api_hash

# 或直接在 config.yaml 中配置

# 运行
uv run python main.py
```

## GitHub Actions 部署

### 1. 添加 Secrets

在 GitHub 仓库 Settings → Secrets and variables → Actions 中添加：

| Secret 名称 | 说明 |
|------------|------|
| `TG_CONFIG` | 完整的配置文件内容（YAML 格式） |

### 2. 定时执行

工作流已配置为每天 UTC 16:05（北京时间 00:05）自动运行。

也可手动触发：在 GitHub 仓库页面点击 Actions → Telegram Auto Check-in → Run workflow

## 目录结构

```
tg-auto-checkin/
├── .github/workflows/checkin.yml  # GitHub Actions 工作流
├── config.yaml.example             # 配置示例
├── generate_session.py            # StringSession 生成工具
├── main.py                        # 主程序
├── pyproject.toml
└── uv.lock
```

## 依赖

- Python >= 3.13
- Telethon >= 1.43.2
- PyYAML