import os
from frequency_count import FrequencyCounter
from huffman_classes import HuffmanTree
from pathlib import Path


INPUT_PATH = "alice_in_wonderland.txt"
TEMP_PATH = os.path.splitext(INPUT_PATH)[0] + "_temp" + ".txt"
OUTPUT_PATH = os.path.splitext(INPUT_PATH)[0] + "_compressed"
OUTPUT_TEMP = OUTPUT_PATH + "_temp" + ".txt"
DECOMPRESSED_PATH = OUTPUT_PATH + "_decompressed.txt"


def archiver():
    with open(INPUT_PATH, "r", encoding="utf-8") as input_text:
        for line in input_text:
            FrequencyCounter.count(line)
    tree = HuffmanTree.build_tree(FrequencyCounter.get())

    with open(INPUT_PATH, "r", encoding="utf-8") as input_text, open(TEMP_PATH, "w", encoding="utf-8") as temp_file:
        size = 0
        table = HuffmanTree.codes(tree)
        for line in input_text:
            size += len(line)
            for char in line:
                temp_file.write(table[char])

    with open(TEMP_PATH, "r", encoding="utf-8") as temp, open(OUTPUT_PATH, "w", encoding="utf-8") as output_file:
        binary_string = temp.readline()
        output_file.writelines(str(tree.codes()) + '\n')
        output_file.writelines(str(size) + '\n')
        temp = binary_string + '0' * (8 - len(binary_string) % 8)
        chars = ''.join([chr(int(temp[i:i + 8], 2))
                         for i in range(0, len(temp), 8)])
        output_file.writelines(chars)
    Path.unlink(Path(TEMP_PATH))
    return


def to_binary():
    with open(OUTPUT_PATH, "r", encoding="utf-8") as compressed, open(OUTPUT_TEMP, "w", encoding="utf-8") as temp:
        table = compressed.readline()

        import ast
        codes = ast.literal_eval(table)
        rev = {}
        for (key, value) in codes.items():
            rev[value] = key
        size = int(compressed.readline()[:-1])
        input_data = "".join(line for line in compressed)
        output_seq = "".join(format(ord(char), '08b') for char in input_data)
        temp.writelines(output_seq)
    return [rev, size]


def parse_binary(codes, size):
    with open(OUTPUT_TEMP, "r", encoding="utf8") as binary, \
            open(DECOMPRESSED_PATH, "w", encoding="utf-8") as decompressed:
        line = binary.readline()
        word = ""
        words = 0
        for c in line:
            word += c
            if codes.get(word) is not None:
                decompressed.write(codes[word])
                word = ""
                words += 1
            if words == size:
                break
    Path.unlink(Path(OUTPUT_TEMP))
    return


def unpacker():
    parse_binary(*to_binary())
    return


if __name__ == "__main__":
    archiver()
    unpacker()
