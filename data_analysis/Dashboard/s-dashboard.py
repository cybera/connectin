import numpy as np
import pandas as pd
from skimage import io, data, transform
from time import sleep

import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table

import dash_canvas
from dash_canvas.components import image_upload_zone
from dash_canvas.utils import (
    image_string_to_PILImage,
    array_to_data_url,
    parse_jsonstring_line,
    brightness_adjust,
    contrast_adjust,
)
from registration import register_tiles
from utils import StaticUrlPath
import pathlib

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server
app.config.suppress_callback_exceptions = True

# get relative data folder
PATH = pathlib.Path(__file__).parent

DATA_PATH = PATH.joinpath("data").resolve()


def demo_explanation():
    # Markdown files
    with open(PATH.joinpath("demo.md"), "r") as file:
        demo_md = file.read()

    return html.Div(
        html.Div([dcc.Markdown(demo_md, className="markdown")]),
        style={"margin": "10px"},
    )


def tile_images(list_of_images, n_rows, n_cols):
    dtype = list_of_images[0].dtype
    if len(list_of_images) < n_rows * n_cols:
        white = np.zeros(list_of_images[0].shape, dtype=dtype)
        n_missing = n_rows * n_cols - len(list_of_images)
        list_of_images += [white] * n_missing
    return np.vstack(
        [
            np.hstack(list_of_images[i_row * n_cols : i_row * n_cols + n_cols])
            for i_row in range(n_rows)
        ]
    )


def untile_images(image_string, n_rows, n_cols):
    big_im = np.asarray(image_string_to_PILImage(image_string))
    tiles = [np.split(im, n_cols, axis=1) for im in np.split(big_im, n_rows)]
    return np.array(tiles)


def demo_data():
    im = data.immunohistochemistry()
    l_c = 128
    l_r = 180
    n_rows = 1
    n_cols = im.shape[1] // l_c
    init_i, init_j = 0, 0
    overlap_h = [5, 25]

    big_im = np.empty((n_rows * l_r, n_cols * l_c, 3), dtype=im.dtype)
    i = 0
    for j in range(n_cols):
        sub_im = im[init_i : init_i + l_r, init_j : init_j + l_c]
        big_im[i * l_r : (i + 1) * l_r, j * l_c : (j + 1) * l_c] = sub_im
        init_j += l_c - overlap_h[1]
        init_i += overlap_h[0]
    return big_im


def _sort_props_lines(props, height, width, ncols):
    props = pd.DataFrame(props)
    index_init = ncols * (((props["top"]) - (props["height"]) // 2) // height) + (
        ((props["left"]) - (props["width"]) // 2) // width
    )
    index_end = ncols * (((props["top"]) + (props["height"]) // 2) // height) + (
        ((props["left"]) + (props["width"]) // 2) // width
    )
    props["index_init"] = index_init
    props["index_end"] = index_end
    overlaps = {}
    for line in props.iterrows():
        overlaps[(line[1]["index_init"], line[1]["index_end"])] = (
            int(line[1]["height"]),
            int(line[1]["width"]),
        )
    return overlaps


def instructions():
    return html.P(
        children=[
            """
    - Choose the number of rows and columns of the mosaic
    - Upload images 
    - Try automatic stitching by pressing the "Run stitching" button 
    - If automatic stitching did not work, adjust the overlap parameter
    """
        ],
        className="instructions-sidebar",
    )


height, width = 200, 500
canvas_width = 800
canvas_height = round(height * canvas_width / width)
scale = canvas_width / width

list_columns = ["length", "width", "height", "left", "top"]
columns = [{"name": i, "id": i} for i in list_columns]

app.layout = html.Div(
    children=[
        html.Div(
            [
                html.Img(
                    src=app.get_asset_url("dash-logo.png"), className="plotly-logo"
                ),
                html.H1(children="Stitching App"),
                instructions(),
                html.Div(
                    [
                        html.Button(
                            "LEARN MORE",
                            className="button_instruction",
                            id="learn-more-button",
                        ),
                        html.Button(
                            "UPLOAD DEMO DATA", className="demo_button", id="demo"
                        ),
                    ],
                    className="mobile_buttons",
                ),
                html.Div(
                    # Empty child function for the callback
                    html.Div(id="demo-explanation", children=[])
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label("Number of rows"),
                                dcc.Input(
                                    id="nrows-stitch",
                                    type="number",
                                    value=1,
                                    name="number of rows",
                                    min=1,
                                    step=1,
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.Label("Number of columns"),
                                dcc.Input(
                                    id="ncolumns-stitch",
                                    type="number",
                                    value=1,
                                    name="number of columns",
                                    min=1,
                                    step=1,
                                ),
                            ]
                        ),
                    ],
                    className="mobile_forms",
                ),
                html.Div(
                    [
                        html.Label("Downsample factor"),
                        dcc.RadioItems(
                            id="downsample",
                            options=[
                                {"label": "1", "value": "1"},
                                {"label": "2", "value": "2"},
                                {"label": "4", "value": "4"},
                                {"label": "8", "value": "8"},
                            ],
                            value="2",
                            labelStyle={"display": "inline-block"},
                            style={"margin-top": "-15px"},
                        ),
                        html.Label("Fraction of overlap (in [0-1] range)"),
                        dcc.Input(
                            id="overlap-stitch", type="number", value=0.15, min=0, max=1
                        ),
                        html.Br(),
                        dcc.Checklist(
                            id="do-blending-stitch",
                            options=[{"label": "Blending images", "value": 1}],
                            value=[1],
                        ),
                    ],
                    className="radio_items",
                ),
                html.Label("Measured shifts between images"),
                html.Div(
                    [
                        dash_table.DataTable(
                            id="table-stitch",
                            columns=columns,
                            editable=True,
                            style_table={
                                "width": "81%",
                                "margin-left": "4.5%",
                                "border-radius": "20px",
                            },
                            style_cell={
                                "text-align": "center",
                                "font-family": "Geneva",
                                "backgroundColor": "#01183A",
                                "color": "#8898B2",
                                "border": "1px solid #8898B2",
                            },
                        )
                    ],
                    className="shift_table",
                ),
                html.Br(),
                html.Button(
                    "Run stitching", id="button-stitch", className="button_submit"
                ),
                html.Br(),
            ],
            className="four columns instruction",
        ),
        html.Div(
            [
                dcc.Tabs(
                    id="stitching-tabs",
                    value="canvas-tab",
                    children=[
                        dcc.Tab(label="IMAGE TILES", value="canvas-tab"),
                        dcc.Tab(label="STITCHED IMAGE", value="result-tab"),
                        dcc.Tab(label="HOW TO USE THIS APP", value="help-tab"),
                    ],
                    className="tabs",
                ),
                html.Div(
                    id="tabs-content-example",
                    className="canvas",
                    style={"text-align": "left", "margin": "auto"},
                ),
                html.Div(className="upload_zone", id="upload-stitch", children=[]),
                html.Div(id="sh_x", hidden=True),
                html.Div(id="stitched-res", hidden=True),
                dcc.Store(id="memory-stitch"),
            ],
            className="eight columns result",
        ),
    ],
    className="row twelve columns",
)

if __name__ == "__main__":
    app.run_server(debug=True)
