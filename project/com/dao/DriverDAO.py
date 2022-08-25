from project import db
from project.com.vo.DriverVO import DriverVO


class DriverDAO:

    def insertDriver(self, driverVO):
        db.session.add(driverVO)
        db.session.commit()

    def viewDriver(self):
        driverList=DriverVO.query.all()
        return driverList

    def viewActiveDriver(self):
        driverList=DriverVO.query.filter_by(driverStatus="Active").all()
        return driverList

    def deleteDriver(self,driverVO):
        driver = DriverVO.query.get(driverVO.driverId)
        db.session.delete(driver)
        db.session.commit()
        return driver

    def editDriver(self,driverVO):
        driverList = DriverVO.query.filter_by(driverId=driverVO.driverId).all()
        return driverList

    def updateDriver(self,driverVO):

        db.session.merge(driverVO)

        db.session.commit()
