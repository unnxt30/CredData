#!/usr/bin/env python3
"""
Script to copy files referenced in trim_meta CSV files along with their metadata
to a separate directory structure.
"""

import os
import csv
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional


def ensure_directory_exists(path: Path) -> None:
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)


def read_csv_files(trim_meta_dir: str) -> List[Dict]:
    """Read all CSV files from trim_meta directory and return combined data."""
    all_data = []
    
    for csv_file in Path(trim_meta_dir).glob("*.csv"):
        print(f"Reading {csv_file}")
        
        with open(csv_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Add source CSV info to the row
                row['SourceCSV'] = csv_file.name
                all_data.append(row)
    
    print(f"Total records found: {len(all_data)}")
    return all_data


def copy_file_with_metadata(row: Dict, output_dir: Path, workspace_root: Path) -> bool:
    """
    Copy a single file with its metadata to the output directory.
    Returns True if successful, False otherwise.
    """
    file_path = row['FilePath']
    source_file = workspace_root / file_path
    
    # Check if source file exists
    if not source_file.exists():
        print(f"Warning: Source file not found: {source_file}")
        return False
    
    # Create destination path maintaining directory structure
    # Remove 'data/' prefix if present to avoid duplication
    relative_path = Path(file_path)
    if relative_path.parts[0] == 'data':
        relative_path = Path(*relative_path.parts[1:])
    
    dest_file = output_dir / "files" / relative_path
    metadata_file = output_dir / "metadata" / relative_path.with_suffix(relative_path.suffix + '.meta.json')
    
    # Ensure destination directories exist
    ensure_directory_exists(dest_file.parent)
    ensure_directory_exists(metadata_file.parent)
    
    try:
        # Copy the file
        shutil.copy2(source_file, dest_file)
        
        # Create metadata
        metadata = {
            'id': row['Id'],
            'file_id': row['FileID'],
            'domain': row['Domain'],
            'repo_name': row['RepoName'],
            'original_file_path': row['FilePath'],
            'copied_file_path': str(dest_file.relative_to(output_dir)),
            'line_start': int(row['LineStart']) if row['LineStart'] else None,
            'line_end': int(row['LineEnd']) if row['LineEnd'] else None,
            'ground_truth': row['GroundTruth'],
            'value_start': int(row['ValueStart']) if row['ValueStart'] else None,
            'value_end': int(row['ValueEnd']) if row['ValueEnd'] else None,
            'cryptography_key': row['CryptographyKey'] if row['CryptographyKey'] else None,
            'predefined_pattern': row['PredefinedPattern'] if row['PredefinedPattern'] else None,
            'category': row['Category'],
            'source_csv': row['SourceCSV']
        }
        
        # Write metadata file
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        return True
        
    except Exception as e:
        print(f"Error copying {source_file}: {e}")
        return False


def create_summary_report(all_data: List[Dict], output_dir: Path, success_count: int) -> None:
    """Create a summary report of the copying operation."""
    summary = {
        'total_records': len(all_data),
        'successfully_copied': success_count,
        'failed_to_copy': len(all_data) - success_count,
        'statistics': {
            'by_ground_truth': {},
            'by_category': {},
            'by_repo': {},
            'by_source_csv': {}
        }
    }
    
    # Generate statistics
    for row in all_data:
        # Ground truth stats
        gt = row['GroundTruth']
        summary['statistics']['by_ground_truth'][gt] = summary['statistics']['by_ground_truth'].get(gt, 0) + 1
        
        # Category stats
        cat = row['Category']
        summary['statistics']['by_category'][cat] = summary['statistics']['by_category'].get(cat, 0) + 1
        
        # Repo stats
        repo = row['RepoName']
        summary['statistics']['by_repo'][repo] = summary['statistics']['by_repo'].get(repo, 0) + 1
        
        # Source CSV stats
        csv_file = row['SourceCSV']
        summary['statistics']['by_source_csv'][csv_file] = summary['statistics']['by_source_csv'].get(csv_file, 0) + 1
    
    # Write summary
    summary_file = output_dir / 'summary_report.json'
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nSummary Report:")
    print(f"Total records: {summary['total_records']}")
    print(f"Successfully copied: {summary['successfully_copied']}")
    print(f"Failed to copy: {summary['failed_to_copy']}")
    print(f"Summary saved to: {summary_file}")


def create_master_metadata(all_data: List[Dict], output_dir: Path) -> None:
    """Create a master metadata file with all records."""
    master_file = output_dir / 'master_metadata.json'
    
    # Convert CSV data to structured format
    structured_data = []
    for row in all_data:
        structured_row = {
            'id': row['Id'],
            'file_id': row['FileID'],
            'domain': row['Domain'],
            'repo_name': row['RepoName'],
            'original_file_path': row['FilePath'],
            'line_start': int(row['LineStart']) if row['LineStart'] else None,
            'line_end': int(row['LineEnd']) if row['LineEnd'] else None,
            'ground_truth': row['GroundTruth'],
            'value_start': int(row['ValueStart']) if row['ValueStart'] else None,
            'value_end': int(row['ValueEnd']) if row['ValueEnd'] else None,
            'cryptography_key': row['CryptographyKey'] if row['CryptographyKey'] else None,
            'predefined_pattern': row['PredefinedPattern'] if row['PredefinedPattern'] else None,
            'category': row['Category'],
            'source_csv': row['SourceCSV']
        }
        structured_data.append(structured_row)
    
    with open(master_file, 'w', encoding='utf-8') as f:
        json.dump(structured_data, f, indent=2)
    
    print(f"Master metadata saved to: {master_file}")


def main():
    """Main function to process all CSV files and copy referenced files."""
    # Configuration
    trim_meta_dir = "trim_meta"
    output_dir = Path("copied_files_with_metadata")
    workspace_root = Path(".")
    
    print("=== File Copy Script with Metadata ===")
    print(f"Source CSV directory: {trim_meta_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Workspace root: {workspace_root.absolute()}")
    
    # Create output directory structure
    ensure_directory_exists(output_dir / "files")
    ensure_directory_exists(output_dir / "metadata")
    
    # Read all CSV files
    all_data = read_csv_files(trim_meta_dir)
    
    if not all_data:
        print("No data found in CSV files!")
        return
    
    # Process each file
    print(f"\nProcessing {len(all_data)} files...")
    success_count = 0
    
    for i, row in enumerate(all_data, 1):
        if i % 100 == 0:  # Progress indicator
            print(f"Processed {i}/{len(all_data)} files...")
        
        if copy_file_with_metadata(row, output_dir, workspace_root):
            success_count += 1
    
    # Create reports
    create_summary_report(all_data, output_dir, success_count)
    create_master_metadata(all_data, output_dir)
    
    print(f"\n=== Process Complete ===")
    print(f"Successfully copied {success_count}/{len(all_data)} files")
    print(f"Files and metadata saved to: {output_dir.absolute()}")


if __name__ == "__main__":
    main() 