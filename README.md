# pdf-pytools
A CLI tool for performing basic PDF manipulations.

## Installation

```bash
pip install -e .
```

## Usage

### Merge PDFs

Combine multiple PDF files into one:

```bash
pdf-pytools -m -o output.pdf file1.pdf file2.pdf file3.pdf
```

### Split a PDF

Split a PDF at a given page number. The two halves are saved as `part1_<output>` and `part2_<output>`:

```bash
pdf-pytools -s 5 -o output.pdf input.pdf
```

### Remove Password

Decrypt a password-protected PDF:

```bash
pdf-pytools -d mypassword -o unlocked.pdf locked.pdf
```

## Options

| Flag | Description |
|------|-------------|
| `-m`, `--merge` | Merge all input files into the output file |
| `-s`, `--split N` | Split input at page N (1-based) |
| `-d`, `--decrypt PASSWORD` | Remove password protection |
| `-o`, `--output FILE` | Output file name (required) |
