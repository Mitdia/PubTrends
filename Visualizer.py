from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import (ColumnDataSource, FileInput, TextInput, 
                         Button, Div, HoverTool, CategoricalColorMapper)
from bokeh.plotting import figure
from bokeh.palettes import Category20
import base64
import io
import numpy as np

# Import your processing function
from DataAnalyser import process_pmids

# Initialize widgets
file_input = FileInput(title="Upload .txt file with PMIDS", 
                      accept=".txt", 
                      description="PMIDS file")
value_input = TextInput(title="Number of clusters:", value="10")
analyze_button = Button(label="Cluster data", button_type="success", align="end")
status_div = Div(text="<i>Upload a file and enter a value to analyze</i>")

# Initialize data source with extra fields for hover and coloring
source = ColumnDataSource(data={
    't-sne dim 1': [],
    't-sne dim 2': [],
    'label': [],
    'cluster': [],
    'pmids': []
})

# Create plot with hover tool
plot = figure(
    title="Dataset clusters", 
    tools="pan,box_zoom,wheel_zoom,reset,hover",
    tooltips="""
        <div>
            <h3>PMID: @pmids</h3>
            <div><strong>Label:</strong> @label</div>
            <div><strong>Cluster:</strong> @cluster</div>
        </div>
    """
)

# Color mapper for clusters
color_mapper = CategoricalColorMapper(
    palette=Category20[20],
    factors=[]
)

# Add scatter plot with cluster coloring
scatter = plot.scatter(
    x='t-sne dim 1', 
    y='t-sne dim 2', 
    source=source, 
    size=10, 
    alpha=0.7,
    color={'field': 'cluster', 'transform': color_mapper},
    legend_field='cluster'
)

# Configure legend
plot.legend.title = 'Clusters'
plot.legend.label_text_font_size = '8pt'
plot.legend.location = "top_left"

def analyze_data():
    try:
        n_clusters = int(value_input.value)
        
        if not file_input.value:
            status_div.text = "<span style='color:red'>Please upload a file first</span>"
            return
        
        # Process uploaded file
        file_content = base64.b64decode(file_input.value)
        file_bytes = io.BytesIO(file_content)
        pmids = file_bytes.read().decode('utf-8').split()
        
        # Process data (using your imported function)
        labels, clusters, embedded_features, geo_ids = process_pmids(pmids, n_clusters)
        
        # Update color mapper with new cluster factors
        color_mapper.factors = [str(i) for i in np.unique(clusters)]
        
        # Update data source
        source.data = {
            't-sne dim 1': embedded_features[:, 0].tolist(),
            't-sne dim 2': embedded_features[:, 1].tolist(),
            'label': list(labels),
            'cluster': [str(c) for c in clusters],
            'pmids': [", ".join(pl) for pl in geo_ids.values()]
        }
        
        status_div.text = f"<span style='color:green'>Showing {len(labels)} points in {n_clusters} clusters</span>"
        
    except Exception as e:
        status_div.text = f"<span style='color:red'>Error: {str(e)}</span>"

analyze_button.on_click(analyze_data)

# Create layout
layout = column(
    Div(text="<h1>Get GEO datasets relevant to PMIDs</h1>"),
    row(file_input, value_input, analyze_button),
    status_div,
    plot
)

curdoc().add_root(layout)
curdoc().title = "Interactive Cluster Analyzer"