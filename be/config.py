from api.models import User
from api.common import SessionLocal
from api.common.utils import hash_password
from env import admin_password


def create_admin():
    db = SessionLocal()

    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        admin = User(
            username="admin",
            password=hash_password(admin_password),
            role="admin"
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)
        db.close()
