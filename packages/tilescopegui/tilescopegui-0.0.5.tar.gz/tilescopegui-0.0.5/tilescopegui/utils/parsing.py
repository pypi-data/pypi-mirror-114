import argparse

from .constants import Constant


class Arguments:
    # pylint: disable=too-few-public-methods
    """Command line argument handler."""

    def __init__(self, url: str, debug: bool, browser: bool) -> None:
        self.url: str = url
        self.debug: bool = debug
        self.browser: bool = browser

    @classmethod
    def parse(cls) -> "Arguments":
        """Parse command line arguments into a data class."""
        parser = Arguments._get_parser()
        args = vars(parser.parse_args())
        return cls(args["url"], args["debug"], args["browser"])

    @staticmethod
    def _get_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description="Process some integers.")
        parser.add_argument(
            "-d",
            "--debug",
            dest="debug",
            action="store_true",
            default=False,
            help="Start server in debug mode.",
        )
        parser.add_argument(
            "-u",
            "--url",
            dest="url",
            default=Constant.DEFAULT_URL,
            type=str,
            help="The webpage to open.",
        )
        parser.add_argument(
            "-b",
            "--no-browser",
            dest="browser",
            action="store_false",
            default=True,
            help="Avoid opening a browser tab at start.",
        )
        return parser
