from typing import Dict, List

# Default category patterns used when config doesn't provide them
DEFAULT_CATEGORY_PATTERNS: Dict[str, List[str]] = {
    "20ft container": [
        "20ft", "20 ft", "20ft container", "20 foot", "twenty foot",
        "20' container", "20 feet",
    ],
    "40ft container": [
        "40ft", "40 ft", "40ft container", "40 foot", "forty foot",
        "40' container", "40 feet", "40hc",
    ],
    "reefer container": [
        "reefer", "refrigerated", "cold storage", "temperature controlled",
        "reefer container", "refrigerated container", "cold container",
    ],
    "high cube container": [
        "high cube", "hc", "high-cube", "extra height", "high cube container",
        "hc container", "tall container",
    ],
    "gp container": [
        "gp", "general purpose", "standard container", "gp container",
        "general purpose container",
    ],
    "dry van container": [
        "dry van", "dry container", "cargo container", "dry van container",
        "standard dry", "dry storage",
    ],
}


def classify_container_type(description: str) -> list[str]:
    """Return all matching category names for a given container type description."""
    description_lower = description.lower()
    matched = []
    for category, patterns in DEFAULT_CATEGORY_PATTERNS.items():
        for pattern in patterns:
            if pattern.lower() in description_lower:
                matched.append(category)
                break
    return matched
