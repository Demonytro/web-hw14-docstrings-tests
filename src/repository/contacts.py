from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel, ContactActiveModel


async def get_contacts(db: Session):
    """
    The get_contacts function returns a list of all contacts in the database.


    :param db: Session: Pass the database session object into the function
    :return: A list of contact objects
    """
    contacts = db.query(Contact).all()
    return contacts


async def get_contacts_birthday(birthday: str, db: Session):
    """
    The get_contacts_birthday function returns a list of contacts with the specified birthday.
        Args:
            birthday (str): The contact's birthday to search for.
            db (Session): A database session object.

    :param birthday: str: Filter the contacts by birthday
    :param db: Session: Pass in the database session to be used
    :return: A list of contacts that have the same birthday
    """
    contacts = db.query(Contact).filter_by(birthday=birthday).all()
    return contacts


async def get_contact_by_id(contact_id: int, db: Session):
    """
    The get_contact_by_id function returns a contact object from the database based on its id.
        Args:
            contact_id (int): The id of the desired contact.
            db (Session): A connection to the database.

    :param contact_id: int: Specify the id of the contact to be retrieved
    :param db: Session: Pass the database session to the function
    :return: The contact with the given id
    """
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def get_contact_by_email(email: str, db: Session):
    """
    The get_contact_by_email function returns a contact object from the database based on the email address provided.
        Args:
            email (str): The email address of the contact to be retrieved.
            db (Session): A connection to our database, which is used for querying and updating data.

    :param email: str: Filter the database by email
    :param db: Session: Pass in a database session
    :return: The contact with the given email address
    """
    contact = db.query(Contact).filter_by(email=email).first()
    return contact


async def get_contacts_by_first_name(first_name: str, db: Session):
    """
    The get_contacts_by_first_name function returns a list of contacts with the given first name.

    :param first_name: str: Specify the first name of the contact
    :param db: Session: Pass the database session into the function
    :return: A list of contact objects
    """
    contacts = db.query(Contact).filter_by(first_name=first_name).all()
    return contacts


async def get_contacts_by_last_name(last_name: str, db: Session):
    """
    The get_contacts_by_last_name function returns a list of contacts with the given last name.

    :param last_name: str: Specify the last name of the contact you want to retrieve
    :param db: Session: Pass the database session object to the function
    :return: A list of contact objects
    """
    contacts = db.query(Contact).filter_by(last_name=last_name).all()
    return contacts


async def create(body: ContactModel, db: Session):
    """
    The create function creates a new contact in the database.


    :param body: ContactModel: Pass the contact information to the database
    :param db: Session: Pass in the database session
    :return: The contact object that was created
    """
    contact = Contact(**body.dict())  # Owner(**body.dict())   Contact(email=body.email)
    db.add(contact)
    db.commit()
    return contact


async def update(contact_id: int, body: ContactModel, db: Session):
    """
    The update function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactModel): The updated version of the ContactModel object.

    :param contact_id: int: Specify the id of the contact that will be deleted
    :param body: ContactModel: Pass the contact data to be updated
    :param db: Session: Access the database
    :return: The updated contact
    """
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.email = body.email
        db.commit()
    return contact


async def remove(contact_id: int, db: Session):
    """
    The remove function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            db (Session): A connection to the database.

    :param contact_id: int: Specify the id of the contact to be removed
    :param db: Session: Pass the database session to the function
    :return: The contact that was removed from the database
    """
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def set_is_active_contact(contact_id: int, body: ContactActiveModel, db: Session):
    """
    The set_is_active_contact function takes in a contact_id and a body containing the is_active_contact value.
    It then gets the contact by id, checks if it exists, sets its is_active value to that of the body's, and commits it to db.


    :param contact_id: int: Find the contact in the database
    :param body: ContactActiveModel: Pass the is_active_contact value to the function
    :param db: Session: Pass the database session to the function
    :return: The contact that was updated
    """
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.is_active_contact = body.is_active_contact
        db.commit()
    return contact
