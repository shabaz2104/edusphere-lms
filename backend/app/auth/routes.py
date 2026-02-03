from flask import Blueprint, request, jsonify
from functools import wraps

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from app.extensions import db
from app.models import User, Class


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


# =========================
# ROLE-BASED DECORATOR
# =========================
def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(int(user_id))

            if not user or user.role != required_role:
                return jsonify({"error": "Access forbidden"}), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper


# =========================
# HEALTH CHECK
# =========================
@auth_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({
        "status": "ok",
        "message": "Auth service is alive"
    })


# =========================
# REGISTER
# =========================
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not all([name, email, password, role]):
        return jsonify({"error": "Missing required fields"}), 400

    if role not in ["student", "teacher"]:
        return jsonify({"error": "Invalid role"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    user = User(name=name, email=email, role=role)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 201


# =========================
# LOGIN
# =========================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Login successful",
        "access_token": access_token
    }), 200


# =========================
# CURRENT USER
# =========================
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }), 200


# =========================
# CREATE CLASS (TEACHER ONLY)
# =========================
@auth_bp.route("/classes", methods=["POST"])
@jwt_required()
@role_required("teacher")
def create_class():
    data = request.get_json()

    title = data.get("title")
    description = data.get("description")
    meet_link = data.get("meet_link")

    if not title or not meet_link:
        return jsonify({"error": "Title and meet link required"}), 400

    teacher_id = int(get_jwt_identity())

    new_class = Class(
        title=title,
        description=description,
        meet_link=meet_link,
        teacher_id=teacher_id
    )

    db.session.add(new_class)
    db.session.commit()

    return jsonify({
        "message": "Class created successfully",
        "class": {
            "id": new_class.id,
            "title": new_class.title,
            "meet_link": new_class.meet_link
        }
    }), 201
