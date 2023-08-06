"""Root resource unit tests."""

from os import environ
import unittest

import common
from notelist.responses import (
    MV_METHOD_NOT_ALLOWED, MT_ERROR_METHOD_NOT_ALLOWED)


class RootTestCase(common.BaseTestCase):
    """Root resource unit tests."""

    def test_get_ok(self):
        """Test the Get method of the Root resource.

        This test tries to call the Get method having the "NOTELIST_ROOT_DOC"
        environment variable set to "yes", which should work.
        """
        v = "NOTELIST_ROOT_DOC"
        environ[v] = "yes"
        r = self.client.get("/")

        # Check status code
        self.assertEqual(r.status_code, 200)

        environ.pop(v)

    def test_get_not_found(self):
        """Test the Get method of the Root resource.

        This test tries to call the Get method without having the
        "NOTELIST_ROOT_DOC" environment variable set to "yes", which should not
        work.
        """
        r = self.client.get("/")

        # Check status code
        self.assertEqual(r.status_code, 404)

    def test_post_error(self):
        """Test the Post method of the Root resource.

        This test tries to call the Post method, which shouldn't work.
        """
        r = self.client.post("/")

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

    def test_put_error(self):
        """Test the Put method of the Root resource.

        This test tries to call the Put method, which shouldn't work.
        """
        r = self.client.put("/")

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

    def test_delete_error(self):
        """Test the Delete method of the Root resource.

        This test tries to call the Delete method, which shouldn't work.
        """
        r = self.client.delete("/")

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
