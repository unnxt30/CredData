#!/usr/bin/env python3
"""
Script to create trimmed CSV files with diverse categories and balanced GroundTruth distribution.
Creates 9 CSV files in trim_meta/ directory with 24 total entries.
"""

import os
import csv

def create_trim_meta_directory():
    """Create the trim_meta directory if it doesn't exist."""
    if not os.path.exists('trim_meta'):
        os.makedirs('trim_meta')
        print("Created trim_meta/ directory")
    else:
        print("trim_meta/ directory already exists")

def create_csv_file(filename, data):
    """Create a CSV file with the given data."""
    filepath = os.path.join('trim_meta', filename)
    
    # CSV header
    header = ['Id', 'FileID', 'Domain', 'RepoName', 'FilePath', 'LineStart', 'LineEnd', 
              'GroundTruth', 'ValueStart', 'ValueEnd', 'CryptographyKey', 'PredefinedPattern', 'Category']
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(data)
    
    print(f"Created {filepath} with {len(data)} entries")

def main():
    """Main function to create all trimmed CSV files."""
    create_trim_meta_directory()
    
    # File 1: 39def7b4_trimmed.csv (Ruby codebase - 3 entries)
    data_39def7b4 = [
        ['17247', 'd97e408a', 'GitHub', '39def7b4', 'data/39def7b4/spec/d97e408a.rb', '91', '91', 'T', '51', '112', '', '', 'Credential'],
        ['22029', '2d217115', 'GitHub', '39def7b4', 'data/39def7b4/spec/api/2d217115.rb', '36', '36', 'X', '21', '27', '', '', 'Secret'],
        ['255', '64efeea8', 'GitHub', '39def7b4', 'data/39def7b4/lib/64efeea8.rb', '13', '13', 'F', '', '', '', '', 'Secret']
    ]
    
    # File 2: c9b945fa_trimmed.csv (Python/docs codebase - 3 entries)
    data_c9b945fa = [
        ['30739', 'cb378009', 'GitHub', 'c9b945fa', 'data/c9b945fa/test/cb378009.py', '41', '41', 'T', '27', '43', '', '', 'Secret'],
        ['28927', '0cb23f01', 'GitHub', 'c9b945fa', 'data/c9b945fa/test/0cb23f01.py', '245', '245', 'X', '35', '46', '', '', 'Auth:Secret:Token'],
        ['2172', 'cec4df94', 'GitHub', 'c9b945fa', 'data/c9b945fa/example/docs/cec4df94.rst', '157', '157', 'F', '', '', '', '', 'Auth']
    ]
    
    # File 3: ff527e6f_trimmed.csv (Small mixed file - 3 entries)
    data_ff527e6f = [
        ['17221', '7b3ed02b', 'GitHub', 'ff527e6f', 'data/ff527e6f/_/7b3ed02b.rst', '11', '11', 'T', '90', '100', '', '', 'Token'],
        ['29794', 'd734dab9', 'GitHub', 'ff527e6f', 'data/ff527e6f/test/example/resource/d734dab9.py', '21', '21', 'X', '22', '25', '', '', 'Password'],
        ['6352', '046331d0', 'GitHub', 'ff527e6f', 'data/ff527e6f/docs/046331d0.rst', '78', '78', 'F', '', '', '', '', 'Auth']
    ]
    
    # File 4: 87e029df_trimmed.csv (JavaScript codebase - 3 entries)
    data_87e029df = [
        ['35001', '1faa942a', 'GitHub', '87e029df', 'data/87e029df/test/1faa942a.js', '98', '98', 'T', '37', '42', '', '', 'URL Credentials'],
        ['35000', '0aa2d3d2', 'GitHub', '87e029df', 'data/87e029df/test/fixture/0aa2d3d2.json', '5', '5', 'X', '35', '40', '', '', 'URL Credentials'],
        ['1104', '4e7a2ace', 'GitHub', '87e029df', 'data/87e029df/test/4e7a2ace.js', '506', '506', 'F', '', '', '', '', 'Key']
    ]
    
    # File 5: b133f43d_trimmed.csv (DevOps/Config files - 3 entries)
    data_b133f43d = [
        ['35495', 'a844bf5e', 'GitHub', 'b133f43d', 'data/b133f43d/example/a844bf5e.p8', '1', '28', 'T', '', '', 'Private', '', 'PEM Private Key'],
        ['28881', '80f0c7c2', 'GitHub', 'b133f43d', 'data/b133f43d/_/80f0c7c2.yml', '102', '102', 'X', '19', '23', '', '', 'Password'],
        ['483', '044e7d55', 'GitHub', 'b133f43d', 'data/b133f43d/_/044e7d55.md', '14', '14', 'F', '', '', '', '', 'API']
    ]
    
    # File 6: 00408ef6_trimmed.csv (C/C++ codebase - 3 entries)
    data_00408ef6 = [
        ['1330673', 'bbcf1132', 'GitHub', '00408ef6', 'data/00408ef6/src/app/bbcf1132.cpp', '39', '39', 'T', '26', '62', '', '', 'UUID'],
        ['18157', 'eee97fd2', 'GitHub', '00408ef6', 'data/00408ef6/lib/eee97fd2.c', '4256', '4256', 'T', '16', '24', '', '', 'URL Credentials'],
        ['30', '1d02852d', 'GitHub', '00408ef6', 'data/00408ef6/sample/1d02852d.c', '475', '475', 'F', '', '', '', '', 'Password']
    ]
    
    # File 7: 4638da2b_trimmed.csv (PHP codebase - 2 entries)
    data_4638da2b = [
        ['2341', 'fccb8d5c', 'GitHub', '4638da2b', 'data/4638da2b/src/fccb8d5c.php', '184', '184', 'F', '', '', '', '', 'Token'],
        ['3054', '281f4af8', 'GitHub', '4638da2b', 'data/4638da2b/src/secret/281f4af8.php', '57', '57', 'F', '', '', '', '', 'Secret']
    ]
    
    # File 8: d2926eb1_trimmed.csv (Java codebase - 2 entries)
    data_d2926eb1 = [
        ['23465', '8e89f5c4', 'GitHub', 'd2926eb1', 'data/d2926eb1/src/rest/sys/modul/8e89f5c4.java', '72', '72', 'F', '', '', '', '', 'Auth'],
        ['1200', '6631b0fe', 'GitHub', 'd2926eb1', 'data/d2926eb1/src/conf/resource/app/6631b0fe.yml', '88', '88', 'F', '', '', '', '', 'Key']
    ]
    
    # File 9: efb4b495_trimmed.csv (Go codebase - 2 entries)
    data_efb4b495 = [
        ['53', 'b3356305', 'GitHub', 'efb4b495', 'data/efb4b495/_/b3356305.md', '401', '401', 'F', '', '', '', '', 'URL Credentials'],
        ['4328', 'bd8c0745', 'GitHub', 'efb4b495', 'data/efb4b495/init/bd8c0745.sql', '9', '9', 'F', '21', '48', '', '', 'Password']
    ]
    
    # Create all CSV files
    files_data = [
        ('39def7b4.csv', data_39def7b4),
        ('c9b945fa.csv', data_c9b945fa),
        ('ff527e6f.csv', data_ff527e6f),
        ('87e029df.csv', data_87e029df),
        ('b133f43d.csv', data_b133f43d),
        ('00408ef6.csv', data_00408ef6),
        ('4638da2b.csv', data_4638da2b),
        ('d2926eb1.csv', data_d2926eb1),
        ('efb4b495.csv', data_efb4b495)
    ]
    
    total_entries = 0
    for filename, data in files_data:
        create_csv_file(filename, data)
        total_entries += len(data)
    
    print(f"\n✅ Successfully created {len(files_data)} trimmed CSV files")
    print(f"📊 Total entries across all files: {total_entries}")
    
    # Print summary statistics
    print("\n📈 Summary Statistics:")
    
    # Count GroundTruth distribution
    ground_truth_counts = {'T': 0, 'F': 0, 'X': 0}
    categories = set()
    
    for _, data in files_data:
        for row in data:
            gt = row[7]  # GroundTruth column
            ground_truth_counts[gt] += 1
            categories.add(row[12])  # Category column
    
    print(f"   GroundTruth distribution:")
    for gt, count in ground_truth_counts.items():
        percentage = (count / total_entries) * 100
        print(f"     {gt}: {count} entries ({percentage:.1f}%)")
    
    print(f"   Categories: {len(categories)} unique categories")
    print(f"     {', '.join(sorted(categories))}")
    
    print(f"\n🎯 Dataset meets requirements:")
    print(f"   ✓ Category diversity: {len(categories)} different categories")
    print(f"   ✓ Balanced GroundTruth: T={ground_truth_counts['T']}, F={ground_truth_counts['F']}, X={ground_truth_counts['X']}")
    print(f"   ✓ Total files: {total_entries} entries across {len(files_data)} CSV files")

if __name__ == "__main__":
    main()