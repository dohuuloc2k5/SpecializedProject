"""Reusable Streamlit UI components for the assistant.

Contains small helper functions to render a sidebar and chat bubbles.
"""
import streamlit as st


def render_sidebar():
	st.sidebar.title("Settings")
	st.sidebar.markdown("Configure environment variables in the .env file before running.")
	if st.sidebar.button("Reload"):
		st.experimental_rerun()


def render_chat_bubble(text: str, sender: str = "user"):
	"""Render a simple chat bubble for user or assistant messages."""
	if sender == "user":
		st.markdown(f"**You:** {text}")
	else:
		st.markdown(f"**Assistant:** {text}")
