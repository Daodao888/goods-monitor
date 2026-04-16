import requests
import feedparser
import os

# --- 这里是你的配置区 ---
RSS_URLS = [
    'https://rsshub.app/twitter/user/animate_cafe', 
    'https://rsshub.app/twitter/user/animateinfo'
]
KEYWORDS = ["受注", "再販", "予約", "限定", "缶バッジ"] 
# -----------------------

def send_discord_msg(content):
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if not webhook_url: return
    data = {"username": "谷子情报官", "content": content}
    requests.post(webhook_url, json=data)

def check_updates():
    for url in RSS_URLS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                if any(word in entry.title for word in KEYWORDS):
                    msg = f"🔔 **发现新情报！**\n\n**内容：** {entry.title}\n**链接：** {entry.link}"
                    send_discord_msg(msg)
        except:
            pass

if __name__ == "__main__":
    check_updates()
