from application import db

class Kirjaus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sisaankirjaus = db.Column(db.DateTime, default=db.func.current_timestamp())
    uloskirjaus = db.Column(db.DateTime, default=db.func.current_timestamp())
    kertyma = db.Column(db.Integer, nullable=False)
    kirjattu_pvm = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, kertyma):
        self.kertyma = 0

