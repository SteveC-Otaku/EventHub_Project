# app.py

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, jsonify, abort, send_from_directory
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

from models import db, User, Event, Registration, Notification

app = Flask(__name__)

# =========================
# 一、Flask + SQLAlchemy 配置（使用 MySQL）
# =========================
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_HOST = "localhost"
MYSQL_DB = "eventhub_db"
MYSQL_PORT = 3306

# Flask-SQLAlchemy 的 URI 格式：
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    "?charset=utf8mb4"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 用于 session 签名，请替换成一段真正随机的字符串
app.config["SECRET_KEY"] = "replace_this_with_a_properly_random_secret_key"

db.init_app(app)
with app.app_context():
    db.create_all()

# 注册 advanced Blueprint（保持不变）
from advanced import advanced_bp
app.register_blueprint(advanced_bp, url_prefix="/advanced")


# =========================
# 二、工具函数
# =========================
def current_user():
    """
    如果 session 中有 user_id，就返回对应 User 对象；否则返回 None
    """
    uid = session.get("user_id")
    if not uid:
        return None
    return User.query.get(uid)


# =========================
# 三、前端静态文件 & HTML 渲染路由
# =========================

# 如果希望 /favicon.ico 正确返回
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


# —— 首页 (渲染 index.html) ——
@app.route("/")
def index():
    return render_template("index.html")


# —— 活动详情页 (/event-details?id=xxx) ——
@app.route("/event-details")
def event_details():
    return render_template("event-details.html")


# —— 组织者登录页 (/organizer-login) ——
@app.route("/organizer-login", methods=["GET", "POST"])
def organizer_login():
    # GET：直接渲染登录页
    if request.method == "GET":
        return render_template("organizer-login.html", error=None)

    # POST：尝试从表单获取 email + password 并做数据库校验
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    # 先打印日志以便排查
    print(f"[organizer_login] Attempt login with email='{email}'")

    try:
        # 如果是 Demo 账户，则绕过密码校验，直接创建或获取数据库里对应的 Organizer
        demo_emails = {"tech@demo.com", "music@demo.com", "business@demo.com"}

        if email in demo_emails:
            org = User.query.filter_by(email=email, role="organizer").first()
            if not org:
                # 第一次点击 Demo 时，数据库里还没有这条记录，需要自动创建
                demo_name_map = {
                    "tech@demo.com": "Tech Events Inc.",
                    "music@demo.com": "Music Festivals LLC",
                    "business@demo.com": "Business Network Association"
                }
                name_to_use = demo_name_map.get(email, "Demo Organizer")
                org = User(
                    name=name_to_use,
                    email=email,
                    password_hash=generate_password_hash("password123", method="pbkdf2:sha256", salt_length=8),
                    role="organizer"
                )
                db.session.add(org)
                db.session.commit()
                print(f"[organizer_login] Created new demo organizer: {email}")
            else:
                print(f"[organizer_login] Found existing demo organizer: {email}")

            # 直接把 org 写进 session，不再验证 password
            session["user_id"] = org.id
            session["role"] = org.role  # "organizer"
            flash("Demo 组织者登录成功！", "success")
            return redirect(url_for("organizer_dashboard"))

        # 以下逻辑走常规“非 Demo”组织者登录
        org = User.query.filter_by(email=email, role="organizer").first()
        if not org:
            print(f"[organizer_login] ERROR: 组织者邮箱不存在或角色不对: {email}")
            flash("组织者账户不存在或密码错误", "error")
            return redirect(url_for("organizer_login"))

        if not check_password_hash(org.password_hash, password):
            print(f"[organizer_login] ERROR: 密码校验失败: {email}")
            flash("组织者账户不存在或密码错误", "error")
            return redirect(url_for("organizer_login"))

        # 验证通过，写入 session
        session["user_id"] = org.id
        session["role"] = org.role
        print(f"[organizer_login] 常规组织者登录成功: {email} (id={org.id})")
        flash("组织者登录成功", "success")
        return redirect(url_for("organizer_dashboard"))

    except Exception as e:
        # 捕获任何异常并打印日志，前端展示错误
        print(f"[organizer_login] EXCEPTION: {e}")
        flash("登录过程中出现异常，请检查日志。", "error")
        return redirect(url_for("organizer_login"))


# —— 组织者仪表盘 (/organizer-dashboard) ——
# 注意：不再使用 @organizer_required 装饰器，允许只要有 session["user_id"] 就可访问
@app.route("/organizer-dashboard")
def organizer_dashboard():
    # 把 server-side session 里的 current_user() 对象传给模板
    return render_template("organizer-dashboard.html", current_user=current_user())


# —— 组织者活动列表 (/organizer-events) ——
@app.route("/organizer-events")
def organizer_events():
    return render_template("organizer-events.html")


# —— 组织者创建/编辑活动页 (/organizer-create-event) ——
@app.route("/organizer-create-event")
def organizer_create_event():
    return render_template("organizer-create-event.html")


# —— 普通用户登录 (/login) ——
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return redirect(url_for("index"))

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    user = User.query.filter_by(email=email, role="user").first()
    if not user or not check_password_hash(user.password_hash, password):
        flash("普通用户不存在或密码错误", "error")
        return redirect(request.referrer or url_for("index"))

    session["user_id"] = user.id
    session["role"] = user.role  # "user"
    flash("登录成功", "success")
    return redirect(url_for("index"))


# —— 普通用户注销 (/logout) ——
@app.route("/logout")
def logout():
    session.clear()
    flash("已退出登录", "info")
    return redirect(url_for("index"))


# —— 普通用户仪表盘 (/user-dashboard) ——
@app.route("/user-dashboard")
def user_dashboard():
    user = current_user()
    return render_template("user-dashboard.html", user_id=user.id if user else "null")


# —— 个人资料页 (/profile) ——
@app.route("/profile")
def profile():
    return render_template("profile.html")


# —— 报名页 (/registration) ——
@app.route("/registration")
def registration():
    return render_template("registration.html")


# —— 设置页 (/settings) ——
@app.route("/settings")
def settings():
    return render_template("settings.html")


# 404 错误处理
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# =========================
# 四、后端 API 路由 —— /api/...
#    （此处保持原有逻辑，不做改动）
# =========================

@app.route("/api/events", methods=["GET", "POST"])
def api_events():
    if request.method == "GET":
        category = request.args.get("category")
        date_str = request.args.get("date")
        query = Event.query
        if category:
            query = query.filter_by(category=category)
        if date_str:
            try:
                d = datetime.strptime(date_str, "%Y-%m-%d").date()
                query = query.filter_by(date=d)
            except ValueError:
                pass
        events = query.order_by(Event.date.asc()).all()
        result = []
        for e in events:
            result.append({
                "id": e.id,
                "title": e.title,
                "description": e.description,
                "date": e.date.isoformat(),
                "time": e.time.strftime("%H:%M"),
                "location": e.location,
                "image": url_for('static', filename=e.image) if e.image else "",
                "category": e.category,
                "organizer": {
                    "id": e.organizer.id,
                    "name": e.organizer.name,
                    "email": e.organizer.email
                },
                "tickets": {
                    "general": {
                        "price": e.general_price,
                        "capacity": e.general_capacity,
                        "remaining": e.general_remaining
                    },
                    "vip": {
                        "price": e.vip_price,
                        "capacity": e.vip_capacity,
                        "remaining": e.vip_remaining
                    }
                },
                "attendees": [
                    {"userId": reg.user_id, "registrationId": reg.id}
                    for reg in e.registrations
                ]
            })
        return jsonify(result)

    else:  # POST —— 创建新活动
        data = request.json or {}
        try:
            title = data["title"]
            description = data.get("description", "")
            date_obj = datetime.strptime(data["date"], "%Y-%m-%d").date()
            time_obj = datetime.strptime(data["time"], "%H:%M").time()
            location = data["location"]
            image = data.get("image", "")
            category = data["category"]
            organizer_id = int(data["organizer"]["id"])
            gprice = float(data["tickets"]["general"]["price"])
            gcap = int(data["tickets"]["general"]["capacity"])
            vprice = float(data["tickets"]["vip"]["price"])
            vcap = int(data["tickets"]["vip"]["capacity"])
        except (KeyError, ValueError):
            return jsonify({"error": "Invalid event data"}), 400

        new_event = Event(
            title=title,
            description=description,
            date=date_obj,
            time=time_obj,
            location=location,
            image=image,
            category=category,
            general_price=gprice,
            general_capacity=gcap,
            general_remaining=gcap,
            vip_price=vprice,
            vip_capacity=vcap,
            vip_remaining=vcap,
            organizer_id=organizer_id
        )
        db.session.add(new_event)
        db.session.commit()
        return jsonify({"id": new_event.id}), 201


@app.route("/api/events/<int:event_id>", methods=["GET", "PUT", "DELETE"])
def api_single_event(event_id):
    e = Event.query.get_or_404(event_id)
    if request.method == "GET":
        return jsonify({
            "id": e.id,
            "title": e.title,
            "description": e.description,
            "date": e.date.isoformat(),
            "time": e.time.strftime("%H:%M"),
            "location": e.location,
            "image": url_for('static', filename=e.image) if e.image else "",
            "category": e.category,
            "organizer": {
                "id": e.organizer.id,
                "name": e.organizer.name,
                "email": e.organizer.email
            },
            "tickets": {
                "general": {
                    "price": e.general_price,
                    "capacity": e.general_capacity,
                    "remaining": e.general_remaining
                },
                "vip": {
                    "price": e.vip_price,
                    "capacity": e.vip_capacity,
                    "remaining": e.vip_remaining
                }
            },
            "attendees": [
                {"userId": reg.user_id, "registrationId": reg.id}
                for reg in e.registrations
            ]
        })
    elif request.method == "PUT":
        data = request.json or {}
        if "title" in data:
            e.title = data["title"]
        if "description" in data:
            e.description = data["description"]
        if "date" in data:
            try:
                e.date = datetime.strptime(data["date"], "%Y-%m-%d").date()
            except ValueError:
                pass
        if "time" in data:
            try:
                e.time = datetime.strptime(data["time"], "%H:%M").time()
            except ValueError:
                pass
        if "location" in data:
            e.location = data["location"]
        if "image" in data:
            e.image = data["image"]
        if "category" in data:
            e.category = data["category"]
        if "tickets" in data:
            t = data["tickets"]
            if "general" in t:
                e.general_price = float(t["general"]["price"])
                e.general_capacity = int(t["general"]["capacity"])
                e.general_remaining = int(t["general"]["capacity"])
            if "vip" in t:
                e.vip_price = float(t["vip"]["price"])
                e.vip_capacity = int(t["vip"]["capacity"])
                e.vip_remaining = int(t["vip"]["capacity"])
        db.session.commit()
        return jsonify({"message": "Event updated"}), 200
    else:  # DELETE
        for reg in e.registrations.all():
            db.session.delete(reg)
        db.session.delete(e)
        db.session.commit()
        return jsonify({"message": "Event deleted"}), 200


@app.route("/api/organizers", methods=["GET", "POST"])
def api_organizers():
    if request.method == "GET":
        email = request.args.get("email")
        query = User.query.filter_by(role="organizer")
        if email:
            query = query.filter_by(email=email)
        orgs = query.all()
        result = []
        for o in orgs:
            result.append({
                "id": o.id,
                "name": o.name,
                "email": o.email,
                "events": [ev.id for ev in o.events]
            })
        return jsonify(result)
    else:  # POST —— 新增组织者
        data = request.json or {}
        try:
            name = data["name"]
            email = data["email"]
            password = data["password"]
        except KeyError:
            return jsonify({"error": "Invalid organizer data"}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already exists"}), 400
        hashed = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)
        new_org = User(name=name, email=email, password_hash=hashed, role="organizer")
        db.session.add(new_org)
        db.session.commit()
        return jsonify({"id": new_org.id}), 201


@app.route("/api/organizers/<int:org_id>", methods=["GET", "PUT", "DELETE"])
def api_single_organizer(org_id):
    o = User.query.filter_by(id=org_id, role="organizer").first_or_404()
    if request.method == "GET":
        return jsonify({
            "id": o.id,
            "name": o.name,
            "email": o.email,
            "events": [ev.id for ev in o.events]
        })
    elif request.method == "PUT":
        data = request.json or {}
        if "name" in data:
            o.name = data["name"]
        if "email" in data:
            o.email = data["email"]
        if "password" in data:
            o.password_hash = generate_password_hash(
                data["password"], method="pbkdf2:sha256", salt_length=8
            )
        db.session.commit()
        return jsonify({"message": "Organizer updated"}), 200
    else:  # DELETE
        for ev in o.events.all():
            for r in ev.registrations.all():
                db.session.delete(r)
            db.session.delete(ev)
        db.session.delete(o)
        db.session.commit()
        return jsonify({"message": "Organizer deleted"}), 200


@app.route("/api/users", methods=["GET", "POST"])
def api_users():
    if request.method == "GET":
        email = request.args.get("email")
        query = User.query.filter_by(role="user")
        if email:
            query = query.filter_by(email=email)
        us = query.all()
        result = []
        for u in us:
            result.append({
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "phone": u.phone,
                "avatar_url": u.avatar_url or "",
                "bio": u.bio or "",
                "interests": (u.interests or "").split(",") if u.interests else [],
                "location": u.location or "",
                "registrations": [r.id for r in u.registrations]
            })
        return jsonify(result)
    else:  # POST —— 新增用户
        data = request.json or {}
        try:
            name = data["name"]
            email = data["email"]
            password = data.get("password", "password")
        except KeyError:
            return jsonify({"error": "Invalid user data"}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already exists"}), 400
        hashed = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)
        new_user = User(
            name=name,
            email=email,
            password_hash=hashed,
            role="user",
            phone=data.get("phone", ""),
            avatar_url=data.get("avatar_url", ""),
            bio=data.get("bio", ""),
            interests=",".join(data.get("interests", [])),
            location=data.get("location", "")
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"id": new_user.id}), 201


@app.route("/api/users/<int:user_id>", methods=["GET", "PUT", "DELETE"])
def api_single_user(user_id):
    u = User.query.filter_by(id=user_id, role="user").first_or_404()
    if request.method == "GET":
        return jsonify({
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "phone": u.phone or "",
            "avatar_url": u.avatar_url or "",
            "bio": u.bio or "",
            "interests": (u.interests or "").split(",") if u.interests else [],
            "location": u.location or "",
            "registrations": [r.id for r in u.registrations]
        })
    elif request.method == "PUT":
        data = request.json or {}
        if "name" in data:
            u.name = data["name"]
        if "email" in data:
            u.email = data["email"]
        if "password" in data:
            u.password_hash = generate_password_hash(
                data["password"], method="pbkdf2:sha256", salt_length=8
            )
        if "phone" in data:
            u.phone = data["phone"]
        if "avatar_url" in data:
            u.avatar_url = data["avatar_url"]
        if "bio" in data:
            u.bio = data["bio"]
        if "interests" in data:
            u.interests = ",".join(data["interests"])
        if "location" in data:
            u.location = data["location"]
        db.session.commit()
        return jsonify({"message": "User updated"}), 200
    else:  # DELETE —— 删除用户
        for reg in u.registrations.all():
            ev = reg.event
            if reg.ticket_type == "general":
                ev.general_remaining += reg.quantity
            else:
                ev.vip_remaining += reg.quantity
            db.session.delete(reg)
        db.session.delete(u)
        db.session.commit()
        return jsonify({"message": "User deleted"}), 200


@app.route("/api/notifications", methods=["GET", "POST"])
def api_notifications():
    if request.method == "GET":
        user_id = request.args.get("userId")
        query = Notification.query
        if user_id:
            try:
                query = query.filter_by(user_id=int(user_id))
            except ValueError:
                pass
        nots = query.order_by(Notification.date.desc()).all()
        result = []
        for n in nots:
            result.append({
                "id": n.id,
                "userId": n.user_id,
                "title": n.title,
                "content": n.content,
                "date": n.date.isoformat(),
                "read": n.read
            })
        return jsonify(result)
    else:  # POST —— 创建通知
        data = request.json or {}
        try:
            user_id = int(data["userId"])
            title = data["title"]
            content = data["content"]
            read_flag = bool(data.get("read", False))
        except (KeyError, ValueError):
            return jsonify({"error": "Invalid notification data"}), 400
        new_notif = Notification(
            user_id=user_id,
            title=title,
            content=content,
            date=datetime.utcnow(),
            read=read_flag
        )
        db.session.add(new_notif)
        db.session.commit()
        return jsonify({"id": new_notif.id}), 201


@app.route("/api/notifications/<int:notif_id>", methods=["PUT", "DELETE"])
def api_single_notification(notif_id):
    n = Notification.query.get_or_404(notif_id)
    if request.method == "PUT":
        data = request.json or {}
        if "read" in data:
            n.read = bool(data["read"])
        db.session.commit()
        return jsonify({"message": "Notification updated"}), 200
    else:  # DELETE
        db.session.delete(n)
        db.session.commit()
        return jsonify({"message": "Notification deleted"}), 200


@app.route("/api/registrations", methods=["GET", "POST"])
def api_registrations():
    if request.method == "GET":
        user_id = request.args.get("userId")
        event_id = request.args.get("eventId")
        query = Registration.query
        if user_id:
            try:
                query = query.filter_by(user_id=int(user_id))
            except ValueError:
                pass
        if event_id:
            try:
                query = query.filter_by(event_id=int(event_id))
            except ValueError:
                pass
        regs = query.order_by(Registration.purchase_date.desc()).all()
        result = []
        for r in regs:
            result.append({
                "id": r.id,
                "userId": r.user_id,
                "eventId": r.event_id,
                "ticketType": r.ticket_type,
                "quantity": r.quantity,
                "totalPrice": r.total_price,
                "purchaseDate": r.purchase_date.isoformat(),
                "attendeeInfo": {
                    "name": r.attendee_name,
                    "email": r.attendee_email,
                    "phone": r.attendee_phone
                }
            })
        return jsonify(result)
    else:  # POST —— 创建报名
        data = request.json or {}
        try:
            user_id = int(data["userId"])
            event_id = int(data["eventId"])
            ticket_type = data["ticketType"]
            quantity = int(data["quantity"])
            total_price = float(data["totalPrice"])
            att_name = data["attendeeInfo"]["name"]
            att_email = data["attendeeInfo"]["email"]
            att_phone = data["attendeeInfo"].get("phone", "")
        except (KeyError, ValueError):
            return jsonify({"error": "Invalid registration data"}), 400

        ev = Event.query.get_or_404(event_id)
        if ticket_type == "general":
            if ev.general_remaining < quantity:
                return jsonify({"error": "Not enough general tickets"}), 400
            ev.general_remaining -= quantity
        else:
            if ev.vip_remaining < quantity:
                return jsonify({"error": "Not enough VIP tickets"}), 400
            ev.vip_remaining -= quantity

        new_reg = Registration(
            user_id=user_id,
            event_id=event_id,
            ticket_type=ticket_type,
            quantity=quantity,
            total_price=total_price,
            purchase_date=datetime.utcnow(),
            attendee_name=att_name,
            attendee_email=att_email,
            attendee_phone=att_phone
        )
        db.session.add(new_reg)

        note = Notification(
            user_id=user_id,
            title=f"Registration Confirmed for {ev.title}",
            content=f"You have successfully registered for {ev.title}.",
            date=datetime.utcnow(),
            read=False
        )
        db.session.add(note)
        db.session.commit()
        return jsonify({"id": new_reg.id}), 201


@app.route("/api/registrations/<int:reg_id>", methods=["GET", "DELETE"])
def api_single_registration(reg_id):
    r = Registration.query.get_or_404(reg_id)
    if request.method == "GET":
        return jsonify({
            "id": r.id,
            "userId": r.user_id,
            "eventId": r.event_id,
            "ticketType": r.ticket_type,
            "quantity": r.quantity,
            "totalPrice": r.total_price,
            "purchaseDate": r.purchase_date.isoformat(),
            "attendeeInfo": {
                "name": r.attendee_name,
                "email": r.attendee_email,
                "phone": r.attendee_phone
            }
        })
    else:  # DELETE —— 取消报名
        ev = r.event
        if r.ticket_type == "general":
            ev.general_remaining += r.quantity
        else:
            ev.vip_remaining += r.quantity
        db.session.delete(r)
        db.session.commit()
        return jsonify({"message": "Registration canceled"}), 200


# =========================
# 五、可选：导入 Mock Seed 数据（仅开发/测试时使用）
# =========================
@app.route("/generate-test-data")
def generate_test_data():
    from faker import Faker
    fake = Faker()

    # 1. 10 个组织者
    organizers = []
    for i in range(10):
        name = fake.company()
        email = f"{name.lower().replace(' ', '_')}@example.com"
        if User.query.filter_by(email=email).first():
            continue
        u = User(
            name=name,
            email=email,
            password_hash=generate_password_hash("password123", method="pbkdf2:sha256", salt_length=8),
            role="organizer"
        )
        db.session.add(u)
        organizers.append(u)
    db.session.commit()

    # 2. 生成 50 个“测试活动”
    events = []
    categories = ["conference", "concert", "workshop", "networking"]
    for i in range(50):
        title = fake.sentence(nb_words=4).rstrip(".")
        desc = fake.paragraph(nb_sentences=3)
        date_obj = fake.date_between(start_date="-30d", end_date="+60d")
        time_obj = fake.time_object()
        location = fake.city()
        category = fake.random_element(categories)
        gprice = fake.random_int(min=10, max=200)
        gcap   = fake.random_int(min=50, max=500)
        vprice = fake.random_int(min=gprice + 10, max=gprice + 100)
        vcap   = fake.random_int(min=20, max=200)
        organizer = fake.random_element(organizers)

        e = Event(
            title=title,
            description=desc,
            date=date_obj,
            time=time_obj,
            location=location,
            image="",
            category=category,
            general_price=gprice,
            general_capacity=gcap,
            general_remaining=gcap,
            vip_price=vprice,
            vip_capacity=vcap,
            vip_remaining=vcap,
            organizer_id=organizer.id
        )
        db.session.add(e)
        events.append(e)
    db.session.commit()

    # 3. 给每个未来的活动插入随机报名 + 通知
    import random
    for e in events:
        if e.date >= datetime.utcnow().date():
            num_regs = random.randint(5, 20)
            for j in range(num_regs):
                u = User.query.filter_by(role="user").order_by(db.func.rand()).first()
                if not u:
                    u = User(
                        name=fake.name(),
                        email=fake.email(),
                        password_hash=generate_password_hash("password123", method="pbkdf2:sha256", salt_length=8),
                        role="user",
                        phone=fake.phone_number(),
                        avatar_url="",
                        bio=fake.text(max_nb_chars=200),
                        interests=",".join(fake.random_elements(elements=categories, length=2)),
                        location=fake.city()
                    )
                    db.session.add(u)
                    db.session.flush()
                ticket_type = fake.random_element(["general", "vip"])
                quantity = fake.random_int(min=1, max=3)
                price = e.general_price * quantity if ticket_type == "general" else e.vip_price * quantity
                if ticket_type == "general" and e.general_remaining < quantity:
                    continue
                if ticket_type == "vip" and e.vip_remaining < quantity:
                    continue
                if ticket_type == "general":
                    e.general_remaining -= quantity
                else:
                    e.vip_remaining -= quantity

                reg = Registration(
                    user_id=u.id,
                    event_id=e.id,
                    ticket_type=ticket_type,
                    quantity=quantity,
                    total_price=price,
                    purchase_date=fake.date_time_between(start_date="-30d", end_date="now"),
                    attendee_name=u.name,
                    attendee_email=u.email,
                    attendee_phone=u.phone
                )
                db.session.add(reg)

                # 给用户生成一条通知
                notif = Notification(
                    user_id=u.id,
                    title=f"Registration Confirmed for {e.title}",
                    content=f"Your registration for {e.title} is confirmed (自动生成).",
                    date=datetime.utcnow(),
                    read=False
                )
                db.session.add(notif)

    db.session.commit()
    return jsonify({"message": "Test data generated: 10 organizers, 50 events, hundreds of regs/notifs."}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
