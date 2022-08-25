from project import db
from project.com.vo.ComplaintVO import ComplaintVO
from project.com.vo.UserVO import UserVO


class ComplaintDAO:
    def insertComplaint(self, complaintVO):
        db.session.add(complaintVO)
        db.session.commit()

    def editComplaint(self,complaintVO):
        complaintList = ComplaintVO.query.filter_by(complaintId=complaintVO.complaintId).all()
        return complaintList

    def updateComplaint(self,complaintVO):
        db.session.merge(complaintVO)
        db.session.commit()

    def adminViewComplaint(self, complaintVO):
        complaintList = db.session.query(ComplaintVO, UserVO) \
            .join(UserVO, ComplaintVO.complaintFrom_LoginId == UserVO.user_LoginId) \
            .filter(ComplaintVO.complaintTo_LoginId == complaintVO.complaintTo_LoginId).all()
        return complaintList

    def viewComplaint(self, complaintVO):
        complaintList = ComplaintVO.query.filter_by(complaintFrom_LoginId=complaintVO.complaintFrom_LoginId).all()
        return complaintList