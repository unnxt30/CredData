import binascii
import json

def reverse_repo_id_lookup(new_repo_id: str, snapshot_file: str = "snapshot.json") -> dict:
    """Get original repo info from 8-character CRC32 hash"""
    with open(snapshot_file, 'r', encoding='utf-8') as f:
        snapshot = json.load(f)
    
    for full_hash, repo_url in snapshot.items():
        # Calculate the 8-character CRC32 hash (same as in download_data.py)
        repo_id_bytes = binascii.unhexlify(full_hash)
        short_hash = f"{binascii.crc32(repo_id_bytes):08x}"
        
        if short_hash == new_repo_id:
            return {
                'original_repo_id': full_hash,
                'repo_url': repo_url,
                'repo_name': repo_url.split('/')[-2] + '/' + repo_url.split('/')[-1],
                'commit_sha': full_hash[:40]  # First 40 chars are commit SHA
            }
    
    return None

# Example usage:
def main():

    files_data = [
        '39def7b4.csv',
        'c9b945fa.csv',
        'ff527e6f.csv',
        '87e029df.csv',
        'b133f43d.csv',
        '00408ef6.csv',
        '4638da2b.csv',
        'd2926eb1.csv',
        'efb4b495.csv'
    ]

    for file in files_data:
        result = reverse_repo_id_lookup(file.split('.')[0])
        if result:
            print(f"Original repo_id: {result['original_repo_id']}")
            print(f"Repository: {result['repo_name']}")
            print(f"URL: {result['repo_url']}")
            print(f"Commit SHA: {result['commit_sha']}") 


if __name__ == "__main__":
    main()