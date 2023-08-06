import collections
from pathlib import Path

import streamlit as st
import utils


def set_up_templates():
    template_dict = collections.defaultdict(dict)
    templates = Path("./webapp/templates").rglob("*.py")
    templates = sorted(templates, key=lambda e: e.name)
    for template in templates:
        try:
            # Templates with task + framework.
            workflow = template.parent.name
            task = template.stem
            template_dict[workflow][task] = template
        except ValueError:
            template_dict[template.name] = template
    return template_dict


def main():
    template_dict = set_up_templates()
    st.set_page_config(layout="wide")
    col1, col2 = st.columns(2)
    with col1:
        st.title("Classy Radiomics")
    with col2:
        st.write(
            """
        ####
        The easiest framework for training models
        using `pyradiomics` and `scikit-learn`.
        """
        )

    with st.sidebar:
        st.write("## Task")
        task = st.selectbox("Select workflow", list(template_dict.keys()))
        if isinstance(template_dict[task], dict):
            framework = st.selectbox(
                "Select task", list(template_dict[task].keys())
            )
            template_path = template_dict[task][framework]
        else:
            template_path = template_dict[task]

    # Show template-specific sidebar components
    # (based on sidebar.py in the template dir).
    template = utils.import_from_file("template", template_path)
    template.show()


if __name__ == "__main__":
    main()
