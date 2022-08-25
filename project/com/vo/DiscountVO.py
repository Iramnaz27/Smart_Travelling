from project import db


class DiscountVO(db.Model):
    __tablename__ = 'discountmaster'
    discountId = db.Column('discountId', db.Integer, primary_key=True, autoincrement=True)
    discountNewcustomer = db.Column('discountNewcustomer', db.Integer)
    discountOldcustomer = db.Column('discountOldcustomer', db.Integer)
    discountAllcustomer = db.Column('discountAllcustomer',db.Integer)
    discountExpireDateForNewCustomer=db.Column('discountExpireDateForNewCustomer',db.DATE)
    discountExpireDateForOldCustomer=db.Column('discountExpireDateForOldCustomer',db.DATE)
    discountExpireDateForAllCustomer=db.Column('discountExpireDateForAllCustomer',db.DATE)

    def as_dict(self):
        return {
            'discountId':self.discountId,
            'discountNewcustomer': self. discountNewcustomer,
            'discountOldcustomer': self.discountOldcustomer,
            'discountAllcustomer': self.discountAllcustomer,
            'discountExpireDateForNewCustomer':self.discountExpireDateForNewCustomer,
            'discountExpireDateForOldCustomer':self.discountExpireDateForOldCustomer,
            'discountExpireDateForAllCustomer':self.discountExpireDateForAllCustomer
        }


db.create_all()