import pytest
from frequency_count import FrequencyCounter
from huffman_classes import *


def test_frequency_counter():
    FrequencyCounter.count("")
    assert FrequencyCounter.get() == {}

    FrequencyCounter.count("a")
    assert FrequencyCounter.get() == {'a': 1}

    FrequencyCounter.count("aa")
    assert FrequencyCounter.get() == {'a': 3}

    FrequencyCounter.count("\n\n")
    assert FrequencyCounter.get() == {'a': 3, '\n': 2}


def test_tree_builder():
    with pytest.raises(IndexError):
        HuffmanTree.build_tree({})

    tree = HuffmanTree.build_tree({'a': 3})
    ans = """HuffmanTree(root=HuffmanNode(char='a', freq=3, left=None, right=None))"""
    assert str(tree) == ans


def test_huffman_codes():
    input_string = """
    Alice's Adventures in Wonderland

                ALICE'S ADVENTURES IN WONDERLAND

                          Lewis Carroll

               THE MILLENNIUM FULCRUM EDITION 3.0




                            CHAPTER I

                      Down the Rabbit-Hole


  Alice was beginning to get very tired of sitting by her sister
on the bank, and of having nothing to do:  once or twice she had
peeped into the book her sister was reading, but it had no
pictures or conversations in it, `and what is the use of a book,'
thought Alice `without pictures or conversation?'

  So she was considering in her own mind (as well as she could,
for the hot day made her feel very sleepy and stupid), whether
the pleasure of making a daisy-chain would be worth the trouble
of getting up and picking the daisies, when suddenly a White
Rabbit with pink eyes ran close by her.
    """
    FrequencyCounter.count(input_string)
    tree = HuffmanTree.build_tree(FrequencyCounter.get())
    table = HuffmanTree.codes(tree)
    for v in table.values():
        for v2 in table.values():
            if v == v2:
                continue
            assert v not in v2[:len(v)]
