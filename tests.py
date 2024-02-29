from models import DEFAULT_IMAGE_URL, User
from app import app, db
from unittest import TestCase
import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"


# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
# app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        db.session.rollback()

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        User.query.delete()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            img_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        """Test status code and html for user list."""
        with app.test_client() as client:
            resp = client.get('/users')
            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_add_user_form(self):
        """Test new user form is rendered."""
        with app.test_client() as client:
            resp = client.get('/users/new')
            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn('<form action="/users/new"', html)

    def test_show_user_info(self):
        """Tests correct user info rendered."""
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_delete_user_redirect(self):
        """Tests redirect."""
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/delete')
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, '/users')

    def test_delete_user_redirect_followed(self):
        """Tests delete user redirect followed and user deleted."""
        with app.test_client() as client:
            resp = client.post(
                f'/users/{self.user_id}/delete', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertNotIn("test1_first", html)
            self.assertNotIn("test1_last", html)
            self.assertIn("Add user", html)
