"""根据书名关键词自动分类电子书"""

CATEGORY_DEFINITIONS = [
    {"slug": "computer", "name": "计算机", "sort_order": 1, "keywords": [
        "编程", "Python", "Java", "C++", "JavaScript", "算法", "数据库", "Linux", "Web",
        "人工智能", "机器学习", "单片机", "软件", "黑客", "Kali", "代码", "开发", "架构",
        "SQL", "HTML", "CSS", "Vue", "React", "物联网", "网络", "信息安全", "渗透",
        "Photoshop", "AfterEffects", "Office", "Excel", "Access", "Primer", "教程",
        "IT", "程序员", "云计算", "大数据", "区块链", "Arduino", "嵌入式",
    ]},
    {"slug": "sci-fi", "name": "科幻玄幻", "sort_order": 2, "keywords": [
        "科幻", "玄幻", "修仙", "仙侠", "穿越", "末日", "奇幻", "武侠", "金庸", "古龙",
        "鬼吹灯", "盗墓", "三体", "斗破", "诛仙", "凡人", "遮天", "洪荒", "网游",
        "魔法", "异世界", "大神", "修炼狂潮", "万古大帝",
    ]},
    {"slug": "literature", "name": "文学小说", "sort_order": 3, "keywords": [
        "小说", "散文", "诗歌", "文学", "名著", "文集", "短篇", "长篇", "童话", "寓言",
        "莎士比亚", "雨果", "莫言", "张爱玲", "鲁迅", "王小波", "川端", "马尔克斯",
        "史诗", "传记文学", "纪实文学", "外国文学", "古典文学", "现代文学",
    ]},
    {"slug": "history", "name": "历史", "sort_order": 4, "keywords": [
        "历史", "朝代", "传记", "史书", "年谱", "民国", "古代", "二战", "战争史",
        "史记", "考古", "中国史", "世界史", "通史", "简史", "王朝", "皇帝",
        "明清", "秦汉", "唐宋", "晚清", "革命", "党史",
    ]},
    {"slug": "business", "name": "经济管理", "sort_order": 5, "keywords": [
        "商业", "创业", "投资", "理财", "股票", "基金", "经济", "管理", "营销", "销售",
        "职场", "领导", "融资", "电商", "淘宝", "财务", "会计", "金融", "期货",
        "招商", "企业", "公司", "巴菲特", "芒格", "博弈",
    ]},
    {"slug": "psychology", "name": "心理励志", "sort_order": 6, "keywords": [
        "心理", "情商", "沟通", "口才", "说服", "读心", "催眠", "情绪", "焦虑",
        "减压", "励志", "成功学", "自控力", "习惯", "思维", "格局", "影响力",
        "共情", "说话", "演讲", "谈判",
    ]},
    {"slug": "education", "name": "教育考试", "sort_order": 7, "keywords": [
        "教程", "考试", "托福", "雅思", "考研", "高考", "教材", "习题", "学习",
        "英语", "日语", "德语", "法语", "入门", "指南", "课本", "教师用书",
        "新概念", "四级", "六级", "GRE", "SAT", "留学", "语法", "单词",
    ]},
    {"slug": "health", "name": "医学健康", "sort_order": 8, "keywords": [
        "医学", "养生", "健康", "中医", "药", "病", "解剖", "护理", "食疗",
        "健身", "减肥", "外科", "内科", "儿科", "妇科", "针灸", "本草", "医案",
        "临床", "诊断", "康复", "营养",
    ]},
    {"slug": "philosophy", "name": "哲学社科", "sort_order": 9, "keywords": [
        "哲学", "思想", "伦理", "逻辑", "宗教", "佛学", "道家", "儒家", "社会学",
        "政治", "法律", "宪法", "民主", "政府", "社会", "文化", "人类学", "伦理学",
    ]},
    {"slug": "life", "name": "生活百科", "sort_order": 10, "keywords": [
        "生活", "美食", "旅游", "旅行", "手工", "家居", "育儿", "早餐", "化妆",
        "穿搭", "烹饪", "菜谱", "摄影", "宠物", "园艺", "游戏", "运动", "羽毛球",
        "足球", "篮球", "钓鱼", "户外",
    ]},
    {"slug": "other", "name": "综合其他", "sort_order": 99, "keywords": []},
]

DEFAULT_COVER = "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400"

CATEGORY_COVERS = {
    "computer": "https://images.unsplash.com/photo-1627398242454-45a1465c2479?w=400",
    "sci-fi": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400",
    "literature": "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=400",
    "history": "https://images.unsplash.com/photo-1457369804613-52c61a468e7c?w=400",
    "business": "https://images.unsplash.com/photo-1553729450-efb1c8d1d8e2?w=400",
    "psychology": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400",
    "education": "https://images.unsplash.com/photo-1524995998254-4ba47062c8ad?w=400",
    "health": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=400",
    "philosophy": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400",
    "life": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400",
    "other": DEFAULT_COVER,
}


def classify_title(title: str) -> str:
    """返回分类 slug"""
    title_lower = title.lower()
    best_slug = "other"
    best_score = 0

    for cat in CATEGORY_DEFINITIONS:
        if cat["slug"] == "other":
            continue
        score = sum(1 for kw in cat["keywords"] if kw.lower() in title_lower or kw in title)
        if score > best_score:
            best_score = score
            best_slug = cat["slug"]

    return best_slug


def get_cover_url(slug: str) -> str:
    return CATEGORY_COVERS.get(slug, DEFAULT_COVER)
