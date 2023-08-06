"""User resources unit tests."""

import unittest

import common
from notelist.responses import (
    MV_METHOD_NOT_ALLOWED, MV_MISSING_TOKEN, MV_INVALID_TOKEN,
    MV_VALIDATION_ERROR, MT_OK, MT_ERROR_METHOD_NOT_ALLOWED,
    MT_ERROR_INVALID_CREDENTIALS, MT_ERROR_MISSING_TOKEN,
    MT_ERROR_INVALID_TOKEN, MT_ERROR_VALIDATION)
from notelist.views.authentication import (
    MV_USER_LOGGED_IN, MV_TOKEN_REFRESHED, MV_USER_LOGGED_OUT,
    MV_INVALID_CREDENTIALS)


class LoginTestCase(common.BaseTestCase):
    """Login resource unit tests."""

    def test_get(self):
        """Test the Get method of the Login resource.

        This test tries to call the Get method, which shouldn't work.
        """
        r = self.client.get("/auth/login")

        # Check status code
        self.assertEqual(r.status_code, 405)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_METHOD_NOT_ALLOWED)
        self.assertEqual(
            res_data[message_keys[1]], MT_ERROR_METHOD_NOT_ALLOWED)

    def test_post(self):
        """Test the Get method of the Login resource.

        This test tries to log in as some user with valid credentials, which
        should work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)

        # Check status code
        self.assertEqual(r.status_code, 200)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_USER_LOGGED_IN)
        self.assertEqual(res_data[message_keys[1]], MT_OK)

        # Check result
        self.assertIn("result", res_data)
        result = res_data["result"]
        self.assertEqual(type(result), dict)

        # Check access token
        self.assertIn("access_token", result)
        access_token = result["access_token"]
        self.assertEqual(type(access_token), str)
        self.assertNotEqual(access_token, "")

        # Check refresh token
        self.assertIn("refresh_token", result)
        refresh_token = result["refresh_token"]
        self.assertEqual(type(refresh_token), str)
        self.assertNotEqual(refresh_token, "")

        # Check user ID
        self.assertIn("user_id", result)
        user_id = result["user_id"]
        self.assertEqual(type(user_id), str)
        self.assertEqual(user_id, self.reg1["id"])

    def test_post_missing_fields(self):
        """Test the Get method of the Login resource.

        This test tries to log in as some user with some mandatory field
        missing, which shouldn't work.
        """
        # Log in (without data)
        r1 = self.client.post("/auth/login")

        # Log in (without username)
        data = {"password": self.reg1["password"]}
        r2 = self.client.post("/auth/login", json=data)

        # Log in (without password)
        data = {"username": self.reg1["username"]}
        r3 = self.client.post("/auth/login", json=data)

        # Check status codes and messages
        message_keys = ("message", "message_type")

        for r in (r1, r2, r3):
            # Status code
            self.assertEqual(r.status_code, 400)

            # Message
            res_data = r.json

            for i in message_keys:
                self.assertIn(i, res_data)
                self.assertEqual(
                    res_data[message_keys[1]], MT_ERROR_VALIDATION)

        self.assertEqual(
            r1.json[message_keys[0]],
            MV_VALIDATION_ERROR.format("username, password"))

        self.assertEqual(
            r2.json[message_keys[0]], MV_VALIDATION_ERROR.format("username"))

        self.assertEqual(
            r3.json[message_keys[0]], MV_VALIDATION_ERROR.format("password"))

    def test_post_disabled_user(self):
        """Test the Get method of the Login resource.

        This test tries to log in as some disabled user, which shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg2["username"],
            "password": self.reg2["password"]}
        r = self.client.post("/auth/login", json=data)

        # Check status code
        self.assertEqual(r.status_code, 401)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_INVALID_CREDENTIALS)
        self.assertEqual(
            res_data[message_keys[1]], MT_ERROR_INVALID_CREDENTIALS)

    def test_post_user_not_found(self):
        """Test the Get method of the Login resource.

        This test tries to log in as a user that doesn't exist, which shouldn't
        work.
        """
        # Log in
        data = {"username": "test", "password": "test_password"}
        r = self.client.post("/auth/login", json=data)

        # Check status code
        self.assertEqual(r.status_code, 401)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_INVALID_CREDENTIALS)
        self.assertEqual(
            res_data[message_keys[1]], MT_ERROR_INVALID_CREDENTIALS)

    def test_post_invalid_password(self):
        """Test the Get method of the Login resource.

        This test tries to log in as some user providing an invalid password,
        which shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"] + "_"}
        r = self.client.post("/auth/login", json=data)

        # Check status code
        self.assertEqual(r.status_code, 401)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_INVALID_CREDENTIALS)
        self.assertEqual(
            res_data[message_keys[1]], MT_ERROR_INVALID_CREDENTIALS)

    def test_put(self):
        """Test the Put method of the Login resource.

        This test tries to call the Put method, which shouldn't work.
        """
        r = self.client.put("/auth/login")

        # Check status code
        self.assertEqual(r.status_code, 405)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_METHOD_NOT_ALLOWED)
        self.assertEqual(
            res_data[message_keys[1]], MT_ERROR_METHOD_NOT_ALLOWED)

    def test_delete(self):
        """Test the Delete method of the Login resource.

        This test tries to call the Delete method, which shouldn't work.
        """
        r = self.client.delete("/auth/login")

        # Check status code
        self.assertEqual(r.status_code, 405)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_METHOD_NOT_ALLOWED)
        self.assertEqual(
            res_data[message_keys[1]], MT_ERROR_METHOD_NOT_ALLOWED)


class TokenRefreshTestCase(common.BaseTestCase):
    """Token Refresh resource unit tests."""

    def test_get(self):
        """Test the Get method of the Token Refresh resource.

        This test tries to get a new, not fresh, access token providing the
        user refresh token, which should work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        refresh_token = r.json["result"]["refresh_token"]

        # Get a new, not fresh, access token
        headers = {"Authorization": f"Bearer {refresh_token}"}
        r = self.client.get("/auth/refresh", headers=headers)

        # Check status code
        self.assertEqual(r.status_code, 200)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_TOKEN_REFRESHED)
        self.assertEqual(res_data[message_keys[1]], MT_OK)

        # Check result
        self.assertIn("result", res_data)
        result = r.json["result"]
        self.assertEqual(type(result), dict)

        # Check new access token
        self.assertIn("access_token", result)
        access_token = result["access_token"]
        self.assertEqual(type(access_token), str)
        self.assertNotEqual(access_token, "")

    def test_get_missing_refresh_token(self):
        """Test the Get method of the Token Refresh resource.

        This test tries to get a new, not fresh, access token without providing
        a refresh token, which shouldn't work.
        """
        # Get access token
        r = self.client.get("/auth/refresh")

        # Check status code
        self.assertEqual(r.status_code, 401)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_MISSING_TOKEN)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_MISSING_TOKEN)

    def test_get_invalid_refresh_token(self):
        """Test the Get method of the Token Refresh resource.

        This test tries to get a new, not fresh, access token given an invalid
        refresh token, which shouldn't work.
        """
        # Get a new, not fresh, access token providing an invalid access token
        # ("1234").
        headers = {"Authorization": "Bearer 1234"}
        r = self.client.get("/auth/refresh", headers=headers)

        # Check status code
        self.assertEqual(r.status_code, 422)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_INVALID_TOKEN)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_INVALID_TOKEN)

    def test_post(self):
        """Test the Post method of the Token Refresh resource.

        This test tries to call the Post method, which shouldn't work.
        """
        r = self.client.post("/auth/refresh")

        # Check status code
        self.assertEqual(r.status_code, 405)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_METHOD_NOT_ALLOWED)
        self.assertEqual(
            res_data[message_keys[1]], MT_ERROR_METHOD_NOT_ALLOWED)

    def test_put(self):
        """Test the Put method of the Token Refresh resource.

        This test tries to call the Put method, which shouldn't work.
        """
        r = self.client.put("/auth/refresh")

        # Check status code
        self.assertEqual(r.status_code, 405)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_METHOD_NOT_ALLOWED)
        self.assertEqual(
            res_data[message_keys[1]], MT_ERROR_METHOD_NOT_ALLOWED)

    def test_delete(self):
        """Test the Delete method of the Token Refresh resource.

        This test tries to call the Delete method, which shouldn't work.
        """
        r = self.client.delete("/auth/refresh")

        # Check status code
        self.assertEqual(r.status_code, 405)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_METHOD_NOT_ALLOWED)
        self.assertEqual(
            res_data[message_keys[1]], MT_ERROR_METHOD_NOT_ALLOWED)


class LogoutTestCase(common.BaseTestCase):
    """Logout resource unit tests."""

    def test_get(self):
        """Test the Get method of the Logout resource.

        This test logs in as some user with valid credentials and then tries to
        log out, which should work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Log out
        headers = {"Authorization": f"Bearer {access_token}"}
        r = self.client.get("/auth/logout", headers=headers)

        # Check status code
        self.assertEqual(r.status_code, 200)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_USER_LOGGED_OUT)
        self.assertEqual(res_data[message_keys[1]], MT_OK)

    def test_get_missing_access_token(self):
        """Test the Get method of the Logout resource.

        This test tries to log out without providing an access token, which
        shouldn't work.
        """
        # Log out without providing the access token
        r = self.client.get("/auth/logout")

        # Check status code
        self.assertEqual(r.status_code, 401)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_MISSING_TOKEN)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_MISSING_TOKEN)

    def test_get_invalid_access_token(self):
        """Test the Get method of the Logout resource.

        This test tries to log out providing an invalid access token, which
        shouldn't work.
        """
        # Log out providing an invalid access token ("1234")
        headers = {"Authorization": "Bearer 1234"}
        r = self.client.get("/auth/refresh", headers=headers)

        # Check status code
        self.assertEqual(r.status_code, 422)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_INVALID_TOKEN)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_INVALID_TOKEN)

    def test_post(self):
        """Test the Post method of the Logout resource.

        This test tries to call the Post method, which shouldn't work.
        """
        r = self.client.post("/auth/logout")

        # Check status code
        self.assertEqual(r.status_code, 405)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_METHOD_NOT_ALLOWED)
        self.assertEqual(
            res_data[message_keys[1]], MT_ERROR_METHOD_NOT_ALLOWED)

    def test_put(self):
        """Test the Put method of the Logout resource.

        This test tries to call the Put method, which shouldn't work.
        """
        r = self.client.put("/auth/logout")

        # Check status code
        self.assertEqual(r.status_code, 405)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_METHOD_NOT_ALLOWED)
        self.assertEqual(
            res_data[message_keys[1]], MT_ERROR_METHOD_NOT_ALLOWED)

    def test_delete(self):
        """Test the Delete method of the Logout resource.

        This test tries to call the Delete method, which shouldn't work.
        """
        r = self.client.delete("/auth/logout")

        # Check status code
        self.assertEqual(r.status_code, 405)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_METHOD_NOT_ALLOWED)
        self.assertEqual(
            res_data[message_keys[1]], MT_ERROR_METHOD_NOT_ALLOWED)


if __name__ == "__main__":
    unittest.main()
