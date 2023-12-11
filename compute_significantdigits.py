from weakref import ref
import plotly as plt
import glob
import os
import argparse
import numpy as np
import significantdigits as sd

def parse_mat_files(base):
    mat_files = glob.glob(os.path.join(base, '**', '*.mat'), recursive=True)
    subjects_mat_files = {}
    for mat_file in mat_files:
        basename = os.path.splitext(os.path.basename(mat_file))[0]
        subjects_mat_files[basename] = subjects_mat_files.get(basename, []) + [mat_file]
    return subjects_mat_files

def load_mat_file(mat_file):
    return np.loadtxt(mat_file)

def print_mat_files(subjects_mat_files):
    for subjects, mat_files in subjects_mat_files.items():
        print(subjects)
        for mat_file in mat_files:
            print(f' - {mat_file}')

def compute_significant_digits(subjects_mat_files):
    significant_digits = {}

    for subjects, mat_files in subjects_mat_files.items():
        mat_array = np.array([load_mat_file(mat_file) for mat_file in mat_files])
        sig = sd.significant_digits(mat_array, reference=mat_array.mean(axis=0))
        significant_digits[subjects] = sig

    return significant_digits

def write_significant_digits(significant_digits, output_file):
    np.savetxt(output_file, significant_digits)
    os.chmod(output_file, 644)


def parse_args():
    parser = argparse.ArgumentParser(description='Plot results')
    parser.add_argument('--input-directory', type=str, default='results', help='results directory')
    parser.add_argument('--output-directory', type=str, default='results/significantdigits', help='output directory')
    parser.add_argument('--dry-run', action='store_true', help='dry run')
    return parser.parse_args()

def main():
    args = parse_args()
    subjects_mat_files = parse_mat_files(args.input_directory)

    if args.dry_run:
        print_mat_files(subjects_mat_files)
    else:
        os.makedirs(args.output_directory, exist_ok=True, mode=755)

    significant_digits = compute_significant_digits(subjects_mat_files)
    for subjects, sig in significant_digits.items():
        if args.dry_run:
            print(f'{subjects}:\n{sig}')
        else:
            output_file = os.path.join(args.output_directory, f'{subjects}.txt')
            write_significant_digits(sig, output_file)

if __name__ == '__main__':
    main()
    