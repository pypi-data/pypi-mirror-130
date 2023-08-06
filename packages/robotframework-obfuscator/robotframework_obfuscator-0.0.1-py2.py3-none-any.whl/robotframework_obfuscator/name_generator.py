from typing import Dict, Optional, List

from functools import partial
import itertools
from robotframework_ls.impl.text_utilities import normalize_robot_name
from robotframework_obfuscator.extract_var_name import get_inner_variable_name
from random import random


class NameGenerator(object):
    def __init__(self, use_stable_names=False):
        self.use_stable_names = use_stable_names
        self._normalized_keyword_old_name_to_new_name: Dict[str, str] = {}
        self._normalized_variable_old_name_to_new_name: Dict[str, str] = {}
        self._next_i = partial(next, itertools.count())
        self._used = set()

    def _next_name(self, name: str) -> str:
        import hashlib
        import time

        m = hashlib.sha256()
        m.update(name.encode("utf-8"))
        if not self.use_stable_names:
            m.update(str(time.time()).encode("utf-8"))
            m.update(str(self._next_i()).encode("utf-8"))

        ret = ("l" + bin(int(m.hexdigest()[:16], 16))[2:]).replace("0", "l")
        while ret in self._used:
            ret += "1"
        self._used.add(ret)

        return ret

    def get_new_keyword_name(self, keyword_name: str) -> Optional[str]:
        normalized_name = normalize_robot_name(keyword_name)
        ret = self._normalized_keyword_old_name_to_new_name.get(normalized_name)
        if not ret:
            return ret
        return self.generate_garbled_keyword_name(ret).lower()

    def get_new_variable_name(self, variable_name: str) -> Optional[str]:
        name = get_inner_variable_name(variable_name)
        if name is None:
            raise AssertionError(f"{variable_name} is not a variable name.")

        normalized_name = normalize_robot_name(name)

        new_name = self._normalized_variable_old_name_to_new_name.get(normalized_name)
        if new_name:
            new_name = self.generate_garbled_keyword_name(new_name).lower()
            return variable_name[0] + "{" + new_name + "}"
        return None

    def on_found_keyword(self, keyword_name: str):
        name = normalize_robot_name(keyword_name)

        if name not in self._normalized_keyword_old_name_to_new_name:
            new_name = self._next_name(name)
            self._normalized_keyword_old_name_to_new_name[name] = new_name

    def on_found_variable(self, variable_name: str):
        name = get_inner_variable_name(variable_name)
        if name is None:
            raise AssertionError(f"{variable_name} is not a variable name.")

        normalized_name = normalize_robot_name(name)

        if normalized_name not in self._normalized_variable_old_name_to_new_name:
            new_name = self._next_name(normalized_name)
            self._normalized_variable_old_name_to_new_name[normalized_name] = new_name

    def get_new_temp_name(self, base_name: str) -> str:
        return self.generate_garbled_keyword_name(self._next_name(base_name)).lower()

    def generate_garbled_keyword_name(self, name: str) -> str:
        """
        Provides the same thing (as far as robot framework is concerned), but a
        bit less readable.
        """
        name = normalize_robot_name(name)
        chars: List[str]

        if self.use_stable_names:
            chars = [
                (c.upper() + " " if (i % 3 == 1) else c) for i, c in enumerate(name)
            ]
        else:
            chars = []
            for c in name:
                if chars and chars[-1] != " ":
                    if random() <= 0.5:
                        chars.append(" ")

                if random() <= 0.5:
                    chars.append(c.upper())
                else:
                    chars.append(c)

        return "".join(chars).strip()
