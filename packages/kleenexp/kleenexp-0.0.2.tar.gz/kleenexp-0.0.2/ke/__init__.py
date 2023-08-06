from parsimonious.exceptions import ParseError as ParsimoniousParseError
import argparse
import re as original_re
from re import ASCII, A, IGNORECASE, I, LOCALE, L, UNICODE, U, MULTILINE, M, DOTALL, S
import sys
import traceback

from ke.parser import Parser
from ke import compiler
from ke import asm
from ke.errors import KleenexpError, error, ParseError

ke_parser = Parser()


def re(kleenexp, syntax="python"):
    if syntax is None:
        syntax = "python"
    try:
        ast = ke_parser.parse(kleenexp)
    except ParsimoniousParseError:
        # we want to raise the nice parsimonious ParseError with all the explanation,
        # but we also want to raise something that isinstance(x, re.error)...
        # so we defined a doubly-inheriting class ParseError and we convert the exception
        # to that, taking care to keep the traceback (as described in
        # http://www.ianbicking.org/blog/2007/09/re-raising-exceptions.html)
        _exc_class, exc, tb = sys.exc_info()
        exc = ParseError(exc.text, exc.pos, exc.expr)
        raise exc.with_traceback(tb)
    compiled = compiler.compile(ast)
    return asm.assemble(compiled, syntax=syntax)


def compile(kleenexp, flags=0, syntax="python"):
    return original_re.compile(re(kleenexp, syntax=syntax), flags=flags)


def match(kleenexp, string, flags=0, syntax="python"):
    return original_re.match(re(kleenexp, syntax=syntax), string, flags=flags)


def search(kleenexp, string, flags=0, syntax="python"):
    return original_re.compile(re(kleenexp, syntax=syntax), string, flags=flags)


parser = argparse.ArgumentParser(
    description="Convert legacy regexp to kleenexp.",
    epilog="""usage: echo "Trololo lolo" | grep -P `ke "[#sl]Tro[0+ #space | 'lo']lo[#el]"`""",
)
parser.add_argument(
    "pattern",
    type=str,
    default="",
    help="a legacy regular expression (remember to escape it correctly)",
)
parser.add_argument(
    "--js",
    dest="syntax",
    action="store_const",
    const="javascript",
    default="python",
    help="output javascript regex syntax",
)


def main():
    args = parser.parse_args()
    try:
        print(re(args.pattern, syntax=args.syntax), end="")
        return 0
    except error:
        t, v, _tb = sys.exc_info()
        print("".join(traceback.format_exception_only(t, v)).strip(), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
