"""Notebook resources unit tests."""

import unittest

import common
from notelist.responses import (
    MV_METHOD_NOT_ALLOWED, MV_MISSING_TOKEN, MV_INVALID_TOKEN,
    MV_USER_UNAUTHORIZED, MV_VALIDATION_ERROR, MT_OK,
    MT_ERROR_METHOD_NOT_ALLOWED, MT_ERROR_MISSING_TOKEN,
    MT_ERROR_INVALID_TOKEN, MT_ERROR_UNAUTHORIZED_USER, MT_ERROR_VALIDATION,
    MT_ERROR_ITEM_EXISTS)
from notelist.views.notebooks import (
    MV_NOTEBOOK_RETRIEVED_1, MV_NOTEBOOK_RETRIEVED, MV_NOTEBOOK_CREATED,
    MV_NOTEBOOK_UPDATED, MV_NOTEBOOK_DELETED, MV_NOTEBOOK_EXISTS)


class NotebookListTestCase(common.BaseTestCase):
    """Notebook List resource unit tests."""

    def test_get(self):
        """Test the Get method of the Notebook List resource.

        This test logs in as some user, creates some notebooks and then tries
        to get the user's notebook list, which should work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Get list
        headers = {"Authorization": f"Bearer {access_token}"}
        r = self.client.get("/notebooks/notebooks", headers=headers)
        res_data = r.json

        # Check status code
        self.assertEqual(r.status_code, 200)

        # Check result
        self.assertIn("result", res_data)
        notebooks = res_data["result"]
        self.assertEqual(type(notebooks), list)

        # Check list
        self.assertEqual(len(notebooks), 0)

        # Create notebook
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)
        res_data = r.json
        notebook_id = res_data["result"]["id"]

        # Get list
        r = self.client.get("/notebooks/notebooks", headers=headers)
        res_data = r.json

        # Check status code
        self.assertEqual(r.status_code, 200)

        # Check message
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_NOTEBOOK_RETRIEVED_1)
        self.assertEqual(res_data[message_keys[1]], MT_OK)

        # Check result
        self.assertIn("result", res_data)
        notebooks = res_data["result"]
        self.assertEqual(type(notebooks), list)

        # Check list
        self.assertEqual(len(notebooks), 1)
        notebook = notebooks[0]
        self.assertEqual(notebook["id"], notebook_id)
        self.assertEqual(notebook["name"], n["name"])

    def test_get_missing_access_token(self):
        """Test the Get method of the Notebook List resource.

        This test tries to get the notebook list of the request user without
        providing the access token, which shouldn't work.
        """
        # Get list without providing the access token
        r = self.client.get("/notebooks/notebooks")
        res_data = r.json

        # Check status code
        self.assertEqual(r.status_code, 401)

        # Check message
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_MISSING_TOKEN)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_MISSING_TOKEN)

    def test_get_invalid_access_token(self):
        """Test the Get method of the Notebook List resource.

        This test tries to get the user's notebook list providing an invalid
        access token, which shouldn't work.
        """
        # Get list providing an invalid access token ("1234")
        headers = {"Authorization": "Bearer 1234"}
        r = self.client.get("/notebooks/notebooks", headers=headers)
        res_data = r.json

        # Check status code
        self.assertEqual(r.status_code, 422)

        # Check message
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_INVALID_TOKEN)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_INVALID_TOKEN)

    def test_post(self):
        """Test the Post method of the Notebook List resource.

        This test tries to call the Post method, which shouldn't work.
        """
        r = self.client.post("/notebooks/notebooks")

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
        """Test the Put method of the Notebook List resource.

        This test tries to call the Put method, which shouldn't work.
        """
        r = self.client.put("/notebooks/notebooks")

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
        """Test the Delete method of the Notebook List resource.

        This test tries to call the Delete method, which shouldn't work.
        """
        r = self.client.delete("/notebooks/notebooks")

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


class NotebookTestCase(common.BaseTestCase):
    """Notebook resource unit tests."""

    def test_get(self):
        """Test the Get method of the Notebook resource.

        This test logs in as some user, creates a notebook and then tries to
        get this notebook, which should work.
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

        # Get the data of the notebook
        r = self.client.get(
            f"/notebooks/notebook/{notebook_id}", headers=headers)

        # Check status code
        self.assertEqual(r.status_code, 200)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_NOTEBOOK_RETRIEVED)
        self.assertEqual(res_data[message_keys[1]], MT_OK)

        # Check result
        self.assertIn("result", r.json)
        notebook = r.json["result"]
        self.assertEqual(type(notebook), dict)

        # Check notebook
        self.assertEqual(len(notebook), 4)
        self.assertIn("id", notebook)
        self.assertIn("name", notebook)
        self.assertIn("created_ts", notebook)
        self.assertIn("last_modified_ts", notebook)
        self.assertEqual(notebook["id"], notebook_id)
        self.assertEqual(notebook["name"], n["name"])

    def test_get_missing_access_token(self):
        """Test the Get method of the Notebook resource.

        This test tries to get a notebook without providing the access token,
        which shouldn't work.
        """
        # Get the notebook with ID 1 (which doesn't exist) without providing
        # the access token.
        r = self.client.get("/notebooks/notebook/1")

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
        """Test the Get method of the Notebook resource.

        This test tries to get a notebook providing an invalid access token,
        which shouldn't work.
        """
        # Get the notebook with ID 1 (which doesn't exist) providing an invalid
        # access token ("1234")
        headers = {"Authorization": "Bearer 1234"}
        r = self.client.get("/notebooks/notebook/1", headers=headers)

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
        """Test the Get method of the Notebook resource.

        This test tries to get a notebook of some user as another user, which
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

        # Log in as another user
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Get notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        r = self.client.get(
            f"/notebooks/notebook/{notebook_id}", headers=headers)

        # Check status code
        self.assertEqual(r.status_code, 403)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_USER_UNAUTHORIZED)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_UNAUTHORIZED_USER)

    def test_get_notebook_not_found(self):
        """Test the Get method of the Notebook resource.

        This test tries to get a notebook that doesn't exist, which shouldn't
        work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Get notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        r = self.client.get("/notebooks/notebook/1", headers=headers)

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
        """Test the Post method of the Notebook resource.

        This test tries to create a notebook, which should work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create a notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)

        # Check status code
        self.assertEqual(r.status_code, 201)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_NOTEBOOK_CREATED)
        self.assertEqual(res_data[message_keys[1]], MT_OK)

        # Check result
        self.assertIn("result", r.json)
        result = res_data["result"]
        self.assertIn("id", result)
        notebook_id = result["id"]
        self.assertEqual(type(notebook_id), str)

    def test_post_missing_access_token(self):
        """Test the Post method of the Notebook resource.

        This test tries to create a notebook without providing the access
        token, which shouldn't work.
        """
        # Create notebook
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", json=n)

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
        """Test the Post method of the Notebook resource.

        This test tries to create a notebook providing an invalid access token,
        which shouldn't work.
        """
        # Create a notebook providing an invalid access token ("1234")
        headers = {"Authorization": "Bearer 1234"}
        n = {"name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)

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
        """Test the Post method of the Notebook resource.

        This test tries to create a notebook with some mandatory field missing,
        which shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook (without data)
        headers = {"Authorization": f"Bearer {access_token}"}
        r1 = self.client.post("/notebooks/notebook", headers=headers)

        # Create notebook (with empty data)
        r2 = self.client.post(
            "/notebooks/notebook", headers=headers, json=dict())

        # Check status codes and messages
        message_keys = ("message", "message_type")

        for r in (r1, r2):
            # Status code
            self.assertEqual(r.status_code, 400)

            # Message
            res_data = r.json

            for i in message_keys:
                self.assertIn(i, res_data)

            self.assertEqual(
                res_data[message_keys[0]], MV_VALIDATION_ERROR.format("name"))
            self.assertEqual(res_data[message_keys[1]], MT_ERROR_VALIDATION)

    def test_post_user(self):
        """Test the Post method of the Notebook resource.

        This test tries to create a new notebook specifying its user, which
        shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create a notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"user_id": 1, "name": "Test Notebook"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)

        # Check status code
        self.assertEqual(r.status_code, 400)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(
            res_data[message_keys[0]], MV_VALIDATION_ERROR.format("user_id"))
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_VALIDATION)

    def test_post_invalid_fields(self):
        """Test the Post method of the Notebook resource.

        This test tries to create a notebook providing some invalid/unexpected
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
        n = {"name": "Test Notebook", "invalid_field": "1234"}
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)

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

    def test_post_notebook_exists(self):
        """Test the Post method of the Notebook resource.

        This test tries to create a notebook with the same name of an existing
        notebook of the request user, which shouldn't work.
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

        # Check status code
        self.assertEqual(r.status_code, 201)

        # Create the same notebook again
        r = self.client.post("/notebooks/notebook", headers=headers, json=n)

        # Check status code
        self.assertEqual(r.status_code, 400)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_NOTEBOOK_EXISTS)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_ITEM_EXISTS)

    def test_put_new(self):
        """Test the Put method of the Notebook resource.

        This test tries to create a notebook, which should work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create a notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.put("/notebooks/notebook", headers=headers, json=n)
        res_data = r.json

        # Check status code
        self.assertEqual(r.status_code, 201)

        # Check result
        self.assertIn("result", res_data)
        result = res_data["result"]
        self.assertIn("id", result)
        notebook_id = result["id"]
        self.assertEqual(type(notebook_id), str)

        # Check message
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_NOTEBOOK_CREATED)
        self.assertEqual(res_data[message_keys[1]], MT_OK)

    def test_put_edit(self):
        """Test the Put method of the Notebook resource.

        This test tries to edit one of the request user's notebooks, which
        should work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create a notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.put("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Edit the notebook
        new_notebook = {"name": "Test Notebook 2"}
        r = self.client.put(
            f"/notebooks/notebook/{notebook_id}", headers=headers,
            json=new_notebook)

        # Check status code
        self.assertEqual(r.status_code, 200)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_NOTEBOOK_UPDATED)
        self.assertEqual(res_data[message_keys[1]], MT_OK)

        # Get notebook data
        r = self.client.get(
            f"/notebooks/notebook/{notebook_id}", headers=headers)
        notebook = r.json["result"]

        # Check data
        self.assertEqual(len(notebook), 4)
        self.assertIn("id", notebook)
        self.assertIn("name", notebook)
        self.assertIn("created_ts", notebook)
        self.assertIn("last_modified_ts", notebook)
        self.assertEqual(notebook["id"], notebook_id)
        self.assertEqual(notebook["name"], new_notebook["name"])

    def test_put_new_missing_access_token(self):
        """Test the Put method of the Notebook resource.

        This test tries to create a new notebook without providing the access
        token, which shouldn't work.
        """
        # Create a notebook without providing the access token
        n = {"name": "Test Notebook"}
        r = self.client.put("/notebooks/notebook", json=n)

        # Check status code
        self.assertEqual(r.status_code, 401)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_MISSING_TOKEN)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_MISSING_TOKEN)

    def test_edit_new_missing_access_token(self):
        """Test the Put method of the Notebook resource.

        This test tries to edit a notebook without providing the access token,
        which shouldn't work.
        """
        # Edit the user with ID 1 (whose username is "self.admin["username"]")
        # without providing the access token.
        n = {"name": "Test Notebook"}
        r = self.client.put("/notebooks/notebook/1", json=n)

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
        """Test the Put method of the Notebook resource.

        This test tries to create a notebook providing an invalid access token,
        which shouldn't work.
        """
        # Create a notebook providing an invalid access token ("1234")
        headers = {"Authorization": "Bearer 1234"}
        n = {"name": "Test Notebook"}
        r = self.client.put("/notebooks/notebook", headers=headers, json=n)

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
        """Test the Put method of the Notebook resource.

        This test tries to edit a notebook providing an invalid access token,
        which shouldn't work.
        """
        # Edit the user with ID 1 (whose username is "self.admin["username"]")
        # providing an invalid access token ("1234").
        headers = {"Authorization": "Bearer 1234"}
        n = {"name": "Test Notebook"}
        r = self.client.put("/notebooks/notebook/1", headers=headers, json=n)

        # Check status code
        self.assertEqual(r.status_code, 422)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_INVALID_TOKEN)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_INVALID_TOKEN)

    def test_put_edit_unauthorized_user(self):
        """Test the Get method of the Notebook resource.

        This test creates a notebook of some user, and then tries to edit the
        notebook as another user, which shouldn't work.
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

        # Edit the notebook as the administrator user
        headers = {"Authorization": f"Bearer {access_token}"}
        new_notebook = {"name": "Test Notebook 2"}

        r = self.client.put(
            f"/notebooks/notebook/{notebook_id}", headers=headers,
            json=new_notebook)

        # Check status code
        self.assertEqual(r.status_code, 403)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_USER_UNAUTHORIZED)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_UNAUTHORIZED_USER)

    def test_put_missing_fields(self):
        """Test the Put method of the Notebook resource.

        This test tries to create a notebook with some mandatory field missing,
        which shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create notebook (without data)
        headers = {"Authorization": f"Bearer {access_token}"}
        r1 = self.client.put("/notebooks/notebook", headers=headers)

        # Create notebook (with empty data)
        r2 = self.client.put(
            "/notebooks/notebook", headers=headers, json=dict())

        # Check status codes and messages
        message_keys = ("message", "message_type")

        for r in (r1, r2):
            # Status code
            self.assertEqual(r.status_code, 400)

            # Message
            res_data = r.json

            for i in message_keys:
                self.assertIn(i, res_data)

            self.assertEqual(
                res_data[message_keys[0]], MV_VALIDATION_ERROR.format("name"))
            self.assertEqual(res_data[message_keys[1]], MT_ERROR_VALIDATION)

    def test_put_new_user(self):
        """Test the Put method of the Notebook resource.

        This test tries to create a notebook specifying its user, which
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
        n = {"user_id": self.reg1["id"], "name": "Test Notebook"}
        r = self.client.put("/notebooks/notebook", headers=headers, json=n)

        # Check status code
        self.assertEqual(r.status_code, 400)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(
            res_data[message_keys[0]], MV_VALIDATION_ERROR.format("user_id"))
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_VALIDATION)

    def test_put_new_invalid_fields(self):
        """Test the Put method of the Notebook resource.

        This test tries to create a notebook providing some invalid/unexpected
        field, which shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Create a notebook providing an invalid field ("invalid_field")
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook", "invalid_field": "1234"}
        r = self.client.put("/notebooks/notebook", headers=headers, json=n)

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

    def test_put_edit_user(self):
        """Test the Put method of the Notebook resource.

        This test tries to change the user of some notebook, which shouldn't
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
        r = self.client.put("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Change notebook user
        new_notebook = {"user_id": self.reg2["id"]}
        r = self.client.put(
            f"/notebooks/notebook/{notebook_id}", headers=headers,
            json=new_notebook)

        # Check status code
        self.assertEqual(r.status_code, 400)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(
            res_data[message_keys[0]], MV_VALIDATION_ERROR.format("user_id"))
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_VALIDATION)

    def test_put_edit_invalid_fields(self):
        """Test the Put method of the Notebook resource.

        This test tries to edit a notebook providing some invalid/unexpected
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
        r = self.client.put("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Edit the notebook providing an invalid field ("invalid_field")
        n = {"name": "Test Notebook", "invalid_field": "1234"}
        r = self.client.put(
            f"/notebooks/notebook/{notebook_id}", headers=headers, json=n)

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

    def test_put_new_notebook_exists(self):
        """Test the Put method of the Notebook resource.

        This test tries to create a notebook with the same name of an existing
        notebook of the request user, which shouldn't work.
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
        r = self.client.put("/notebooks/notebook", headers=headers, json=n)

        # Check status code
        self.assertEqual(r.status_code, 201)

        # Create same notebook again
        r = self.client.put("/notebooks/notebook", headers=headers, json=n)

        # Check status code
        self.assertEqual(r.status_code, 400)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_NOTEBOOK_EXISTS)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_ITEM_EXISTS)

    def test_put_edit_notebook_not_found(self):
        """Test the Put method of the Notebook resource.

        This test tries to edit a notebook that doesn't exist, which shouldn't
        work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Edit a notebook with ID 1 (which doesn't exist)
        headers = {"Authorization": f"Bearer {access_token}"}
        n = {"name": "Test Notebook"}
        r = self.client.put("/notebooks/notebook/1", headers=headers, json=n)

        # Check status code
        self.assertEqual(r.status_code, 403)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_USER_UNAUTHORIZED)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_UNAUTHORIZED_USER)

    def test_delete(self):
        """Test the Delete method of the Notebook resource.

        This test creates a notebook and then tries to delete it, which should
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
        r = self.client.put("/notebooks/notebook", headers=headers, json=n)
        notebook_id = r.json["result"]["id"]

        # Get user notebook list
        r = self.client.get("/notebooks/notebooks", headers=headers)
        notebooks = r.json["result"]

        # Check list
        self.assertEqual(len(notebooks), 1)
        self.assertEqual(notebooks[0]["name"], n["name"])

        # Delete notebook
        r = self.client.delete(
            f"/notebooks/notebook/{notebook_id}", headers=headers)

        # Check status code
        self.assertEqual(r.status_code, 200)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_NOTEBOOK_DELETED)
        self.assertEqual(res_data[message_keys[1]], MT_OK)

        # Get user notebook list
        r = self.client.get("/notebooks/notebooks", headers=headers)
        notebooks = r.json["result"]

        # Check list
        self.assertEqual(len(notebooks), 0)

    def test_delete_missing_access_token(self):
        """Test the Delete method of the Notebook resource.

        This test tries to delete an existing notebook without providing the
        access token, which shouldn't work.
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

        # Delete notebook without providing the access token
        r = self.client.delete(f"/notebooks/notebook/{notebook_id}")

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
        """Test the Delete method of the Notebook resource.

        This test tries to delete a notebook providing an invalid access token,
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

        # Delete notebook providing an invalid access token ("1234")
        headers = {"Authorization": "Bearer 1234"}
        r = self.client.delete(
            f"/notebooks/notebook/{notebook_id}", headers=headers)

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
        """Test the Delete method of the Notebook resource.

        This test tries to delete a notebook of a user different than the
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

        # Log in as another user
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Delete notebook
        headers = {"Authorization": f"Bearer {access_token}"}
        r = self.client.delete(
            f"/notebooks/notebook/{notebook_id}", headers=headers)

        # Check status code
        self.assertEqual(r.status_code, 403)

        # Check message
        res_data = r.json
        message_keys = ("message", "message_type")

        for i in message_keys:
            self.assertIn(i, res_data)

        self.assertEqual(res_data[message_keys[0]], MV_USER_UNAUTHORIZED)
        self.assertEqual(res_data[message_keys[1]], MT_ERROR_UNAUTHORIZED_USER)

    def test_delete_notebook_not_found(self):
        """Test the Delete method of the Notebook resource.

        This test tries to delete a notebook that doesn't exist, which
        shouldn't work.
        """
        # Log in
        data = {
            "username": self.reg1["username"],
            "password": self.reg1["password"]}
        r = self.client.post("/auth/login", json=data)
        access_token = r.json["result"]["access_token"]

        # Delete the notebook with ID 1 (which doesn't exist)
        headers = {"Authorization": f"Bearer {access_token}"}
        r = self.client.delete("/notebooks/notebook/1", headers=headers)

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
