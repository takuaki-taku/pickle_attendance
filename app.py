import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///events.db"
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or "fallback_secret_key"

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Migrate オブジェクトを作成
login_manager = LoginManager(app)
login_manager.login_view = "login"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255))
    color = db.Column(db.String(20), default="#3788d8")
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    created_by_user = db.relationship("User", backref="events")

    def __repr__(self):
        return f"<Event {self.title} ({self.start} - {self.end})>"


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    status = db.Column(db.String(20), default="未定")

    event = db.relationship("Event", backref="participants")
    user = db.relationship("User", backref="participations")

    def __repr__(self):
        return (
            f"<Participant {self.user.username} - {self.event.title} ({self.status})>"
        )


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash("管理者権限が必要です。", "error")
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return decorated_function


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("ログインしました。", "success")
            return redirect(url_for("index"))
        else:
            flash("ユーザー名またはパスワードが間違っています。", "error")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("ログアウトしました。", "success")
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # email = request.form.get("email")  # この行を削除
        user = User.query.filter_by(username=username).first()
        if user:
            flash("このユーザー名はすでに使用されています。", "error")
            return redirect(url_for("register"))
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("登録が完了しました。", "success")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/events", methods=["GET"])
@login_required
def get_events():
    start = request.args.get("start")
    end = request.args.get("end")
    events = (
        Event.query.filter(Event.start >= start, Event.end <= end)
        .order_by(Event.start)
        .all()
    )
    return jsonify(
        [
            {
                "id": event.id,
                "title": event.title,
                "start": event.start.isoformat(),
                "end": event.end.isoformat(),
                "color": event.color,
                "location": event.location,
            }
            for event in events
        ]
    )


@app.route("/event", methods=["POST"])
@login_required
@admin_required
def add_or_update_event():
    event_data = request.json
    if "id" in event_data:
        event = Event.query.get(event_data["id"])
        if not event:
            return jsonify({"error": "Event not found"}), 404
    else:
        event = Event(created_by=current_user.id)

    event.title = event_data["title"]
    event.start = datetime.fromisoformat(event_data["start"])
    event.end = datetime.fromisoformat(event_data["end"])
    event.location = event_data.get("location", "")
    event.color = event_data.get("color", "#3788d8")

    if "id" in event_data:
        db.session.commit()
        return jsonify({"message": "Event updated successfully"}), 200
    else:
        db.session.add(event)
        db.session.commit()
        return jsonify({"message": "Event created successfully"}), 201


@app.route("/event/<int:id>/delete", methods=["DELETE"])
@login_required
@admin_required
def delete_event(id):
    event = Event.query.get(id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    try:
        # イベントに関連付けられた参加者を削除
        for participant in event.participants:
            db.session.delete(participant)
        # イベントを削除
        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": "Event deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting event: {str(e)}")
        return jsonify({"error": "Failed to delete event"}), 500


@app.route("/event/<int:id>/participants", methods=["GET", "POST"])
@login_required
def get_or_update_participants(id):
    event = Event.query.get(id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    if request.method == "GET":
        participants = Participant.query.filter_by(event_id=id).all()
        return jsonify(
            [
                {
                    "id": p.id,
                    "user_id": p.user_id,
                    "username": User.query.get(p.user_id).username,
                    "status": p.status,
                }
                for p in participants
            ]
        )

    elif request.method == "POST":
        status = request.json.get("status")
        if status not in ["参加", "不参加", "未定"]:
            return jsonify({"error": "Invalid status"}), 400
        participant = Participant.query.filter_by(
            event_id=id, user_id=current_user.id
        ).first()
        if participant:
            participant.status = status
        else:
            participant = Participant(
                event_id=id, user_id=current_user.id, status=status
            )
            db.session.add(participant)
        db.session.commit()
        return jsonify({"status": status}), 201


@app.route("/event/<int:id>/participant/<int:participant_id>", methods=["DELETE"])
@login_required
@admin_required
def delete_participant(id, participant_id):
    participant = Participant.query.get(participant_id)
    if participant and participant.event_id == id:
        db.session.delete(participant)
        db.session.commit()
        return "", 204
    return (
        jsonify(
            {"error": "Participant not found or you do not have permission to delete"}
        ),
        404,
    )


@app.route("/admin")
@login_required
@admin_required
def admin_panel():
    users = User.query.all()
    return render_template("admin.html", users=users)


@app.route("/admin/toggle_admin/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def toggle_admin(user_id):
    user = User.query.get(user_id)
    if user:
        user.is_admin = not user.is_admin
        db.session.commit()
        flash(
            f'ユーザー {user.username} の管理者権限を{"付与" if user.is_admin else "削除"}しました。',
            "success",
        )
    else:
        flash("ユーザーが見つかりません。", "error")
    return redirect(url_for("admin_panel"))


@app.route("/admin/delete_user/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        # ユーザーに関連付けられたイベントの参加者を削除
        for event in user.events:
            for participant in event.participants:
                if participant.user_id == user_id:
                    db.session.delete(participant)
        # ユーザーを削除
        db.session.delete(user)
        db.session.commit()
        flash(f"ユーザー {user.username} を削除しました。", "success")
    else:
        flash("ユーザーが見つかりません。", "error")
    return redirect(url_for("admin_panel"))


@app.route("/collect")
@login_required
def collect():
    date_str = request.args.get("date")
    if date_str:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        events = Event.query.filter(db.func.date(Event.start) == date).all()

        for event in events:
            event.attending = [p.user for p in event.participants if p.status == "参加"]
            event.not_attending = [
                p.user for p in event.participants if p.status == "不参加"
            ]
            event.undecided = [p.user for p in event.participants if p.status == "未定"]

        return render_template("collect.html", events=events, selected_date=date)

    return render_template("collect.html", events=None, selected_date=None)


@app.route("/admin/bulk_create_events", methods=["GET", "POST"])
@login_required
@admin_required
def bulk_create_events():
    if request.method == "POST":
        try:
            events_data = request.json.get("events").split("\n")
            events = []
            for event_line in events_data:
                if event_line.strip():  # 空行をスキップ
                    date, title, start_time, end_time, location, color = (
                        event_line.strip().split(",")
                    )
                    start = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
                    end = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")
                    event = Event(
                        title=title,
                        start=start,
                        end=end,
                        location=location,
                        color=color,
                        created_by=current_user.id,
                    )
                    events.append(event)

            db.session.bulk_save_objects(events)
            db.session.commit()

            return jsonify({"message": "Events created successfully"}), 201
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error creating events: {str(e)}")
            return jsonify({"error": str(e)}), 400

    return render_template("bulk_create_events.html")
