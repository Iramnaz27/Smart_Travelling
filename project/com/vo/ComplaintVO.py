from project import db
from project.com.vo.LoginVO import LoginVO


class ComplaintVO(db.Model):
    __tablename__ = 'complaintmaster'
    complaintId = db.Column('complaintId', db.Integer, primary_key=True, autoincrement=True)
    complaintSubject = db.Column('complaintSubject', db.String(100))
    complaintDescription = db.Column('complaintDescription', db.String(100))
    complaintReply = db.Column('complaintReply', db.String(500))
    complaintDate = db.Column('complaintDate', db.DATE)
    complaintTime = db.Column('complaintTime', db.TIME)
    complaintTo_LoginId = db.Column('complaintTo_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))
    complaintFrom_LoginId = db.Column('complaintFrom_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {

            'complaintId': self.complaintId,
            'complaintSubject': self.complaintSubject,
            'complaintDescription': self.complaintDescription,
            'complaintReply': self.complaintReply,
            'complaintDate': self.complaintDate,
            'complaintTime': self.complaintTime,
            'complaintTo_LoginId': self.complaintTo_LoginId,
            'complaintFrom_LoginId': self.complaintFrom_LoginId
        }


db.create_all()
