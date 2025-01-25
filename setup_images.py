import os
import requests
from pathlib import Path

# Create directories
base_dir = Path(__file__).parent
static_dir = base_dir / 'static'
images_dir = static_dir / 'images'

os.makedirs(static_dir, exist_ok=True)
os.makedirs(images_dir, exist_ok=True)

# Sample image URLs (using placeholder images)
image_urls = {
    'rayban-aviator.jpg': 'https://picsum.photos/400/400?random=1',
    'nike-cap.jpg': 'https://picsum.photos/400/400?random=2',
    'laroche-sunscreen.jpg': 'https://picsum.photos/400/400?random=3',
    'adidas-shorts.jpg': 'https://picsum.photos/400/400?random=4',
    'northface-jacket.jpg': 'https://picsum.photos/400/400?random=5',
    'hm-sweater.jpg': 'https://picsum.photos/400/400?random=6',
    'gucci-scarf.jpg': 'https://picsum.photos/400/400?random=7',
    'uniqlo-thermal.jpg': 'https://picsum.photos/400/400?random=8',
    'burberry-umbrella.jpg': 'https://picsum.photos/400/400?random=9',
    'columbia-jacket.jpg': 'https://picsum.photos/400/400?random=10',
    'hunter-boots.jpg': 'https://picsum.photos/400/400?random=11',
    'target-poncho.jpg': 'https://picsum.photos/400/400?random=12',
    'canadagoose-parka.jpg': 'https://picsum.photos/400/400?random=13',
    'timberland-boots.jpg': 'https://picsum.photos/400/400?random=14',
    'northface-snowpants.jpg': 'https://picsum.photos/400/400?random=15',
    'burton-snowboard.jpg': 'https://picsum.photos/400/400?random=16',
    'philips-foglights.jpg': 'https://picsum.photos/400/400?random=17',
    '3m-vest.jpg': 'https://picsum.photos/400/400?random=18',
    'gopro-hero.jpg': 'https://picsum.photos/400/400?random=19',
    'midland-radio.jpg': 'https://picsum.photos/400/400?random=20',
    'anker-powerbank.jpg': 'https://picsum.photos/400/400?random=21',
    'apc-surge.jpg': 'https://picsum.photos/400/400?random=22',
    'iphone13.jpg': 'https://picsum.photos/400/400?random=23',
    'samsung-watch.jpg': 'https://picsum.photos/400/400?random=24',
    'zara-tshirt.jpg': 'https://picsum.photos/400/400?random=25',
    'levis-501.jpg': 'https://picsum.photos/400/400?random=26',
    'nike-airmax.jpg': 'https://picsum.photos/400/400?random=27'
}

# Download images
for filename, url in image_urls.items():
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(images_dir / filename, 'wb') as f:
                f.write(response.content)
            print(f'Downloaded {filename}')
        else:
            print(f'Failed to download {filename}')
    except Exception as e:
        print(f'Error downloading {filename}: {str(e)}')

print('Image setup complete!')
