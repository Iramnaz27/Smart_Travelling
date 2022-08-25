from project import db
from project.com.vo.LoginVO import LoginVO
from sqlalchemy import func


class LoginDAO:
    def validateLogin(self,loginVO):
        loginList = LoginVO.query.filter_by(loginEmail=func.binary(loginVO.loginEmail), loginPassword=func.binary(loginVO.loginPassword)).all()
        return loginList

    def insertLogin(self, loginVO):
        db.session.add(loginVO)
        db.session.commit()

    def deleteLogin(self,loginVO):

        loginList = LoginVO.query.get(loginVO.loginId)

        db.session.delete(loginList)

        db.session.commit()

    def updateLogin(self,loginVO):

        db.session.merge(loginVO)

        db.session.commit()