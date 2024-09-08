import subprocess
import os

# ANSI escape code for green text
GREEN = "\033[0;32m"
RESET = "\033[0m"

def run_command(command):
    """Helper function to run a shell command and return the output."""
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
    return result.stdout.strip()

def is_package_installed(package):
    """Check if the specified package is installed."""
    try:
        run_command(['rpm', '-q', package])
        return True
    except subprocess.CalledProcessError:
        return False

def get_package_metadata(package):
    """Get the metadata of the installed package."""
    try:
        metadata = run_command(['rpm', '-qi', package])
        return metadata
    except subprocess.CalledProcessError:
        return None

def get_gpg_key_installed(package):
    """Get the GPG key ID of the installed package."""
    output = run_command(['rpm', '-qi', package])
    for line in output.splitlines():
        if "Signature" in line:
            return line.split()[-1].strip()
    return None

def download_rpm_package(package, arch):
    """Download the binary RPM for the package and architecture."""
    try:
        run_command(['yumdownloader', '--archlist=' + arch, package, '--destdir=/tmp'])
    except subprocess.CalledProcessError as e:
        print(f"Error downloading RPM package: {e}")
        return None
    rpms = [f for f in os.listdir('/tmp') if f.startswith(package) and f.endswith('.rpm') and '.src.rpm' not in f]
    return rpms[0] if rpms else None

def get_rpm_metadata(rpm_path):
    """Extract the metadata from the downloaded RPM."""
    try:
        metadata = run_command(['rpm', '-qpi', f'/tmp/{rpm_path}'])
        return metadata
    except subprocess.CalledProcessError:
        return None

def get_gpg_key_from_rpm_metadata(metadata):
    """Extract the GPG key ID from RPM metadata."""
    for line in metadata.splitlines():
        if "Signature" in line:
            return line.split()[-1].strip()
    return None

def verify_package_files(package):
    """Verify the package files."""
    try:
        run_command(['rpm', '-V', package])
        print(f"{GREEN}The {package} package is installed and the files exist.{RESET}")
    except subprocess.CalledProcessError:
        print(f"Warning: The {package} package files do not exist or verification failed.")

def check_package_lib(package):
    """Main function to check GPG key integrity and package metadata."""
    print(f"Checking the integrity of the {package} package...")

    # Check if the package is installed
    if not is_package_installed(package):
        print(f"Warning: The {package} package is not installed.")
        return

    # Get and display the installed package metadata
    installed_metadata = get_package_metadata(package)
    if installed_metadata:
        print("Installed Package Metadata:")
        print(installed_metadata)
    else:
        print(f"Warning: Could not retrieve metadata for the installed {package} package.")
        return

    # Get the GPG key ID of the installed package
    gpg_key_installed = get_gpg_key_installed(package)
    print(f"Installed GPG key ID: {gpg_key_installed}")

    # Detect architecture of the installed package
    arch = run_command(['rpm', '-q', '--qf', '%{ARCH}', package])
    print(f"Detected architecture: {arch}")

    # Download the binary RPM for the same architecture as the installed package
    rpm_file = download_rpm_package(package, arch)
    if not rpm_file:
        print(f"Error: Could not download RPM for {package}.")
        return
    print(f"Downloaded RPM file: {rpm_file}")

    # Get and display the downloaded package metadata
    rpm_metadata = get_rpm_metadata(rpm_file)
    if rpm_metadata:
        print("Downloaded Package Metadata:")
        print(rpm_metadata)
    else:
        print(f"Warning: Could not retrieve metadata for the downloaded {package} package.")

    # Extract the GPG key ID from the downloaded RPM
    gpg_key_legit = get_gpg_key_from_rpm_metadata(rpm_metadata)
    print(f"Repository GPG key ID: {gpg_key_legit}")

    # Compare the GPG key IDs
    if gpg_key_legit != gpg_key_installed:
        print(f"Warning: The GPG key ID of the installed {package} package does not match the repository GPG key ID.")
    else:
        print(f"{GREEN}The GPG key ID of the installed {package} package matches the repository GPG key ID.{RESET}")

    # Verify the package files
    verify_package_files(package)

    # Clean up the downloaded RPM
    os.remove(f'/tmp/{rpm_file}')

def main():
    package = input("Enter the package name to check: ")
    if package:
        check_package_lib(package)
    else:
        print("Please provide a valid package name.")

if __name__ == "__main__":
    main()
