from project import db
from project.com.vo.LoginVO import LoginVO

class UserVO(db.Model):
    __tablename__ = 'usermaster'
    userId = db.Column('userId', db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column('userName', db.String(100))
    userEmail = db.Column('userEmail', db.String(100))
    userMobile = db.Column('userMobile',db.String(11))
    userAddress = db.Column('userAddress',db.String(100))
    userStatus = db.Column('userStatus',db.String(100))
    userJoiningDate = db.Column('userJoiningDate',db.DATE)
    userDiscountStatus = db.Column('userDiscountStatus',db.Integer)
    userFileName = db.Column('userFileName', db.String(100))
    userFilePath = db.Column('userFilePath', db.String(100))
    user_LoginId = db.Column('user_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'userId': self.userId,
            'userName': self.userName,
            'userEmail': self.userEmail,
            'userMobile': self.userMobile,
            'userAddress': self.userAddress,
            'userStatus': self.userStatus,
            'userJoiningDate': self.userJoiningDate,
            'userDiscountStatus': self.userDiscountStatus,
            'userFileName': self.userFileName,
            'userFilePath': self.userFilePath,
            'user_LoginId': self.user_LoginId
        }


db.create_all()


