import argparse
import os
import sys

import PyPDF2


def _validate_input_files(pdf_files):
    """Raise SystemExit if any input file does not exist."""
    for f in pdf_files:
        if not os.path.isfile(f):
            sys.exit(f"Error: file not found: {f}")


def merge_pdf_files(pdf_files, output_file):
    if not pdf_files:
        sys.exit("Error: at least one input PDF file is required for merging.")
    _validate_input_files(pdf_files)

    merger = PyPDF2.PdfWriter()
    try:
        for pdf in pdf_files:
            merger.append(pdf)
        with open(output_file, 'wb') as f:
            merger.write(f)
    finally:
        merger.close()


def split_pdf_files(pdf_file, output_file, split_page):
    _validate_input_files([pdf_file])

    with open(pdf_file, 'rb') as infile:
        reader = PyPDF2.PdfReader(infile)
        total_pages = len(reader.pages)

        if split_page < 1 or split_page >= total_pages:
            sys.exit(
                f"Error: split page must be between 1 and {total_pages - 1} "
                f"(the PDF has {total_pages} pages)."
            )

        writer1 = PyPDF2.PdfWriter()
        writer2 = PyPDF2.PdfWriter()

        for i in range(split_page):
            writer1.add_page(reader.pages[i])
        for i in range(split_page, total_pages):
            writer2.add_page(reader.pages[i])

        with open(f'part1_{output_file}', 'wb') as outfile1:
            writer1.write(outfile1)
        with open(f'part2_{output_file}', 'wb') as outfile2:
            writer2.write(outfile2)


def remove_password(pdf_file, output_file, password):
    _validate_input_files([pdf_file])

    with open(pdf_file, 'rb') as infile:
        reader = PyPDF2.PdfReader(infile)

        if reader.is_encrypted:
            result = reader.decrypt(password)
            if result == PyPDF2.PasswordType.NOT_DECRYPTED:
                sys.exit("Error: incorrect password or unsupported encryption.")

        writer = PyPDF2.PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        with open(output_file, 'wb') as f:
            writer.write(f)


def build_parser():
    parser = argparse.ArgumentParser(description='Process some PDF files.')
    parser.add_argument('pdf_files', nargs='*', help='Input PDF file(s)')

    parser.add_argument('-m', '--merge', action='store_true',
                        help='Merge the input PDF files into a single file')
    parser.add_argument('-o', '--output', help='Output PDF file name', required=True)
    parser.add_argument('-s', '--split', help='Split at given page number (1-based)', type=int)
    parser.add_argument('-d', '--decrypt', help='Password to remove from an encrypted PDF', type=str)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.merge:
        merge_pdf_files(args.pdf_files, args.output)
    elif args.split is not None:
        if len(args.pdf_files) != 1:
            sys.exit("Error: exactly one input PDF file is required for splitting.")
        split_pdf_files(args.pdf_files[0], args.output, args.split)
    elif args.decrypt is not None:
        if len(args.pdf_files) != 1:
            sys.exit("Error: exactly one input PDF file is required for decryption.")
        remove_password(args.pdf_files[0], args.output, args.decrypt)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
