import requests
import feedparser
import os
from datetime import datetime, timedelta, timezone

# --- 这里是你的配置区 ---
# 使用了多个不同的稳定镜像站，通过混合使用来降低失败率
RSS_URLS = [
    # 镜像站 A (.moeyu.org)
    'https://rsshub.moeyu.org/twitter/user/animate_cafe', 
    'https://rsshub.moeyu.org/twitter/user/animateinfo', 
    'https://rsshub.moeyu.org/twitter/user/oshinoko_love', 
    'https://rsshub.moeyu.org/twitter/user/animejujutsuten',
    'https://rsshub.moeyu.org/twitter/user/AMNIBUS',
    # 镜像站 B (.at)
    'https://rsshub.at/twitter/user/Jumpcs_Shueisha',
    'https://rsshub.at/twitter/user/es_acrossstage',
    'https://rsshub.at/twitter/user/jujutsu_goods',
    'https://rsshub.at/twitter/user/eeo_store',
    'https://rsshub.at/twitter/user/toman_goods',
    # 镜像站 C (.wukon.me)
    'https://rsshub.wukon.me/twitter/user/kujibikido',
    'https://rsshub.wukon.me/twitter/user/medicos_et_02',
    'https://rsshub.wukon.me/twitter/user/anime_eupho',
    'https://rsshub.wukon.me/twitter/user/princesscafe333',
    'https://rsshub.wukon.me/twitter/user/kimetsu_off',
    'https://rsshub.wukon.me/twitter/user/kimetsugoods',
    'https://rsshub.wukon.me/twitter/user/animehaikyu_com',
    'https://rsshub.wukon.me/twitter/user/NatsumeYujincho',
    'https://rsshub.wukon.me/twitter/user/kuroshitsuji_pr',
    'https://rsshub.wukon.me/twitter/user/naruto_check',
    'https://rsshub.wukon.me/twitter/user/OPcom_info'
]

# 监控关键词
KEYWORDS = ["受注", "再販", "予約", "限定", "缶バッジ"] 
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
    # 检查过去 48 小时内的帖子，确保不漏掉情报
    time_threshold = now - timedelta(hours=48)
    
    # 用来记录已经处理过的链接，防止单次运行内重复推送
    processed_links = set()

    print(f"--- 巡逻开始 (UTC: {now.strftime('%Y-%m-%d %H:%M:%S')}) ---")

    for url in RSS_URLS:
        try:
            print(f"正在检查: {url.split('/')[-1]}")
            # 设置 15 秒超时保护
            response = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code != 200:
                continue
                
            feed = feedparser.parse(response.content)
            
            for entry in feed.entries:
                # 检查链接是否已处理过
                if entry.link in processed_links:
                    continue
                
                # 获取并解析发布时间
                pub_parsed = entry.get('published_parsed') or entry.get('updated_parsed')
                if not pub_parsed: continue
                published_time = datetime(*pub_parsed[:6], tzinfo=timezone.utc)

                # 判断逻辑：时间在48小时内 且 包含关键词
                if published_time > time_threshold:
                    if any(word in entry.title for word in KEYWORDS):
                        msg = f"🔔 **发现新情报！**\n\n**内容：** {entry.title}\n**发布时间：** {published_time.strftime('%Y-%m-%d %H:%M:%S')} (UTC)\n**链接：** {entry.link}"
                        send_discord_msg(msg)
                        processed_links.add(entry.link) # 标记为已处理
                else:
                    # RSS通常按时间倒序，看到旧帖即可跳过该账号
                    break
                    
        except Exception as e:
            print(f"账号 {url} 暂时无法访问，已跳过")

if __name__ == "__main__":
    check_updates()
