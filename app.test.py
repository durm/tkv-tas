#!/usr/bin/env python3

import os
import unittest
import requests
import uuid
import time


host = os.environ.get("HOST", "localhost")
port = os.environ.get("POST", 5051)


class KVAPITestCase(unittest.TestCase):

    def base_url(self):
        return "http://{}:{}/kv".format(host, port)

    def target_url(self, id):
        return "{}/{}".format(self.base_url(), id)

    def rand(self):
        return str(uuid.uuid4())

    def test_create(self):
        time.sleep(1)
        k = self.rand()

        resp = requests.post(self.base_url(), json={})
        self.assertEqual(400, resp.status_code)
        time.sleep(1)

        resp = requests.post(self.base_url(), json={"key": k})
        self.assertEqual(400, resp.status_code)
        time.sleep(1)

        resp = requests.post(self.base_url(), json={"value": k})
        self.assertEqual(400, resp.status_code)
        time.sleep(1)

        resp = requests.post(self.base_url(), json={"key": k, "value": "val"})
        self.assertEqual(200, resp.status_code)
        data = resp.json()
        self.assertEqual(k, data[0])
        self.assertEqual("val", data[1])
        time.sleep(1)

        resp = requests.post(self.base_url(), json={"key": k, "value": "value2"})
        self.assertEqual(409, resp.status_code)

    def test_read(self):
        time.sleep(1)
        k = self.rand()

        resp = requests.get(self.target_url(k))
        self.assertEqual(404, resp.status_code)
        time.sleep(1)
        
        resp = requests.post(self.base_url(), json={"key": k, "value": "val"})
        self.assertEqual(200, resp.status_code)
        data = resp.json()
        self.assertEqual(k, data[0])
        self.assertEqual("val", data[1])
        time.sleep(1)
        
        resp = requests.get(self.target_url(k))
        self.assertEqual(200, resp.status_code)
        data = resp.json()
        self.assertEqual(k, data[0])
        self.assertEqual("val", data[1])

    def test_update(self):
        time.sleep(1)
        k = self.rand()

        resp = requests.put(self.target_url(k), json={})
        self.assertEqual(400, resp.status_code)
        time.sleep(1)
        
        resp = requests.put(self.target_url(k), json={"value": "val2222"})
        self.assertEqual(404, resp.status_code)
        time.sleep(1)

        resp = requests.post(self.base_url(), json={"key": k, "value": "val"})
        self.assertEqual(200, resp.status_code)
        data = resp.json()
        self.assertEqual(k, data[0])
        self.assertEqual("val", data[1])
        time.sleep(1)
        
        resp = requests.put(self.target_url(k), json={"value": "val2222"})
        self.assertEqual(200, resp.status_code)
        time.sleep(1)

        resp = requests.get(self.target_url(k))
        self.assertEqual(200, resp.status_code)
        data = resp.json()
        self.assertEqual(k, data[0])
        self.assertEqual("val2222", data[1])
        
    def test_delete(self):
        time.sleep(1)
        k = self.rand()

        resp = requests.get(self.target_url(k))
        self.assertEqual(404, resp.status_code)
        time.sleep(1)

        resp = requests.delete(self.target_url(k))
        self.assertEqual(200, resp.status_code)
        time.sleep(1)

        resp = requests.post(self.base_url(), json={"key": k, "value": "val"})
        self.assertEqual(200, resp.status_code)
        data = resp.json()
        self.assertEqual(k, data[0])
        self.assertEqual("val", data[1])
        time.sleep(1)

        resp = requests.delete(self.target_url(k))
        self.assertEqual(200, resp.status_code)
        time.sleep(1)

        resp = requests.get(self.target_url(k))
        self.assertEqual(404, resp.status_code)

    def test_request_limit(self):
        time.sleep(1)
        self.assertTrue(429 in (requests.get(self.target_url(self.rand())).status_code for _ in range(10)))


if __name__ == "__main__":
    unittest.main()
