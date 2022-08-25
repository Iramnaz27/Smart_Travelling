from project import db


class InquiryVO(db.Model):
    __tablename__ = 'inquirymaster'
    inquiryId = db.Column('inquiryId', db.Integer, primary_key=True, autoincrement=True)
    inquiryEmail = db.Column('inquiryEmail', db.String((100)))
    inquirySubject = db.Column('inquirySubject',db.String(100))
    inquiryMessage = db.Column('inquiryMessage',db.String(200))
    inquiryDate = db.Column('inquiryDate',db.DATE)
    inquiryReply=db.Column('inquiryReply',db.String(200))
   
    def as_dict(self):
        return {
            'inquiryId':self.inquiryId,
            'inquiryEmail': self.inquiryEmail,
            'inquirySubject': self.inquirySubject,
            'inquiryMessage': self.inquiryMessage,
            'inquiryDate':self.inquiryDate,
            'inquityReply':self.inquiryReply
        }


db.create_all() 