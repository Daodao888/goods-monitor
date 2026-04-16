import requests
import feedparser
import os
from datetime import datetime, timedelta, timezone

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
    'https://rsshub.app/twitter/user/OPcom_info'
]

# 监控关键词
KEYWORDS = ["受注", "再販", "予約", "限定", "缶バッジ"] 
# -----------------------

def send_discord_msg(content):
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if not webhook_url: return
    data = {"username": "谷子情报官", "content": content}
    try:
        # 增加超时保护，防止推送时卡住
        requests.post(webhook_url, json=data, timeout=10)
    except:
        pass

def check_updates():
    # 获取当前时间（UTC时间）
    now = datetime.now(timezone.utc)
    # 只要过去 24 小时内的帖子
    time_threshold = now - timedelta(hours=24)

    print(f"开始巡逻，当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')} UTC")

    for url in RSS_URLS:
        try:
            print(f"正在检查账号: {url.split('/')[-1]}")
            # 设置 15 秒超时，防止某个 RSS 链接卡死整个程序
            response = requests.get(url, timeout=15) 
            feed = feedparser.parse(response.content)
            
            for entry in feed.entries:
                # 获取帖子发布时间
                published_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

                # 判断：时间在24小时内 且 包含关键词
                if published_time > time_threshold:
                    if any(word in entry.title for word in KEYWORDS):
                        msg = f"🔔 **发现新情报！**\n\n**内容：** {entry.title}\n**发布时间：** {published_time.strftime('%Y-%m-%d %H:%M:%S')} (UTC)\n**链接：** {entry.link}"
                        send_discord_msg(msg)
                else:
                    # RSS通常按时间倒序，看到旧帖即可停止当前账号的检查
                    break
                    
        except Exception as e:
            print(f"访问 {url} 出错或超时，已跳过。错误信息: {e}")

if __name__ == "__main__":
    check_updates()
