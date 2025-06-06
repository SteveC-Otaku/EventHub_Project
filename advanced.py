# advanced.py

from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    current_app as app,
    redirect,
    url_for,
    flash
)
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from werkzeug.security import generate_password_hash

# 假设 models.py 中定义了 User, Event, Registration, Notification
from models import db, User, Event, Registration, Notification

advanced_bp = Blueprint(
    "advanced",
    __name__,
    template_folder="templates/advanced",
    static_folder="static/advanced",
    static_url_path="/static/advanced"
)

# ======================
# 1. 扩展的“活动列表”页面（带多维度筛选：日期/地点/价格区间）
#    GET /advanced/events
# ======================
@advanced_bp.route("/events")
def events_advanced():
    """
    渲染一个新的页面：advanced-events.html
    前端会用 JS 调用 /advanced/api/events 接口，传递 date、location、price_min、price_max、category 等参数。
    """
    return render_template("advanced-events.html")


# ======================
# 2. 扩展的“活动 API”，支持更多查询参数
#    GET /advanced/api/events
#    参数示例：?category=concert&date=2023-07-20&location=New+York&price_min=20&price_max=100
# ======================
@advanced_bp.route("/api/events", methods=["GET"])
def api_advanced_events():
    # 前端传递的筛选参数
    category   = request.args.get("category", type=str)
    date_str   = request.args.get("date", type=str)
    location   = request.args.get("location", type=str)
    price_min  = request.args.get("price_min", type=float)
    price_max  = request.args.get("price_max", type=float)

    query = Event.query

    if category:
        query = query.filter_by(category=category)
    if date_str:
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d").date()
            query = query.filter_by(date=d)
        except ValueError:
            pass
    if location:
        # 简单的“地点模糊匹配”
        query = query.filter(Event.location.ilike(f"%{location}%"))
    if price_min is not None:
        query = query.filter(Event.general_price >= price_min)
    if price_max is not None:
        query = query.filter(Event.general_price <= price_max)

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
            "price": {
                "general": e.general_price,
                "vip": e.vip_price
            }
        })
    return jsonify(result)


# ======================
# 3. 扩展的“支付页”
#    GET /advanced/payment/<int:event_id>
#    POST /advanced/payment/checkout  （模拟支付网关回调）
# ======================
@advanced_bp.route("/payment/<int:event_id>")
def payment_page(event_id):
    """
    渲染一个新的支付页面 advanced-payment.html，
    并把 event 和当前登录用户 user 传入模板。
    """
    event = Event.query.get_or_404(event_id)

    # 将 current_user 的导入移到函数内部，避免循环导入
    from app import current_user
    user = current_user()

    return render_template("advanced-payment.html", event=event, user=user)


@advanced_bp.route("/payment/checkout", methods=["POST"])
def payment_checkout():
    """
    这是一个“模拟”的支付网关回调接口。
    """
    data = request.json
    # data 应该包含 { eventId, userId, amount, paymentToken, ticketType, quantity, attendeeName, attendeeEmail, attendeePhone } 等
    try:
        event_id     = int(data["eventId"])
        user_id      = int(data["userId"])
        ticket_type  = data["ticketType"]
        quantity     = int(data["quantity"])
        total_price  = float(data["amount"])
        stripe_token = data["paymentToken"]
    except (KeyError, ValueError):
        return jsonify({"error": "Invalid payment data"}), 400

    # 模拟在后端调用 Stripe 等支付网关进行验证（此处省略）
    # 假设支付成功，则继续：
    ev = Event.query.get_or_404(event_id)
    if ticket_type == "general":
        if ev.general_remaining < quantity:
            return jsonify({"error": "Not enough general tickets"}), 400
        ev.general_remaining -= quantity
    else:
        if ev.vip_remaining < quantity:
            return jsonify({"error": "Not enough VIP tickets"}), 400
        ev.vip_remaining -= quantity

    # 插入一条新的 Registration 记录
    new_reg = Registration(
        user_id=user_id,
        event_id=event_id,
        ticket_type=ticket_type,
        quantity=quantity,
        total_price=total_price,
        purchase_date=datetime.utcnow(),
        attendee_name=data.get("attendeeName", ""),
        attendee_email=data.get("attendeeEmail", ""),
        attendee_phone=data.get("attendeePhone", "")
    )
    db.session.add(new_reg)

    # 同时生成一条通知给该用户
    note = Notification(
        user_id=user_id,
        title=f"Registration Confirmed for {ev.title}",
        content=f"You have successfully paid ${total_price:.2f} for {ev.title}.",
        date=datetime.utcnow(),
        read=False
    )
    db.session.add(note)

    db.session.commit()
    return jsonify({"message": "Payment succeeded and registration created"}), 200


# ======================
# 4. 扩展的“管理后台”——批准/拒绝报名、修改活动、取消/退款等
#    GET /advanced/manage/registrations
#    GET /advanced/api/manage/registrations
#    POST /advanced/api/manage/registrations/<int:reg_id>/approve
#    POST /advanced/api/manage/registrations/<int:reg_id>/reject
#    GET /advanced/manage/events/<int:event_id>/edit
#    POST /advanced/manage/events/<int:event_id>/edit
#    POST /advanced/manage/events/<int:event_id>/cancel
# ======================
@advanced_bp.route("/manage/registrations")
def manage_registrations():
    """
    渲染“Approve/Reject Registrations”页面 advanced-manage-registrations.html。
    """
    return render_template("advanced-manage-registrations.html")


@advanced_bp.route("/api/manage/registrations", methods=["GET"])
def api_manage_regs_list():
    """
    返回所有报名记录（可在前端根据需要展示为待审批/已审批等状态）。
    """
    regs = Registration.query.order_by(Registration.purchase_date.desc()).all()
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
            # 如果在模型中添加了 status 字段，可以在这里加入 "status": r.status
        })
    return jsonify(result)


@advanced_bp.route("/api/manage/registrations/<int:reg_id>/approve", methods=["POST"])
def api_manage_reg_approve(reg_id):
    reg = Registration.query.get_or_404(reg_id)
    # 如果有 reg.status 字段，可写成： reg.status = "approved"
    db.session.commit()

    # 发送通知给用户
    notif = Notification(
        user_id=reg.user_id,
        title=f"Registration Approved for event {reg.event.title}",
        content=f"Your registration for {reg.event.title} has been approved by the organizer.",
        date=datetime.utcnow(),
        read=False
    )
    db.session.add(notif)
    db.session.commit()

    return jsonify({"message": f"Registration {reg_id} approved"}), 200


@advanced_bp.route("/api/manage/registrations/<int:reg_id>/reject", methods=["POST"])
def api_manage_reg_reject(reg_id):
    reg = Registration.query.get_or_404(reg_id)
    ev = reg.event
    # 将票数退回活动
    if reg.ticket_type == "general":
        ev.general_remaining += reg.quantity
    else:
        ev.vip_remaining += reg.quantity

    # 删除该报名记录
    db.session.delete(reg)
    db.session.commit()

    # 给用户发通知
    notif = Notification(
        user_id=reg.user_id,
        title=f"Registration Rejected for event {ev.title}",
        content=f"Your registration for {ev.title} has been rejected by the organizer. You will be refunded shortly.",
        date=datetime.utcnow(),
        read=False
    )
    db.session.add(notif)
    db.session.commit()

    return jsonify({"message": f"Registration {reg_id} rejected and tickets returned"}), 200


@advanced_bp.route("/manage/events/<int:event_id>/edit", methods=["GET", "POST"])
def manage_event_edit(event_id):
    """
    GET：渲染“编辑活动”页面 advanced-manage-edit-event.html，将 event 传给模板。
    POST：接收表单数据，更新 Event 对象及其图片（如有上传）。
    """
    event = Event.query.get_or_404(event_id)

    if request.method == "GET":
        # 渲染模板时把 event 传进去
        return render_template("advanced-manage-edit-event.html", event=event)

    # POST：更新活动信息
    data = request.form
    try:
        event.title = data.get("title", event.title)
        if data.get("description"):
            event.description = data["description"]
        if data.get("date"):
            event.date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        if data.get("time"):
            event.time = datetime.strptime(data["time"], "%H:%M").time()
        if data.get("location"):
            event.location = data["location"]
        if data.get("category"):
            event.category = data["category"]

        # 如果前端允许上传新图片
        if "image" in request.files:
            f = request.files["image"]
            if f.filename:
                filename = secure_filename(f.filename)
                upload_dir = os.path.join(app.root_path, "static", "images", "event_covers")
                os.makedirs(upload_dir, exist_ok=True)
                path = os.path.join(upload_dir, filename)
                f.save(path)
                # 将相对路径存入数据库
                event.image = f"images/event_covers/{filename}"
    except Exception as e:
        flash(f"Failed to update event: {e}", "error")
        return redirect(request.url)

    db.session.commit()
    flash("Event updated successfully", "success")
    return redirect(url_for("advanced.manage_event_edit", event_id=event_id))


@advanced_bp.route("/manage/events/<int:event_id>/cancel", methods=["POST"])
def manage_event_cancel(event_id):
    """
    取消活动：给所有已报名用户发通知，退还票数后删除活动及关联报名。
    """
    event = Event.query.get_or_404(event_id)

    for reg in event.registrations.all():
        notif = Notification(
            user_id=reg.user_id,
            title=f"Event Canceled: {event.title}",
            content=f"The event \"{event.title}\" has been canceled by the organizer. You will be refunded shortly.",
            date=datetime.utcnow(),
            read=False
        )
        db.session.add(notif)

        # 退还票数
        if reg.ticket_type == "general":
            event.general_remaining += reg.quantity
        else:
            event.vip_remaining += reg.quantity

        db.session.delete(reg)

    # 最后删除该活动
    db.session.delete(event)
    db.session.commit()

    flash(f"Event {event.title} and all registrations have been canceled", "info")
    return redirect(url_for("advanced.manage_registrations"))


@advanced_bp.route("/api/events/<int:event_id>/remaining", methods=["GET"])
def api_event_remaining(event_id):
    """
    返回某个活动的实时剩余票数（供前端轮询使用）。
    """
    ev = Event.query.get_or_404(event_id)
    return jsonify({
        "eventId": event_id,
        "general_remaining": ev.general_remaining,
        "vip_remaining": ev.vip_remaining
    })


# ======================
# 5. 测试数据生成（可选）
#    GET /advanced/generate-test-data
# ======================
@advanced_bp.route("/generate-test-data")
def generate_test_data():
    """
    简单脚本：生成 10 个组织者、50 个活动、随机注册和通知之类的测试数据。
    仅供开发环境调用，生产环境请移除或添加权限验证。
    """
    from faker import Faker
    fake = Faker()

    # 1. 生成 10 个“测试组织者”
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
            image="",  # 占位
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

    # 3. 随机插入一些报名和通知
    import random
    for e in events:
        # 只给未来的活动插入报名
        if e.date >= datetime.utcnow().date():
            num_regs = random.randint(5, 20)
            for j in range(num_regs):
                u = User.query.filter_by(role="user").order_by(db.func.rand()).first()
                if not u:
                    # 如果没有普通用户，就创建一个
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
                    db.session.flush()  # 拿到 u.id

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
