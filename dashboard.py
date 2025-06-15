import pandas as pd
from dash import dcc, html, Dash, callback, Input, Output
import plotly.express as px
from dash import dash_table
from dash.dash_table.Format import Group



region_mapping = {
        2360: {"region": "New York", "lat": 40.7128, "lon": -74.0060},  # Example: New York
        8670: {"region": "LA", "lat": 34.0522, "lon": -118.2437},  # Example: Los Angeles
        4660: {"region": "Chicago", "lat": 41.8781, "lon": -87.6298},  # Example: Chicago
        2440: {"region": "Houston", "lat": 29.7604, "lon": -95.3698},  # Example: Houston
        4140: {"region": "Atlanta", "lat": 33.7490, "lon": -84.3880},  # Example: Atlanta
        2490: {"region": "Denver", "lat": 39.7392, "lon": -104.9903}, # Example: Denver
        8370: {"region": "Seattle", "lat": 47.6062, "lon": -122.3321}, # Example: Seattle
    }
main_df = pd.read_csv(r"C:\Users\ARDA\Desktop\final_df.csv")

variables = ['customer_age', 'vendor_count', 'product_count', 'total_spend', 'total_orders', 'average_order_revenue']

app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(
        html.H1(
            "ABCDEats Customer Segmentation Dashboard",
            className="text-center",
            style={
                "font-size": "36px",
                "color": "#FF7F50",  
                "margin": "20px 0",
                "text-shadow": "2px 2px 4px rgba(0, 0, 0, 0.4)", 
                "font-family": "'Arial', sans-serif",
                "text-align": "center", 
            },
        ),
        style={
            "background-color": "#f9f9f9",
            "padding": "20px",
            "border-radius": "8px",
            "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.2)"
        }
    ),

    # Tabs
    dcc.Tabs([
        # Overview Tab
        dcc.Tab(label="Overview", children=[
            # KPI Cards
            html.Div([
                html.Div([
                    html.H4("Total Product Count:", className="card-title", style={"font-size": "28px", "color": "orange", "font-weight": "bold"}),
                    html.P(id="total-product-count", className="card-text", style={"font-size": "28px", "font-weight": "bold"}),
                ], className="card bg-light mb-3", style={"padding": "10px", "margin": "10px"}),
                html.Div([
                    html.H4("Total Spend:", className="card-title", style={"font-size": "28px", "color": "orange", "font-weight": "bold"}),
                    html.P(id="total-spend", className="card-text", style={"font-size": "28px", "font-weight": "bold"}),
                ], className="card bg-light mb-3", style={"padding": "10px", "margin": "10px"}),
                html.Div([
                    html.H4("Total Orders:", className="card-title", style={"font-size": "28px", "color": "orange", "font-weight": "bold"}),
                    html.P(id="total-orders", className="card-text", style={"font-size": "28px", "font-weight": "bold"}),
                ], className="card bg-light mb-3", style={"padding": "10px", "margin": "10px"}),
            ], style={"display": "flex", "justify-content": "space-around"}),

            # Dropdowns Below KPI Cards
            html.Div([
                html.Label("Select Cluster:"),
                dcc.Dropdown(
                    id='cluster-dropdown',
                    options=[{'label': str(c), 'value': c} for c in main_df['cluster_som'].unique()],
                    placeholder="Select a cluster",
                ),
                html.Label("Select Variable:"),
                dcc.Dropdown(
                    id='variable-dropdown',
                    options=[{'label': v, 'value': v} for v in variables],
                    value='customer_age',  # We added default variable not to show empty graph
                    placeholder="Select a variable",
                ),
            ], style={'width': '50%', 'margin': '20px auto'}),  

            # US Map and Regional Summary Table Side by Side
            html.Div([
                dcc.Graph(id='customer-region-map', style={"height": "600px", "width": "48%", "display": "inline-block"}),  # US Map
                html.Div(id='regional-summary-table', style={"height": "600px", "width": "48%", "display": "inline-block", "overflow-y": "auto", "padding": "10px"}),  # Regional Table
            ], style={"display": "flex", "justify-content": "space-between", "margin-top": "20px"}),

            # Additional Charts Side by Side
            html.Div([
                dcc.Graph(id='cluster-bar-chart', style={"width": "48%", "display": "inline-block"}),  # Cluster Bar Chart
                dcc.Graph(id='bubble-chart', style={"width": "48%", "display": "inline-block"}),  # Bubble Chart
            ], style={"display": "flex", "justify-content": "space-between", "margin-top": "20px"}),  # Side-by-Side Charts
        ]),

        # Cluster Analysis Tab
        dcc.Tab(label="Distributions of Clusters", children=[
            # Dropdowns Below Tab Buttons
            html.Div([
                html.Label("Select Cluster:"),
                dcc.Dropdown(
                    id='cluster-dropdown-analysis',
                    options=[{'label': str(c), 'value': c} for c in main_df['cluster_som'].unique()],
                    placeholder="Select a cluster",
                ),
                html.Label("Select Variable:"),
                dcc.Dropdown(
                    id='variable-dropdown-analysis',
                    options=[{'label': v, 'value': v} for v in variables],
                    value='customer_age',  # Default variable is customer_age
                    placeholder="Select a variable",
                ),
            ], style={'width': '50%', 'margin': '20px auto'}),  # Dropdown Filters

            # Side-by-Side Charts
            html.Div([
                html.Div([
                    dcc.Graph(id='boxplot-chart', style={'width': '48%', 'display': 'inline-block'}),
                    dcc.Graph(id='distribution-chart', style={'width': '48%', 'display': 'inline-block'}),
                ], style={'display': 'flex', 'justify-content': 'space-between'}),  # Side-by-Side Charts

                html.Div([
                    dcc.Graph(id='violin-chart', style={'width': '48%', 'display': 'inline-block'}),
                    dcc.Graph(id='correlation-heatmap', style={'width': '48%', 'display': 'inline-block'}),
                ], style={'display': 'flex', 'justify-content': 'space-between', "margin-top": "20px"}),  # Side-by-Side New Charts
            ]),
        ]),

        # Regional Analysis Tab
        dcc.Tab(label="Regional Analysis", children=[
            # Dropdown for Regional Analysis
            html.Div([
                html.Label("Select Cluster:"),
                dcc.Dropdown(
                    id='cluster-dropdown-regional',
                    options=[{'label': str(c), 'value': c} for c in main_df['cluster_som'].unique()],
                    placeholder="Select a cluster",
                ),
            ], style={'width': '50%', 'margin': '20px auto'}),  # Dropdown Filters

            # US Map and Donut Chart Side by Side
            html.Div([
                dcc.Graph(id='us-density-map', style={"width": "48%", "display": "inline-block"}),  # US Map
                dcc.Graph(id='regional-donut-chart', style={"width": "48%", "display": "inline-block"}),  # Donut Chart
            ], style={"display": "flex", "justify-content": "space-between", "margin-top": "20px"}),  # Side-by-Side Layout
        ]),

       # Fourth Tab (Last Promo Analysis Tab)
        dcc.Tab(label="Customer Behavior Insights", children=[
            # Dropdown for Last Promo Tab
            html.Div([
                html.Label("Select Cluster:"),
                dcc.Dropdown(
                    id='cluster-dropdown-last-promo',
                    options=[{'label': str(c), 'value': c} for c in main_df['cluster_som'].unique()],
                    placeholder="Select a cluster",
                ),
            ], style={'width': '50%', 'margin': '20px auto'}),  # Dropdown Filters

            # Table and Pie Chart Side by Side
            html.Div([
                html.Div(
                    id='last-promo-table',
                    style={
                        "width": "48%", "display": "inline-block", "padding": "10px", 
                        "height": "600px", "overflowY": "auto", "border": "1px solid #ccc"
                    },
                ),  # Last Promo Table
                dcc.Graph(
                    id='last-promo-pie-chart',
                    style={
                        "width": "48%", "display": "inline-block", "height": "600px"
                    },
                ),  # Last Promo Pie Chart
            ], style={"display": "flex", "justify-content": "space-between", "margin-top": "20px"}),

            # Payment Method Table and Bar Chart Side by Side
            html.Div([
                html.Div(
                    id='payment-method-table',
                    style={
                        "width": "48%", "display": "inline-block", "padding": "10px", 
                        "height": "600px", "overflowY": "auto", "border": "1px solid #ccc"
                    },
                ),  # Payment Method Table
                dcc.Graph(
                    id='payment-method-bar-chart',
                    style={
                        "width": "48%", "display": "inline-block", "height": "600px"
                    },
                ),  # Payment Method Bar Chart
            ], style={"display": "flex", "justify-content": "space-between", "margin-top": "20px"}),
              
# Hour Table and Donut Chart Side by Side
            html.Div([
                html.Div(
                    id='hour-table',
                    style={
                        "width": "48%", "display": "inline-block", "padding": "10px",
                        "height": "600px", "overflowY": "auto", "border": "1px solid #ccc"
                    },
                ),  # Hour Table
                dcc.Graph(
                    id='hour-donut-chart',
                    style={
                        "width": "48%", "display": "inline-block", "height": "600px"
                    },
                ),  # Hour Donut Chart
            ], style={"display": "flex", "justify-content": "space-between", "margin-top": "20px"}),  # Hour Section
            html.Div([
                html.Div(
                    id='day-table',
                    style={
                        "width": "48%", "display": "inline-block", "padding": "10px",
                        "height": "600px", "overflowY": "auto", "border": "1px solid #ccc"
                    },
                ),  # Day Table
                dcc.Graph(
                    id='day-donut-chart',
                    style={
                        "width": "48%", "display": "inline-block", "height": "600px"
                    },
                ),  # Day Donut Chart
            ], style={"display": "flex", "justify-content": "space-between", "margin-top": "20px"}),
        ]),
        # Fifth Tab (Cuisine Analysis Tab)
        dcc.Tab(label="Cuisine Analysis", children=[
                    # Dropdown for Cuisine Analysis
            html.Div([
                html.Label("Select Cluster:"),
                dcc.Dropdown(
                    id='cluster-dropdown-cuisine',
                    options=[{'label': str(c), 'value': c} for c in main_df['cluster_som'].unique()],
                    placeholder="Select a cluster",
                ),
            ], style={'width': '50%', 'margin': '20px auto'}),  # Dropdown Filter
            # Favorite Cuisines Table
            html.Div(
                id='favorite-cuisines-table-cuisine',
                style={
                    "width": "100%", "padding": "10px", "margin-top": "20px",
                    "border": "1px solid #ccc", "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.1)"
                }
            ),  # Favorite Cuisines Tabl
            # Top 3 Favorite Cuisines Table
            html.Div(
                id='top-3-cuisines-table-cuisine',
                style={
                    "width": "100%", "padding": "10px", "margin-top": "20px",
                    "border": "1px solid #ccc", "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.1)"
                }
            ), # Top 3 Favorite Cuisines Table
            html.Div([
                            dcc.Graph(
                                id='funnel-chart',
                                style={"width": "48%", "display": "inline-block", "height": "600px"}
                            ),  # Funnel Chart
                            dcc.Graph(
                                id='pyramid-chart',
                                style={"width": "48%", "display": "inline-block", "height": "600px"}
                            ),  # Pyramid Chart
                        ], style={"display": "flex", "justify-content": "space-between", "margin-top": "20px"}
                        
            ),
         ]),
     ]),
 ])





# Callback to update the bar chart
@callback(
    Output('cluster-bar-chart', 'figure'),
    [Input('cluster-dropdown', 'value'),
     Input('variable-dropdown', 'value')]
)
def update_bar_chart(selected_cluster, selected_variable):
    """
    Update the bar chart based on the selected cluster and variable.
    """
    
    grouped_df = main_df.groupby('cluster_som')[variables].mean().reset_index()
    
    
    if selected_cluster and selected_variable:
        filtered_df = grouped_df[grouped_df['cluster_som'] == selected_cluster]
        fig = px.bar(
            filtered_df,
            x='cluster_som',
            y=selected_variable,
            title=f"Mean {selected_variable} for Cluster {selected_cluster}",
            text_auto=True
        )
    elif selected_cluster:
        filtered_df = grouped_df[grouped_df['cluster_som'] == selected_cluster].melt(
            id_vars='cluster_som', value_vars=variables)
        fig = px.bar(
            filtered_df,
            x='variable',
            y='value',
            title=f"Mean Values for All Variables in Cluster {selected_cluster}",
            text_auto=True
        )
    elif selected_variable:
        filtered_df = grouped_df[['cluster_som', selected_variable]]
        fig = px.bar(
            filtered_df,
            x='cluster_som',
            y=selected_variable,
            title=f"Mean {selected_variable} Across All Clusters",
            text_auto=True
        )
    else:
        melted_df = grouped_df.melt(id_vars='cluster_som', value_vars=variables)
        fig = px.bar(
            melted_df,
            x='cluster_som',
            y='value',
            color='variable',
            title="Mean Values for All Clusters and Variables",
            barmode='group'
        )
    
    fig.update_layout(paper_bgcolor="#f9f9f9", height=600)
    return fig


@callback(
    Output('bubble-chart', 'figure'),
    [Input('cluster-dropdown', 'value')]
)
def update_bubble_chart(selected_cluster):
    """
    Update the bubble chart based on the selected cluster or show all clusters.
    """
    
    grouped_df = main_df.groupby('cluster_som')['total_spend'].sum().reset_index()
    
    
    if selected_cluster:
        grouped_df = grouped_df[grouped_df['cluster_som'] == selected_cluster]

    
    fig = px.scatter(
        grouped_df,
        x='cluster_som',
        y='total_spend',
        size='total_spend',
        color='cluster_som',
        title="Bubble Chart of Total Spend by Cluster",
        labels={'cluster_som': 'Cluster', 'total_spend': 'Total Spend'},
    )
    
    fig.update_xaxes(tickmode='linear', tick0=0, dtick=1)
    fig.update_layout(paper_bgcolor="#f9f9f9", height=600)
    return fig


@callback(
    Output('distribution-chart', 'figure'),
    [Input('cluster-dropdown', 'value'),
     Input('variable-dropdown', 'value')]
)

def update_density_chart(selected_cluster, selected_variable):
    """
    Update the density chart to show only histograms for the selected cluster and variable.
    """
    
    filtered_df = main_df if not selected_cluster else main_df[main_df['cluster_som'] == selected_cluster]
    
    
    if not selected_variable:
        return px.histogram(title="Please select a variable to view its distribution.")
    
    
    fig = px.histogram(
        filtered_df,
        x=selected_variable,
        color='cluster_som',
        barmode='overlay',  # Overlap the bars for all clusters
        title=f"Histogram of {selected_variable}" + (f" in Cluster {selected_cluster}" if selected_cluster else ""),
        labels={'cluster_som': 'Cluster', selected_variable: 'Value'},
    )
    
    
    fig.update_layout(
        paper_bgcolor="#f9f9f9",
        height=600,
        xaxis_title=selected_variable,
        yaxis_title="Count",
    )
    return fig

# Callback to update the boxplot chart
@callback(
    Output('boxplot-chart', 'figure'),
    [Input('cluster-dropdown', 'value'),
     Input('variable-dropdown', 'value')]
)
def update_boxplot_chart(selected_cluster, selected_variable):
    """
    Update the boxplot chart based on the selected cluster and variable.
    """
    
    filtered_df = main_df if not selected_cluster else main_df[main_df['cluster_som'] == selected_cluster]
    
    
    fig = px.box(
        filtered_df,
        x='cluster_som',
        y=selected_variable,
        color='cluster_som',
        title=f"Box Plot of {selected_variable}" + (f" in Cluster {selected_cluster}" if selected_cluster else " by Cluster"),
        labels={'cluster_som': 'Cluster', selected_variable: 'Value'}
    )
    
    
    fig.update_layout(
        paper_bgcolor="#f9f9f9",
        height=600,
        xaxis_title="Cluster",
        yaxis_title=selected_variable,
    )
    return fig

@callback(
    Output('violin-chart', 'figure'),
    [Input('cluster-dropdown', 'value'),
     Input('variable-dropdown', 'value')]
)
def update_violin_chart(selected_cluster, selected_variable):
    """
    Update the violin chart based on the selected cluster and variable.
    """
    
    filtered_df = main_df if not selected_cluster else main_df[main_df['cluster_som'] == selected_cluster]
    
    
    fig = px.violin(
        filtered_df,
        x='cluster_som',
        y=selected_variable,
        color='cluster_som',
        box=False,  # Hide the box plot
        points='all',  
        title=f"Violin Plot of {selected_variable}" + (f" in Cluster {selected_cluster}" if selected_cluster else " by Cluster"),
        labels={'cluster_som': 'Cluster', selected_variable: 'Value'}
    )
    
    
    fig.update_layout(
        paper_bgcolor="#f9f9f9",
        height=600,
        xaxis_title="Cluster",
        yaxis_title=selected_variable,
    )
    return fig

@callback(
    Output('correlation-heatmap', 'figure'),
    [Input('cluster-dropdown', 'value')]
)
def update_correlation_heatmap(selected_cluster):
    """
    Update the correlation heatmap based on the selected cluster.
    """
    
    filtered_df = main_df if not selected_cluster else main_df[main_df['cluster_som'] == selected_cluster]

    
    correlation_matrix = filtered_df[variables].corr()

   
    fig = px.imshow(
        correlation_matrix,
        text_auto=True,  # Show correlation values on heatmap
        color_continuous_scale="Viridis",
        title=f"Correlation Heatmap" + (f" for Cluster {selected_cluster}" if selected_cluster else ""),
        labels=dict(color="Correlation"),
    )

   
    fig.update_layout(
        paper_bgcolor="#f9f9f9",
        height=600,
        xaxis_title="Variables",
        yaxis_title="Variables",
    )
    return fig



# Callback to update KPI values
@callback(
    [Output('total-product-count', 'children'),
     Output('total-spend', 'children'),
     Output('total-orders', 'children')],
    [Input('cluster-dropdown', 'value')]
)
def update_kpis(selected_cluster):
    """
    Update the KPI values based on the selected cluster.
    """
    
    filtered_df = main_df if not selected_cluster else main_df[main_df['cluster_som'] == selected_cluster]
    
    
    total_product_count = filtered_df['product_count'].sum()
    total_spend = filtered_df['total_spend'].sum()
    total_orders = filtered_df['total_orders'].sum()
    
    
    return (f"{total_product_count:,}", f"${total_spend:,.2f}", f"{total_orders:,}")


@callback(
    Output('customer-region-map', 'figure'),
    [Input('cluster-dropdown', 'value')]
)

def update_region_map(selected_cluster):
    """
    Update the customer region map based on the selected cluster.
    """
    
    map_df = main_df.copy()

    
    map_df = map_df[map_df['customer_region'] != '-']

    
    map_df['region_name'] = map_df['customer_region'].map(lambda x: region_mapping.get(int(x), {}).get("region"))
    map_df['latitude'] = map_df['customer_region'].map(lambda x: region_mapping.get(int(x), {}).get("lat"))
    map_df['longitude'] = map_df['customer_region'].map(lambda x: region_mapping.get(int(x), {}).get("lon"))

    
    map_df = map_df.dropna(subset=['latitude', 'longitude'])

    
    if selected_cluster:
        map_df = map_df[map_df['cluster_som'] == selected_cluster]

    
    fig = px.scatter_geo(
        map_df,
        lat='latitude',
        lon='longitude',
        text='region_name',  
        title="US Customer Regions",
        scope="usa",  
        color="cluster_som",
        labels={'cluster_som': 'Cluster'}
    )

    
    fig.update_layout(
        paper_bgcolor="#f9f9f9",
        height=600,
        margin={"r": 0, "t": 50, "l": 0, "b": 0}
    )

    return fig

@callback(
    Output('regional-summary-table', 'children'),
    [Input('cluster-dropdown', 'value')]
)
def update_regional_summary(selected_cluster):
    """
    Generate a summary table showing regional total spend and total orders.
    """
    
    summary_df = main_df.copy()

    
    summary_df = summary_df[summary_df['customer_region'] != '-']

    
    summary_df['region_name'] = summary_df['customer_region'].map(lambda x: region_mapping.get(int(x), {}).get("region"))

    
    if selected_cluster:
        summary_df = summary_df[summary_df['cluster_som'] == selected_cluster]

    
    region_summary = summary_df.groupby('region_name').agg(
        total_spend=('total_spend', 'sum'),
        total_orders=('total_orders', 'sum')
    ).reset_index()

    
    return dash_table.DataTable(
        data=region_summary.to_dict('records'),
        columns=[
            {'name': 'Region', 'id': 'region_name'},
            {'name': 'Total Spend', 'id': 'total_spend', 'type': 'numeric', 'format': {'specifier': ',.2f'}},
            {'name': 'Total Orders', 'id': 'total_orders', 'type': 'numeric', 'format': {'specifier': ',d'}}
        ],
        style_table={'height': '500px', 'overflowY': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '10px'},
        style_header={'backgroundColor': '#f9f9f9', 'fontWeight': 'bold'},
        style_data_conditional=[
            {'if': {'column_id': 'total_spend'}, 'color': 'blue'},
            {'if': {'column_id': 'total_orders'}, 'color': 'green'},
        ],
    )

@callback(
    Output('regional-donut-chart', 'figure'),
    [Input('cluster-dropdown-regional', 'value')]
)
def update_donut_chart(selected_cluster):
    """
    Update the donut chart showing the distribution of customers by region.
    """
    
    map_df = main_df.copy()

    
    map_df = map_df[map_df['customer_region'] != '-']

    
    filtered_df = map_df if not selected_cluster else map_df[map_df['cluster_som'] == selected_cluster]

    
    regional_counts = filtered_df.groupby('customer_region').size().reset_index(name='customer_count')

    
    region_mapping = {
        2360: {"region": "New York", "lat": 40.7128, "lon": -74.0060},
        8670: {"region": "LA", "lat": 34.0522, "lon": -118.2437},
        4660: {"region": "Chicago", "lat": 41.8781, "lon": -87.6298},
        2440: {"region": "Houston", "lat": 29.7604, "lon": -95.3698},
        4140: {"region": "Atlanta", "lat": 33.7490, "lon": -84.3880},
        2490: {"region": "Denver", "lat": 39.7392, "lon": -104.9903},
        8370: {"region": "Seattle", "lat": 47.6062, "lon": -122.3321},
    }
    
    regional_counts['region_name'] = regional_counts['customer_region'].map(
        lambda x: region_mapping.get(int(x), {}).get("region", "Unknown") if x.isdigit() else "Unknown"
    )

    
    fig = px.pie(
        regional_counts,
        names='region_name',
        values='customer_count',
        title="Customer Distribution by Region",
        hole=0.4,  
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    
    fig.update_layout(
        paper_bgcolor="#f9f9f9",
        height=600,
    )

    return fig

@callback(
    Output('us-density-map', 'figure'),
    [Input('cluster-dropdown-regional', 'value')]
)
def update_us_density_map(selected_cluster):
    """
    Update the US map with density by customer count, based on the selected cluster.
    """
    
    map_df = main_df.copy()

    
    map_df = map_df[map_df['customer_region'] != '-']

    

    map_df['region_name'] = map_df['customer_region'].map(lambda x: region_mapping.get(int(x), {}).get("region"))
    map_df['latitude'] = map_df['customer_region'].map(lambda x: region_mapping.get(int(x), {}).get("lat"))
    map_df['longitude'] = map_df['customer_region'].map(lambda x: region_mapping.get(int(x), {}).get("lon"))

    
    map_df = map_df.dropna(subset=['latitude', 'longitude'])

    
    if selected_cluster:
        map_df = map_df[map_df['cluster_som'] == selected_cluster]

    
    density_df = map_df.groupby(['region_name', 'latitude', 'longitude']).size().reset_index(name='customer_count')

    
    fig = px.scatter_geo(
        density_df,
        lat='latitude',
        lon='longitude',
        size='customer_count',
        color='customer_count',
        text='region_name',  # Display region names on hover
        title="Customer Density by Region",
        scope='usa',
        color_continuous_scale="Greens",
        labels={'customer_count': 'Customer Count'}
    )

    
    fig.update_layout(
        paper_bgcolor="#f9f9f9",
        height=600,
        margin={"r": 0, "t": 50, "l": 0, "b": 0}
    )

    return fig


@callback(
    Output('last-promo-table', 'children'),
    [Input('cluster-dropdown-last-promo', 'value')]
)
def update_last_promo_table(selected_cluster):
    """
    Update the table showing last_promo usage by cluster.
    """
    
    filtered_df = main_df if not selected_cluster else main_df[main_df['cluster_som'] == selected_cluster]

    
    promo_counts = filtered_df.groupby('last_promo').size().reset_index(name='usage_count')

    
    table = dash_table.DataTable(
        columns=[{"name": col, "id": col} for col in promo_counts.columns],
        data=promo_counts.to_dict('records'),
        style_table={'overflowX': 'auto',
                     'width': '100%',
                     'height': '600px',
                    },
        style_cell={'textAlign': 'center', 'padding': '10px'},
        style_header={'backgroundColor': '#f9f9f9', 'fontWeight': 'bold'},
        style_as_list_view=True
    )
    return table


@callback(
    Output('last-promo-pie-chart', 'figure'),
    [Input('cluster-dropdown-last-promo', 'value')]
)
def update_last_promo_pie_chart(selected_cluster):
    """
    Update the pie chart showing last_promo usage by cluster.
    """
    
    filtered_df = main_df if not selected_cluster else main_df[main_df['cluster_som'] == selected_cluster]

    
    promo_counts = filtered_df.groupby('last_promo').size().reset_index(name='usage_count')

    
    fig = px.pie(
        promo_counts,
        names='last_promo',
        values='usage_count',
        title="Last Promo Usage Distribution",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    
    fig.update_layout(
        paper_bgcolor="#f9f9f9",
        height=600,
    )
    return fig

@callback(
    Output('payment-method-table', 'children'),
    [Input('cluster-dropdown-last-promo', 'value')]
)
def update_payment_method_table(selected_cluster):
    """
    Update the table showing payment method usage by cluster.
    """
    
    filtered_df = main_df if not selected_cluster else main_df[main_df['cluster_som'] == selected_cluster]

    
    payment_counts = filtered_df.groupby('payment_method').size().reset_index(name='usage_count')

    # Create a Dash DataTable
    table = dash_table.DataTable(
        columns=[{"name": col, "id": col} for col in payment_counts.columns],
        data=payment_counts.to_dict('records'),
        style_table={
            'overflowX': 'auto',
            'height': '600px',  
        },
        style_cell={'textAlign': 'center', 'padding': '10px'},
        style_header={'backgroundColor': '#f9f9f9', 'fontWeight': 'bold'},
        style_as_list_view=True
    )
    return table

@callback(
    Output('payment-method-bar-chart', 'figure'),
    [Input('cluster-dropdown-last-promo', 'value')]
)
def update_payment_method_bar_chart(selected_cluster):
    """
    Update the bar chart showing payment method usage by cluster.
    """
    
    filtered_df = main_df if not selected_cluster else main_df[main_df['cluster_som'] == selected_cluster]

    
    payment_counts = filtered_df.groupby('payment_method').size().reset_index(name='usage_count')

    
    fig = px.bar(
        payment_counts,
        x='payment_method',
        y='usage_count',
        title="Payment Method Usage",
        color_discrete_sequence=['purple']  
    )

    
    fig.update_layout(
        paper_bgcolor="#f9f9f9",
        height=600,
        xaxis_title="Payment Method",
        yaxis_title="Usage Count",
    )

    return fig

@callback(
    Output('hour-table', 'children'),
    [Input('cluster-dropdown-last-promo', 'value')]
)
def update_hour_table(selected_cluster):
    """
    Update the Hour Table based on the selected cluster.
    """
    
    filtered_df = main_df if not selected_cluster else main_df[main_df['cluster_som'] == selected_cluster]

    
    hour_counts = filtered_df['hour'].value_counts().reset_index()
    hour_counts.columns = ['hour', 'usage_count']

    
    hour_counts = hour_counts.sort_values(by='hour')

    
    table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in hour_counts.columns],
        data=hour_counts.to_dict('records'),
        style_table={"height": "600px", "overflowY": "auto"},
        style_cell={"textAlign": "center", "padding": "10px"},
        style_header={"fontWeight": "bold", "border": "1px solid black"},
    )

    return table

@callback(
    Output('hour-donut-chart', 'figure'),
    [Input('cluster-dropdown-last-promo', 'value')]
)
def update_hour_donut_chart(selected_cluster):
    """
    Update the Hour Donut Chart based on the selected cluster.
    """
    
    filtered_df = main_df if not selected_cluster else main_df[main_df['cluster_som'] == selected_cluster]

    
    hour_counts = filtered_df['hour'].value_counts().reset_index()
    hour_counts.columns = ['hour', 'usage_count']

    
    fig = px.pie(
        hour_counts,
        names='hour',
        values='usage_count',
        title="Hourly Usage Distribution",
        hole=0.4,  # Donut chart
        color_discrete_sequence=px.colors.qualitative.Pastel  # Soft pastel colors
    )

    
    fig.update_layout(
        paper_bgcolor="#f9f9f9",
        height=600,
    )

    return fig


@callback(
    Output('day-table', 'children'),
    [Input('cluster-dropdown-last-promo', 'value')]
)
def update_day_table(selected_cluster):
    """
    Update the Day Table based on the selected cluster.
    """
    
    filtered_df = main_df if not selected_cluster else main_df[main_df['cluster_som'] == selected_cluster]

    
    day_counts = filtered_df['day'].value_counts().reset_index()
    day_counts.columns = ['day', 'usage_count']

    
    table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in day_counts.columns],
        data=day_counts.to_dict('records'),
        style_table={"height": "600px", "overflowY": "auto"},
        style_cell={"textAlign": "center", "padding": "10px"},
        style_header={"fontWeight": "bold", "border": "1px solid black"},
    )

    return table


@callback(
    Output('day-donut-chart', 'figure'),
    [Input('cluster-dropdown-last-promo', 'value')]
)
def update_day_donut_chart(selected_cluster):
    """
    Update the Day Donut Chart based on the selected cluster.
    """
    
    filtered_df = main_df if not selected_cluster else main_df[main_df['cluster_som'] == selected_cluster]

   
    day_counts = filtered_df['day'].value_counts().reset_index()
    day_counts.columns = ['day', 'usage_count']

    
    fig = px.pie(
        day_counts,
        names='day',
        values='usage_count',
        title="Daily Usage Distribution",
        hole=0.4,  # Donut chart
        color_discrete_sequence=px.colors.qualitative.Set3  # Diverse color set
    )

   
    fig.update_layout(
        paper_bgcolor="#f9f9f9",
        height=600,
    )

    return fig

@callback(
    Output('favorite-cuisines-table-cuisine', 'children'),
    [Input('cluster-dropdown-cuisine', 'value')]
)
def update_favorite_cuisines_table(selected_cluster):
    """
    Update the Favorite Cuisines Table based on the selected cluster.
    """
    
    cui_columns = [col for col in main_df.columns if col.startswith("CUI_")]

   
    if not cui_columns:
        return html.P("No cuisine data available.", style={"textAlign": "center", "color": "red"})

    
    cui_percentages_by_cluster = main_df.groupby("cluster_som")[cui_columns].mean() * 100
    cui_percentages_by_cluster = cui_percentages_by_cluster.round(2)

    
    if selected_cluster:
        cui_percentages_by_cluster = cui_percentages_by_cluster.loc[[selected_cluster]]

    
    cui_percentages_by_cluster = cui_percentages_by_cluster.reset_index()

    
    table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in cui_percentages_by_cluster.columns],
        data=cui_percentages_by_cluster.to_dict('records'),
        style_table={"height": "200px", "overflowY": "auto"},
        style_cell={"textAlign": "center", "padding": "10px"},
        style_header={"fontWeight": "bold", "border": "1px solid black"},
    )

    return table

@callback(
    Output('top-3-cuisines-table-cuisine', 'children'),
    [Input('cluster-dropdown-cuisine', 'value')]
)
def update_top_3_cuisines_table(selected_cluster):
    """
    Update the Top 3 Favorite Cuisines Table based on the selected cluster.
    """
    
    cui_columns = [col for col in main_df.columns if col.startswith("CUI_")]

    
    if not cui_columns:
        return html.P("No cuisine data available.", style={"textAlign": "center", "color": "red"})

    
    cui_percentages_by_cluster = main_df.groupby("cluster_som")[cui_columns].mean() * 100
    cui_percentages_by_cluster = cui_percentages_by_cluster.round(2)

    
    pivot_table = cui_percentages_by_cluster.T
    top_3_df = pd.DataFrame(columns=["cluster", "first_favourite", "second_favourite", "third_favourite"])

    
    for cluster in pivot_table.columns:
        top_3 = pivot_table[cluster].sort_values(ascending=False).head(3)
        top_3_df = pd.concat([
            top_3_df,
            pd.DataFrame({
                "cluster": [cluster],
                "first_favourite": [f"{top_3.index[0]} ({top_3.iloc[0]}%)"],
                "second_favourite": [f"{top_3.index[1]} ({top_3.iloc[1]}%)"],
                "third_favourite": [f"{top_3.index[2]} ({top_3.iloc[2]}%)"]
            })
        ], ignore_index=True)

    
    if selected_cluster:
        top_3_df = top_3_df[top_3_df['cluster'] == selected_cluster]

    
    table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in top_3_df.columns],
        data=top_3_df.to_dict('records'),
        style_table={"height": "200px", "overflowY": "auto"},
        style_cell={"textAlign": "center", "padding": "10px"},
        style_header={"fontWeight": "bold", "border": "1px solid black"},
    )

    return table

@callback(
    Output('funnel-chart', 'figure'),
    [Input('cluster-dropdown-cuisine', 'value')]
)
def update_funnel_chart(selected_cluster):
    """
    Update the funnel chart based on the selected cluster.
    """

    filtered_df = main_df if not selected_cluster else main_df[main_df['cluster_som'] == selected_cluster]
    cui_columns = [col for col in filtered_df.columns if col.startswith("CUI_")]
    cui_percentages = filtered_df[cui_columns].mean() * 100
    cui_percentages = cui_percentages.sort_values(ascending=False).head(5)

    # Create the funnel chart
    fig = px.funnel(
        x=cui_percentages.values,
        y=cui_percentages.index.str.replace("CUI_", "").str.title(),
        title="Top 5 Favorite Cuisines (Funnel)",
        labels={"x": "Percentage", "y": "Cuisine"}
    )

    # Update layout
    fig.update_layout(
        paper_bgcolor="#f9f9f9",
        height=600,
    )

    return fig

@callback(
    Output('pyramid-chart', 'figure'),
    [Input('cluster-dropdown-cuisine', 'value')]
)
def update_pyramid_chart(selected_cluster):
    """
    Update the pyramid chart based on the selected cluster.
    """
   
    filtered_df = main_df if not selected_cluster else main_df[main_df['cluster_som'] == selected_cluster]

    
    cui_columns = [col for col in filtered_df.columns if col.startswith("CUI_")]
    cui_percentages = filtered_df[cui_columns].mean() * 100
    cui_percentages = cui_percentages.sort_values(ascending=False).head(5)

    
    fig = px.bar(
        x=cui_percentages.values,
        y=cui_percentages.index.str.replace("CUI_", "").str.title(),
        title="Top 5 Favorite Cuisines (Pyramid)",
        labels={"x": "Percentage", "y": "Cuisine"},
        orientation='h'
    )

    fig.update_yaxes(autorange="reversed")

    # Update layout
    fig.update_layout(
        paper_bgcolor="#f9f9f9",
        height=600,
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)
