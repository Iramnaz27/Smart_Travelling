from project import db
from project.com.vo.InquiryVO import InquiryVO


class InquiryDAO:

    def insertInquiry(self, inquiryVO):
        db.session.add(inquiryVO)
        db.session.commit()

    def viewInquiry(self):
        inquiryList=InquiryVO.query.all()
        return inquiryList

    def updateReply(self,inquiryVO):
        db.session.merge(inquiryVO)
        db.session.commit()


    def insertReply(self, inquiryVO):
        db.session.add(inquiryVO)
        db.session.commit()    

    def viewInquiryById(self,inquiryVO):
        inquiryVO = InquiryVO.query.get(inquiryVO.inquiryId)
        return inquiryVO


   
   