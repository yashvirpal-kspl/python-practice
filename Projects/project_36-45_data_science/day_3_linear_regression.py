import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

#Load data csv
data = pd.read_csv("experience_salary.csv")

X = data[["YearsExperience"]]
Y = data["Salary"]

model = LinearRegression()
model.fit(X,Y)

data["PredictedSalary"] = model.predict(X)

print("Modal Coefficient (slope)", round(float(model.coef_[0]),2))
print("Modal Intercept (base salarry)", round(float(model.intercept_),2))

plt.scatter(X,Y,color="blue",label="Actual Data")
plt.plot(X,data["PredictedSalary"],color="red",label="Regression line")
plt.xlabel("Years of experience")
plt.ylabel("Salary")
plt.title("Salary vs Experience")
plt.grid(True)
plt.tight_layout()
plt.show()
