import re
import sys
import typing

import googletrans

translator = googletrans.Translator()
regex = re.compile(r" +")


def translate(input: str) -> typing.Optional[str]:
    translated = None

    try:
        translated = translator.translate(input, src="de", dest="uk").text
    except Exception as e:
        sys.stderr.write(f"{e} \n")
        sys.stderr.flush()
        pass

    return translated


class WebvttLine:
    number: str
    cue: str
    content_original: typing.List[str]
    content_translated: typing.Optional[str]

    def __init__(self: 'WebvttLine', number: str, cue: str, content: typing.List[str]) -> None:
        self.number = number
        self.cue = cue
        self.content_original = content
        self.content_translated = None

    def get_file_repr(self: 'WebvttLine') -> str:
        return "\n".join([self.number, self.cue + " line:-1", regex.sub(" ".join(self.content_original), " ")])

    def get_file_repr_translated(self: 'WebvttLine') -> str:
        while self.content_translated is None:
            self.translate()
        return "\n".join([self.number, self.cue + " line:1", self.content_translated])

    def translate(self: 'WebvttLine') -> None:
        if self.content_translated is not None:
            return
        self.content_translated = translate(regex.sub(" ".join(self.content_original), " "))

        sys.stderr.write(self.number + "\n")
        sys.stderr.flush()
