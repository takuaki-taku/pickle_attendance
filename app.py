from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
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
app.config["SECRET_KEY"] = (
    "your_secret_key"  # 本番環境では安全な秘密鍵を使用してください
)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100))
    color = db.Column(db.String(20))
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    # ここに変更を加えました
    return db.session.get(User, int(user_id))


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("この操作には管理者権限が必要です。", "error")
            return redirect(url_for("index"))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and check_password_hash(user.password_hash, request.form["password"]):
            login_user(user)
            return redirect(url_for("index"))
        flash("ユーザー名またはパスワードが正しくありません。", "error")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if User.query.filter_by(username=username).first():
            flash("このユーザー名は既に使用されています。", "error")
        else:
            new_user = User(
                username=username, password_hash=generate_password_hash(password)
            )
            db.session.add(new_user)
            db.session.commit()
            flash("登録が完了しました。ログインしてください。", "success")
            return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/events")
@login_required
def get_events():
    events = Event.query.all()
    return jsonify(
        [
            {
                "id": event.id,
                "title": event.title,
                "start": event.start.isoformat(),
                "end": event.end.isoformat(),
                "location": event.location,
                "color": event.color,
                "participants_count": Participant.query.filter_by(
                    event_id=event.id, status="参加"
                ).count(),
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

    if "id" not in event_data:
        db.session.add(event)
    db.session.commit()

    return jsonify(
        {
            "id": event.id,
            "title": event.title,
            "start": event.start.isoformat(),
            "end": event.end.isoformat(),
            "location": event.location,
            "color": event.color,
            "participants_count": Participant.query.filter_by(
                event_id=event.id, status="参加"
            ).count(),
        }
    )


@app.route("/event/<int:id>", methods=["DELETE"])
@login_required
@admin_required
def delete_event(id):
    event = Event.query.get(id)
    if event:
        db.session.delete(event)
        db.session.commit()
        return "", 204
    return jsonify({"error": "Event not found"}), 404


@app.route("/event/<int:id>/participants", methods=["GET", "POST"])
@login_required
def manage_participants(id):
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

    participant_data = request.json
    existing_participant = Participant.query.filter_by(
        event_id=id, user_id=current_user.id
    ).first()
    if existing_participant:
        existing_participant.status = participant_data["status"]
    else:
        new_participant = Participant(
            event_id=id, user_id=current_user.id, status=participant_data["status"]
        )
        db.session.add(new_participant)
    db.session.commit()

    return jsonify(
        {
            "id": (
                existing_participant.id if existing_participant else new_participant.id
            ),
            "user_id": current_user.id,
            "username": current_user.username,
            "status": participant_data["status"],
        }
    ), (200 if existing_participant else 201)


@app.route("/event/<int:event_id>/participant/<int:participant_id>", methods=["DELETE"])
@login_required
def delete_participant(event_id, participant_id):
    participant = Participant.query.get(participant_id)
    if participant and participant.user_id == current_user.id:
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


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
