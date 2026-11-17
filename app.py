"""
File Manager Studio
--------------------
A polished Streamlit front-end for a Python file-handling CRUD project
(create / read / update / delete text files).

Run locally with:
    pip install streamlit
    streamlit run app.py
"""

from pathlib import Path
from datetime import datetime
import streamlit as st

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------
WORKSPACE = Path("workspace")
WORKSPACE.mkdir(exist_ok=True)

st.set_page_config(
    page_title="File Manager Studio",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------
# Styling
# --------------------------------------------------------------------------
st.markdown(
    """
    <style>
        .main { padding-top: 1rem; }
        .stApp header { background: transparent; }
        .app-title {
            font-size: 2.1rem;
            font-weight: 700;
            margin-bottom: 0;
            letter-spacing: -0.5px;
        }
        .app-subtitle {
            color: #8a8f98;
            font-size: 0.95rem;
            margin-top: 0.15rem;
            margin-bottom: 1.5rem;
        }
        div[data-testid="stMetricValue"] { font-size: 1.4rem; }
        .stButton>button {
            border-radius: 8px;
            font-weight: 600;
        }
        .file-row {
            padding: 0.4rem 0.6rem;
            border-radius: 8px;
        }
        .file-row:hover { background-color: rgba(120,120,120,0.08); }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Helpers (same logic as the original script, adapted to be UI-driven
# and sandboxed to WORKSPACE so the demo is safe to host publicly)
# --------------------------------------------------------------------------
def safe_path(name: str) -> Path:
    """Resolve a user-given filename inside the sandboxed workspace only."""
    candidate = (WORKSPACE / name.strip()).resolve()
    if WORKSPACE.resolve() not in candidate.parents and candidate != WORKSPACE.resolve():
        raise ValueError("Invalid path — files must stay inside the workspace.")
    return candidate


def list_files():
    files = [p for p in WORKSPACE.iterdir() if p.is_file()]
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files


def human_size(num_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if num_bytes < 1024:
            return f"{num_bytes:.0f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} TB"


# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------
st.markdown('<div class="app-title">🗂️ File Manager Studio</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">A Streamlit interface for a Python CRUD file-handling engine '
    '— create, read, update, and delete text files.</div>',
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Sidebar — workspace explorer
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 📁 Workspace")
    files = list_files()
    c1, c2 = st.columns(2)
    c1.metric("Files", len(files))
    c2.metric("Total size", human_size(sum(f.stat().st_size for f in files)) if files else "0 B")

    st.divider()

    if not files:
        st.caption("No files yet — create one from the panel on the right.")
    else:
        for f in files:
            stat = f.stat()
            with st.container():
                st.markdown(f"**📄 {f.name}**")
                st.caption(
                    f"{human_size(stat.st_size)} · "
                    f"{datetime.fromtimestamp(stat.st_mtime):%b %d, %Y %H:%M}"
                )

    st.divider()
    st.caption("All files are sandboxed to a local `workspace/` folder for safe demoing.")

# --------------------------------------------------------------------------
# Main — CRUD tabs
# --------------------------------------------------------------------------
tab_create, tab_read, tab_update, tab_delete = st.tabs(
    ["➕ Create", "📖 Read", "✏️ Update", "🗑️ Delete"]
)

# ---- CREATE ----
with tab_create:
    st.subheader("Create a new file")
    with st.form("create_form", clear_on_submit=True):
        name = st.text_input("File name", placeholder="notes.txt")
        content = st.text_area("Content", height=180, placeholder="Write something...")
        submitted = st.form_submit_button("Create file", type="primary")

    if submitted:
        if not name.strip():
            st.error("Please enter a file name.")
        else:
            try:
                path = safe_path(name)
                if path.exists():
                    st.warning(f"'{path.name}' already exists. Choose a different name or use Update.")
                else:
                    path.write_text(content, encoding="utf-8")
                    st.success(f"'{path.name}' created successfully.")
                    st.rerun()
            except Exception as err:
                st.error(f"An error occurred: {err}")

# ---- READ ----
with tab_read:
    st.subheader("Read a file")
    files = list_files()
    if not files:
        st.info("No files in the workspace yet.")
    else:
        choice = st.selectbox("Choose a file", [f.name for f in files])
        if choice:
            path = safe_path(choice)
            try:
                text = path.read_text(encoding="utf-8")
                st.code(text if text else "(empty file)", language=None)
                st.download_button(
                    "⬇️ Download file",
                    data=text,
                    file_name=path.name,
                    mime="text/plain",
                )
            except Exception as err:
                st.error(f"An error occurred: {err}")

# ---- UPDATE ----
with tab_update:
    st.subheader("Update a file")
    files = list_files()
    if not files:
        st.info("No files in the workspace yet.")
    else:
        choice = st.selectbox("Choose a file", [f.name for f in files], key="update_select")
        operation = st.radio(
            "Operation",
            ["Rename", "Append", "Overwrite"],
            horizontal=True,
        )
        path = safe_path(choice)

        if operation == "Rename":
            new_name = st.text_input("New file name")
            if st.button("Rename", type="primary"):
                try:
                    new_path = safe_path(new_name)
                    if not new_name.strip():
                        st.error("Please enter a new name.")
                    elif new_path.exists():
                        st.warning(f"'{new_path.name}' already exists.")
                    else:
                        path.rename(new_path)
                        st.success(f"Renamed to '{new_path.name}'.")
                        st.rerun()
                except Exception as err:
                    st.error(f"An error occurred: {err}")

        elif operation == "Append":
            addition = st.text_area("Text to append", height=140)
            if st.button("Append", type="primary"):
                try:
                    with open(path, "a", encoding="utf-8") as f:
                        f.write("\n" + addition)
                    st.success(f"Appended to '{path.name}'.")
                except Exception as err:
                    st.error(f"An error occurred: {err}")

        elif operation == "Overwrite":
            current = path.read_text(encoding="utf-8") if path.exists() else ""
            new_content = st.text_area("New content (replaces the file)", value=current, height=180)
            if st.button("Overwrite", type="primary"):
                try:
                    path.write_text(new_content, encoding="utf-8")
                    st.success(f"'{path.name}' overwritten.")
                except Exception as err:
                    st.error(f"An error occurred: {err}")

# ---- DELETE ----
with tab_delete:
    st.subheader("Delete a file")
    files = list_files()
    if not files:
        st.info("No files in the workspace yet.")
    else:
        choice = st.selectbox("Choose a file", [f.name for f in files], key="delete_select")
        st.warning("This action cannot be undone.")
        confirm = st.checkbox(f"I understand, delete '{choice}' permanently.")
        if st.button("Delete file", type="primary", disabled=not confirm):
            try:
                safe_path(choice).unlink()
                st.success(f"'{choice}' deleted.")
                st.rerun()
            except Exception as err:
                st.error(f"An error occurred: {err}")

# --------------------------------------------------------------------------
# Footer
# --------------------------------------------------------------------------
st.divider()
st.caption("Built with Python & Streamlit · File Manager Studio")
