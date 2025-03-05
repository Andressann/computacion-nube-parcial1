from db.db import db  

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(255), nullable=False)  
    userEmail = db.Column(db.String(255), nullable=False)  
    saleTotal = db.Column(db.Numeric(10,2), nullable=False)  
    date = db.Column(db.DateTime, default=db.func.current_timestamp())  

