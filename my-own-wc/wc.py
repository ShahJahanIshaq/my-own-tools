import argparse
import sys

parser = argparse.ArgumentParser(
    prog="my-own-wc-tool",
    description="Returns the word count, byte count, and line count in input files"
)

parser.add_argument('-c', '--bytes', action='store_true', help='get file size in bytes')
parser.add_argument('-l', '--lines', action='store_true', help='get the number of lines in file')
parser.add_argument('-w', '--words', action='store_true', help='get the number of words in file')
parser.add_argument('-m', '--chars', action='store_true', help='get the number of characters in file')
parser.add_argument('files', nargs='*')

args = parser.parse_args()

def get_required_metrics():
    return [args.lines, args.words, args.bytes, args.chars]

def get_binary_file(filename):
    with open(filename, 'rb') as file:
        return file.read()
    
def get_metrics(binary_data):
    byte_count = len(binary_data)
    content = binary_data.decode()
    line_count = content.count('\n')
    word_count = len(content.split())
    char_count = len(content)
    return (line_count, word_count, byte_count, char_count)

def make_print_message(metrics, filename, stdin=False):
    required_metrics = get_required_metrics()
    message = ''
    if not any(get_required_metrics()):
        message = f"{metrics[0]:>8} {metrics[1]:>8} {metrics[2]:>8}"
        if not stdin:
            message += f" {filename}"
    else:
        for i in range(len(metrics)):
            if i == 3 and required_metrics[i - 1]:
                continue
            if required_metrics[i]: message += f"{metrics[i]:>8}"
        if not stdin:
            message += f" {filename}"
    return message

def compute_running_total(metrics, curr_totals):
    for i in range(len(metrics)):
        curr_totals[i] += metrics[i]
    return curr_totals

def make_total_print_message(totals):
    message = ''
    required_metrics = get_required_metrics()
    if not any(get_required_metrics()):
        message = f"{totals[0]:>8} {totals[1]:>8} {totals[2]:>8} total"
    else:
        for i in range(len(totals)):
            if i == 3 and required_metrics[i - 1]:
                continue
            if required_metrics[i]: message += f"{totals[i]:>8}"
        message += " total"
    return message


def main():
    totals = [0] * 4
    if len(args.files) == 0:
        data = sys.stdin.buffer.read()
        metrics = get_metrics(data)
        totals = compute_running_total(metrics, totals)
        message = make_print_message(metrics, None, stdin=True)
        print(message)
    for filename in args.files:
        binary_file = get_binary_file(filename)
        metrics = get_metrics(binary_file)
        totals = compute_running_total(metrics, totals)
        message = make_print_message(metrics, filename)
        print(message)
    if len(args.files) > 1:
        total_message = make_total_print_message(totals)
        print(total_message)

if __name__ == '__main__':
    main()