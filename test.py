import unittest
import requests

class ApiTest(unittest.TestCase):

    API_URL = "http://127.0.0.1:5000/process_search"
    param = {"q":"venk"}

    def test_response_have_param(self):
        r = requests.get(ApiTest.API_URL,ApiTest.param)
        self.assertEqual(r.status_code,200)
        names = r.json()
        for name in names["results"]:
            self.assertEquals(ApiTest.param["q"] in name["name"].lower(),True)

    def test_response_in_order(self):
        r = requests.get(ApiTest.API_URL,ApiTest.param)
        self.assertEqual(r.status_code,200)
        names = r.json()
        result= names["results"]
        for i in range(len(result)):
            if result[i]["name"].startswith(ApiTest.param["q"]) and i<len(result)-1:
                self.assertEquals(len(result[i]["name"])<=len(result[i+1]["name"]),True)

    def test_response_with_incorrect_param(self):
        r = requests.get(ApiTest.API_URL,{"q":"ve"})
        self.assertEqual(r.status_code,200)
        res = r.json()
        self.assertEquals(res["results"][0]["name"],"This is invalid, just to demo AJAX call is working")