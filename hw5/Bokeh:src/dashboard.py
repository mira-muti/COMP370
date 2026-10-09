from bokeh.plotting import figure, show
from bokeh.models import Select, ColumnDataSource
from bokeh.layouts import column
from bokeh.io import curdoc
import os
import pandas as pd

DATA_DIR = os.path.abspath("../data")

def get_zip_data(zip):
    # gets the monthly avg response times for the given zip by reading the corresponding csv data file
    # if zip = 0, then get the monthly avg response times from all zips
    
    if zip:
        file = f"{zip}_mon_avg_reponse.csv"
    else:
        file = "all_mon_avg_reponse.csv"

    data_dir = os.path.abspath("../data")
    path = os.path.join(DATA_DIR, file)
    
    df = pd.read_csv(path)
    
    return df["avg_reponse_time"].tolist()

def load_all_zip_data(zip_list):
    # loads all the zip data from the zip_list into a dictionary
    dataset = {}

    for z in zip_list:
        dataset[z] = get_zip_data(z)

    return dataset
        

# month data
x_axis = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# loading zipcode data -- only a list of 10 zipcodes so the dropdown isn't too long
zip_df = pd.read_csv(os.path.join(DATA_DIR, "selected_zipcodes.csv"))
zipcodes = zip_df["zip"].tolist()

data = load_all_zip_data(zipcodes)
all_avg = get_zip_data(0)

src1 = ColumnDataSource({"mon": x_axis, "zip1": data[10454]})
src2 = ColumnDataSource({"mon": x_axis, "zip2": data[10580]})


# create plot
p = figure(
    title="Monthly Average Reponse Times",
    x_axis_label="Month",
    y_axis_label="Average Reponse Times (Hours)",
    height=600,
    width=800,
    x_range=x_axis
)

# add curves for all data, zip 1, and zip 2
p.line(x=x_axis, y=all_avg, color="red", line_width=2, legend_label="2024 data from all zipcodes")
p.line(x="mon", y="zip1", source=src1, color="blue", line_width=2, legend_label="2024 data for zipcode 1")
p.line(x="mon", y="zip2", source=src2, color="green", line_width=2, legend_label="2024 data for zipcode 2")



# dropdowns for zipcode selection
dropdown1 = Select(
    title="Select zipcode 1:",
    value="10454",
    options=[str(z) for z in zipcodes]
)

dropdown2 = Select(
    title="Select zipcode 2:",
    value="10580",
    options=[str(z) for z in zipcodes]
)

# callbacks to make the dropdowns interactive
def update_graph1(attr, old, new):
    src1.data = {"mon": x_axis, "zip1": data[int(new)]}

def update_graph2(attr, old, new):
    src2.data = {"mon": x_axis, "zip2": data[int(new)]}
    
dropdown1.on_change("value", update_graph1)
dropdown2.on_change("value", update_graph2)

# column() displays the elements vertically
curdoc().add_root(column(dropdown1, dropdown2, p))

