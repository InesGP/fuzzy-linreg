#!/usr/bin/env python

import os
import glob
import json
import argparse
import sys

def find_t1s(base):
  regexp = os.path.join(base, 'sub-*', 'ses-*', 'anat', '*_T1w.nii.gz')
  t1s = glob.glob(regexp)
  return t1s

def extract_fields(t1_path):
  base, subject, session, anat, t1 = t1_path.split(os.sep)
  return {
    'base': base,
    'subject': subject,
    'session': session,
    't1': t1}

def extract_sessions(t1_paths):
  subject_t1_map = {}
  for t1 in t1_paths:
    fields = extract_fields(t1)
    subject = fields['subject']
    session = fields['session']
    if session == 'ses-1':
      subject_t1_map[subject] = subject_t1_map.get(subject, {})
      subject_t1_map[subject]['session-1'] = t1
    elif session == 'ses-2':
      subject_t1_map[subject] = subject_t1_map.get(subject, {})
      subject_t1_map[subject]['session-2'] = t1
    
  return subject_t1_map

def create_flirt_invocation(subject, subject_t1_map, prefix=''):
  prefix = f'{prefix}_' if prefix else ''
  in_file = subject_t1_map[subject]['session-1']
  reference = subject_t1_map[subject]['session-2']
  out_file = prefix + f'{subject}.nii.gz'
  out_mat_file = prefix + f'{subject}.mat'

  invocation = {
    'in_file': in_file,
    'reference': reference,
    'out_file': out_file,
    'out_mat_file': out_mat_file
  }
  return invocation


def write_invocation(invocation, output_dir, output_file, dry_run=False):
  if dry_run:
    print("write invocation")
    json.dump(invocation, sys.stdout, indent=4)
    return
  with open(os.path.join(output_dir, output_file), 'w') as outfile:
    json.dump(invocation, outfile, indent=4)


def main():
  args = parse_args()
  t1s = find_t1s(args.base)
  subject_t1_map = extract_sessions(t1s)

  if args.dry_run:    
    for subject, sessions in subject_t1_map.items():
      for session, t1 in sessions.items():
        print(f'{subject} {session} {t1}')

  for subject in subject_t1_map.keys():
    invocation = create_flirt_invocation(subject, subject_t1_map, args.prefix)
    write_invocation(invocation, args.output_directory, f'{subject}.json', args.dry_run)
  

def parse_args():
  parser = argparse.ArgumentParser(description='Create invocations for the IEEE paper')
  parser.add_argument('--base', type=str, default='CORR', help='Base directory')
  parser.add_argument('--prefix', type=str, default='', help='Prefix for output files')
  parser.add_argument('--output-directory', type=str, default='invocations', help='Output directory')
  parser.add_argument('--dry-run', action='store_true', help='Dry run')
  return parser.parse_args()

if '__main__' == __name__:
  main()
  