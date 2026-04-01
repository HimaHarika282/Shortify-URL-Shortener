from flask import Blueprint, request, jsonify, redirect
from services.url_service import create_short_url, get_original_url
from models import db, URL
from sqlalchemy import func
from models import Click
from flask import session
from flask import render_template

url_bp = Blueprint('url', __name__)

@url_bp.route('/shorten', methods=['POST'])
def shorten_url():
    try:
        user_id = session.get("user_id")

        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        data = request.get_json()

        original_url = data.get('url')
        expiry_minutes = data.get('expiry_minutes')
        expiry_days = data.get('expiry_days')
        custom_alias = data.get('custom_alias')

        short_code = create_short_url(
            original_url,
            expiry_minutes,
            expiry_days,
            user_id,
            custom_alias
        )

        if not short_code:
            return jsonify({"error": "Failed to create URL"}), 500

        return jsonify({
            "short_url": request.url_root + short_code
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": "Internal error"}), 500

@url_bp.route('/<short_code>')
def redirect_url(short_code):
    try:
        original_url = get_original_url(short_code)

        if not original_url:
            return jsonify({"error": "Short URL Not Found"}), 404

        return render_template("preview.html", url=original_url)

    except Exception as e:
        print("❌ ERROR in redirect:", e)
        return jsonify({"error": "Internal Server Error"}), 500


@url_bp.route('/delete/<short_code>', methods=['DELETE'])
def delete_url(short_code):
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    url = URL.query.filter_by(short_code=short_code, user_id=user_id).first()

    if not url:
        return jsonify({"error": "Not found"}), 404

    db.session.delete(url)
    db.session.commit()

    return jsonify({"message": "Deleted"})

@url_bp.route('/stats/<short_code>')
def stats(short_code):
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    url = URL.query.filter_by(short_code=short_code, user_id=user_id).first()

    if not url:
        return jsonify({"clicks": 0, "expiry_date": None})

    return jsonify({
        "clicks": url.click_count,
        "expiry_date": url.expiry_date.isoformat() if url.expiry_date else None
    })


@url_bp.route('/myurls')
def get_user_urls():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify([])

    urls = URL.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            "original": u.original_url,
            "code": u.short_code,
            "clicks": u.click_count,
            "created": u.created_at.isoformat(),
            "expiry": u.expiry_date.isoformat() if u.expiry_date else None
        }
        for u in urls
    ])

from datetime import datetime

@url_bp.route('/analytics')
def analytics():

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    urls = URL.query.filter_by(user_id=user_id).all()

    total_urls = len(urls)
    total_clicks = sum(u.click_count for u in urls)

    now = datetime.utcnow()

    active_urls = [
        u for u in urls
        if not u.expiry_date or u.expiry_date > now
    ]

    top_url = None
    top_clicks = 0

    if active_urls:
        top = max(active_urls, key=lambda x: x.click_count)
        top_url = top.original_url
        top_clicks = top.click_count

    recent_url = None
    if urls:
        recent = URL.query.filter_by(user_id=user_id)\
            .order_by(URL.created_at.desc())\
            .first()

        recent_url = recent.original_url if recent else None
    
    click_data = db.session.query(
    func.date(Click.clicked_at),
    func.count(Click.id)
    ).join(URL, Click.url_id == URL.id)\
    .filter(URL.user_id == user_id)\
    .group_by(func.date(Click.clicked_at))\
    .all()

    dates = [row[0] for row in click_data]
    counts = [row[1] for row in click_data]

    return jsonify({
    "total_urls": total_urls,
    "total_clicks": total_clicks,
    "recent_url": recent_url,
    "dates": dates,
    "counts": counts
    })
