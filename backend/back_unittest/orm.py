import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from crud import update_tag, update_insight, create_insight, delete_insight, delete_tag, \
    create_tag, list_cards
from entitys import Base, NewInsight, Tag


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
        self.assertEqual(tag.name, 'teste')
        return tag

    def test_create_insight_with_new_tag(self):
        new_insight = NewInsight(texto='teste de insight', tags=['teste'])
        insight = create_insight(self.session, new_insight)
        print(insight)
        self.assertEqual(insight.texto, 'teste de insight')
        return insight

    def test_list_all_insight(self):
        insight = self.test_create_insight_with_new_tag()
        insights = list_cards(self.session)
        print(insights)
        self.assertListEqual(insights, [insight])

    def test_delete_insight(self):
        tag = self.test_create_tag()
        insight = self.test_create_insight_with_new_tag()
        delete_insight(self.session, insight.id)
        insights = list_cards(self.session)
        print(insights)
        self.session.refresh(tag)
        self.assertListEqual(insights, [])
        self.assertListEqual(tag.insights, [])

    def test_create_insight_with_old_tag(self):
        tag = self.test_create_tag()
        insight = self.test_create_insight_with_new_tag()
        print(tag, insight, sep='\n')
        self.assertEqual(insight.tags[0], tag)
        return insight

    def test_update_tag_ok(self):
        tag = self.test_create_tag()
        new_tag = update_tag(self.session, tag.id, Tag(name='teste2'))
        print(new_tag)
        self.assertEqual(new_tag.name, 'teste2')

    def test_update_tag_nok(self):
        tag = self.test_create_tag()
        with self.assertRaises(ValueError):
            new_tag = update_tag(self.session, tag.id, Tag(name=tag.name))
            print(new_tag)

    def test_update_insight_ok(self):
        insight = self.test_create_insight_with_new_tag()
        new_insight = update_insight(self.session, insight.id, NewInsight(texto='Teste 2 de insight', tags=['teste2']))
        print(new_insight)
        self.assertEqual(insight.id, new_insight.id)
        self.assertEqual(insight.texto, 'Teste 2 de insight')
        self.assertEqual(len(insight.tags), 1)
        self.assertEqual(insight.tags[0].name, 'teste2')

    def test_update_insight_nok(self):
        insight = self.test_create_insight_with_new_tag()
        with self.assertRaises(ValueError):
            new_insight = update_insight(self.session, insight.id, NewInsight(texto=insight.texto, tags=insight.tags))
            print(new_insight)

    def test_delete_tag(self):
        tag = self.test_create_tag()
        insight = self.test_create_insight_with_new_tag()
        delete_tag(self.session, tag.id)
        self.session.refresh(insight)
        print(insight)
        self.assertListEqual(insight.tags, [])

    def test_list_insights(self):
        trash = [
            create_insight(self.session, NewInsight(texto=f'Teste {i}', tags=[f'teste{k}' for k in range(j)]))
            for i in range(3)
            for j in range(3)
        ]

        test_insights = [
            create_insight(self.session, NewInsight(texto=f'Teste {i}', tags=['teste3'])) for i in range(5)
        ]

        insights = list_cards(self.session, ['teste3'])
        print(insights)
        self.assertListEqual(sorted(insights, key=lambda x: x.texto), test_insights)


if __name__ == '__main__':
    unittest.main()
