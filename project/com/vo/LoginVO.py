from project import db


class LoginVO(db.Model):
    __tablename__ = 'loginmaster'
    loginId = db.Column('loginId', db.Integer, primary_key=True, autoincrement=True)
    loginEmail = db.Column('loginEmail', db.String(100), nullable=False)
    loginPassword = db.Column('loginPassword', db.String(100), nullable=False)
    loginRole = db.Column('loginRole', db.String(100), nullable=False)

    def as_dict(self):
        return {
            'loginId': self.loginId,
            'loginEmail': self.loginEmail,
            'loginPassword': self.loginPassword,
            'loginRole':self.loginRole
        }


db.create_all()
