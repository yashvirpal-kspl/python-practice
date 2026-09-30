import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import streamlit as st


data = pd.read_csv("experience_salary.csv")

X = data[["YearsExperience"]]
Y = data["Salary"]

model = LinearRegression()
model.fit(X,Y)

st.title("Salary Predictor based on salery")
st.write("Enter your experiance to predit your salary")

years_input = st.number_input("Year of eexperience",min_value=0.0,max_value=50.0,step=0.1)

if years_input:
    print(years_input)
    
    predicted_salary = model.predict([[years_input]])[0]
    #st.success(f"Estimated Salary: {round(predicted_salary)}")
    st.success(f"Estimated Salary: {predicted_salary}")
    
st.subheader("Regression Line")

fig,ax = plt.subplot()
ax.scatter(X,Y,color="blue",label="Actual Data")
ax.plot(X,model.predict(X ),color="red",label="Regression line")
ax.xlabel("Years of experience")
ax.ylabel("Salary")
ax.title("Salary vs Experience")
ax.grid(True)
ax.tight_layout()
ax.show()    
st.pyplot(fig)