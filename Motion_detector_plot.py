from Motion_detector import df
from bokeh.plotting import figure,output_file, show
from bokeh.models import HoverTool , ColumnDataSource


# reformatting the df strings

df["start_string"] = df["start"].dt.strftime("%Y-%m-%d  %H:%m%s")
df["end_string"] = df["end"].dt.strftime("%Y-%m-%d  %H:%m%s")

#converting the dataframe into columns data source
cds = ColumnDataSource(df)


p = figure(x_axis_type = "datetime", width = 500, height = 100 , title ="Motion Detector", responsive = True)
hover = HoverTool(tooltips = [("start","@start_string"),("end","@end_string")])
p.add_tools(hover)

q = p.quad(left = df["start"], right = df["end"], bottom = 0 , top = 1, color = "blue", source = cds)

output_file("final_project.html")
show(p)
