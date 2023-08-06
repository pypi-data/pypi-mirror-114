"""Console script for sindri."""

import fire


def help():
    print("sindri")
    print("=" * len("sindri"))
    print("Set of python functions")


def main():
    fire.Fire({"help": help})


if __name__ == "__main__":
    main()  # pragma: no cover
