import time

def stream_text(text: str, delay: float = 0.02):
    """
    Simulates a streaming response for the UI by yielding words incrementally.
    This provides a typing effect on the Streamlit interface.
    """
    words = text.split(" ")
    for word in words:
        yield word + " "
        time.sleep(delay)
