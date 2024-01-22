import os
from frequency_count import FrequencyCounter
from huffman_classes import HuffmanTree
from pathlib import Path


INPUT_PATH = "alice_in_wonderland.txt"
TEMP_PATH = os.path.splitext(INPUT_PATH)[0] + "_temp" + ".txt"
OUTPUT_PATH = os.path.splitext(INPUT_PATH)[0] + "_compressed"
OUTPUT_TEMP = OUTPUT_PATH + "_temp" + ".txt"
DECOMPRESSED_PATH = OUTPUT_PATH + "_decompressed.txt"


def parse(path: str, counter: FrequencyCounter) -> str:
    with open(path, "r", encoding="utf-8") as input_text:
        for line in input_text:
            counter.count(line)
    return "OK"


def encode(input_path: str, output_path: str, table: dict):
    with open(input_path, "r", encoding="utf-8") as input_text, open(output_path, "w", encoding="utf-8") as output_file:
        size = 0
        for line in input_text:
            size += len(line)
            for char in line:
                output_file.write(table[char])
    return size


def binary_string_to_ascii(binary_string):
    padded_binary_string = binary_string + '0' * (8 - len(binary_string) % 8)

    ascii_characters = [chr(int(padded_binary_string[i:i+8], 2))
                        for i in range(0, len(padded_binary_string), 8)]

    result_string = ''.join(ascii_characters)
    return result_string


def compress():
    counter = FrequencyCounter()
    parse(INPUT_PATH, counter)
    tree = HuffmanTree.build_tree(counter.get())
    size = encode(INPUT_PATH, TEMP_PATH, tree.huffman_codes())
    with open(TEMP_PATH, "r", encoding="utf-8") as temp, open(OUTPUT_PATH, "w", encoding="utf-8") as output_file:
        i = temp.readline()
        output_file.writelines(str(tree.huffman_codes()) + '\n')
        output_file.writelines(str(size) + '\n')
        output_file.writelines(binary_string_to_ascii(i))
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
    with open(OUTPUT_TEMP, "r", encoding="utf8") as binary, open(DECOMPRESSED_PATH, "w", encoding="utf-8") as dc:
        line = binary.readline()
        word = ""
        words = 0
        for c in line:
            word += c
            if codes.get(word) is not None:
                dc.write(codes[word])
                word = ""
                words += 1
            if words == size:
                break
    Path.unlink(Path(OUTPUT_TEMP))
    return


def decompress():
    parse_binary(*to_binary())
    return


if __name__ == "__main__":
    compress()
    decompress()
