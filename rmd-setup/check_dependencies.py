import sys

# Check Python version
required_python_version = (3, 7)
if sys.version_info < required_python_version:
    print(f"Python {required_python_version[0]}.{required_python_version[1]} or higher is required.")
else:
    print(f"Python version is {sys.version_info[0]}.{sys.version_info[1]}, requirement satisfied.")

# List of packages to check
packages = ["cv2", "numpy", "matplotlib", "picamera", "pyaudio"]

# Check each package
for package in packages:
    try:
        __import__(package)
        print(f"{package} is installed.")
    except ImportError:
        print(f"{package} is not installed.")
