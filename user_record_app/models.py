from user_record_app import db

class User(db.Model):
    """
    Data model for user accounts.
    """
    __tablename__ = "user_records"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    first_name = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    last_name = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    phone_number = db.Column(
        db.String(20),
        index=False,
        unique=False,
        nullable=False
    )
    city = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=True
    )
    street = db.Column(
        db.String(20),
        index=False,
        unique=False,
        nullable=True
    )
    province = db.Column(
        db.String(2),
        index=False,
        unique=False,
        nullable=True
    )

    def as_dict(self):
        """
        Returns the attributes of the class into a dictionary that is indexed by
        the class' id.
        """
        dict = {
            self.id : {
                "city": self.city,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "phone_number": self.phone_number,
                "province": self.province,
                "street": self.street
            }
        }

        return dict
