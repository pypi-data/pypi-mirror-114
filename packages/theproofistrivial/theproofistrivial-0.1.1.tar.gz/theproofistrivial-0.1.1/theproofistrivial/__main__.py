import argparse

import theproofistrivial


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--oneline", action="store_true",
                        help="show output as a single line")
    args = parser.parse_args()

    quote = theproofistrivial.QuoteGenerator()
    output = quote.create()

    if args.oneline:
        print(" ".join(output))
    else:
        print("\n".join(output))

if __name__ == '__main__':
    main()
