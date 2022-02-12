import unittest
from datetime import datetime, timedelta

from app import create_app, db
from app.models import Post, User
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='hardkoro')
        u.set_password('gene')
        self.assertFalse(u.check_password('koro'))
        self.assertTrue(u.check_password('gene'))

    def test_avatar(self):
        u = User(username='test', email='test@example.com')
        self.assertEqual(
            u.avatar(128),
            (
                'https://www.gravatar.com/avatar/'
                '55502f40dc8b7c769880b10874abc9d0'
                '?d=identicon&s=128'
            )
        )

    def test_follow(self):
        u1 = User(username='test', email='test@example.com')
        u2 = User(username='hardkoro', email='hardkoro@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u2.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'hardkoro')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'test')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # create four users
        u1 = User(username='test', email='test@example.com')
        u2 = User(username='hardkoro', email='hardkoro@example.com')
        u3 = User(username='new', email='new@example.com')
        u4 = User(username='old', email='old@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(
            body='post from test',
            author=u1,
            timestamp=now + timedelta(seconds=1)
        )
        p2 = Post(
            body='post from hardkoro',
            author=u2,
            timestamp=now + timedelta(seconds=4)
        )
        p3 = Post(
            body='post from new',
            author=u3,
            timestamp=now + timedelta(seconds=3)
        )
        p4 = Post(
            body='post from old',
            author=u4,
            timestamp=now + timedelta(seconds=2)
        )
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # test follows hardkoro
        u1.follow(u4)  # test follows old
        u2.follow(u3)  # hardkoro follows new
        u3.follow(u4)  # new follows old
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])


if __name__ == '__main__':
    unittest.main(verbosity=2)
