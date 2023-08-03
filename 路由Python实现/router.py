from typing import Dict, Callable, Optional, List, Tuple

from trie import Node


class Router:
    def __init__(self, roots: Optional[Dict[str, Node]] = None, handlers: Optional[Dict[str, Callable]]= None) -> None:
        self.roots = roots or dict()
        self.handlers = handlers or dict()
    
    @staticmethod
    def parse_pattern(pattern: str) -> List[str]:
        vs = pattern.split("/")

        parts = []
        for item in vs:
            if item != "":
                parts.append(item)
                if item[0] == "*":
                    break
        
        return parts
    
    def add_route(self, method: str, pattern: str, handler: Callable):
        parts = self.parse_pattern(pattern)
    
        key = f"{method}-{pattern}"
        if method not in self.roots:
            self.roots[method] = Node()
        self.roots[method].insert(pattern, parts, 0)
        self.handlers[key] = handler
    
    def get_route(self, method: str, path: str) -> Tuple[Optional[Node], Optional[Dict[str, str]]]:
        search_parts = self.parse_pattern(path)
        params = dict()

        root = self.roots.get(method)
        if not root:
            return None, None
        
        n = root.search(search_parts, 0)
        if n is not None:
            parts = self.parse_pattern(n.pattern)
            for index, part in enumerate(parts):
                if part[0] == ":":
                    params[part[1:]] = search_parts[index]
                if part[0] == "*" and len(part) > 1:
                    params[part[1:]] = "/".join(search_parts[index:])
                    break
            return n, params

        return None, None
    
    def get_routes(self, method: str) -> List[Node]:
        root = self.roots.get(method)
        if root is None:
            return []
        
        nodes = []
        root.travel(nodes)
        return nodes
    
    def handle(self, method: str, path: str, *args, **kwargs):
        n, params = self.get_route(method, path)
        if n is not None:
            key = f"{method}-{n.pattern}"
            self.handlers[key](params, args, kwargs)
        else:
            print(f"404 NOT FOUND {path}")
    

    

