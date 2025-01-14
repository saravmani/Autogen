import streamlit as st
import time

def main():
    st.title("Saravana's Streamlit App")

    # Text box
    user_name = st.text_input("Enter your name")

    # Text area
    user_message = st.text_area("Enter your message")

    # Progress bar
    progress_bar = st.progress(0)

    # Button
    if st.button("Submit"):
        # Simulate some work being done
        for i in range(100):
            progress_bar.progress(i + 1)
            time.sleep(0.01)

        # Display the result
        st.write(f"Hello, {user_name}! Your message is: {user_message}")

if __name__ == "__main__":
    main()