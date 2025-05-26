import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

df = pd.read_csv("covid_policy_tracker.csv")
korea_policy = df[df["countryname"]=="South Korea"]

print(korea_policy.head(10))