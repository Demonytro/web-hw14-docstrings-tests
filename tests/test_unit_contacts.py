import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.repository.contacts import (
                                get_contacts,
                                get_contacts_birthday,
                                get_contact_by_id,
                                get_contact_by_email,
                                get_contacts_by_first_name,
                                get_contacts_by_last_name,
                                create,
                                update,
                                remove,
                                set_is_active_contact
)
from src.schemas import ContactModel


class TestContacts(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        # self.contact = Contact(id=1, email="test@test.api.com")

    async def test_get_contacts(self):
        contacts = [Contact() for _ in range(5)]
        self.session.query(Contact).all.return_value = contacts
        result = await get_contacts(self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_birthday(self):
        ...
    async def test_get_contact_by_id(self):
        ...
    async def test_get_contact_by_email(self):
        ...
    async def test_get_contacts_by_first_name(self):
        ...
    async def test_get_contacts_by_last_name(self):
        ...
    async def test_update(self):
        ...
    async def test_remove(self):
        ...
    async def test_set_is_active_contact(self):
        ...




    async def test_create(self):
        body = ContactModel(
            id=1,
            first_name='Dmytro',
            last_name='Oseledko',
            email="test@test.api.com",
            phone_number='050-907-97-77',
            birthday='10-04-2019',
            nick='Badrunt',
            is_active_contact=True,
            description="Це дуже багато коду"

            # nick='Barsik',
            # age=4,
            # vaccinated=False,
            # description="Це дуже багато коду",
            # owner_id=self.owner.id
        )

        result = await create(body, self.session)
        self.assertEqual(result.nick, body.nick)
        self.assertTrue(hasattr(result, 'id'))
