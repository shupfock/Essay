from __future__ import annotations

from typing import List, Optional


class Node:
    def __init__(self, part: str, is_wild: bool, children: Optional[List[Node]] = None, pattern: str = ""):
        """
        :param pattern: 待匹配路由
        :param part: 路由的一部分
        :param children: 子节点
        :param is_wild: 是否精确匹配
        """
        self.part = part
        self.is_wild = is_wild
        self.children: List[None] = children or []
        self.pattern = pattern

    def match_child(self, part: str) -> Optional[Node]:
        """第一个匹配成功的节点"""
        for child in self.children:
            if child.part == part or child.is_wild:
                return child
        return None

    def match_children(self, part: str) -> List[Node]:
        """所有匹配成功的节点"""
        nodes = []
        for child in self.children:
            if child.part == part or child.is_wild:
                nodes.append(child)

        return nodes


    def insert(self, pattern: str, parts: List[str], height: int) -> None:
        """插入一个节点"""
        if len(parts) == height:
            self.pattern = pattern
            return
        
        part = parts[height]
        child = self.match_child(part)
        if child is None:
            child = self.__class__(part=part, is_wild=(part[0] == ":" or part[0] == "*"))
            self.children.append(child)
        child.insert(pattern, parts, height+1)
    
    def search(self, parts: List[str], height: int) -> Optional[Node]:
        """查找一个节点"""
        if len(parts) == height or self.part.startswith("*"):
            if self.pattern == "":
                return None
            return self
        
        part = parts[height]
        children = self.match_children(part)

        for child in children:
            result = child.search(parts, height+1)
            if result is not None:
                return result
        return None









