import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.database.models import Group
from src.schemas.groups import GroupModel
from src.repository.groups import (
    create_group,
    get_all,
    get_groups,
    update_group,
    delete_group,
)


class TestGroupRepository(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)

    async def test_get_groups(self):
        groups = [Group(), Group(), Group()]
        self.session.query().order_by().limit().offset().all.return_value = groups
        result = await get_groups(10, 0, self.session)
        self.assertEqual(result, groups)

    async def test_create_group(self):
        body = GroupModel(name="test")
        result = await create_group(body, self.session)
        print(result)
        self.assertEqual(result.name, body.name)
        self.assertTrue(hasattr(result, "id"))
        self.assertTrue(hasattr(result, "name"))
