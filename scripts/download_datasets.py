# scripts/setup/download_datasets.py
"""
Dataset Download Script for ML Engineer Challenge
Downloads and prepares all required datasets for the challenge.
"""

import os
import requests
import zipfile
import tarfile
import hashlib
from pathlib import Path
from tqdm import tqdm
import argparse

class DatasetDownloader:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Dataset configurations
        self.datasets = {
            'cifar100': {
                'url': 'https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz',
                'filename': 'cifar-100-python.tar.gz',
                'extract_dir': 'cifar-100-python',
                'md5': 'eb9058c3a382ffc7106e4002c42a8d85'
            },
            'tiny_imagenet': {
                'url': 'http://cs231n.stanford.edu/tiny-imagenet-200.zip',
                'filename': 'tiny-imagenet-200.zip',
                'extract_dir': 'tiny-imagenet-200',
                'md5': None  # Large file, skip MD5 for demo
            },
            'coco_sample': {
                'url': 'http://images.cocodataset.org/zips/val2017.zip',
                'filename': 'val2017.zip',
                'extract_dir': 'coco_val2017',
                'md5': None,  # Large file, skip MD5 for demo
                'sample_size': 1000  # Only download first 1000 images
            },
            'test_images': {
                'url': 'https://github.com/EliSchwartz/imagenet-sample-images/archive/master.zip',
                'filename': 'imagenet-samples.zip',
                'extract_dir': 'test_images',
                'md5': None
            }
        }

    def calculate_md5(self, filepath):
        """Calculate MD5 hash of a file."""
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def download_with_progress(self, url, filepath):
        """Download file with progress bar."""
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        with open(filepath, 'wb') as f, tqdm(
            desc=f"Downloading {filepath.name}",
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))

    def verify_file(self, filepath, expected_md5):
        """Verify file integrity."""
        if expected_md5 is None:
            return True
        
        actual_md5 = self.calculate_md5(filepath)
        return actual_md5 == expected_md5

    def extract_archive(self, filepath, extract_dir):
        """Extract archive based on file extension."""
        if filepath.suffix == '.zip':
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
        elif filepath.suffix == '.gz':
            with tarfile.open(filepath, 'r:gz') as tar_ref:
                tar_ref.extractall(extract_dir)

    def download_dataset(self, dataset_name):
        """Download and extract a specific dataset."""
        if dataset_name not in self.datasets:
            raise ValueError(f"Unknown dataset: {dataset_name}")
        
        config = self.datasets[dataset_name]
        filepath = self.data_dir / config['filename']
        extract_path = self.data_dir / config['extract_dir']
        
        # Skip if already exists and valid
        if extract_path.exists():
            print(f"Dataset {dataset_name} already exists at {extract_path}")
            return
        
        # Download
        print(f"Downloading {dataset_name}...")
        self.download_with_progress(config['url'], filepath)
        
        # Verify
        if not self.verify_file(filepath, config.get('md5')):
            raise ValueError(f"File verification failed for {dataset_name}")
        
        # Extract
        print(f"Extracting {dataset_name}...")
        self.extract_archive(filepath, extract_path)
        
        # Cleanup
        filepath.unlink()  # Remove archive
        print(f"Dataset {dataset_name} ready at {extract_path}")

    def download_all(self):
        """Download all datasets."""
        for dataset_name in self.datasets:
            try:
                self.download_dataset(dataset_name)
            except Exception as e:
                print(f"Failed to download {dataset_name}: {e}")
                continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download datasets for ML challenge")
    parser.add_argument("--dataset", choices=list(DatasetDownloader({}).datasets.keys()) + ["all"], 
                       default="all", help="Dataset to download")
    parser.add_argument("--data-dir", default="data", help="Data directory")
    
    args = parser.parse_args()
    
    downloader = DatasetDownloader(args.data_dir)
    
    if args.dataset == "all":
        downloader.download_all()
    else:
        downloader.download_dataset(args.dataset)