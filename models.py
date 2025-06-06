# models.py

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# —— User 表 ——（既存普通用户，也存储组织者，role 区分）
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")  # "user" or "organizer"
    phone = db.Column(db.String(20), nullable=True)
    avatar_url = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    interests = db.Column(db.String(255), nullable=True)       # 存 CSV 格式： "conferences,concerts"
    location = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 如果 role == "organizer"，则 events 代表他创建的活动
    events = db.relationship("Event", backref="organizer", lazy="dynamic")

    # registrations 代表这个用户（无论 user 还是 organizer）报名过的记录
    registrations = db.relationship("Registration", backref="user", lazy="dynamic")

    # notifications 代表给该用户推送的所有通知
    notifications = db.relationship("Notification", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"


# —— Event 表 ——
class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # 把 date, time 单独拆出来
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    location = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(255), nullable=True)   # 存相对路径，例如 "images/xxx.jpg"
    category = db.Column(db.String(50), nullable=False)  # "conference", "concert", ...

    # 票务信息
    general_price = db.Column(db.Float, nullable=False, default=0.0)
    general_capacity = db.Column(db.Integer, nullable=False, default=0)
    general_remaining = db.Column(db.Integer, nullable=False, default=0)

    vip_price = db.Column(db.Float, nullable=False, default=0.0)
    vip_capacity = db.Column(db.Integer, nullable=False, default=0)
    vip_remaining = db.Column(db.Integer, nullable=False, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 外键：哪个组织者创建了这个活动
    organizer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # 这个活动对应的所有报名
    registrations = db.relationship("Registration", backref="event", lazy="dynamic")

    def __repr__(self):
        return f"<Event {self.title} on {self.date}>"


# —— Registration 表 ——
class Registration(db.Model):
    __tablename__ = "registrations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)

    ticket_type = db.Column(db.String(20), nullable=False)   # "general" or "vip"
    quantity = db.Column(db.Integer, nullable=False, default=1)
    total_price = db.Column(db.Float, nullable=False, default=0.0)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)

    # 这一段“attendeeInfo” 信息前端会传过来，我们把它存成 JSON 格式的字符串
    attendee_name = db.Column(db.String(100), nullable=False)
    attendee_email = db.Column(db.String(120), nullable=False)
    attendee_phone = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f"<Registration user={self.user_id} event={self.event_id} qty={self.quantity}>"


# —— Notification 表 ——
class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Notification {self.title} to user {self.user_id}>"
