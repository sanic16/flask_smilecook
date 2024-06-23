from extensions import db

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    type = db.Column(db.String(16), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    def add(self):
        db.session.add(self)
        db.session.commit()

