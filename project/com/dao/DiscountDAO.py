from project import db
from project.com.vo.DiscountVO import DiscountVO


class DiscountDAO:
    def viewDiscount(self):
       discountList = DiscountVO.query.get(1)
       return discountList

    def updateDiscount(self,discountVO):
        db.session.merge(discountVO)
        db.session.commit()
