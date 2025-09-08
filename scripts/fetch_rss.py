import feedparser
import json
import datetime
from pathlib import Path

def fetch_feeds():
    # 读取配置
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    all_items = []
    
    for source in config['sources']:
        feed = feedparser.parse(source['url'])
        
        for entry in feed.entries[:10]:  # 每个源最多10条
            item = {
                'title': entry.title,
                'link': entry.link,
                'published': entry.get('published', ''),
                'source': source['name'],
                'category': source['category'],
                'retention_days': source['retention_days']
            }
            all_items.append(item)
    
    # 合并历史数据并清理过期内容
    existing_data = []
    if Path('data/feeds.json').exists():
        with open('data/feeds.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    
    # 去重和清理逻辑
    merged_data = merge_and_clean(all_items, existing_data)
    
    # 保存数据
    with open('data/feeds.json', 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)

def merge_and_clean(new_items, existing_items):
    # 实现去重和过期清理逻辑
    # ...
    return merged_items

if __name__ == '__main__':
    fetch_feeds()
