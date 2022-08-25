from project import db

class DriverVO(db.Model):
    __tablename__ = 'drivermaster'
    driverId = db.Column('driverId', db.Integer, primary_key=True, autoincrement=True)
    driverName = db.Column('driverName', db.String(100))
    driverEmail = db.Column('driverEmail', db.String(100))
    driverGender = db.Column('driverGender', db.String(7))
    driverMobile = db.Column('driverMobile',db.String(11))
    driverAddress = db.Column('driverAddress',db.String(100))
    driverStatus = db.Column('driverStatus',db.String(100))
    driverFlag = db.Column('driverFlag',db.Integer)
    driverPrice = db.Column('driverPrice',db.Integer)
    driverExtraDayPrice = db.Column('driverExtraDayPrice', db.Integer)
    driverFileName = db.Column('driverFileName', db.String(100))
    driverFilePath = db.Column('driverFilePath', db.String(100))
    driverLicenseNumber = db.Column('driverLicenseNumber', db.String(100))

    def as_dict(self):
        return {
            'driverId': self.driverId,
            'driverName': self.driverName,
            'driverEmail': self.driverEmail,
            'driverGender': self.driverGender,
            'driverMobile': self.driverMobile,
            'driverAddress': self.driverAddress,
            'driverStatus': self.driverStatus,
            'driverFlag': self.driverFlag,
            'driverPrice': self.driverPrice,
            'driverExtraDayPrice': self.driverExtraDayPrice,
            'driverFileName': self.driverFileName,
            'driverFilePath': self.driverFilePath,
            'driverLicenseNumber': self.driverLicenseNumber,
        }


db.create_all()


