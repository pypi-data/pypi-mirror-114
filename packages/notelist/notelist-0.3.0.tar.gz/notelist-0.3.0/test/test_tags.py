"""Tag resources unit tests."""

import unittest

import common
from notelist.responses import (
    MV_URL_NOT_FOUND, MV_METHOD_NOT_ALLOWED, MV_MISSING_TOKEN,
    MV_INVALID_TOKEN, MV_VALIDATION_ERROR, MV_USER_UNAUTHORIZED, MT_OK,
    MT_ERROR_URL_NOT_FOUND, MT_ERROR_METHOD_NOT_ALLOWED,
    MT_ERROR_MISSING_TOKEN, MT_ERROR_INVALID_TOKEN, MT_ERROR_UNAUTHORIZED_USER,
    MT_ERROR_VALIDATION, MT_ERROR_ITEM_EXISTS)
from notelist.views.tags import (
    MV_TAG_RETRIEVED_N, MV_TAG_RETRIEVED, MV_TAG_CREATED, MV_TAG_UPDATED,
    MV_TAG_DELETED, MV_TAG_EXISTS)


class TagListTestCase(common.BaseTestCase):
    """Tag List resource unit tests."""

    def test_get(self):
        """Test the Get method of the Tag List resource.

        This test creates a notebook with some tags and then tries to get the
        notebook's tag list, which should work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create tags
        tags = [
            {"notebook_id": notebook_id, "name": "Test Tag 1"},
            {"notebook_id": notebook_id, "name": "Test Tag 2"}]

        for t in tags:
            r = self.client.post("/tags/tag", headers=headers, json=t)

        # Get notebook tag list
        r = self.client.get(f"/tags/tags/{notebook_id}", headers=headers)

        # Check status code
        self.assertEqual(r.status_code, 200)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(
            res_data[message_keys[0]], MV_TAG_RETRIEVED_N.format(2))
        self.assertEqual(res_data[message_keys[1]], MT_OK)

        # Check result
        self.assertIn("result", res_data)
        res_tags = res_data["result"]
        self.assertEqual(type(res_tags), list)

        # Check list
        c = len(res_tags)
        self.assertEqual(c, 2)

        for t in res_tags:
            self.assertEqual(type(t), dict)
            self.assertEqual(len(t), 5)

            for i in ("id", "name", "color", "created_ts", "last_modified_ts"):
                self.assertIn(i, t)

        for i in range(c):
            self.assertEqual(type(res_tags[i]), dict)
            self.assertEqual(res_tags[i]["name"], tags[i]["name"])

    def test_get_missing_access_token(self):
        """Test the Get method of the Tag List resource.

        This test tries to get the tag list of a notebook without providing the
        access token, which shouldn't work.
        """
        # Get the tags of the notebook with ID 1 (which doesn't exist) without
        # providing the access token.
        r = self.client.get("/tags/tags/1")

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
        """Test the Get method of the Tag List resource.

        This test tries to get the tag list of a notebook providing an invalid
        access token, which shouldn't work.
        """
        # Get the tags of the notebook with ID 1 (which doesn't exist)
        # providing an invalid access token ("1234").
        headers = {"Authorization": "Bearer 1234"}
        r = self.client.get("/tags/tags/1", headers=headers)

        # Check status code
        self.assertEqual(r.status_code, 422)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_INVALID_TOKEN)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_INVALID_TOKEN)

    def test_get_unauthorized_user(self):
        """Test the Get method of the Tag List resource.

        This test tries to get the tag list of a notebook that doesn't belong
        to the request user, which shouldn't work.
        """
        # Log in
        data = {
            "username": self.admin["username"],
            "password": self.admin["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Log in as another user
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Get tag list
        headers = {"Authorization": f"Bearer {access_token}"}
        r = self.client.get(f"/tags/tags/{notebook_id}", headers=headers)

        # Check status code
        self.assertEqual(r.status_code, 403)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_USER_UNAUTHORIZED)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_UNAUTHORIZED_USER)

    def test_get_missing_notebook_id(self):
        """Test the Get method of the Tag List resource.

        This test tries to get the tag list of a notebook without providing the
        notebook ID, which shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Get tag list
        headers = {"Authorization": f"Bearer {access_token}"}
        r = self.client.get("/tags/tags", headers=headers)

        # Check status code
        self.assertEqual(r.status_code, 404)

    def test_post(self):
        """Test the Post method of the Tag List resource.

        This test tries to call the Post method, which shouldn't work.
        """
        r1 = self.client.post("/tags/tags")
        r2 = self.client.post("/tags/tag/1")

        # Check status code
        self.assertEqual(r1.status_code, 404)
        self.assertEqual(r2.status_code, 405)

        # Check messages
        message_keys = ("message", "message_type")

        for r in (r1, r2):
            res_data = r.json

            for i in message_keys:
                self.assertIn(i, res_data)

        self.assertEqual(r1.json[message_keys[0]], MV_URL_NOT_FOUND)
        self.assertEqual(r1.json[message_keys[1]], MT_ERROR_URL_NOT_FOUND)

        self.assertEqual(r2.json[message_keys[0]], MV_METHOD_NOT_ALLOWED)
        self.assertEqual(r2.json[message_keys[1]], MT_ERROR_METHOD_NOT_ALLOWED)

    def test_put(self):
        """Test the Put method of the Tag List resource.

        This test tries to call the Put method, which shouldn't work.
        """
        r1 = self.client.put("/tags/tags")
        r2 = self.client.put("/tags/tags/1")

        # Check status code
        self.assertEqual(r1.status_code, 404)
        self.assertEqual(r2.status_code, 405)

        # Check messages
        message_keys = ("message", "message_type")

        for r in (r1, r2):
            res_data = r.json

            for i in message_keys:
                self.assertIn(i, res_data)

        self.assertEqual(r1.json[message_keys[0]], MV_URL_NOT_FOUND)
        self.assertEqual(r1.json[message_keys[1]], MT_ERROR_URL_NOT_FOUND)

        self.assertEqual(r2.json[message_keys[0]], MV_METHOD_NOT_ALLOWED)
        self.assertEqual(r2.json[message_keys[1]], MT_ERROR_METHOD_NOT_ALLOWED)

    def test_delete(self):
        """Test the Delete method of the Tag List resource.

        This test tries to call the Delete method, which shouldn't work.
        """
        r1 = self.client.delete("/tags/tags")
        r2 = self.client.delete("/tags/tags/1")

        # Check status code
        self.assertEqual(r1.status_code, 404)
        self.assertEqual(r2.status_code, 405)

        # Check messages
        message_keys = ("message", "message_type")

        for r in (r1, r2):
            res_data = r.json

            for i in message_keys:
                self.assertIn(i, res_data)

        self.assertEqual(r1.json[message_keys[0]], MV_URL_NOT_FOUND)
        self.assertEqual(r1.json[message_keys[1]], MT_ERROR_URL_NOT_FOUND)

        self.assertEqual(r2.json[message_keys[0]], MV_METHOD_NOT_ALLOWED)
        self.assertEqual(r2.json[message_keys[1]], MT_ERROR_METHOD_NOT_ALLOWED)


class TagTestCase(common.BaseTestCase):
    """Tag resource unit tests."""

    def test_get(self):
        """Test the Get method of the Tag resource.

        This test creates a notebook, adds a tag to the notebook and then tries
        to get the tag, which should work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create tag
        t = {
            "notebook_id": notebook_id, "name": "Test Tag", "color": "#ffffff"}
        r = self.client.post("/tags/tag", headers=headers, json=t)
        tag_id = r.json["result"]["id"]

        # Get tag
        r = self.client.get(f"/tags/tag/{tag_id}", headers=headers)

        # Check status code
        self.assertEqual(r.status_code, 200)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_TAG_RETRIEVED)
        self.assertEqual(res_data[message_keys[1]], MT_OK)

        # Check result
        self.assertIn("result", res_data)
        tag = res_data["result"]
        self.assertEqual(type(tag), dict)

        # Check data
        self.assertEqual(len(tag), 6)
        self.assertIn("id", tag)
        self.assertIn("notebook_id", tag)
        self.assertIn("name", tag)
        self.assertIn("color", tag)
        self.assertIn("created_ts", tag)
        self.assertIn("last_modified_ts", tag)

        self.assertEqual(tag["id"], tag_id)
        self.assertEqual(tag["notebook_id"], notebook_id)
        self.assertEqual(tag["name"], t["name"])
        self.assertEqual(tag["color"], t["color"])

    def test_get_missing_access_token(self):
        """Test the Get method of the Tag resource.

        This test tries to get the data of a tag without providing the access
        token, which shouldn't work.
        """
        # Get the tag with ID 1 (which doesn't exist) without providing the
        # acess token.
        r = self.client.get("/tags/tag/1")

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
        """Test the Get method of the Tag resource.

        This test tries to get the data of some tag providing an invalid access
        token, which shouldn't work.
        """
        # Get the tag with ID 1 (which doesn't exist) providing an invalid
        # access token ("1234").
        headers = {"Authorization": "Bearer 1234"}
        r = self.client.get("/tags/tag/1", headers=headers)

        # Check status code
        self.assertEqual(r.status_code, 422)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_INVALID_TOKEN)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_INVALID_TOKEN)

    def test_get_unauthorized_user(self):
        """Test the Get method of the Tag resource.

        This test tries to get a tag of a user from another user, which
        shouldn't work.
        """
        # Log in
        data = {
            "username": self.admin["username"],
            "password": self.admin["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create tag
        t = {"notebook_id": notebook_id, "name": "Test Tag"}
        r = self.client.post("/tags/tag", headers=headers, json=t)
        tag_id = r.json["result"]["id"]

        # Log in as another user
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Get tag
        headers = {"Authorization": f"Bearer {access_token}"}
        r = self.client.get(f"/tags/tag/{tag_id}", headers=headers)

        # Check status code
        self.assertEqual(r.status_code, 403)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_USER_UNAUTHORIZED)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_UNAUTHORIZED_USER)

    def test_get_tag_not_found(self):
        """Test the Get method of the Tag resource.

        This test tries to get a tag that doesn't exist, which shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Get tag
        headers = {"Authorization": f"Bearer {access_token}"}
        r = self.client.get("/tags/tag/1", headers=headers)

        # Check status code
        self.assertEqual(r.status_code, 403)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_USER_UNAUTHORIZED)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_UNAUTHORIZED_USER)

    def test_post(self):
        """Test the Post method of the Tag resource.

        This test tries to create a tag, which should work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create tag
        t = {
            "notebook_id": notebook_id, "name": "Test Tag", "color": "#ffffff"}
        r = self.client.post("/tags/tag", headers=headers, json=t)

        # Check status code
        self.assertEqual(r.status_code, 201)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_TAG_CREATED)
        self.assertEqual(res_data[message_keys[1]], MT_OK)

        # Check result
        self.assertIn("result", res_data)
        tag_id = res_data["result"]["id"]
        self.assertEqual(type(tag_id), str)

    def test_post_missing_access_token(self):
        """Test the Post method of the Tag resource.

        This test tries to create a tag without providing the access token,
        which shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create tag
        t = {"notebook_id": notebook_id, "name": "Test Tag"}
        r = self.client.post("/tags/tag", json=t)

        # Check status code
        self.assertEqual(r.status_code, 401)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_MISSING_TOKEN)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_MISSING_TOKEN)

    def test_post_invalid_access_token(self):
        """Test the Post method of the Tag resource.

        This test tries to create a tag providing an invalid access token,
        which shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create a tag providing an invalid access token ("1234")
        headers = {"Authorization": "Bearer 1234"}
        t = {"notebook_id": notebook_id, "name": "Test Tag"}
        r = self.client.post("/tags/tag", headers=headers, json=t)

        # Check status code
        self.assertEqual(r.status_code, 422)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_INVALID_TOKEN)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_INVALID_TOKEN)

    def test_post_missing_fields(self):
        """Test the Post method of the Tag resource.

        This test tries to create a tag with some mandatory field missing,
        which shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create tag (without data)
        r = self.client.post("/tags/tag", headers=headers)

        # Check status code
        self.assertEqual(r.status_code, 400)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(
            res_data[message_keys[0]],
            MV_VALIDATION_ERROR.format("notebook_id, name"))
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_VALIDATION)

        # Create tag (without name)
        t = {"notebook_id": notebook_id}
        r = self.client.post("/tags/tag", headers=headers, json=t)

        # Check status code
        self.assertEqual(r.status_code, 400)

        # Check message
        res_data = r.json

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(
            res_data[message_keys[0]], MV_VALIDATION_ERROR.format("name"))
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_VALIDATION)

    def test_post_invalid_fields(self):
        """Test the Post method of the Tag resource.

        This test tries to create a tag providing some invalid/unexpected
        field, which shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create a tag with an invalid field ("invalid_field")
        t = {
            "notebook_id": notebook_id, "name": "Test Tag", "invalid_field": 1}
        r = self.client.post("/tags/tag", headers=headers, json=t)

        # Check status code
        self.assertEqual(r.status_code, 400)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(
            res_data[message_keys[0]],
            MV_VALIDATION_ERROR.format("invalid_field"))
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_VALIDATION)

    def test_post_notebook_user_unauthorized(self):
        """Test the Post method of the Tag resource.

        This test tries to create a tag for a notebook that doesn't belong to
        the request user, which shouldn't work.
        """
        # Log in
        data = {
            "username": self.admin["username"],
            "password": self.admin["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Log in as another user
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create tag
        headers = {"Authorization": f"Bearer {access_token}"}
        t = {"notebook_id": notebook_id, "name": "Test Tag"}
        r = self.client.post("/tags/tag", headers=headers, json=t)

        # Check status code
        self.assertEqual(r.status_code, 403)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_USER_UNAUTHORIZED)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_UNAUTHORIZED_USER)

    def test_post_notebook_not_found(self):
        """Test the Post method of the Tag resource.

        This test tries to create a tag for a notebook that doesn't exist,
        which shouldn't work.
        """
        # Log in
        data = {
            "username": self.admin["username"],
            "password": self.admin["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create a tag for the notebook with ID "1" (which doesn't exist)
        headers = {"Authorization": f"Bearer {access_token}"}
        t = {"notebook_id": "1", "name": "Test Tag"}
        r = self.client.post("/tags/tag", headers=headers, json=t)

        # Check status code
        self.assertEqual(r.status_code, 403)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_USER_UNAUTHORIZED)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_UNAUTHORIZED_USER)

    def test_post_tag_exists(self):
        """Test the Post method of the Tag resource.

        This test tries to create a tag with the same name of an existing tag
        in the same notebook, which shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create tag
        t = {
            "notebook_id": notebook_id, "name": "Test Tag", "color": "#ff0000"}
        r = self.client.post("/tags/tag", headers=headers, json=t)

        # Check status code
        self.assertEqual(r.status_code, 201)

        # Create tag
        t = {
            "notebook_id": notebook_id, "name": "Test Tag", "color": "#00ff00"}
        r = self.client.post("/tags/tag", headers=headers, json=t)

        # Check status code
        self.assertEqual(r.status_code, 400)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_TAG_EXISTS)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_ITEM_EXISTS)

    def test_put_new(self):
        """Test the Put method of the Tag resource.

        This test tries to create a tag, which should work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create tag
        t = {
            "notebook_id": notebook_id, "name": "Test Tag", "color": "#ffffff"}
        r = self.client.put("/tags/tag", headers=headers, json=t)

        # Check status code
        self.assertEqual(r.status_code, 201)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_TAG_CREATED)
        self.assertEqual(res_data[message_keys[1]], MT_OK)

        # Check result
        self.assertIn("result", res_data)
        tag_id = res_data["result"]["id"]
        self.assertEqual(type(tag_id), str)

    def test_put_edit(self):
        """Test the Put method of the Tag resource.

        This test tries to edit one of the tags of one of the request user's
        notebooks, which should work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create tag
        t = {
            "notebook_id": notebook_id, "name": "Test Tag 1",
            "color": "#ff0000"}
        r = self.client.put("/tags/tag", headers=headers, json=t)
        tag_id = r.json["result"]["id"]

        # Edit tag
        new_tag = {"name": "Test Tag 2", "color": "#00ff00"}
        r = self.client.put(
            f"/tags/tag/{tag_id}", headers=headers, json=new_tag)

        # Check status code
        self.assertEqual(r.status_code, 200)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_TAG_UPDATED)
        self.assertEqual(res_data[message_keys[1]], MT_OK)

        # Get tag
        r = self.client.get(f"/tags/tag/{tag_id}", headers=headers)
        tag = r.json["result"]

        # Check tag
        self.assertEqual(len(tag), 6)

        for i in (
            "id", "notebook_id", "name", "color", "created_ts",
            "last_modified_ts"
        ):
            self.assertIn(i, tag)

        self.assertEqual(tag["id"], tag_id)
        self.assertEqual(tag["notebook_id"], notebook_id)
        self.assertEqual(tag["name"], new_tag["name"])
        self.assertEqual(tag["color"], new_tag["color"])

    def test_put_new_missing_access_token(self):
        """Test the Put method of the Tag resource.

        This test tries to create a tag without providing the access token,
        which shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create tag
        t = {"notebook_id": notebook_id, "name": "Test Tag"}
        r = self.client.put("/tags/tag", json=t)

        # Check status code
        self.assertEqual(r.status_code, 401)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_MISSING_TOKEN)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_MISSING_TOKEN)

    def test_put_edit_missing_access_token(self):
        """Test the Put method of the Tag resource.

        This test tries to edit a tag without providing the access token, which
        shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create tag
        t = {
            "notebook_id": notebook_id, "name": "Test Tag 1",
            "color": "#ff0000"}
        r = self.client.put("/tags/tag", headers=headers, json=t)
        tag_id = r.json["result"]["id"]

        # Edit tag
        new_tag = {"name": "Test Tag 2", "color": "#00ff00"}
        r = self.client.put(f"/tags/tag/{tag_id}", json=new_tag)

        # Check status code
        self.assertEqual(r.status_code, 401)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_MISSING_TOKEN)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_MISSING_TOKEN)

    def test_put_new_invalid_access_token(self):
        """Test the Put method of the Tag resource.

        This test tries to create a tag providing an invalid access token,
        which shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create tag providing an invalid access token ("1234")
        headers = {"Authorization": "Bearer 1234"}
        t = {"notebook_id": notebook_id, "name": "Test Tag"}
        r = self.client.put("/tags/tag", headers=headers, json=t)

        # Check status code
        self.assertEqual(r.status_code, 422)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_INVALID_TOKEN)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_INVALID_TOKEN)

    def test_put_edit_invalid_access_token(self):
        """Test the Put method of the Tag resource.

        This test tries to edit a tag providing an invalid access token, which
        shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create tag
        t = {
            "notebook_id": notebook_id, "name": "Test Tag 1",
            "color": "#ff0000"}
        r = self.client.put("/tags/tag", headers=headers, json=t)
        tag_id = r.json["result"]["id"]

        # Edit tag providing an invalid access token ("1234")
        headers = {"Authorization": "Bearer 1234"}
        new_tag = {"name": "Test Tag 2", "color": "#00ff00"}
        r = self.client.put(
            f"/tags/tag/{tag_id}", headers=headers, json=new_tag)

        # Check status code
        self.assertEqual(r.status_code, 422)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_INVALID_TOKEN)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_INVALID_TOKEN)

    def test_put_new_missing_fields(self):
        """Test the Put method of the Tag resource.

        This test tries to create a tag with some mandatory field missing,
        which shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create tag (without data)
        r1 = self.client.put("/tags/tag", headers=headers)

        # Create tag (without name)
        t = {"notebook_id": notebook_id}
        r2 = self.client.put("/tags/tag", headers=headers, json=t)

        # Check status codes and messages
        message_keys = ("message", "message_type")

        for r in (r1, r2):
            # Status code
            self.assertEqual(r.status_code, 400)

            # Message
            res_data = r.json

            for i in message_keys:
                self.assertIn(i, res_data)

            self.assertEqual(res_data[message_keys[1]], MT_ERROR_VALIDATION)

        self.assertEqual(
            r1.json[message_keys[0]],
            MV_VALIDATION_ERROR.format("notebook_id, name"))

        self.assertEqual(
            r2.json[message_keys[0]], MV_VALIDATION_ERROR.format("name"))

    def test_put_edit_notebook(self):
        """Test the Put method of the Notebook resource.

        This test tries to edit a tag specifying its notebook, which shouldn't
        work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create tag
        t = {"notebook_id": notebook_id, "name": "Test Tag"}
        r = self.client.put("/tags/tag", headers=headers, json=t)
        tag_id = r.json["result"]["id"]

        # Edit tag
        new_tag = {"notebook_id": notebook_id, "name": "Test Tag"}
        r = self.client.put(
            f"/tags/tag/{tag_id}", headers=headers, json=new_tag)

        # Check status code
        self.assertEqual(r.status_code, 400)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(
            res_data[message_keys[0]],
            MV_VALIDATION_ERROR.format("notebook_id"))
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_VALIDATION)

    def test_put_new_invalid_fields(self):
        """Test the Put method of the Tag resource.

        This test tries to create a tag providing some invalid/unexpected
        field, which shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create a tag with an invalid field ("invalid_field")
        t = {
            "notebook_id": notebook_id, "name": "Test Tag", "invalid_field": 1}
        r = self.client.put("/tags/tag", headers=headers, json=t)

        # Check status code
        self.assertEqual(r.status_code, 400)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(
            res_data[message_keys[0]],
            MV_VALIDATION_ERROR.format("invalid_field"))
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_VALIDATION)

    def test_put_edit_invalid_fields(self):
        """Test the Put method of the Tag resource.

        This test tries to edit a tag providing some invalid/unexpected field,
        which shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create tag
        t = {"notebook_id": notebook_id, "name": "Test Tag"}
        r = self.client.put("/tags/tag", headers=headers, json=t)
        tag_id = r.json["result"]["id"]

        # Edit tag with an invalid field ("invalid_field")
        new_tag = {"name": "Test Tag", "invalid_field": 1}
        r = self.client.put(
            f"/tags/tag/{tag_id}", headers=headers, json=new_tag)

        # Check status code
        self.assertEqual(r.status_code, 400)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(
            res_data[message_keys[0]],
            MV_VALIDATION_ERROR.format("invalid_field"))
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_VALIDATION)

    def test_put_new_notebook_user_unauthorized(self):
        """Test the Put method of the Tag resource.

        This test tries to create a tag for a notebook that doesn't belong to
        the request user, which shouldn't work.
        """
        # Log in
        data = {
            "username": self.admin["username"],
            "password": self.admin["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Log in as another user
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create tag
        headers = {"Authorization": f"Bearer {access_token}"}
        t = {"notebook_id": notebook_id, "name": "Test Tag"}
        r = self.client.put("/tags/tag", headers=headers, json=t)

        # Check status code
        self.assertEqual(r.status_code, 403)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_USER_UNAUTHORIZED)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_UNAUTHORIZED_USER)

    def test_put_new_notebook_not_found(self):
        """Test the Put method of the Tag resource.

        This test tries to create a tag for a notebook that doesn't exist,
        which shouldn't work.
        """
        # Log in
        data = {
            "username": self.admin["username"],
            "password": self.admin["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create a tag for the notebook with ID "1" (which doesn't exist)
        headers = {"Authorization": f"Bearer {access_token}"}
        t = {"notebook_id": "1", "name": "Test Tag"}
        r = self.client.put("/tags/tag", headers=headers, json=t)

        # Check status code
        self.assertEqual(r.status_code, 403)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_USER_UNAUTHORIZED)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_UNAUTHORIZED_USER)

    def test_put_edit_user_unauthorized(self):
        """Test the Put method of the Tag resource.

        This test tries to edit a tag of a notebook that doesn't belong to the
        request user, which shouldn't work.
        """
        # Log in
        data = {
            "username": self.admin["username"],
            "password": self.admin["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create tag
        t = {"notebook_id": notebook_id, "name": "Test Tag"}
        r = self.client.put("/tags/tag", headers=headers, json=t)
        tag_id = r.json["result"]["id"]

        # Log in as another user
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Edit tag
        headers = {"Authorization": f"Bearer {access_token}"}
        new_tag = {"name": "Test Tag 2"}
        r = self.client.put(
            f"/tags/tag/{tag_id}", headers=headers, json=new_tag)

        # Check status code
        self.assertEqual(r.status_code, 403)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_USER_UNAUTHORIZED)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_UNAUTHORIZED_USER)

    def test_put_new_tag_exists(self):
        """Test the Put method of the Tag resource.

        This test tries to create a tag with the same name of an existing tag
        in the same notebook of the request user, which shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create tag
        t = {
            "notebook_id": notebook_id, "name": "Test Tag", "color": "#ff0000"}
        self.client.put("/tags/tag", headers=headers, json=t)

        # Create tag
        t = {
            "notebook_id": notebook_id, "name": "Test Tag", "color": "#00ff00"}
        r = self.client.put("/tags/tag", headers=headers, json=t)

        # Check status code
        self.assertEqual(r.status_code, 400)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_TAG_EXISTS)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_ITEM_EXISTS)

    def test_put_edit_tag_exists(self):
        """Test the Put method of the Tag resource.

        This test tries to edit a tag with the same name that it currently has
        (which should work) and tries to edit a tag with the same name of
        another existing tag in the same notebook, which shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create tags
        t1 = {"notebook_id": notebook_id, "name": "Test Tag 1"}
        t2 = {"notebook_id": notebook_id, "name": "Test Tag 2"}

        r = self.client.put("/tags/tag", headers=headers, json=t1)
        tag_id = r.json["result"]["id"]

        self.client.put("/tags/tag", headers=headers, json=t2)

        # Edit tag with its same name
        new_tag = {"name": "Test Tag"}
        r = self.client.put(
            f"/tags/tag/{tag_id}", headers=headers, json=new_tag)

        # Check status code
        self.assertEqual(r.status_code, 200)

        # Edit tag with the same name of the other tag
        new_tag = {"name": "Test Tag 2"}
        r = self.client.put(
            f"/tags/tag/{tag_id}", headers=headers, json=new_tag)

        # Check status code
        self.assertEqual(r.status_code, 400)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_TAG_EXISTS)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_ITEM_EXISTS)

    def test_delete(self):
        """Test the Delete method of the Tag resource.

        This test creates a tag and then tries to delete it, which should work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        nb = {"name": "Test Notebook"}
        r = self.client.put("/notebooks/notebook", headers=headers, json=nb)
        notebook_id = r.json["result"]["id"]

        # Create tag
        t = {"notebook_id": notebook_id, "name": "Test Tag"}
        r = self.client.post("/tags/tag", headers=headers, json=t)
        tag_id = r.json["result"]["id"]

        # Get notebook tag list
        r = self.client.get(f"/tags/tags/{notebook_id}", headers=headers)
        tags = r.json["result"]

        # Check list
        self.assertEqual(len(tags), 1)
        self.assertEqual(tags[0]["id"], tag_id)
        self.assertEqual(tags[0]["name"], t["name"])

        # Create a note with the tag
        n = {
            "notebook_id": notebook_id,
            "title": "Test Note",
            "tags": [t["name"]]}
        r = self.client.post("/notes/note", headers=headers, json=n)
        note_id = r.json["result"]["id"]

        # Delete tag
        r = self.client.delete(f"/tags/tag/{tag_id}", headers=headers)

        # Check status code
        self.assertEqual(r.status_code, 200)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_TAG_DELETED)
        self.assertEqual(res_data[message_keys[1]], MT_OK)

        # Get notebook tag list
        r = self.client.get(f"/tags/tags/{notebook_id}", headers=headers)
        tags = r.json["result"]

        # Check list
        self.assertEqual(len(tags), 0)

        # Check that the note doesn't have now the tag
        r = self.client.get(f"/notes/note/{note_id}", headers=headers)
        tags = r.json["result"]["tags"]
        self.assertEqual(len(tags), 0)

    def test_delete_missing_access_token(self):
        """Test the Delete method of the Tag resource.

        This test tries to delete an existing tag without providing the access
        token, which shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create tag
        t = {"notebook_id": notebook_id, "name": "Test Tag"}
        r = self.client.post("/tags/tag", headers=headers, json=t)
        tag_id = r.json["result"]["id"]

        # Delete tag
        r = self.client.delete(f"/tags/tag/{tag_id}")

        # Check status code
        self.assertEqual(r.status_code, 401)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_MISSING_TOKEN)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_MISSING_TOKEN)

    def test_delete_invalid_access_token(self):
        """Test the Delete method of the Tag resource.

        This test tries to delete a tag providing an invalid access token,
        which shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create tag
        t = {"notebook_id": notebook_id, "name": "Test Tag"}
        r = self.client.post("/tags/tag", headers=headers, json=t)
        tag_id = r.json["result"]["id"]

        # Delete tag providing an invalid access token ("1234")
        headers = {"Authorization": "Bearer 1234"}
        r = self.client.delete(f"/tags/tag/{tag_id}", headers=headers)

        # Check status code
        self.assertEqual(r.status_code, 422)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_INVALID_TOKEN)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_INVALID_TOKEN)

    def test_delete_unauthorized_user(self):
        """Test the Delete method of the Tag resource.

        This test tries to delete a tag of a user different than the request
        user, which shouldn't work.
        """
        # Log in
        data = {
            "username": self.admin["username"],
            "password": self.admin["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Create tag
        t = {"notebook_id": notebook_id, "name": "Test Tag"}
        r = self.client.post("/tags/tag", headers=headers, json=t)
        tag_id = r.json["result"]["id"]

        # Log in as another user
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Delete tag
        headers = {"Authorization": f"Bearer {access_token}"}
        r = self.client.delete(f"/tags/tag/{tag_id}", headers=headers)

        # Check status code
        self.assertEqual(r.status_code, 403)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_USER_UNAUTHORIZED)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_UNAUTHORIZED_USER)

    def test_delete_tag_not_found(self):
        """Test the Delete method of the Tag resource.

        This test tries to delete a tag that doesn't exist, which shouldn't
        work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Delete the tag with ID 1 (which doesn't exist)
        headers = {"Authorization": f"Bearer {access_token}"}
        r = self.client.delete("/tags/tag/1", headers=headers)

        # Check status code
        self.assertEqual(r.status_code, 403)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_USER_UNAUTHORIZED)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_UNAUTHORIZED_USER)


if __name__ == "__main__":
    unittest.main()
