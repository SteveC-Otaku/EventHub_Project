# seed_data.py

import random
from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash

# 请根据你自己的项目结构修改下面两行的导入路径：
# - 确保 app.py 中实例化了 Flask() 并初始化了 db
# - 确保 models.py 定义了 User 和 Event 两个 SQLAlchemy 模型
from app import app, db
from models import User, Event

# -----------------------------
# 配置区：你可以根据需要在这里调整各种参数
# -----------------------------
NUM_ORGANIZERS = 10    # 生成多少个“组织者”账号
NUM_EVENTS = 50        # 生成多少条“活动”记录
PASSWORD_PLAINTEXT = "password123"  # 初始密码（所有组织者都是这个密码）

# 一些示例的活动分类，可按需增减
CATEGORIES = ["conference", "concert", "workshop", "networking"]

# 一些示例城市/地点，用于随机拼凑活动的 location 字段
LOCATIONS = [
    "Convention Center, New York",
    "Central Park, New York",
    "Grand Hotel, Boston",
    "Tech Hub, San Francisco",
    "Innovation Center, Austin",
    "Science Center, Seattle",
    "Expo Hall, Chicago",
    "Downtown Arena, Los Angeles",
    "City Conference Hall, Denver",
    "Riverside Pavilion, Miami",
    "University Auditorium, Atlanta",
    "Convention Plaza, Dallas"
]

# 示例的活动标题前缀、后缀、描述模板
TITLE_PREFIXES = [
    "Tech Conference", "Summer Music Festival", "Business Networking Lunch",
    "Web Development Workshop", "Startup Pitch Competition", "AI & ML Conference",
    "Digital Marketing Seminar", "Healthcare Innovation Forum", "Blockchain Meetup",
    "Film & Media Expo"
]
DESCRIPTION_TEMPLATES = [
    "Join us for the biggest {cat} of the year in {loc}.",
    "Don't miss this exclusive {cat} at {loc}.",
    "An unforgettable {cat} experience, happening at {loc}.",
    "Connect and learn at our {cat} in {loc}.",
    "Experience the latest in {cat} held at {loc}.",
    "A must-attend {cat} for professionals, hosted at {loc}."
]

IMAGE_PATHS = [
    "images/tech_conference_2023.jpg",
    "images/summer_music_festival.jpg",
    "images/business_networking_lunch.jpg",
    "images/web_development_workshop.jpg",
    "images/startup_pitch_competition.jpg",
    "images/ai_machine_learning_conference.jpg",
    "images/digital_marketing_seminar.jpg",
    "images/healthcare_innovation_forum.jpg",
    "images/blockchain_meetup.jpg",
    "images/film_media_expo.jpg"
]
# -----------------------------


def random_date_between(start: datetime, end: datetime) -> datetime:
    """
    在 start ~ end 范围内随机选一个日期时间（精确到分钟）。
    """
    delta = end - start
    rand_seconds = random.randrange(int(delta.total_seconds()))
    return start + timedelta(seconds=rand_seconds)


def seed_organizers():
    """
    生成 NUM_ORGANIZERS 个“组织者”账号，插入到 User 表中，
    role 一律设置为 "organizer"。
    如果 email 已存在，则跳过该条（避免重复运行时插入冲突）。
    """
    print(f"开始生成 {NUM_ORGANIZERS} 个组织者账号...")
    for i in range(1, NUM_ORGANIZERS + 1):
        name = f"Organizer {i}"
        email = f"organizer{i}@example.com"
        existing = User.query.filter_by(email=email, role="organizer").first()
        if existing:
            print(f"  [跳过] 账号已存在：{email}")
            continue

        hashed = generate_password_hash(PASSWORD_PLAINTEXT, method="pbkdf2:sha256", salt_length=8)
        org = User(
            name=name,
            email=email,
            password_hash=hashed,
            role="organizer",
            phone="",
            avatar_url="",
            bio="",
            interests="",
            location="",
            created_at=datetime.utcnow()
        )
        db.session.add(org)
        print(f"  已插入：{email}")
    db.session.commit()
    print("组织者账号生成完毕。\n")


def seed_events():
    """
    生成 NUM_EVENTS 条“活动”记录，随机分配给上面生成的组织者。
    Event 表中的字段示例如下：
    - title, description, date, time, location, image, category
    - general_price, general_capacity, general_remaining
    - vip_price, vip_capacity, vip_remaining
    - created_at, organizer_id
    """
    print(f"开始生成 {NUM_EVENTS} 条活动记录...")

    # 先取出所有已经存在的组织者 ID，随机分配给 Event.organizer_id
    organizers = User.query.filter_by(role="organizer").all()
    if not organizers:
        raise RuntimeError("未找到任何 role='organizer' 的用户，请先运行 seed_organizers()。")
    organizer_ids = [org.id for org in organizers]

    now = datetime.utcnow()
    one_year_later = now + timedelta(days=365)

    for i in range(1, NUM_EVENTS + 1):
        # 随机挑一个组织者
        org_id = random.choice(organizer_ids)

        # 随机拼一个标题：TITLE_PREFIXES 中随机选 + 序号
        prefix = random.choice(TITLE_PREFIXES)
        title = f"{prefix} {2023 + (i // 10)}"  # 举例：年份保持稍微多样

        # 随机 category
        cat = random.choice(CATEGORIES)

        # 随机 location
        loc = random.choice(LOCATIONS)

        # 随机 description：用 DESCRIPTION_TEMPLATES 模板替换
        template = random.choice(DESCRIPTION_TEMPLATES)
        description = template.format(cat=cat, loc=loc)

        # 随机生成一个未来某天（今天到一年后之间），并随机到分钟
        dt = random_date_between(now, one_year_later)
        date_str = dt.date()
        time_str = dt.time().replace(second=0, microsecond=0)

        # 随机选一张图片（可为相对路径）
        image = random.choice(IMAGE_PATHS)

        # 随机价格和容量
        general_price = random.choice([20, 25, 30, 40, 50, 60, 75, 100])
        general_capacity = random.choice([50, 100, 200, 300, 500, 1000])
        general_remaining = general_capacity  # 初始剩余等于容量

        vip_price = general_price * random.choice([1.5, 2, 2.5])
        vip_price = int(vip_price)
        vip_capacity = max(1, general_capacity // random.choice([5, 4, 3, 2]))
        vip_remaining = vip_capacity

        # 检查是否已存在相同 title 和 organizer_id 的活动，以免重复
        exists = Event.query.filter_by(title=title, organizer_id=org_id).first()
        if exists:
            print(f"  [跳过] 已存在同名活动：{title}，组织者ID={org_id}")
            continue

        ev = Event(
            title=title,
            description=description,
            date=date_str,
            time=time_str,
            location=loc,
            image=image,
            category=cat,
            general_price=general_price,
            general_capacity=general_capacity,
            general_remaining=general_remaining,
            vip_price=vip_price,
            vip_capacity=vip_capacity,
            vip_remaining=vip_remaining,
            created_at=datetime.utcnow(),
            organizer_id=org_id
        )
        db.session.add(ev)
        if i % 10 == 0:
            # 每插 10 条就提交一次，减少一次性提交压力
            db.session.commit()
            print(f"  已插入 {i} 条活动...")

    db.session.commit()
    print("活动记录生成完毕。\n")


if __name__ == "__main__":
    # 使用 Flask 的 app.app_context()，确保可以正常访问 db
    with app.app_context():
        # 先生成组织者，再生成活动
        seed_organizers()
        seed_events()

    print("所有测试数据已完成插入，共插入：")
    print(f" - 组织者（role='organizer'）最多 {NUM_ORGANIZERS} 条（重复会被跳过）")
    print(f" - 活动（Event）       最多 {NUM_EVENTS} 条（重复会被跳过）")
