import os
import shutil

from enum import Enum
from io import BytesIO, StringIO
from typing import Union

import pandas as pd
import streamlit as st

STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""


class FileUpload(object):

    def __init__(self, upload_dir='uploads'):
        self.fileTypes = ["csv", "png", "jpg", "jpeg", "mp4", "webm", "ogg"]
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)

    def run(self):
        """
        Upload File on Streamlit Code
        :return:
        """
        st.info(__doc__)
        st.markdown(STYLE, unsafe_allow_html=True)
        files = st.file_uploader("Upload files", type=self.fileTypes, accept_multiple_files=True)
        if not files:
            st.warning("Please upload a file of type: " + ", ".join(self.fileTypes))
            return
        selected_files = []
        for file in files:
            content = file.getvalue()
            filepath = os.path.join(self.upload_dir, file.name)
            with open(filepath, 'wb') as f:
                f.write(content)
            if file.type.startswith('image/'):
                st.image(file, use_column_width=True)
            elif file.type.startswith('video/'):
                st.video(file)
            elif file.type == 'text/csv':
                data = pd.read_csv(BytesIO(content))
                st.dataframe(data.head(10))
            else:
                st.warning("Unsupported file type: " + file.type)
                continue
            if st.checkbox("Download " + file.name):
                selected_files.append((file, filepath))
        if st.button("Download All"):
            for file, filepath in selected_files:
                if file.type.startswith('image/'):
                    st.image(file, use_column_width=True)
                elif file.type.startswith('video/'):
                    st.video(file)
                elif file.type == 'text/csv':
                    st.download_button(
                        label="Download " + file.name,
                        data=open(filepath, 'rb').read(),
                        file_name=file.name,
                        mime="text/csv"
                    )


if __name__ == "__main__":
    helper = FileUpload()
    helper.run()
