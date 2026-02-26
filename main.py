import sys
from dotenv import load_dotenv

load_dotenv()

from src.container_info import analyze_container_image
from src.container_info.models import ContainerInfo


def print_result(info: ContainerInfo) -> None:
    if not info.is_container:
        print("No container found in the image.")
        return

    print("Container detected!")
    print(f"  Container ID   : {info.container_id or 'Not visible'}")

    if not info.is_osg:
        print(f"  Type (raw)     : {info.container_type_description or 'Unknown'}")
        print(f"  Type (category): {info.container_type or ['Unclassified']}")


if __name__ == "__main__":
    image_path = sys.argv[1] if len(sys.argv) > 1 else r"E:\OSG\container_info\container_img_test\Selected photo (1).jpg"
    result = analyze_container_image(image_path)
    print_result(result)
