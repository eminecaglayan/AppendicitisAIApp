# app/utils/image_utils.py

def categorize_diameter(value: float) -> str:
    return "yes" if value > 6.0 else "no"
