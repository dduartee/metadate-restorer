#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Date Restorer - Restore file creation/modification dates from filenames

This script analyzes filenames (photos, videos, etc.) and extracts date/time information
to restore creation and modification metadata. Useful for chronologically organizing
media files from various sources.

The script works regardless of its filename - you can rename it to anything.py
and it will still function correctly, adapting all examples and help text.

How to add new filename patterns:
1. Find the 'extract_date' function in the code
2. Add a new pattern section following the existing examples
3. Use regex to extract date components from the filename
4. Return a datetime object and an explanation string

License: MIT
"""

import os
import re
import time
import sys
import argparse
import logging
from datetime import datetime

def normalize_digits(s):
    """
    Convert unicode digits (Arabic, Persian, etc.) to Western digits (0-9).
    
    Args:
        s (str): String containing possible unicode digits
        
    Returns:
        str: String with digits converted to Western format
    """
    return s.translate(str.maketrans(
        '٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹',
        '01234567890123456789'
    ))

def extract_date(filename):
    """
    Extract date and time information from a filename.
    
    This function recognizes several common media filename patterns:
    - Digital cameras: 20181128_110755.jpg, IMG_20180507_192217158.jpg
    - WhatsApp: WhatsApp Image 2018-11-27 at 18.41.02.png, IMG-20181225-WA0014.jpg
    - Screenshots: Screenshot_20200101-151016_Calendar.jpg
    - Unix timestamps: FB_IMG_1545742864733.jpg
    - And many other common patterns
    
    HOW TO ADD A NEW PATTERN:
    1. Add a comment describing the pattern
    2. Create a regex that captures the date/time components
    3. Use try/except to handle potential parsing errors
    4. Return a tuple with (datetime_object, explanation_string)
    
    Example template for adding a new pattern:
    ```python
    # Pattern X: DESCRIPTION_OF_PATTERN (e.g., Camera_YYYYMMDD.jpg)
    m = re.search(r'YOUR_REGEX_PATTERN_HERE', filename)
    if m:
        try:
            # Extract date components from regex groups
            # Convert to datetime object
            dt = datetime.strptime(date_string, 'format_string')
            return dt, f"explanation string with {captured_values}"
        except ValueError:
            pass
    ```
    
    Args:
        filename (str): Filename to analyze
        
    Returns:
        tuple: (datetime object or None, extraction explanation or None)
    """
    filename = normalize_digits(filename)
    
    # Pattern 1: 20181128_110755.jpg or IMG_20180507_192217158.jpg
    m = re.search(r'(\d{8})_(\d{6})', filename)
    if m:
        try:
            dt = datetime.strptime(m.group(1) + m.group(2), '%Y%m%d%H%M%S')
            return dt, f"{m.group(1)} {m.group(2)}"
        except ValueError:
            pass
            
    # Pattern 2A: 2020-01-01 12.30.59.jpg (format with date and time separated) - MOVED UP for precedence
    m = re.search(r'(\d{4})-(\d{2})-(\d{2}) (\d{2})\.(\d{2})\.(\d{2})', filename)
    if m:
        try:
            date_part = f"{m.group(1)}{m.group(2)}{m.group(3)}"
            time_part = f"{m.group(4)}{m.group(5)}{m.group(6)}"
            dt = datetime.strptime(date_part + time_part, '%Y%m%d%H%M%S')
            return dt, f"{date_part} {time_part}"
        except ValueError:
            pass
            
    # Pattern 2B: WhatsApp Image 2018-11-27 at 18.41.02.png
    m = re.search(r'(\d{4})-(\d{2})-(\d{2})', filename)
    if m:
        try:
            date_part = f"{m.group(1)}{m.group(2)}{m.group(3)}"
            m2 = re.search(r'at (\d{2})\.(\d{2})\.(\d{2})', filename)
            if m2:
                time_part = f"{m2.group(1)}{m2.group(2)}{m2.group(3)}"
            else:
                time_part = "000000"
            dt = datetime.strptime(date_part + time_part, '%Y%m%d%H%M%S')
            return dt, f"{date_part} {time_part}"
        except ValueError:
            pass

    # Pattern 3: FB_IMG_1545742864733.jpg or standalone timestamp files like 1531699202381.jpg
    # Very restrictive - only matches specific prefixes or standalone timestamp files
    m = re.search(r'(?:FB_IMG_|IMG_)(\d{9,13})(?=\.|_|$)', filename)
    if not m:
        # Try standalone timestamp files (entire filename is just digits + extension)
        m = re.match(r'^(\d{9,13})\.(jpg|jpeg|png|mp4|mov|gif|bmp|tif|tiff|webm|avi|mkv)$', filename, re.IGNORECASE)
    
    if m:
        try:
            # For 13-digit numbers, assume milliseconds and take first 10 digits
            # For 9-10 digit numbers, use as-is (seconds)
            timestamp_str = m.group(1)
            if len(timestamp_str) == 13:
                timestamp = int(timestamp_str[:10])
            else:
                timestamp = int(timestamp_str)
            
            dt = datetime.fromtimestamp(timestamp)
            
            # Validate timestamp is reasonable (from 1970 to current date)
            now = datetime.now()
            unix_epoch = datetime(1970, 1, 1)  # Beginning of Unix time
            
            if unix_epoch <= dt <= now:
                return dt, f"timestamp {timestamp}"
        except (ValueError, OverflowError):
            pass

    # Pattern 4: Screenshot_20200101-151016_Calendar.jpg or Screenshot_20200224-162219.jpg
    m = re.search(r'Screenshot_(\d{8})-(\d{6})', filename)
    if m:
        try:
            dt = datetime.strptime(m.group(1) + m.group(2), '%Y%m%d%H%M%S')
            return dt, f"{m.group(1)} {m.group(2)}"
        except ValueError:
            pass

    # Pattern 5: VID-20200615-WA0127.mp4
    m = re.search(r'VID-(\d{8})-WA', filename)
    if m:
        try:
            dt = datetime.strptime(m.group(1), '%Y%m%d')
            return dt, f"{m.group(1)} 000000"
        except ValueError:
            pass

    # Pattern 6: IMG-20181225-WA0014.jpg or IMG-20181218-WA0002.jpeg or IMG-20181128-WA0047.jpg
    m = re.search(r'IMG-(\d{8})-WA', filename)
    if m:
        try:
            dt = datetime.strptime(m.group(1), '%Y%m%d')
            return dt, f"{m.group(1)} 000000"
        except ValueError:
            pass
            
    # Pattern 7: Photo_20200101_123059.jpg (common on Android phones)
    m = re.search(r'Photo_(\d{8})_(\d{6})', filename)
    if m:
        try:
            dt = datetime.strptime(m.group(1) + m.group(2), '%Y%m%d%H%M%S')
            return dt, f"{m.group(1)} {m.group(2)}"
        except ValueError:
            pass
            
    # Pattern 9: JPEG_20200722_183656.jpg (common on smartphones)
    m = re.search(r'JPEG_(\d{8})_(\d{6})', filename)
    if m:
        try:
            dt = datetime.strptime(m.group(1) + m.group(2), '%Y%m%d%H%M%S')
            return dt, f"{m.group(1)} {m.group(2)}"
        except ValueError:
            pass
            
    return None, None

def process_folder_recursively(root_path, dry_run=False, verbose=False, extensions=None):
    """
    Recursively process all files in a folder, adjusting their dates
    based on patterns found in their names.
    
    Args:
        root_path (str): Root path to start the search
        dry_run (bool): If True, simulates changes without actually making them
        verbose (bool): If True, displays detailed information about each file
        extensions (list): List of file extensions to process (e.g., ['.jpg', '.mp4'])
    
    Returns:
        tuple: (int, int, list) - Total files processed, total files modified, and list of unrecognized files
    """
    total_files = 0
    modified_files = 0
    unrecognized_files = []
    
    logging.info(f"Starting file processing in: {root_path}")
    
    try:
        for dirpath, dirnames, filenames in os.walk(root_path):
            for fname in filenames:
                fpath = os.path.join(dirpath, fname)
                
                # Skip files that don't match specified extensions (if extensions are provided)
                if extensions and not any(fname.lower().endswith(ext.lower()) for ext in extensions):
                    if verbose:
                        logging.debug(f"Skipping {fpath} (extension doesn't match)")
                    continue
                
                total_files += 1
                    
                if not os.path.isfile(fpath):
                    continue

                try:
                    dt, info = extract_date(fname)
                    if dt:
                        modified_files += 1
                        ts = time.mktime(dt.timetuple())
                        
                        if dry_run:
                            logging.info(f"[SIMULATION] {fpath} => {dt} ({info})")
                        else:
                            try:
                                os.utime(fpath, (ts, ts))
                                logging.info(f"{fpath} => {dt} ({info})")
                            except (PermissionError, OSError) as e:
                                logging.error(f"Error changing date of {fpath}: {str(e)}")
                    else:
                        unrecognized_files.append(fpath)
                        if verbose:
                            logging.debug(f"{fpath} => pattern not recognized, date unchanged")
                except Exception as e:
                    logging.error(f"Error processing {fpath}: {str(e)}")
    except Exception as e:
        logging.error(f"Error walking directory {root_path}: {str(e)}")
        
    return total_files, modified_files, unrecognized_files

def configure_logger(log_level=logging.INFO):
    """Configure the logger for the script"""
    format_str = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=log_level,
        format=format_str,
        handlers=[
            logging.StreamHandler()
        ]
    )
    return logging.getLogger()

def parse_arguments():
    """Parses command line arguments"""
    # Get the script name for usage examples
    script_name = os.path.basename(sys.argv[0])
    
    parser = argparse.ArgumentParser(
        description='Restore file dates based on patterns found in their filenames.',
        epilog=f'Examples: \n'
               f'  python {script_name} ./photos \n'
               f'  python {script_name} ./photos --dry-run --verbose \n'
               f'  python {script_name} ./photos --ext jpg jpeg png',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument('folder', type=str, help='Folder for recursive processing')
    parser.add_argument('-s', '--dry-run', action='store_true',
                        help='Run in simulation mode (does not modify files)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Show detailed information during processing')
    parser.add_argument('-e', '--ext', nargs='+', metavar='EXTENSION',
                        help='Only process files with these extensions (ex: jpg png mp4)')
    parser.add_argument('--log', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        default='INFO', help='Set logging detail level')
    parser.add_argument('--ignore-text', action='store_true',
                        help='Ignore common text files (.txt, .md, .py, etc.)')
    
    return parser.parse_args()

if __name__ == "__main__":
    # Get the script name from the file being executed
    script_name = os.path.basename(__file__)
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Configure logger
    log_level = getattr(logging, args.log)
    configure_logger(log_level)
    
    # Check if folder exists
    folder = args.folder
    if not os.path.isdir(folder):
        logging.error(f"Error: {folder} is not a valid directory.")
        sys.exit(1)
    
    # Process extensions if specified
    extensions = None
    if args.ext:
        extensions = [f".{ext.lstrip('.')}" for ext in args.ext]
        logging.info(f"Processing only files with extensions: {', '.join(extensions)}")
    elif args.ignore_text:
        # Common media file extensions to include by default
        extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff", 
                    ".mp4", ".mov", ".avi", ".mkv", ".webm", ".wmv", ".3gp"]
        logging.info(f"Ignoring text files. Processing only media files.")
    
    # Show configuration
    mode = "SIMULATION" if args.dry_run else "PRODUCTION"
    logging.info(f"Starting in {mode} mode")
    logging.info(f"Source folder: {folder}")
    
    # Process files
    try:
        start_time = time.time()
        total, modified, unrecognized = process_folder_recursively(
            folder, 
            dry_run=args.dry_run,
            verbose=args.verbose,
            extensions=extensions
        )
        duration = time.time() - start_time
        
        # Show statistics
        logging.info(f"Processing completed in {duration:.2f} seconds")
        logging.info(f"Total files analyzed: {total}")
        logging.info(f"Files with restored dates: {modified}")
        logging.info(f"Files without recognized patterns: {total - modified}")
        
        # If there are unrecognized files and verbose mode, show the list
        if unrecognized and (args.verbose or args.log == 'DEBUG'):
            logging.info("Files without recognized pattern:")
            for file in unrecognized:
                logging.info(f"  - {file}")
        
    except KeyboardInterrupt:
        logging.warning("Process interrupted by user.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error during processing: {str(e)}")
        sys.exit(1)
