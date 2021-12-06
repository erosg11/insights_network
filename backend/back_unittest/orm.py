import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from crud import update_tag, update_insight, create_insight, delete_insight, get_insight_by_id, delete_tag, \
        get_tag_by_id, create_multiple_tags, create_tag, list_cards

from entitys import Base


class ORMTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine(f'sqlite:///:memory:')

        Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.session = Session()

    def tearDown(self) -> None:
        self.session.close()

    def test_create_tag(self):
        tag = create_tag(self.session, 'teste')
        print(tag)
        self.assertEqual(tag.nome, 'teste')

    def test_create_insight(self):
        insight = create_insight()


if __name__ == '__main__':
    unittest.main()