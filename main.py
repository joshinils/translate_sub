#!/usr/bin/env python3
import sys
from concurrent.futures import ThreadPoolExecutor

from webvtt_line import WebvttLine


def main() -> None:
    filename = sys.argv[1]
    with open(filename) as file:
        lines = file.read().splitlines()

    lines.pop(0)  # remove leading WEBVTT line

    webvtt_lines = []
    while len(lines) > 0:
        line = lines.pop(0)
        if line == "":
            continue
        number = line
        cue = lines.pop(0)

        text_lines = []
        text_line = lines.pop(0)
        while text_line != "":
            text_lines.append(text_line)
            text_line = lines.pop(0)
        webvtt_lines.append(WebvttLine(number, cue, text_lines))

        # print(len(line), "\t", line)

    with ThreadPoolExecutor(max_workers=32) as executor:
        for webvtt_line in webvtt_lines:
            executor.submit(webvtt_line.translate)
        # executor.shutdown()

    print("WEBVTT")
    print()
    for webvtt_line in webvtt_lines:
        print(webvtt_line.get_file_repr())
        print()
        print(webvtt_line.get_file_repr_translated())
        print()


if __name__ == "__main__":
    main()
