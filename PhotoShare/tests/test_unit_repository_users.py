import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Photos, Users
from src.schemas import PhotoBase, PhotoStatusUpdate, UserModel, UserDb, UserResponse
from src.repository.photo import (
    get_photos,
    get_photo,
    create_photo,
    remove_photo,
    update_photo,
    update_status_photo
)

class TestContact(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = Users(id=1)

    async def test_get_contacts(self):
        contacts = [Photos(), Photos(), Photos()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_photos(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact(self):
        contact = Photos()
        self.session.query().filter().filter().first.return_value = contact
        result = await get_photo(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().filter().first.return_value = None
        result = await get_photo(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = PhotoBase(photo="string", description="string", tags="string", user_id ="string", created_at="string")
        photo = [Photos(id=1, user_id=1)]
        self.session.query().filter().filter().all.return_value = photo
        result = await create_photo(body=body, user=self.user, db=self.session)
        self.assertEqual(result.photo, body.photo)
        self.assertEqual(result.description, body.description)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact(self):
        contact = Photos()
        self.session.query().filter().filter().first.return_value = contact
        result = await remove_photo(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_note_not_found(self):
        self.session.query().filter().filter().first.return_value = None
        result = await remove_photo(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact(self):
        body = PhotoBase(photo="string", description="string", tags="string", user_id ="string", created_at="string")
        contact = Photos()
        self.session.query().filter().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_photo(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body = PhotoBase(name="string_name", surname="string", email_address="string", phone_number="string", date_of_birth="2024-07-25", additional_data="string")
        self.session.query().filter().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_photo(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_status_contact_found(self):
        body = PhotoStatusUpdate(done=True)
        contact = Photos()
        self.session.query().filter().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_status_photo(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_status_note_not_found(self):
        body = PhotoStatusUpdate(done=True)
        self.session.query().filter().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_status_photo(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()

