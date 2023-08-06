"""About resources unit tests."""

import unittest

import common
from notelist.responses import (
    MV_METHOD_NOT_ALLOWED, MT_OK, MT_ERROR_METHOD_NOT_ALLOWED)
from notelist.views.about import MV_API_INFO_RETRIEVED


class AboutTestCase(common.BaseTestCase):
    """About resource unit tests."""

    def test_get_ok(self):
        """Test the Get method of the About resource.

        This test tries to call the Get method, which should work.
        """
        r = self.client.get("/about")

        # Check status code
        self.assertEqual(r.status_code, 200)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_API_INFO_RETRIEVED)
        self.assertEqual(res_data[message_keys[1]], MT_OK)

        # Check result
        self.assertIn("result", res_data)
        result = res_data["result"]
        self.assertEqual(type(result), dict)
        self.assertEqual(len(result), 4)

        for i in ("name", "version", "description", "author"):
            self.assertIn(i, result)
            self.assertEqual(type(i), str)

    def test_post_error(self):
        """Test the Post method of the About resource.

        This test tries to call the Post method, which shouldn't work.
        """
        r = self.client.post("/about")

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
        """Test the Put method of the About resource.

        This test tries to call the Put method, which shouldn't work.
        """
        r = self.client.put("/about")

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
        """Test the Delete method of the About resource.

        This test tries to call the Delete method, which shouldn't work.
        """
        r = self.client.delete("/about")

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
