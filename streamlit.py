import streamlit as st
st.header("Shapes Calculation App")
st.sidebar.header("Select Shape")
with st.sidebar:
    shape=st.selectbox("'choose shape", ["Circle", "Rectangle",] )
    if shape=="Circle":
     radius=st.number_input('Raduis',min_value=0.0,step=0.1,format="%.2f")
     area=3.14*radius*radius
     ct_btn=st.button("Calculate Area")
     if ct_btn:
        with st.spinner("Calculating..."):
           st.write(f"Area of Circle: {area:.2f}")
    elif shape=="Rectangle":
        length=st.number_input('Length',min_value=0.0,step=0.1,format="%.2f")
        width=st.number_input('Width',min_value=0.0,step=0.1,format="%.2f")
        area=length*width
        rt_btn=st.button("Calculate Area")
        if rt_btn:
           with st.spinner("Calculating..."):
              st.write(f"Area of Rectangle: {area:.2f}")
    
