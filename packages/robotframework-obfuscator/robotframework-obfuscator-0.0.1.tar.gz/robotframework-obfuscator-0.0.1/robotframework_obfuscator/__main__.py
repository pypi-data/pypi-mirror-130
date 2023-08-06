import argparse
import sys
from typing import Optional, List
import typing
from robotframework_obfuscator.obfuscator import IOpts, IDoWrite


def add_arguments(parser):
    parser.description = "RobotFramework Obfuscator"

    parser.add_argument(
        "--stable-names",
        action="store_true",
        help="If passed, the names will always be the same among runs.",
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="If passed, just prints the version to the standard output and exits.",
    )

    parser.add_argument(
        "--dest",
        help="The directory where the contents should be written.",
    )

    parser.add_argument(
        "--skip-keyword",
        action="append",
        help="A keyword name that should not be translated (may be specified multiple times).",
    )

    parser.add_argument(
        "--skip-var",
        action="append",
        help="A variable name that should not be translated (may be specified multiple times).",
    )

    parser.add_argument(
        "target",
        nargs="+",
        help="The directory/directories with the contents that should be obfuscated.",
    )


def main(args: Optional[List[str]] = None, do_write: Optional[IDoWrite] = None):
    original_args = args if args is not None else sys.argv[1:]
    parser = argparse.ArgumentParser()
    add_arguments(parser)

    opts = typing.cast(IOpts, parser.parse_args(args=original_args))
    if opts.version:
        import robotframework_obfuscator

        sys.stdout.write(robotframework_obfuscator.__version__)
        sys.stdout.flush()
        return

    if not opts.dest:
        sys.stderr.write(
            "The --dest <directory> where the obfuscated version should be written to must be provided."
        )
        sys.exit(1)
    from robotframework_obfuscator.obfuscator import RobotFrameworkObfuscator

    obfuscator = RobotFrameworkObfuscator(opts, do_write=do_write)
    obfuscator.obfuscate()


if __name__ == "__main__":
    main()
