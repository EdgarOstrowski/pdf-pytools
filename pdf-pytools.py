import argparse

import PyPDF2


def merge_pdf_files(pdf_files, output_file):
    merger = PyPDF2.PdfWriter()

    for pdf in pdf_files:
        merger.append(pdf)

    merger.write(output_file)
    merger.close()


def split_pdf_files(pdf_file, output_file):
    with open(pdf_file, 'rb') as infile:
        reader = PyPDF2.PdfReader(infile)
        writer1 = PyPDF2.PdfWriter()
        writer2 = PyPDF2.PdfWriter()

        for i in range(args.split):
            writer1.add_page(reader.pages[i])
        for i in range(args.split, len(reader.pages)):
            writer2.add_page(reader.pages[i])

        with open(f'part1_{output_file}', 'wb') as outfile1:
            writer1.write(outfile1)
        with open(f'part2_{output_file}', 'wb') as outfile2:
            writer2.write(outfile2)

def build_parser():
    parser = argparse.ArgumentParser(description='Process some PDF files.')
    parser.add_argument("pdf_files", nargs='*', help='Input PDF files')

    parser.add_argument('-m', '--merge', action='store_true',
                        help='List of PDF files to merge with the input file')
    parser.add_argument('-o', '--output', help='Output PDF file name', required=True)
    parser.add_argument('-s', '--split', help='Split at given page number', type=int)

    return parser


if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()

    if args.merge:
        merge_pdf_files(args.pdf_files, args.output)



