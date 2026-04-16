import requests
import feedparser
import os
from datetime import datetime, timedelta, timezone

# --- 这里是你的配置区 ---
# 批量更换为 .moeyu.org 镜像站，通常比 .app 更稳
RSS_URLS = [
    'https://rsshub.moeyu.org/twitter/user/animate_cafe', 
    'https://rsshub.moeyu.org/twitter/user/animateinfo', 
    'https://rsshub.moeyu.org/twitter/user/oshinoko_love', 
    'https://rsshub.moeyu.org/twitter/user/animejujutsuten',
    'https://rsshub.moeyu.org/twitter/user/AMNIBUS',
    'https://rsshub.moeyu.org/twitter/user/Jumpcs_Shueisha',
    'https://rsshub.moeyu.org/twitter/user/es_acrossstage',
    'https://rsshub.moeyu.org/twitter/user/jujutsu_goods',
    'https://rsshub.moeyu.org/twitter/user/eeo_store',
    'https://rsshub.moeyu.org/twitter/user/toman_goods',
    'https://rsshub.moeyu.org/twitter/user/kujibikido',
    'https://rsshub.moeyu.org/twitter/user/medicos_et_02',
    'https://rsshub.moeyu.org/twitter/user/anime_eupho',
    'https://rsshub.moeyu.org/twitter/user/princesscafe333',
    'https://rsshub.moeyu.org/twitter/user/kimetsu_off',
    'https://rsshub.moeyu.org/twitter/user/kimetsugoods',
    'https://rsshub.moeyu.org/twitter/user/animehaikyu_com',
    'https://rsshub.moeyu.org/twitter/user/NatsumeYujincho',
    'https://rsshub.moeyu.org/twitter/user/kuroshitsuji_pr',
    'https://rsshub.moeyu.org/twitter/user/naruto_check',
    'https://rsshub.moeyu.org/twitter/user/OPcom_info'
]

# 临时放宽关键词和时间进行【暴力测试】
KEYWORDS = ["受注", "再販", "予約", "限定", "缶バッジ", "。"] # 加了个句号，基本必中
# -----------------------

def send_discord_msg(content):
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if not webhook_url: return
    data = {"username": "谷子情报官", "content": content}
    try:
        requests.post(webhook_url, json=data, timeout=10)
    except Exception as e:
        print(f"推送 Discord 失败: {e}")

def check_updates():
    now = datetime.now(timezone.utc)
    # 暂时设为 48 小时，确保能抓到内容验证功能
    time_threshold = now - timedelta(hours=48)

    for url in RSS_URLS:
        try:
            print(f"正在尝试抓取: {url}")
            response = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
            
            if response.status_code != 200:
                print(f"❌ 链接失效 (状态码: {response.status_code}): {url}")
                continue
                
            feed = feedparser.parse(response.content)
            if not feed.entries:
                print(f"⚠️ 抓取成功但该账号暂时没发帖: {url}")
                continue

            for entry in feed.entries:
                published_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                if published_time > time_threshold:
                    if any(word in entry.title for word in KEYWORDS):
                        msg = f"🔔 **发现新情报！**\n\n**内容：** {entry.title}\n**时间：** {published_time.strftime('%Y-%m-%d %H:%M:%S')}\n**链接：** {entry.link}"
                        send_discord_msg(msg)
                else:
                    break
        except Exception as e:
            print(f"访问 {url} 彻底挂了: {e}")

if __name__ == "__main__":
    check_updates()
