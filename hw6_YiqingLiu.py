import pandas as pd

from bokeh.io import show
from pandas import DataFrame

from bokeh.io import export_png
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.models import Title


from bokeh.layouts import gridplot
from bokeh.palettes import GnBu3, OrRd3
from bokeh.palettes import Viridis10
from bokeh.palettes import Plasma10

from bokeh.palettes import Category20c




#Grouped Bar Charts

# import csv file
index=1
df=pd.read_csv('HSall_members.csv')
df = df.rename(columns={'state_abbrev': 'state'})



count_df=df.loc[df['chamber'] == 'House']
count_df=DataFrame({'count': count_df.groupby(["state", "chamber"]).size()}).reset_index()
count_df=count_df.sort_values(by='count',ascending=False)
count_df=count_df[0:10]
state = count_df['state'].tolist()
count = count_df['count'].tolist()
# Bokeh's mapping of column names and data lists
source = ColumnDataSource(data=dict(state=state, count=count, color=Viridis10))
# Bokeh's convenience function for creating a Figure object
p = figure(x_range=state, y_range=(0, 5000), plot_height=350, title="which state has more House Members",
           toolbar_location=None, tools="")
# Render and show the vbar plot
p.vbar(x='state', top='count', width=0.9, color='color', source=source)
# show(p)
export_png(p, filename=str(index)+".png")
index=index+1


count_df=df.loc[df['chamber'] == 'Senate']
count_df=DataFrame({'count': count_df.groupby(["state", "chamber"]).size()}).reset_index()
count_df=count_df.sort_values(by='count',ascending=False)
count_df=count_df[0:10]
state = count_df['state'].tolist()
count = count_df['count'].tolist()
# Bokeh's mapping of column names and data lists
source = ColumnDataSource(data=dict(state=state, count=count, color=Plasma10))
# Bokeh's convenience function for creating a Figure object
p = figure(x_range=state, y_range=(0, 260), plot_height=350, title="which state has more Senate Members",
           toolbar_location=None, tools="")
# Render and show the vbar plot
p.vbar(x='state', top='count', width=0.9, color='color', source=source)
# show(p)
export_png(p, filename=str(index)+".png")
index=index+1



# print(df.dtypes)

# remove alive people 
df=df.loc[df['died'] == df['died']]
# print(df.died .unique())

# remove president
df=df.loc[df['chamber'] != 'President']
# print(df.chamber .unique())
df['age']=df.died-df.born
# print(df.dtypes)


group = df.groupby(by=['state','chamber'])
source = ColumnDataSource(group)

p = figure(plot_width=1500, plot_height=300, title="average age amonge House&Senate",
           x_range=group, toolbar_location=None, tools="")

p.xgrid.grid_line_color = None
p.xaxis.axis_label = "states (House,Senate)"
p.xaxis.major_label_orientation = 1.2
MyPalette=['#2b83ba', '#abdda4', '#9b59b6', '#fdae61', '#d7191c']
MyPalette.extend(MyPalette)
MyPalette.extend(MyPalette)
MyPalette.extend(MyPalette)
MyPalette.extend(MyPalette)
index_cmap = factor_cmap('state_chamber',palette=MyPalette,factors=sorted(df.state.unique()), end=1)

p.vbar(x='state_chamber', top='age_mean', width=1, source=source,
       line_color="white", fill_color=index_cmap, 
       hover_line_color="darkgrey", hover_fill_color=index_cmap)

p.add_tools(HoverTool(tooltips=[("age", "@age_mean"), ("state,chamber", "@state_chamber")]))
export_png(p, filename=str(index)+".png")
index=index+1



#some states
df.state = df.state.astype(str)
state_list = (['IL', 'FL','CA','NY','TX']) 
df=df[df['state'].isin(state_list)]

group = df.groupby(by=['state','chamber'])
source = ColumnDataSource(group)

p = figure(plot_width=600, plot_height=300, title="average age amonge House&Senate",
           x_range=group, toolbar_location=None, tools="")

p.xgrid.grid_line_color = None
p.xaxis.axis_label = "states (House,Senate)"
p.xaxis.major_label_orientation = 1.2

index_cmap = factor_cmap('state_chamber',palette=['#2b83ba', '#abdda4', '#9b59b6', '#fdae61', '#d7191c'],factors=sorted(df.state.unique()), end=1)

p.vbar(x='state_chamber', top='age_mean', width=1, source=source,
       line_color="white", fill_color=index_cmap, 
       hover_line_color="darkgrey", hover_fill_color=index_cmap)

p.add_tools(HoverTool(tooltips=[("age", "@age_mean"), ("state,chamber", "@state_chamber")]))
export_png(p, filename=str(index)+".png")
index=index+1

# grid plot

source_house = ColumnDataSource(data=df.loc[df['chamber'] == 'House'])
source_Senate = ColumnDataSource(data=df.loc[df['chamber']== 'Senate'])
TOOLS = "box_select,lasso_select,help"

# create a new plot and add a renderer
left = figure(tools=TOOLS, width=300, height=300, title="House")
left.circle('age', 'occupancy', line_color="navy", fill_color="orange", fill_alpha=0.5,source=source_house)
left.title.text_font_size = "25px"


# create another new plot and add a renderer
right = figure(tools=TOOLS, width=300, height=300, title="Senate")
right.square('age', 'occupancy',  color="firebrick", alpha=0.6,source=source_Senate)
right.title.text_font_size = "25px"


p = gridplot([[left, right]])
left.add_layout(Title(text="age", align="center"), "below")
right.add_layout(Title(text="age", align="center"), "below")
export_png(p, filename=str(index)+".png")
index=index+1



