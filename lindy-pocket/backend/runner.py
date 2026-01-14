import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python runner.py <flow_id>")
        sys.exit(1)
    flow_id = sys.argv[1]
    print(f"Runner stub started for flow: {flow_id}")


if __name__ == "__main__":
    main()