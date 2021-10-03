from flask_login import UserMixin

from dbms import get_db


class User(UserMixin):
    def __init__(self, id_, name, discriminator, email, profile_pic_url):
        self.id = id_
        self.name = name
        self.discriminator = discriminator
        self.email = email
        self.profile_pic_url = profile_pic_url

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0],
            name=user[1],
            discriminator=user[2],
            email=user[3],
            profile_pic_url=user[4],
        )
        return user

    @staticmethod
    def create(id_, name, discriminator, email, profile_pic_url):
        db = get_db()
        db.execute(
            "INSERT INTO user (id, name, discriminator, email, profile_pic_url) "
            "VALUES (?, ?, ?, ?,?)",
            (id_, name, discriminator, email, profile_pic_url),
        )
        db.commit()
