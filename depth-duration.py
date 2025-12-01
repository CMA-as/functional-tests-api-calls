
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# User inputs
L = st.slider("Lower Threshold", 40, 90, 70)
U = st.slider("Upper Threshold", 90, 160, 100)
tightening = st.selectbox("Tightening Function", ["Linear", "Exponential", "Logarithmic"])

# Time
T = 60
t = np.linspace(0, T, 300)

# Compute f(t)
if tightening == "Linear":
    f = ((U - L)/2) * t / T
elif tightening == "Exponential":
    f = 15 * (1 - np.exp(-0.05 * t))
else:
    f = 10 * np.log1p(t) / np.log1p(T)

lower = L + f
upper = U - f

# Plot
fig, ax = plt.subplots()
ax.fill_between(t, lower, upper, color='green', alpha=0.3)
ax.set_xlabel("Time (s)")
ax.set_ylabel("HR Range")
st.pyplot(fig)
