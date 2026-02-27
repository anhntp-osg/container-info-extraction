import io
import os
import tempfile
from typing import Optional

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from src.container_info import analyze_container_image
from src.container_info.models import ContainerInfo


def render_result(info: ContainerInfo) -> None:
    if not info.is_container:
        st.error("No container found in the image.")
        return

    st.success("Container detected!")

    # Container ID
    st.write("### Core")
    st.write(f"- **Container ID**: `{info.container_id or 'Not visible'}`")

    if getattr(info, "is_osg", False):
        st.info("OSG container detected (details may be handled differently).")
    else:
        st.write("### Type")
        st.write(f"- **Type (raw)**: {info.container_type_description or 'Unknown'}")

        container_type = info.container_type if info.container_type else ["Unclassified"]
        if isinstance(container_type, (list, tuple)):
            st.write(f"- **Type (category)**: {', '.join(map(str, container_type))}")
        else:
            st.write(f"- **Type (category)**: {container_type}")


def analyze_uploaded_image(uploaded_file) -> Optional[ContainerInfo]:
    """Lưu file upload ra temp file để analyze_container_image đọc theo path."""

    suffix = os.path.splitext(uploaded_file.name)[1].lower() or ".jpg"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getbuffer())
        tmp_path = tmp.name

    try:
        return analyze_container_image(tmp_path)
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass


def main():
    st.set_page_config(page_title="Container Info Analyzer", layout="wide")

    st.title("Container Info Analyzer")

    with st.sidebar:
        st.header("Input")
        uploaded = st.file_uploader(
            "Upload container image",
            type=["jpg", "jpeg", "png", "bmp", "webp", "tiff"],
            accept_multiple_files=False,
        )
        # run_btn = st.button("Analyze", type="primary", use_container_width=True)

    col_left, col_right = st.columns([1, 1], gap="large")
    if uploaded is not None:
        with col_left:
            st.subheader("Preview")
            st.image(uploaded, use_container_width=True)

        with col_right:
            st.subheader("Result")
            with st.spinner("Analyzing..."):
                try:
                    info = analyze_uploaded_image(uploaded)
                except Exception as e:
                    st.exception(e)
                    return

            if info is None:
                st.error("Can't read image.")
                return

            render_result(info)



if __name__ == "__main__":
    main()