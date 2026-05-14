from bisect import bisect
from hashlib import md5


class ConsistentHash:
    def __init__(self, number_of_replicas, nodes=None):
        self.number_of_replicas = number_of_replicas

        # Sorted list of hash positions
        self.ring = []

        # hash_position -> node
        self.hash_map = {}

        if nodes:
            for node in nodes:
                self.add(node)

    def _hash(self, key):
        """
        Generate a stable integer hash using MD5.
        """
        return int(md5(str(key).encode()).hexdigest(), 16)

    def add(self, node):
        """
        Add a node with virtual replicas.
        """
        for i in range(self.number_of_replicas):
            virtual_node = f"{node}:{i}"

            hash_value = self._hash(virtual_node)

            self.ring.append(hash_value)
            self.hash_map[hash_value] = node

        self.ring.sort()

    def remove(self, node):
        """
        Remove a node and all its replicas.
        """
        for i in range(self.number_of_replicas):
            virtual_node = f"{node}:{i}"

            hash_value = self._hash(virtual_node)

            if hash_value in self.hash_map:
                self.ring.remove(hash_value)
                del self.hash_map[hash_value]

    def get(self, key):
        """
        Find which node should store the key.
        """
        if not self.ring:
            return None

        hash_value = self._hash(key)

        # Find first node clockwise
        index = bisect(self.ring, hash_value)

        # Wrap around if needed
        if index == len(self.ring):
            index = 0

        return self.hash_map[self.ring[index]]
