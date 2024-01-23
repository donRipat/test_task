from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class HuffmanNode:
    """Class defining a tree node for Huffman encoding.
    
    The node carries a data about character and its frequency.
    """
    char: Optional[str] = None
    freq: int = 0
    left: Optional["HuffmanNode"] = None
    right: Optional["HuffmanNode"] = None

    def __lt__(self, other: "HuffmanNode") -> bool:
        return self.freq < other.freq


@dataclass
class HuffmanTree:
    """Class representing a tree for Huffman encoding
    
    Attributes:
    root : HuffmanNode
    
    Methods:
    build_tree(freq_table: Dict[str, int]) -> HuffmanTree
    huffman_codes() -> Dict[str, str]
    """
    root: HuffmanNode

    @classmethod
    def build_tree(cls, freq_table: Dict[str, int]) -> "HuffmanTree":
        import heapq

        priority_queue = [HuffmanNode(char, freq)
                          for char, freq
                          in freq_table.items()]
        heapq.heapify(priority_queue)

        while len(priority_queue) > 1:
            left_child = heapq.heappop(priority_queue)
            right_child = heapq.heappop(priority_queue)

            internal_node = HuffmanNode(freq=left_child.freq 
                                        + right_child.freq)
            internal_node.left = left_child
            internal_node.right = right_child

            heapq.heappush(priority_queue, internal_node)

        return cls(priority_queue[0])

    def codes(self) -> Dict[str, str]:
        codes = {}

        def traverse_tree(node: Optional[HuffmanNode] = None, code: str = ""):
            if node:
                if node.char is not None:
                    codes[node.char] = code
                traverse_tree(node.left, code + "0")
                traverse_tree(node.right, code + "1")

        traverse_tree(self.root)
        return codes
