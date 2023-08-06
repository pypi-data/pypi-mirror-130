from typing import List, Iterable, Union, Dict, Optional, Tuple
import pathlib
import sys
from os import scandir, makedirs
from robotframework_ls.impl.protocols import (
    ICompletionContext,
)
from robotframework_obfuscator.name_generator import NameGenerator
from robotframework_ls.impl.text_utilities import normalize_robot_name
from robotframework_obfuscator.extract_var_name import get_inner_variable_name


class _Collector(object):
    def __init__(
        self,
        completion_context: ICompletionContext,
        name_generator: NameGenerator,
        relative_path: pathlib.Path,
    ) -> None:
        self.completion_context = completion_context
        self._name_generator = name_generator
        self.relative_path = relative_path

    def on_keyword(self, keyword_node_name: str) -> None:
        self._name_generator.on_found_keyword(keyword_node_name)

    def on_variable(self, variable_name: str) -> None:
        self._name_generator.on_found_variable(variable_name)


class IOpts(object):
    version: bool  # Should print --version?
    stable_names: bool  # Use stable names? (otherwise, each run will provide different names)
    dest: Optional[str]  # Dest directory
    target: List[str]  # Target directories to obfuscate
    skip_keyword: List[str]  # Keyword names that should not be obfuscated
    skip_var: List[str]  # Variable names that should not be obfuscated


class IDoWrite(object):
    def __call__(self, path: pathlib.Path, contents: Union[str, bytes]):
        pass


class RobotFrameworkObfuscator(object):
    def __init__(self, opts: IOpts, do_write: Optional[IDoWrite]):
        self._opts = opts
        paths = []
        for d in opts.target:
            p = pathlib.Path(d)
            if not p.exists():
                self._critical(f"Target: '{p}' does not exist.")
            paths.append(p.absolute())

        self._paths: List[pathlib.Path] = paths
        if do_write is None:

            checked = set()

            def _do_write(path: pathlib.Path, contents: Union[str, bytes]):
                if path.parent not in checked:
                    makedirs(path.parent, exist_ok=True)
                    checked.add(path.parent)

                if isinstance(contents, str):
                    path.write_text(contents, "utf-8")
                else:
                    path.write_bytes(contents)

            self._do_write = _do_write
        else:
            self._do_write = do_write

    def _critical(self, txt):
        sys.stderr.write(txt)
        sys.stderr.write("\n")
        sys.stderr.flush()
        sys.exit(1)

    def _iter_dir(self, p: Union[pathlib.Path, str]) -> Iterable[str]:
        for entry in scandir(p):
            if entry.is_dir():
                yield from self._iter_dir(entry.path)
            else:
                yield entry.path

    def _iter_files(self) -> Iterable[Tuple[pathlib.Path, pathlib.Path]]:
        """
        Provides the base directory and the target file.

        i.e.: yield(base_dir, filename)
        """
        p: pathlib.Path
        for p in self._paths:
            if p.is_dir():
                for entry in self._iter_dir(p):
                    yield p, pathlib.Path(entry)
            else:
                yield p.parent, p

    def obfuscate(self) -> None:
        from robotframework_ls.impl.completion_context import CompletionContext
        from robotframework_ls.impl.robot_workspace import RobotDocument
        from robocorp_ls_core import uris
        from robotframework_ls.impl import ast_utils
        from robotframework_obfuscator.ast_to_code import ast_to_code
        from robotframework_obfuscator.obfuscator_transformer import (
            ObfuscatorTransformer,
        )
        from robot.api.parsing import Token

        opts = self._opts
        file_to_collector: Dict[pathlib.Path, _Collector] = {}
        name_generator = NameGenerator(use_stable_names=opts.stable_names)

        skip_keyword_names = (
            set(normalize_robot_name(name) for name in opts.skip_keyword)
            if opts.skip_keyword
            else set()
        )

        skip_variable_names = (
            set(normalize_robot_name(name) for name in opts.skip_var)
            if opts.skip_var
            else set()
        )
        assert opts.dest
        dest_base = pathlib.Path(opts.dest).absolute()

        # The first step is collecting information on the keywords that are available.
        for base_dir, f in self._iter_files():
            relative_path = f.relative_to(base_dir)
            lower_name = f.name.lower()
            if not lower_name.endswith((".robot", ".resource")):
                if lower_name.endswith(".pyc"):
                    continue

                # Not a robot file and not excluded, copy the file as is.
                target = dest_base / relative_path
                try:
                    self._do_write(target, f.read_bytes())
                except Exception:
                    raise Exception(f"Error when copying {f} to {target}.")
                continue

            # We need to collect keywords/variables first to know which keyword/variable names
            # we should translate (we shouldn't translate keyword/variable names defined
            # elsewhere).
            uri = uris.from_fs_path(str(f))
            doc = RobotDocument(uri)
            completion_context = CompletionContext(doc)
            collector = _Collector(completion_context, name_generator, relative_path)
            ast = doc.get_ast()
            for node_info in ast_utils.iter_all_nodes(ast):
                accept_token_types = [Token.VARIABLE, Token.ASSIGN]
                node = node_info.node
                if node.__class__.__name__ == "Keyword":
                    normalized_name = normalize_robot_name(node.name)
                    if normalized_name not in skip_keyword_names:
                        collector.on_keyword(node.name)
                elif node.__class__.__name__ == "Arguments":
                    accept_token_types.append(Token.ARGUMENT)

                try:
                    tokens = node.tokens
                except:
                    pass
                else:
                    for t in tokens:
                        if "{" in t.value:
                            if t.type in accept_token_types:
                                name = get_inner_variable_name(t.value)
                                if name is not None:
                                    tokenized = list(t.tokenize_variables())
                                    assert (
                                        len(tokenized) == 1
                                    ), f"Did not expect variable or assign ({t.type} - {t.value}) to have multiple vars ({tokenized})."

                                    normalized_var_name = normalize_robot_name(name)
                                    if normalized_var_name not in skip_variable_names:
                                        collector.on_variable(t.value)

            file_to_collector[f] = collector

            # ast_utils.print_ast(ast)

        # Now that we have information on the keywords available, the 2nd step is
        # providing a new name for each keyword.
        # Note that at this point we'll change the ast directly.
        for f, collector in file_to_collector.items():
            ast = collector.completion_context.get_ast()
            ObfuscatorTransformer(name_generator).visit(ast)

            text = ast_to_code(ast)
            if opts.dest:
                target = pathlib.Path(opts.dest) / collector.relative_path
                self._do_write(target, text)
