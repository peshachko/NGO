#!/usr/bin/env python
"""Extract form fields from a PDF membership application.

Note
-----
Requires: ``sudo dnf install pdftk-java``

"""

import argparse
import subprocess


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract form fields from a PDF membership application."
    )
    parser.add_argument("filename", help="Path to the PDF file")

    return parser.parse_args()


def extract_form_data(pdf_path):
    result = subprocess.run(
        ["pdftk", pdf_path, "dump_data_fields_utf8"],
        capture_output=True,
        text=True,
    )

    fields = {}
    current_name = None

    for line in result.stdout.splitlines():
        if line.startswith("FieldName:"):
            current_name = line.split(":", 1)[1].strip()
        elif line.startswith("FieldValue:") and current_name is not None:
            fields[current_name] = line.split(":", 1)[1].strip()

    return fields


def main(filename):
    data = extract_form_data(filename)
    for key, value in data.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    args = parse_args()
    main(args.filename)
