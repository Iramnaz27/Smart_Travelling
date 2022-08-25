from project import db


class VehicleVO(db.Model):
    __tablename__ = 'vehiclemaster'
    vehicleId = db.Column('vehicleId', db.Integer, primary_key=True, autoincrement=True)
    vehicleType = db.Column('vehicleName', db.String(100))
    vehicleDescription = db.Column('vehicleDescription', db.String(100))
    vehicleColor = db.Column('vehicleColor',db.String(11))
    vehicleStatus = db.Column('vehicleStatus',db.String(100))
    vehicleFlag = db.Column('vehicleFlag',db.Integer)
    vehiclePriceperkm = db.Column('vehiclePriceperkm',db.Integer)
    vehiclePrice = db.Column('vehiclePrice', db.Integer)
    vehicleExtraDayPrice = db.Column('vehicleExtraDayPrice', db.Integer)
    vehicleFileName = db.Column('vehicleFileName', db.String(100))
    vehicleFilePath = db.Column('vehicleFilePath', db.String(100))
    vehicleCapacity = db.Column('vehicleCapacity', db.String(100))
    vehicleNumberplate = db.Column('vehicleNumberplate',db.String(100))
    vehicleCurrentkm = db.Column('vehicleCurrent',db.String(100))

    def as_dict(self):
        return {
            'vehicleId': self.vehicleId,
            'vehicleType': self.vehicleType,
            'vehicleDescription': self.vehicleDescription,
            'vehicleColor': self.vehicleColor,
            'vehicleStatus': self.vehicleStatus,
            'vehicleFlag': self.vehicleFlag,
            'vehiclePriceperkm': self.vehiclePriceperkm,
            'vehiclePrice': self.vehiclePrice,
            'vehicleExtraDayPrice': self.vehicleExtraDayPrice,
            'vehicleFileName': self.vehicleFileName,
            'vehicleFilePath': self.vehicleFilePath,
            'vehicleCapacity': self.vehicleCapacity,
            'vehicleNumberplate': self.vehicleNumberplate,
            'vehicleCurrentkm': self.vehicleCurrentkm
        }


db.create_all()