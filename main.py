import streamlit as st
import pandas as pd
import numpy as np
import itertools
import plotly.graph_objects as go
import plotly.express as px



HEADER_COLOR_CYCLE = itertools.cycle(
    [
        "#00c0f2",  # light-blue-70",
        "#ffbd45",  # "orange-70",
        "#00d4b1",  # "blue-green-70",
        "#1c83e1",  # "blue-70",
        "#803df5",  # "violet-70",
        "#ff4b4b",  # "red-70",
        "#21c354",  # "green-70",
        "#faca2b",  # "yellow-80",
    ]
)
    
def colored_header(label, description=None, color=None):
    """Shows a header with a colored underline and an optional description."""
    st.write("")
    if color is None:
        color = next(HEADER_COLOR_CYCLE)
    st.subheader(label)
    st.write(
        f'<hr style="background-color: {color}; margin-top: 0; margin-bottom: 0; height: 3px; border: none; border-radius: 3px;">',
        unsafe_allow_html=True,
    )
    if description:
        st.caption(description)


@st.cache
def load_data(nrows,DATE_COLUMN):
    DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

def main ():
    #DATE_COLUMN = 'date/time'
    st.title('Graph')
    # Create a text element and let the reader know the data is loading.
    data_load_state = st.text('Loading data...')
    x = np.arange(-2*np.pi, 2*np.pi, np.pi/36)

    sin_num = np.sin(x)
    table_sin=pd.DataFrame(data = sin_num, columns = ["sin"])

    cos_num = np.cos(x)
    table_cos=pd.DataFrame(data = cos_num, columns = ["cos"])

    sin_num_half = np.sin(x)/2
    table_sin_num_half=pd.DataFrame(data = sin_num_half, columns = ["1/2 sin"])


    table = pd.concat([table_sin,table_cos,table_sin_num_half],axis = 1)
    #print(table)

    # Notify the reader that the data was successfully loaded.
    data_load_state.text('Loading data...done!')

    #setting bottun
    st.sidebar.title("Which do you want to see?")
    control_features = st.sidebar.multiselect("Control which features?",
            ["sin","1/2 sin","cos"],
            default=["sin","1/2 sin","cos"])

    st.sidebar.title("X axis")
    x_axis_setting = st.sidebar.slider(label='Min',
                    min_value=0,
                    max_value=max(table.index),
                    value=(0, 100))
    #x_axis_setting_max = st.sidebar.slider(label='Max',
                    #min_value=0,
                    #max_value=max(table.index),
                    #value=30
                    #)
    

    st.sidebar.title("Y axis")
    y_axis_setting = st.sidebar.slider(label='Max',
                min_value=-2,
                max_value=2,
                value=(-1,1))
    #y_axis_setting_max = st.sidebar.slider(label='Min',
                #min_value=-1,
                #max_value=1,
                #value=1,
                #)


    #print(control_features)


    #if st.checkbox('Show raw data'): #テェックボックス
        #st.subheader('Raw data')
        #st.write(table_sin.T)
        #st.write(table_cos.T)
        #st.write(table_tan.T)

    # Other library
    # https://docs.streamlit.io/library/api-reference/charts

    st.subheader('Show raw data')
    with st.expander("Open"):
        #control_features

        #if "sin" in control_features:
            #st.write(table_sin.T)
        #if "cos" in control_features:
            #st.write(table_cos.T)
        #if "tan" in control_features:
            #st.write(table_tan.T)

        st.write(table[control_features])





    fig = px.line(table[control_features])
    fig.update_layout(xaxis=dict(title='X axis',range=(x_axis_setting[0],x_axis_setting[1])),
    yaxis=dict(title='Y axis',range=(y_axis_setting[0],y_axis_setting[1])))


    #print(y_axis_setting)
    st.plotly_chart(fig)
    #st.line_chart(table[control_features])

    #st.subheader('Map of all pickups')
    #st.map(data)



    #hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h

    #sharing site share.streamlit.io
    #https://blog.streamlit.io/built-in-charts-get-a-new-look-and-parameters/





if __name__ == "__main__":
    main()








