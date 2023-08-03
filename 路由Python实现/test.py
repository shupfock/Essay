from router import Router
from trie import Node


def fake_handler(*args, **kwargs):
    print(args)
    print(kwargs)


class TestRouter:

    @staticmethod
    def new_test_router() -> Router:
        r = Router()
        r.add_route("GET", "/", fake_handler)
        r.add_route("GET", "/hello/:name", fake_handler)
        r.add_route("GET", "/hello/b/c", fake_handler)
        r.add_route("GET", "/hi/:name", fake_handler)
        r.add_route("GET", "/assets/*filepath", fake_handler)
        return r
    
    def test_parse_pattern(self):
        r = self.new_test_router()
        assert ["p", ":name"] == r.parse_pattern("/p/:name")
        assert ["p", "*"] == r.parse_pattern("/p/*")
        assert ["p", "*name"] == r.parse_pattern("/p/*name/*")

    def test_get_route(self):
        r = self.new_test_router()
        n, ps = r.get_route("GET", "/hello/python")
        assert n is not None
        assert n.pattern == "/hello/:name"
        assert ps["name"] == "python"
        
    def test_get_route2(self):
        r = self.new_test_router()
        n, ps = r.get_route("GET", "/assets/file1.txt")
        assert n.pattern == "/assets/*filepath" and ps["filepath"] == "file1.txt"

        n2, ps2 = r.get_route("GET", "/assets/css/test.css")
        assert n2.pattern == "/assets/*filepath" and ps2["filepath"] == "css/test.css"

    def test_get_routes(self):
        r = self.new_test_router()
        nodes = r.get_routes("GET")
        for i, n in enumerate(nodes):
            print(i+1, n)
        
        assert len(nodes) == 5
