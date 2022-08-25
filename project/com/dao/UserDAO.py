from project import db
from project.com.vo.UserVO import UserVO


class UserDAO:

    def insertUser(self, userVO):
        db.session.add(userVO)
        db.session.commit()

    def viewUser(self):
        userList=UserVO.query.all()
        return userList

    def deleteUser(self,userVO):

        userList = UserVO.query.get(userVO.userId)

        db.session.delete(userList)

        db.session.commit()

        return userList

    def editUser(self,userVO):

        userList = UserVO.query.filter_by(userId=userVO.userId).all()

        return userList

    def updateUser(self,userVO):

        db.session.merge(userVO)

        db.session.commit()
