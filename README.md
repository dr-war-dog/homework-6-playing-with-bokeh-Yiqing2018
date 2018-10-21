![](https://ws1.sinaimg.cn/large/006tNbRwly1fvh59oez3dj304t04uaap.jpg)
# Homework 6: EPlaying with Bokeh

|Author|Yiqing Liu|
|---|---
|E-mail|yiqing5@:corn:.edu

### Requirements

I want you to use the data you have to investigate an country's government for corruption, U.N. violations, or maybe they are just a good government. 

- Do not use more dimensions (color, shape, size, etc.) than you need. Having circles appear both larger and darker due to more divisiveness is redundant.
- Convey only relevant information – think of the message your graphic is meant to present; for each piece of information, ask yourself if the graphic would work equally well without!

****

### data source  
scource: Lewis, Jeffrey B., Keith Poole, Howard Rosenthal, Adam Boche, Aaron Rudkin, and Luke Sonnet (2018). Voteview: Congressional Roll-Call Votes Database. [voteview data](https://voteview.com/data)  

****

### data description  
Member Ideology (August 17, 2018) [Quick Link](https://voteview.com/static/data/out/members/HSall_members.csv) (all congresses, all chambers, CSV format)  

The Member Ideology data export contains biographical and ideological information about members of congress for the chamber(s) and congress(es) that were selected.

##### Biographical Fields:

|attribute| explanation
|---|---
|congress|The number of the congress that this member’s row refers to.|
|chamber|House, Senate, or President. The chamber in which the member served.|
|icpsr|an ID code which identifies the member in question|
|state_icpsr|Identifier for the state|
|district_code|Identifier for the district|
|state_abbrev| Two-character postal abbreviation for state|
|party_code|Identifying code for the member’s party|
|occupancy|ICPSR occupancy code.|
|last_means|ICPSR Attain-Office Code.|
|bioname|Name of the member|
|bioguide_id| Member identifier in the Biographical Directory of Congress.|
|born|Year of member’s birth.|
|died|Year of member’s death.|


##### Ideological Fields:

|attribute| explanation
|---|---
|nominate_dim1|reports the first dimension (often interpreted as economic liberalism-conservatism) of members as estimated by NOMINATE.|
|nominate_dim2| NOMINATE second dimension estimate.|
|log_likelihood| Log-likelihood of the NOMINATE estimate.|
|geo_mean_probability| Geometric mean probability of NOMINATE estimate.|
|number_of_votes| Number of votes cast by the member during a given congress.|
|conditional| 1 indicates NOMINATE was estimated conditionally for a given member. 0 otherwise. |
|nokken_poole_dim1| Nokken-Poole First dimension estimate.|
|nokken_poole_dim2| Nokken-Poole Second dimension estimate.|

##### making use of Ideological Data
there are two main estimates of a legislator’s ideology: NOMINATE and Nokken-Poole.  
according to the data scource "We expect that most users of our data will primarily make use of the nominate_dim1 field, which reports the first dimension (often interpreted as economic liberalism-conservatism) of members as estimated by NOMINATE." So, we are more focused on "nominate_dim1" attribute.
****

### Data Preprocessing
##### rename
we can rename some columns for convience :)  

```
df = df.rename(columns={'state_abbrev': 'state'})
```
##### delete row  
There are one tuple with chamber='President', which is kind of "outlier" in our dataset, so we just get rid of it
```
df = df.loc[df['chamber'] != 'President']

```

##### new attribute
for convience, we generate a new column 'age'
```
df['age']=df.died-df.born
```
****  


### Bokeh
#### basical bars
#####  Question: which state has more House/Sentate Members  
here, we use built-in method to calculate the count of House members from each state, sort them. Then use Bokeh to generate graphs.  

```
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
```
![](https://ws3.sinaimg.cn/large/006tNbRwly1fwcabrgb1uj30go09qaa5.jpg)  
![](https://ws2.sinaimg.cn/large/006tNbRwly1fwcac8n2e9j30go09qq31.jpg)

#### Grouped
#####  Question: House/Sentate Members age in each state
When creating bar charts, it is often desirable to visually display the data according to sub-groups. There are two basic methods that can be used, depending on your use case: using nested categorical coordinates, or applying vidual dodges. Here we use nested categorical coordinates!

```
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
```
![](https://ws2.sinaimg.cn/large/006tNbRwly1fwcaj349lpj315o08cmxv.jpg)  
we tak a look at five specific states (Why them? ... because I only know these abbreviations)  

![](https://ws4.sinaimg.cn/large/006tNbRwly1fwcakcqqg2j30go08cdfz.jpg)  

#### grid plot
#####  Question: the relationship between Members age and occupancy  
it's like 60-70 is Golden Age... Probably, I didn't "take alive" members into consideration...  

![](https://ws2.sinaimg.cn/large/006tNbRwly1fwcalil0inj30go096aas.jpg)  
****

