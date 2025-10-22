import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
import requests
import matplotlib.pyplot as plt

st.title("AI Alekhah - Draw and Get Equation")

# Canvas
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=3,
    stroke_color="#000000",
    background_color="#FFFFFF",
    height=400,
    width=400,
    drawing_mode="freedraw",
    key="canvas",
)

if canvas_result.image_data is not None:
    # Convert canvas image to x, y coordinates
    img = canvas_result.image_data[:, :, 0]
    y_idxs, x_idxs = np.where(img < 250)  # black pixels
    if len(x_idxs) > 0:
        x_norm = (x_idxs - x_idxs.min()) / (x_idxs.max() - x_idxs.min())
        y_norm = (y_idxs - y_idxs.min()) / (y_idxs.max() - y_idxs.min())

        st.write("Sending points to backend...")
        payload = {"x": x_norm.tolist(), "y": y_norm.tolist()}

        # Call backend
        try:
            response = requests.post("https://YOUR_BACKEND_URL/predict", json=payload)
            if response.status_code == 200:
                data = response.json()
                st.latex(data["equation"])  # display in LaTeX
                plt.plot(data["fitted_x"], data["fitted_y"], color="red")
                plt.scatter(x_norm, y_norm, s=5, color="blue")
                st.pyplot(plt)
            else:
                st.error("Backend error!")
        except Exception as e:
            st.error(f"Request failed: {e}")
