from models import db, URL
from utils.generator import generate_short_code
from datetime import datetime, timedelta
from models import Click

def create_short_url(original_url, expiry_minutes=None, expiry_days=None, user_id=None, custom_alias=None):

    try:
        expiry_date = None

        if expiry_minutes:
            expiry_date = datetime.utcnow() + timedelta(minutes=int(expiry_minutes))
        elif expiry_days:
            expiry_date = datetime.utcnow() + timedelta(days=int(expiry_days))

        if custom_alias:
            custom_alias = custom_alias.strip()

            if " " in custom_alias:
                return None

            existing = URL.query.filter_by(short_code=custom_alias).first()

            if existing:
                return None

            short_code = custom_alias

        else:
            while True:
                short_code = generate_short_code()
                exists = URL.query.filter_by(short_code=short_code).first()
                if not exists:
                    break

        new_url = URL(
            original_url=original_url,
            short_code=short_code,
            expiry_date=expiry_date,
            user_id=user_id,
            created_at=datetime.utcnow()  
        )

        db.session.add(new_url)
        db.session.commit()

        print("✅ URL SAVED:", short_code) 

        return short_code

    except Exception as e:
        db.session.rollback()  
        print("❌ ERROR in create_short_url:", e)
        return None


def get_original_url(short_code):

    try:
        url = URL.query.filter_by(short_code=short_code).first()

        if not url:
            return None

        if url.expiry_date and datetime.utcnow() > url.expiry_date:
            return None

        click = Click(url_id=url.id)
        db.session.add(click)

        url.click_count += 1
        db.session.commit()

        return url.original_url

    except Exception as e:
        db.session.rollback()
        print("❌ ERROR in get_original_url:", e)
        return None