import feedparser
import json
import datetime
from pathlib import Path

def fetch_feeds():
    # 确保data目录存在
    Path('data').mkdir(exist_ok=True)
    
    # 读取配置
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    all_items = []
    
    for source in config['sources']:
        try:
            print(f"Fetching {source['name']}...")
            feed = feedparser.parse(source['url'])
            
            for entry in feed.entries[:10]:
                item = {
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.get('published', ''),
                    'source': source['name'],
                    'category': source['category'],
                    'retention_days': source['retention_days'],
                    'fetch_time': datetime.datetime.now().isoformat()
                }
                all_items.append(item)
        except Exception as e:
            print(f"Error fetching {source['name']}: {e}")
    
    # 合并历史数据
    existing_data = []
    if Path('data/feeds.json').exists():
        with open('data/feeds.json', 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except:
                existing_data = []
    
    # 简单去重（基于链接）
    existing_links = {item['link'] for item in existing_data}
    new_items = [item for item in all_items if item['link'] not in existing_links]
    
    # 合并并按时间排序
    merged_data = existing_data + new_items
    merged_data.sort(key=lambda x: x.get('fetch_time', ''), reverse=True)
    
    # 限制总条数（可选）
    merged_data = merged_data[:500]
    
    # 保存数据
    with open('data/feeds.json', 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)
    
    print(f"Updated with {len(new_items)} new items. Total: {len(merged_data)} items.")

if __name__ == '__main__':
    fetch_feeds()
