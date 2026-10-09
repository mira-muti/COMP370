import csv
import os

from bokeh.plotting import figure
from bokeh.models import Select, ColumnDataSource
from bokeh.layouts import column
from bokeh.io import curdoc

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

# month data
x_axis = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def load_data():
    # loads the precomputed monthly averages (from reponse_time.py) into a
    # dictionary: zip -> list of 12 monthly averages. "all" holds the average
    # over every zip. months with no incidents are NaN, so the line shows a gap.
    dataset = {}

    with open(os.path.join(DATA_DIR, "monthly_avg_response.csv"), "r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row["zip"] not in dataset:
                dataset[row["zip"]] = [float("nan")] * 12

            dataset[row["zip"]][x_axis.index(row["month"])] = float(row["avg_response_time"])

    return dataset


data = load_data()
all_avg = data["all"]
zipcodes = sorted(z for z in data if z != "all")

# starting selections (fall back to the first two zips if these aren't in the data)
start1 = "10454" if "10454" in data else zipcodes[0]
start2 = "10580" if "10580" in data else zipcodes[1]

src1 = ColumnDataSource({"mon": x_axis, "zip1": data[start1]})
src2 = ColumnDataSource({"mon": x_axis, "zip2": data[start2]})

# create plot
p = figure(
    title="Monthly Average Response Times",
    x_axis_label="Month (incident closed)",
    y_axis_label="Average Response Time (Hours)",
    height=600,
    width=800,
    x_range=x_axis
)

# add curves for all data, zip 1, and zip 2
p.line(x=x_axis, y=all_avg, color="red", line_width=2, legend_label="2024 data from all zipcodes")
p.line(x="mon", y="zip1", source=src1, color="blue", line_width=2, legend_label="2024 data for zipcode 1")
p.line(x="mon", y="zip2", source=src2, color="green", line_width=2, legend_label="2024 data for zipcode 2")

# dropdowns for zipcode selection
dropdown1 = Select(title="Select zipcode 1:", value=start1, options=zipcodes)
dropdown2 = Select(title="Select zipcode 2:", value=start2, options=zipcodes)


# callbacks to make the dropdowns interactive
def update_graph1(attr, old, new):
    src1.data = {"mon": x_axis, "zip1": data[new]}


def update_graph2(attr, old, new):
    src2.data = {"mon": x_axis, "zip2": data[new]}


dropdown1.on_change("value", update_graph1)
dropdown2.on_change("value", update_graph2)

# column() displays the elements vertically
curdoc().add_root(column(dropdown1, dropdown2, p))
