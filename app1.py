import pandas as pd
import six.moves.urllib.request as urlreq
from six import PY3

import dash
import dash_bio as dashbio
import dash_html_components as html
import dash_core_components as dcc
import dash_auth
import plotly


VALID_USERNAME_PASSWORD_PAIRS = [
    ['hello', 'world']
    ]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/dash-bio-docs-files/master/' +
    'manhattan_data.csv'
)


markdown_text = '''
***Variants plot from SNP*** 
**Human example**
'''


app.layout = html.Div([
    html.H1('Welcome to the app'),
    html.H3('You are successfully authorized'),
    dcc.Markdown(children=markdown_text),
    dcc.Slider(
        id='manhattanplot-input',
        min=1,
        max=6,
        marks={
            i: {'label': str(i)} for i in range(10)
        },
        value=6
    ),
    html.Br(),
    html.Div(
        dcc.Graph(
            id='my-dashbio-manhattanplot',
            figure=dashbio.ManhattanPlot(
                dataframe=df
            )
        )
    )
])


@app.callback(
    dash.dependencies.Output('my-dashbio-manhattanplot', 'figure'),
    [dash.dependencies.Input('manhattanplot-input', 'value')]
)
def update_manhattanplot(threshold):

    return dashbio.ManhattanPlot(
        dataframe=df,
        genomewideline_value=threshold,
        suggestiveline_color='#AA00AA',
        genomewideline_color='#AA5500',
    )


if __name__ == '__main__':
    app.run_server(debug=True)