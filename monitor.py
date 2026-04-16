import requests
import feedparser
import os

# --- 这里是你的配置区 ---
RSS_URLS = [
    'https://rsshub.app/twitter/user/animate_cafe', 
    'https://rsshub.app/twitter/user/animateinfo', 
    'https://rsshub.app/twitter/user/oshinoko_love', 
    'https://rsshub.app/twitter/user/animejujutsuten',
    'https://rsshub.app/twitter/user/AMNIBUS',
    'https://rsshub.app/twitter/user/Jumpcs_Shueisha',
    'https://rsshub.app/twitter/user/es_acrossstage',
    'https://rsshub.app/twitter/user/jujutsu_goods',
     'https://rsshub.app/twitter/user/animateinfo',
    'https://rsshub.app/twitter/user/eeo_store',
    'https://rsshub.app/twitter/user/toman_goods',
    'https://rsshub.app/twitter/user/kujibikido',
    'https://rsshub.app/twitter/user/medicos_et_02',
    'https://rsshub.app/twitter/user/anime_eupho',
    'https://rsshub.app/twitter/user/princesscafe333',
    'https://rsshub.app/twitter/user/kimetsu_off',
    'https://rsshub.app/twitter/user/kimetsugoods',
    'https://rsshub.app/twitter/user/animehaikyu_com',
    'https://rsshub.app/twitter/user/NatsumeYujincho',
    'https://rsshub.app/twitter/user/kuroshitsuji_pr',
    'https://rsshub.app/twitter/user/naruto_check',
    'https://rsshub.app/twitter/user/OPcom_info',
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
