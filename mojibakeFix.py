__author__ = 'loromichi'

from decoder import UTF_8


def main():
    with open("sample.txt", "rb") as f:
        lines = f.read()
    print(lines.decode("UTF-8", errors="replace"))

    u = UTF_8()
    fixed_string = u.fix_mojibake(lines, b"\x81\x45")
    print(fixed_string)


if __name__ == '__main__':
    main()