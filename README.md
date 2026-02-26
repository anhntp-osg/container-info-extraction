# Container Info

Analyze container images using Google Gemini AI — automatically detect containers, extract container IDs, and classify container types.

## Features

- Detect whether an image contains a container
- Extract **container ID** from the image
- Classify **container type** (20ft, 40ft, high cube, reefer, dry van, gp, ...)
- Multi-label support: a single container can match multiple types (e.g. `40ft high cube`)
- Skip classification for internal OSG containers — ID only

## Project Structure

```
container_info/
├── src/
│   └── container_info/
│       ├── __init__.py       # Public API
│       ├── models.py         # ContainerInfo dataclass
│       ├── classifier.py     # Container type classification
│       └── analyzer.py       # Gemini API integration
├── .env                      # API key (not committed)
├── .env.example              # Configuration template
├── main.py                   # Entry point
└── requirements.txt
```

## Installation

```bash
pip install -r requirements.txt
```

Copy the environment template and fill in your API key:

```bash
cp .env.example .env
```

```env
# .env
GOOGLE_API_KEY=your_gemini_api_key_here
```

> Get your API key at: https://aistudio.google.com/app/apikey

## Usage

**Run with default image** (path configured in `main.py`):

```bash
python main.py
```

**Pass an image path as an argument:**

```bash
python main.py "path/to/container.jpg"
```

### Sample Output

Standard container:
```
Container detected!
  Container ID   : MSCU1234567
  Type (raw)     : 40ft high cube dry van
  Type (category): ['40ft container', 'high cube container', 'dry van container']
```

OSG container (classification skipped, ID only):
```
Container detected!
  Container ID   : OSG-5410
```

No container found:
```
No container found in the image.
```

## Using as a Library

```python
from dotenv import load_dotenv
load_dotenv()

from src.container_info import analyze_container_image

info = analyze_container_image("path/to/image.jpg")

if info.is_container:
    print(info.container_id)    # "MSCU1234567"
    print(info.container_type)  # ["40ft container", "high cube container"]
    print(info.is_osg)          # False
```

## Adding New Container Types

Edit `DEFAULT_CATEGORY_PATTERNS` in [src/container_info/classifier.py](src/container_info/classifier.py):

```python
"open top container": [
    "open top", "ot container", "open-top",
],
```
