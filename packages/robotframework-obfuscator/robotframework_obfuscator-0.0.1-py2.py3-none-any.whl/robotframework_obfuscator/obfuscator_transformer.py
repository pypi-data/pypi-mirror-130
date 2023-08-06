from robot.api.parsing import ModelTransformer, Token, KeywordCall
from robotframework_obfuscator.name_generator import NameGenerator
from robotframework_ls.impl.keywords_in_args import KEYWORD_NAME_TO_KEYWORD_INDEX
from robotframework_ls.impl.text_utilities import normalize_robot_name
from robotframework_obfuscator.extract_var_name import get_inner_variable_name


class ObfuscatorTransformer(ModelTransformer):
    def __init__(self, name_generator: NameGenerator):
        self.name_generator = name_generator

    def rename_node(self, node, token):
        self._update_common(node)

        if not token or not token.value:
            return node

        splitted = token.value.split(".")
        old_name = splitted[-1]
        old_normalized_name = normalize_robot_name(old_name)
        new_name = self.name_generator.get_new_keyword_name(old_normalized_name)
        ret = [node]
        if new_name:
            splitted[-1] = new_name
            token.value = ".".join(splitted)
        else:
            # We can't use it directly, but let's at least garble it a bit...
            splitted[-1] = self.name_generator.generate_garbled_keyword_name(
                splitted[-1]
            )
            token.value = ".".join(splitted)

            if token.type == Token.KEYWORD:
                # Check if this was some 'Run Keyword' variant where we should also
                # translate a parameter.
                consider_keyword_at_index = KEYWORD_NAME_TO_KEYWORD_INDEX.get(
                    old_normalized_name
                )
                if consider_keyword_at_index is not None:
                    i_arg = 0
                    for arg in node.tokens:
                        if arg.type == token.ARGUMENT:
                            i_arg += 1
                            if i_arg == consider_keyword_at_index:
                                new_arg_name = self.name_generator.get_new_keyword_name(
                                    normalize_robot_name(arg.value)
                                )
                                if new_arg_name:
                                    arg.value = new_arg_name

                # It's a call from a third party library, so, we can't directly replace it.
                # Still, we can change some things to make the call a bit more obfuscated
                # by replacing it with an evaluation.
                if len(splitted) == 1:
                    tokens = list(node.tokens)
                    if len(tokens) >= 2:
                        sep_token = tokens[0]
                        name_token = tokens[1]

                        if (
                            sep_token.type == Token.SEPARATOR
                            and name_token.type == Token.KEYWORD
                        ):
                            var_name = "${%s}" % self.name_generator.get_new_temp_name(
                                splitted[0]
                            )

                            eval_str = []
                            for c in splitted[0]:
                                eval_str.append("chr(%s)" % hex(ord(c)))

                            # Do it only for the simplest cases.
                            new_tokens = [
                                sep_token,
                                Token(Token.ASSIGN, var_name),
                                Token(Token.SEPARATOR, "  "),
                                Token(
                                    Token.KEYWORD,
                                    self.name_generator.generate_garbled_keyword_name(
                                        "Evaluate"
                                    ),
                                ),
                                Token(Token.SEPARATOR, "  "),
                                Token(
                                    Token.ARGUMENT, "''.join([%s])" % ",".join(eval_str)
                                ),
                                Token(Token.EOL, "\n"),
                            ]

                            del tokens[1]
                            tokens.insert(
                                1,
                                Token(
                                    Token.KEYWORD,
                                    self.name_generator.generate_garbled_keyword_name(
                                        "Run Keyword"
                                    ),
                                ),
                            )
                            tokens.insert(2, Token(Token.SEPARATOR, "  "))
                            tokens.insert(3, Token(Token.KEYWORD, var_name))
                            node.tokens = tuple(tokens)
                            ret = [KeywordCall(tokens=new_tokens), node]

        return ret

    def visit_KeywordName(self, node):
        return self.rename_node(node, node.get_token(Token.KEYWORD_NAME))

    def visit_KeywordCall(self, node):
        return self.rename_node(node, node.get_token(Token.KEYWORD))

    def generic_visit(self, node):
        self._update_common(node)
        ret = ModelTransformer.generic_visit(self, node)
        return ret

    def _update_common(self, node):
        try:
            tokens = node.tokens
        except AttributeError:
            return
        else:
            for token in tokens:
                # i.e.: Remove tokens.
                if token.type == token.COMMENT:
                    token.value = ""

                else:
                    if "{" in token.value:
                        new_token_value = []
                        tokenized = list(token.tokenize_variables())
                        changed = False
                        for t in tokenized:
                            value = t.value
                            v = get_inner_variable_name(value)

                            if v is not None:
                                new_name = self.name_generator.get_new_variable_name(
                                    value
                                )
                                if new_name:
                                    changed = True
                                    new_token_value.append(new_name)
                                else:
                                    new_token_value.append(value)
                            else:
                                new_token_value.append(value)

                        if changed:
                            token.value = "".join(new_token_value)
