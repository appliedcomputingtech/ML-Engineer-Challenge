import os
import requests
import zipfile
from torchvision import transforms, datasets
from torch.utils.data import DataLoader

def download_and_extract_tiny_imagenet(url, dataset_path='tiny-imagenet-200'):
    # Define the download path
    download_path = f'{dataset_path}.zip'

    # Download the dataset
    print(f'Downloading {url}...')
    response = requests.get(url, stream=True)
    with open(download_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)
    
    # Extract the dataset
    print(f'Extracting {download_path}...')
    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        zip_ref.extractall(dataset_path)
    
    # Clean up the zip file
    os.remove(download_path)
    print(f'Dataset downloaded and extracted to {dataset_path}')

def get_tiny_imagenet_dataloaders(data_dir, batch_size=32, num_workers=2):
    # Define the transforms for training and validation
    transform_train = transforms.Compose([
        transforms.RandomResizedCrop(64),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.4802, 0.4481, 0.3975], std=[0.2302, 0.2265, 0.2262]),
    ])

    transform_val = transforms.Compose([
        transforms.Resize(64),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.4802, 0.4481, 0.3975], std=[0.2302, 0.2265, 0.2262]),
    ])

    # Load the datasets with ImageFolder
    train_dataset = datasets.ImageFolder(os.path.join(data_dir, 'train'), transform=transform_train)
    val_dataset = datasets.ImageFolder(os.path.join(data_dir, 'val'), transform=transform_val)

    # Create DataLoaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)

    return train_loader, val_loader

# Example usage
if __name__ == "__main__":
    # Download and extract the dataset
    url = 'http://cs231n.stanford.edu/tiny-imagenet-200.zip'
    dataset_path = 'tiny-imagenet-200'
    if not os.path.exists(dataset_path):
        download_and_extract_tiny_imagenet(url, dataset_path)
    
    # Create DataLoaders
    train_loader, val_loader = get_tiny_imagenet_dataloaders(dataset_path, batch_size=32, num_workers=4)
    
    # Print dataset sizes
    print(f'Training set size: {len(train_loader.dataset)}')
    print(f'Validation set size: {len(val_loader.dataset)}')