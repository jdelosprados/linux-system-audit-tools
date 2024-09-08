"""
This script checks the GPG key integrity of installed RPM packages on a system. 
It retrieves a list of all installed packages, finds the GPG key used to sign each package, 
and compares it with the system's installed GPG public keys. Packages with missing or unmatched 
GPG keys are flagged for review. Practically, this can be used to ensure package authenticity and 
verify that installed software hasn't been tampered with or signed by untrusted sources.
"""


import subprocess

def get_installed_packages():
    """Get a list of all installed RPM packages."""
    result = subprocess.run(['rpm', '-qa'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
    packages = result.stdout.strip().split('\n')
    return packages

def get_gpg_key_id(package):
    """Get the GPG key ID of an installed RPM package."""
    try:
        result = subprocess.run(['rpm', '-qi', package], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
        for line in result.stdout.split('\n'):
            if 'Signature' in line and 'Key ID' in line:
                key_id = line.split('Key ID ')[-1].strip()
                return key_id
        return "No GPG key ID found"
    except subprocess.CalledProcessError:
        return "Error retrieving GPG key ID"

def get_installed_gpg_keys():
    """Get a list of all installed GPG keys."""
    result = subprocess.run(['rpm', '-q', 'gpg-pubkey'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
    keys = [line.split('-')[2] for line in result.stdout.strip().split('\n')]
    return keys

def key_id_matches_gpg_key(key_id, gpg_keys):
    """Check if the key ID matches any of the installed GPG keys."""
    for gpg_key in gpg_keys:
        if key_id.endswith(gpg_key):
            return True
    return False

def main():
    installed_packages = get_installed_packages()
    installed_gpg_keys = get_installed_gpg_keys()
    
    if not installed_packages:
        print("No packages found.")
        return

    missing_keys = {}
    
    for package in installed_packages:
        gpg_key_id = get_gpg_key_id(package)
        print(f"Package: {package}, GPG Key ID: {gpg_key_id}")
        if gpg_key_id != "No GPG key ID found" and not key_id_matches_gpg_key(gpg_key_id, installed_gpg_keys):
            missing_keys[package] = gpg_key_id

    if missing_keys:
        print("\nPackages with missing GPG keys:")
        for package, key_id in missing_keys.items():
            print(f"{package}: Missing GPG key ID {key_id}")
    else:
        print("\nNo missing GPG keys found.")

if __name__ == "__main__":
    main()