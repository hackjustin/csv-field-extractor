#!/usr/bin/env python3
import pandas as pd


def extract_field_from_csv(csv_file_path, field_name,
                           sort_alphabetically=False):
    """
    Extract a specific field from a CSV file.

    Args:
        csv_file_path (str): Path to the CSV file
        field_name (str): Name of the field/column to extract
        sort_alphabetically (bool): Whether to sort the results

    Returns:
        list: List of values from the specified field
    """
    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Check if field exists
    if field_name not in df.columns:
        available = list(df.columns)
        raise ValueError(f"Field '{field_name}' not found in CSV. "
                         f"Available fields: {available}")

    # Extract the field and remove any null/empty values
    field_values = df[field_name].dropna().tolist()
    field_values = [str(val).strip() for val in field_values
                    if str(val).strip()]

    # Sort if requested
    if sort_alphabetically:
        field_values.sort()

    return field_values


def main():
    """Command-line interface for the CSV field extractor."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Extract a specific field from a CSV file',
        epilog='Example: python csv_field_extractor.py data.csv Symbol --sort')

    parser.add_argument('csv_file', help='Path to the CSV file')
    parser.add_argument('field_name', help='Name of field/column to extract')
    parser.add_argument('--sort', '-s', action='store_true',
                        help='Sort the results alphabetically')
    parser.add_argument('--output', '-o',
                        choices=['lines', 'comma', 'space'],
                        default='lines',
                        help='Output format: lines (default), '
                             'comma-separated, or space-separated')

    args = parser.parse_args()

    try:
        # Extract the field
        values = extract_field_from_csv(args.csv_file, args.field_name,
                                        args.sort)

        # Format output
        if args.output == 'lines':
            for value in values:
                print(value)
        elif args.output == 'comma':
            print(','.join(values))
        elif args.output == 'space':
            print(' '.join(values))

    except FileNotFoundError:
        print(f"Error: File '{args.csv_file}' not found.")
        return 1
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

    return 0


# Example usage as library:
if __name__ == "__main__":
    import sys
    sys.exit(main())
