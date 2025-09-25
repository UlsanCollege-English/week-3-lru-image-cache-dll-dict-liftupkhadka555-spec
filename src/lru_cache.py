### /src/lru_cache.py

class _Node:
    __slots__ = ("key", "val", "prev", "next")
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity):
        assert capacity > 0
        self.cap = capacity
        self.map = {}
        # sentinels
        self.head = _Node("__H__", None)  # most recent after head
        self.tail = _Node("__T__", None)  # least recent before tail
        self.head.next = self.tail
        self.tail.prev = self.head

    # ----------------- Helpers -----------------
    def _remove(self, node):
        """Detach node from the list"""
        prev, nxt = node.prev, node.next
        prev.next = nxt
        nxt.prev = prev

    def _add_to_front(self, node):
        """Insert node right after head (most recent)"""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def _move_to_front(self, node):
        """Move an existing node to the front (most recent)"""
        self._remove(node)
        self._add_to_front(node)

    # ----------------- API -----------------
    def get(self, key):
        if key not in self.map:
            return None   # <-- fix here
        node = self.map[key]
        self._move_to_front(node)
        return node.val

    def put(self, key, val):
        if key in self.map:
            # update value and move to front
            node = self.map[key]
            node.val = val
            self._move_to_front(node)
        else:
            if len(self.map) == self.cap:
                # evict least recently used (before tail)
                lru = self.tail.prev
                self._remove(lru)
                del self.map[lru.key]

            # add new node
            node = _Node(key, val)
            self.map[key] = node
            self._add_to_front(node)
