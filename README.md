# Telegram 多账号自动签到工具

基于 `Telethon` 的 Telegram 多账号自动签到工具，支持多账号配置和 GitHub Actions 定时执行。

## 功能特性

- 支持多账号独立配置（每个账号有独立的 `api_id`、`api_hash`、`session`）
- 单个账号可向多个 Bot 发送不同消息
- 自动标记 bot 回复为已读
- 基于 GitHub Actions 每天自动执行

---

## 准备工作

### 1. 申请 Telegram API credentials

1. 访问 https://my.telegram.org
2. 登录后点击 "API development tools"
3. 创建一个应用，获取 `api_id` 和 `api_hash`

### 2. 生成 StringSession

StringSession 是账号的登录凭证，用于无需密码即可登录。

```bash
uv run python generate_session.py
```

按提示输入 `api_id`、`api_hash`、手机号和验证码。

---

## 配置文件

复制示例配置文件：

```bash
cp config.yaml.example config.yaml
```

编辑 `config.yaml`：

```yaml
accounts:
  - api_id: 12345
    api_hash: "your_api_hash"
    session: "YOUR_STRING_SESSION"
    tasks:
      - bot: "@bot_username"
        message: "/start"
      - bot: "@another_bot"
        message: "/checkin"

  - api_id: 67890
    api_hash: "another_api_hash"
    session: "ANOTHER_STRING_SESSION"
    tasks:
      - bot: "@third_bot"
        message: "/daily"
```

### 配置说明

| 字段 | 说明 |
|-----|------|
| `api_id` | Telegram API ID |
| `api_hash` | Telegram API Hash |
| `session` | StringSession 字符串 |
| `tasks` | 该账号要执行的任务列表 |
| `bot` | 目标 Bot 的用户名（@后面的部分）或用户ID |
| `message` | 要发送的消息 |

---

## 运行

### 本地运行

```bash
uv run python main.py
```

### GitHub Actions

#### 1. 添加 Secrets

在仓库 Settings → Secrets and variables → Actions 中添加：

| Secret 名称 | 说明 |
|------------|------|
| `TG_CONFIG` | 完整的 `config.yaml` 内容 |

#### 2. 触发方式

- **定时任务**：每天自动运行，由于 GitHub Actions 的队列延迟，真实运行时间不可预测
- **手动触发**：点击 Actions → Telegram Auto Check-in → Run workflow

---

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