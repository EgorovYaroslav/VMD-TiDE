from sqlalchemy.orm import Session

class CRUD:
    """
    Generic CRUD class to operate with SQLAlchemy ORM models.
    """

    def __init__(self, model):
        """
        Initialize the CRUD class with the ORM model.
        :param model: The SQLAlchemy ORM model class (e.g., Data, Forecast7).
        """
        self.model = model

    def create(self, db: Session, **kwargs):
        """
        Create a new record in the database.
        :param db: SQLAlchemy session object.
        :param kwargs: Key-value pairs representing the record's fields.
        :return: The created record.
        """
        obj = self.model(**kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get_by_id(self, db: Session, id: int):
        """
        Retrieve a record by its primary key (id).
        :param db: SQLAlchemy session object.
        :param id: Primary key value.
        :return: The retrieved record or None if not found.
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, db: Session):
        """
        Retrieve all records from the table.
        :param db: SQLAlchemy session object.
        :return: List of all records.
        """
        return db.query(self.model).all()

    def update(self, db: Session, id: int, **kwargs):
        """
        Update a record by its primary key (id).
        :param db: SQLAlchemy session object.
        :param id: Primary key value.
        :param kwargs: Key-value pairs representing the fields to update.
        :return: True if the record was updated, False otherwise.
        """
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            for key, value in kwargs.items():
                setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
            return True
        return False

    def delete(self, db: Session, id: int):
        """
        Delete a record by its primary key (id).
        :param db: SQLAlchemy session object.
        :param id: Primary key value.
        :return: True if the record was deleted, False otherwise.
        """
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False