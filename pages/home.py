
import dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import services.dash_app_data as d
import plotly.express as px
from dash import dcc, Input, Output
from datetime import date
import dash_bootstrap_components as dbc
import datetime
from app import app


##################################################
# Starting Variables
##################################################

end_date =  datetime.date.today()
start_date = datetime.date(end_date.year, end_date.month - 5, 1).strftime("%Y-%m-%d")
end_date = end_date.strftime("%Y-%m-%d")

indicator_chart_height = 200
indicator_font_size = 32

##################################################
# Tile: Average Inventory Price
##################################################

# Creates a graph object that displays avg car price based on last scraped month
@app.callback(
  Output(component_id = 'avg_inventory_price', component_property = 'children'),
  Input('date-picker', 'start_date'),
  Input('date-picker', 'end_date')
)
def make_avg_price_indicator_chart (start_date, end_date):
  """
      start_date: The start date chosen by the user via dash callback
      end_dte: The end date chosen by the user via dash callback

      Returns: Plotly graph object
  """
  price = d.avg_inventory_price(start_date, end_date)
  return dcc.Graph(
    figure = {
      'data': [
        go.Indicator(
          mode = "number",
          value = price,
          number={"font":{"size": indicator_font_size}},
        )
      ],
      'layout': go.Layout(
        title = 'Average Inventory Price',
        height = indicator_chart_height,
      )
    }
  )

##################################################
# Tile: Average Inventory Year
##################################################

@app.callback(
    Output('avg_inventory_make_year', 'children'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')
)
def make_avg_make_year_chart (start_date, end_date):
  """
      start_date: The start date chosen by the user via dash callback
      end_dte: The end date chosen by the user via dash callback

      Returns: Plotly graph object
  """
  avg_year = d.avg_vehicle_year(start_date, end_date)
  return dcc.Graph(
    figure = {
        'data': [
          go.Indicator(
              mode = "number",
              value = avg_year,
              number={"font":{"size": indicator_font_size}},
          )
        ],
        'layout': go.Layout(
            title = 'Average Inventory Make Year',
            height = indicator_chart_height
        )
    }
  )

##################################################
# Tile: Average Inventory Mileage
##################################################

@app.callback(
    Output(component_id = 'avg_inventory_mileage', component_property = 'children'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')
)
def make_avg_inventory_mileage (start_date, end_date):
  """
      start_date: The start date chosen by the user via dash callback
      end_dte: The end date chosen by the user via dash callback

      Returns: Plotly graph object
  """
  avg_mileage = d.avg_vehicle_mileage(start_date, end_date)
  return dcc.Graph(
    figure = {
      'data': [
        go.Indicator(
          mode = "number",
          value = avg_mileage,
          number={"font":{"size": indicator_font_size}},
        )
      ],
      'layout': go.Layout(
        title = 'Average Inventory Mileage',
        height = indicator_chart_height
      )
    }
  )

##################################################
# Count of Makes Bar Chart
##################################################

@app.callback(
    Output('make_count_bar_chart', 'children'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')
)
def make_bar_chart (start_date, end_date):
  """
      start_date: The start date chosen by the user via dash callback
      end_dte: The end date chosen by the user via dash callback

      Returns: Plotly graph object
  """
  makes_data = d.make_count(start_date, end_date)
  return dcc.Graph(figure = px.bar(
    makes_data,
    y='vin',
    x='make',
    text_auto='.2s',
    title="Count of Used Cars by Make",
    labels={ # replaces default labels by column name
        "vin": "Count of Vehicles", "make": "Make"
    }
  ))


##################################################
# Avg Price by Month Line Chart
##################################################

@app.callback(
    Output('avg_price_line_chart', 'children'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')
)
def make_avg_price_line_chart(start_date, end_date):
  """
    start_date: The start date chosen by the user via dash callback
    end_dte: The end date chosen by the user via dash callback

    Returns: Plotly graph object
  """
  line_chart_data = d.avg_price_by_month(start_date, end_date)
  return dcc.Graph(figure = px.line(
      line_chart_data,
      x='inventory_month',
      y='price',
      title="Average Inventory Price by Month",
      labels={ # replaces default labels by column name
          "inventory_month": "Inventory Month", "price": "Avg Inventory Price"
      }
  ))

##################################################
# Avg Delaership Inventory Size by Month Line Chart
##################################################

@app.callback(
    Output(component_id = 'avg_dealership_inventory_size_by_month_line_chart', component_property = 'children'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')
)
def make_avg_dealership_inventory_size_line_chart(start_date, end_date):
  """
      start_date: The start date chosen by the user via dash callback
      end_dte: The end date chosen by the user via dash callback

      Returns: Plotly graph object
  """
  line_chart_data = d.avg_dealership_inventory_size_by_month(start_date, end_date)
  return dcc.Graph(
    figure = px.line(
        line_chart_data,
        x='inventory_month',
        y='inventory_size',
        title="Average Dealership Inventory Size by Month",
        labels={ # replaces default labels by column name
            "inventory_month": "Inventory Month", "inventory_size": "Average Inventory Size per Dealership"
        }
    )
  )


##################################################
## Main Layout
##################################################

layout = dbc.Container([

    dash.html.Div([
        dash.html.H1("Summary", className="dashboard-title")
    ], className="dashboard-title-section"),

    # Filter section
    dbc.Row(
        dbc.Col(
            dcc.DatePickerRange(
                id='date-picker',
                min_date_allowed=date(2022, 1, 1),
                initial_visible_month=start_date,
                start_date=start_date,
                end_date=end_date
            ),
            width={"size": 6},
        ), justify="flex-start", className="dashboard-filter-section"
    ),

    dash.html.Div(id="indicators", children = [
      dash.html.Div(id="avg_inventory_price", children = [], className="indicator-chart"),
      dash.html.Div(id="avg_inventory_make_year", children = [], className="indicator-chart"),
      dash.html.Div(id="avg_inventory_mileage", children = [], className="indicator-chart")
    ], className="indicator-chart-section"),

    dash.html.Div(id="graphs", children =[
      dash.html.Div(id="avg_price_line_chart", children = []),
      dash.html.Div(id="make_count_bar_chart", children = []),
      dash.html.Div(id="avg_price_by_make_bar_chart", children = []),
      dash.html.Div(id="avg_dealership_inventory_size_by_month_line_chart", children = [])
    ], className="dashboard-body")

])
