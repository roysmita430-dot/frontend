# app.py
import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Alekhah AI", layout="wide")

st.title("Alekhah AI: Draw and Get Equation")

# --- Canvas for user input ---
st.write("Draw your shape below (or input points manually):")

# Input points
x_points = st.text_input("X coordinates (comma-separated)", "0,1,2,3,4,5")
y_points = st.text_input("Y coordinates (comma-separated)", "0,1,0,-1,0,1")

try:
    x = [float(v.strip()) for v in x_points.split(",")]
    y = [float(v.strip()) for v in y_points.split(",")]
except:
    st.error("Invalid input. Enter comma-separated numbers.")
    st.stop()

if st.button("Generate Equation"):
    with st.spinner("Processing..."):
        # Send to backend
        try:
            response = requests.post(
                "https://<YOUR_RENDER_BACKEND_URL>/predict",
                json={"x": x, "y": y}
            )
            data = response.json()

            fitted_x = data["fitted_x"]
            fitted_y = data["fitted_y"]
            latex_eq = data["latex_equation"]

            # Plot original points and fitted curve
            plt.figure(figsize=(8,5))
            plt.scatter(x, y, color='red', label='Original Points')
            plt.plot(fitted_x, fitted_y, color='blue', label='Fitted Curve')
            plt.legend()
            plt.xlabel("X")
            plt.ylabel("Y")
            plt.title("Curve Fitting via Alekhah AI")
            st.pyplot(plt.gcf())

            # Show LaTeX equation
            st.markdown("### LaTeX Equation:")
            st.latex(latex_eq)

        except Exception as e:
            st.error(f"Error contacting backend: {e}")
