from models import DEFAULT_IMAGE_URL, User, Post, Tag
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

# COULD SEPARATE TO TagViewTestCase and PostViewTestCase


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        db.session.rollback()

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.

        Tag.query.delete()

        Post.query.delete()

        User.query.delete()

        # Test user
        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            img_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        self.user_id = test_user.id

        # Test post
        test_post = Post(
            title="Test Title",
            content="Test Content",
            user_id=self.user_id
        )

        db.session.add(test_post)
        db.session.commit()

        self.post_id = test_post.id

        # Test tag
        test_tag = Tag(name='test_tag')

        db.session.add(test_tag)
        db.session.commit()

        self.tag_id = test_tag.id

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
            self.assertIn(f"{DEFAULT_IMAGE_URL}", html)

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

# Below this line are our posts tests

    def test_display_post(self):
        """Tests display of post given post_id"""
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn("Test Title", html)
            self.assertIn("Test Content", html)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_show_edit_post_form(self):
        """Tests whether edit post form shows"""
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}/edit')
            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn("Edit Post", html)
            self.assertIn('<input class="btn btn-warning"', html)
            self.assertIn('<input class="btn btn-success"', html)

    def test_delete_post_redirect_followed(self):
        """Tests that post got deleted on rendered template"""
        with app.test_client() as client:
            resp = client.post(
                f'/posts/{self.post_id}/delete', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertNotIn("Test Title", html)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

# Below this line are our tag tests

    def test_display_tags(self):
        """Tests that tags list shows."""
        with app.test_client() as client:
            resp = client.get('/tags')
            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn("test_tag", html)
            self.assertIn("Add Tag", html)

    def test_display_tag_form(self):
        """Tests that tag form displays."""
        with app.test_client() as client:
            resp = client.get('/tags/new')
            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn("Create a tag", html)

    def test_edit_tag_redirect_followed(self):
        """Tests that tag properly edited."""
        with app.test_client() as client:
            resp = client.post(f'/tags/{self.tag_id}/edit',
                               follow_redirects=True,
                               data={'tag_name': 'edited_test_tag'}
                               )
            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn("Tags", html)
            self.assertIn("edited_test_tag", html)
