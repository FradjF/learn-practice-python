import argparse

parser = argparse.ArgumentParser(description="Process some integers")
parser.add_argument("num1", type=int, help="First integer to add")
parser.add_argument("num2", type=int, help="Second integer to add")
parser.add_argument("-v", "--verbose", action="store_true", help="Increase "
                                                                 "output verbosity")
args = parser.parse_args()
result = args.num1 + args.num2

print(f"The sum of {args.num1} and {args.num2} is {result}")

if args.verbose:
    print("Calculation completed successfully.")