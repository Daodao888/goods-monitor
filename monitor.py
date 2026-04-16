import requests
import feedparser
import os
from datetime import datetime, timedelta, timezone

# --- 这里是你的配置区 ---
# 改用目前更稳定的镜像节点
BASE_URL = 'https://rss.bloonix.org/?type=twitter&user='

ACCOUNTS = [
    'oshinoko_love', 'animate_cafe', 'animateinfo', 'animejujutsuten',
    'AMNIBUS', 'Jumpcs_Shueisha', 'es_acrossstage', 'jujutsu_goods',
    'eeo_store', 'toman_goods', 'kujibikido', 'medicos_et_02',
    'anime_eupho', 'princesscafe333', 'kimetsu_off', 'kimetsugoods',
    'animehaikyu_com', 'NatsumeYujincho', 'kuroshitsuji_pr', 'naruto_check', 'OPcom_info'
]

# 暴力测试关键词：加了句号和空格，确保一定能抓到东西来验证通道
KEYWORDS = ["受注", "再販", "予約", "限定", "缶バッジ", "。", " "] 
# -----------------------

def send_discord_msg(content):
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if not webhook_url: return
    data = {"username": "谷子情报官", "content": content}
    try:
        requests.post(webhook_url, json=data, timeout=10)
    except:
        pass

def check_updates():
    now = datetime.now(timezone.utc)
    time_threshold = now - timedelta(hours=48) # 检查过去48小时

    print(f"--- 巡逻开始 ---")

    for user in ACCOUNTS:
        url = f"{BASE_URL}{user}"
        try:
            print(f"正在检查账号: @{user}")
            # 模拟浏览器访问
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=20)
            
            if response.status_code != 200:
                print(f"❌ 账号 @{user} 访问失败，错误码: {response.status_code}")
                continue
                
            feed = feedparser.parse(response.content)
            
            if not feed.entries:
                print(f"⚠️ 账号 @{user} 抓取成功但没内容（推特可能封锁了该请求）")
                continue

            for entry in feed.entries:
                # 尝试解析多种时间格式
                pub_parsed = entry.get('published_parsed') or entry.get('updated_parsed')
                if not pub_parsed: continue
                
                published_time = datetime(*pub_parsed[:6], tzinfo=timezone.utc)

                if published_time > time_threshold:
                    # 只要匹配到任何一个词
                    if any(word.lower() in entry.title.lower() for word in KEYWORDS):
                        print(f"✅ 发现符合条件的帖：{entry.title[:20]}...")
                        msg = f"🔔 **新情报：@{user}**\n\n**内容：** {entry.title}\n**链接：** {entry.link}"
                        send_discord_msg(msg)
                else:
                    break
        except Exception as e:
            print(f"🔥 检查 @{user} 时发生崩溃: {e}")

if __name__ == "__main__":
    check_updates()
