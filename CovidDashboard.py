import numpy as np                              #Version 1.21.4
import pandas as pd                             #Version 1.3.4
import matplotlib.pyplot as plt                 #Version 3.5.0
import plotly.express as px                     #Version 5.4.0
import folium                                   #Version 0.12.1.post1
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash import Dash
import plotly.graph_objs as go
from plotly.subplots import make_subplots

#Load Data
url = (
    "https://raw.githubusercontent.com/Leonieen/COVID19/main/Daten"
)
#Allgemeine Übersicht Daten
de_altersstruktur = f"{url}/bund-covid-altersstruktur-zeitreihe_ab-2021-04-29.csv"
de_altersstruktur_data = pd.read_csv(de_altersstruktur)
de_hospi = f"{url}/DE_Hospi_2.csv"
de_hospi_data = pd.read_csv(de_hospi)
bl_impfungen = f"{url}/Aktuell_Deutschland_Impfquoten_COVID-19.csv"
bl_impfungen_data = pd.read_csv(bl_impfungen)
#Windrose Daten
lk_altersstruktur_icu = f"{url}/2021-12-19_12-15_teilbare_divi_daten.csv"
lk_altersstruktur_icu_data = pd.read_csv(lk_altersstruktur_icu)
#Heatmap Daten
col_list2 = ["A", "verh_frei_belegt", "Anteil", "betten_frei"]
lk_altersstruktur_icu_heat = f"{url}/2021-12-19_12-15_teilbare_divi_daten2.csv"
df_heat = pd.read_csv(lk_altersstruktur_icu_heat, usecols=col_list2)
#Scatter Daten
col_list2 = ["RS,C,5", "cases7_p_1,C,6"]
lk_infektionen = f"{url}/RKI_Corona_Landkreise.csv"
lk_infektionen_data_scatter = pd.read_csv(lk_infektionen, usecols=col_list2)
#Bubbles Daten
bl_df = f"{url}/d_bl_anteil_65.csv"
bl_df_data = pd.read_csv(bl_df)
#Map1 Daten
de_lk = f"{url}/RKI_Corona_Landkreise.geojson"
de_demo_alt = f"{url}/aeltere_bevoelkerung_regional.csv"
de_demo_alt_data = pd.read_csv(de_demo_alt)
de_divi = f"{url}/2021-12-19_12-15_teilbare_divi_daten-gs.csv"
de_divi_data = pd.read_csv(de_divi)
bins1 = list(de_demo_alt_data["Anteil ueber 65-Jaehrigen"].quantile([0, 0.25, 0.5, 0.75, 1]))
bins2 = list(de_divi_data["verh_frei_belegt"].quantile([0, 0.25, 0.5, 0.75, 1]))
#Map2 Daten BIvaraite
bi_color = f"{url}/Bivariate_facecolor.csv"
df = pd.read_csv(bi_color)
de_demo_alt = f"{url}/Bivariate_facecolor.csv"
df = pd.read_csv(de_demo_alt)
geojson = r"https://raw.githubusercontent.com/Leonieen/COVID19/main/Daten/RKI_Corona_Landkreise.geojson"
#Balken Daten
col_list1_b = ["A", "Altersgruppe", "AnzTodesfall100kM", "AnzTodesfall100kW", "AnzFall100kM"]
#de_lk = f"{url}/RKI_Corona_Landkreise/RKI_Corona_Landkreise.geojson"
de_altersgruppen = f"{url}/RKI_Altersgruppen.csv"
de_altersgruppen_data = pd.read_csv(de_altersgruppen, usecols=col_list1_b)
col_list2_b = ["AdmUnitId,N,5,0"]
de_lk_nr = f"{url}/RKI_Corona_Landkreise_tb.csv"
de_lk_nr_data = pd.read_csv(de_lk_nr, usecols=col_list2_b)

#Figure without input
fig_allgemein1 = px.bar(de_altersstruktur_data, x="Datum",
                        y=['Stratum_80_Plus', 'Stratum_70_Bis_79', 'Stratum_60_Bis_69', 'Stratum_50_Bis_59',
                           'Stratum_40_Bis_49', 'Stratum_30_Bis_39', 'Stratum_18_Bis_29', 'Stratum_17_Minus'],
                        color_discrete_sequence=px.colors.sequential.Plasma_r,
                        title="Jahresverlauf Coronainfektionen nach Altersgruppen")#, height=600, width=1000)
fig_allgemein2 = px.bar(de_hospi_data, x="Datum", y=['80', '60-79', '35-59', '15-34', '05-14', '00-04'],
                        color_discrete_sequence=px.colors.sequential.Plasma_r,
                        title="Jahresverlauf Todeszahlen nach Altersgruppen")#, height=600, width=1000)
fig_allgemein3 = px.line(bl_impfungen_data, x="Bundesland",
                         y=['Impfquote_60plus_voll', 'Impfquote_18plus_voll', 'Impfquote_18bis59_voll',
                            'Impfquote_12bis17_voll', 'Impfquote_05bis11_voll'],
                         color_discrete_sequence=px.colors.sequential.Plasma_r,
                         title="Impfquote der Altersgruppen Bundesländer")#, height=600, width=1000)
#Figure Heatmap
fig_heatmap1 = px.density_heatmap(df_heat, x="Anteil", y="verh_frei_belegt",
                                  labels=dict(x="Anteil der über 65-Jährigen", y="Hospitalisierung"),
                                  title="Hospitalisierung und Anteil der über 65-Jährigen")
fig_heatmap1.update_traces(dict(colorscale='cividis', showscale=True, coloraxis=None), )
#Figure Scatter
fig_scatter1 = px.scatter(df_heat, x=df_heat.Anteil, y=df_heat.verh_frei_belegt, color=lk_infektionen_data_scatter["cases7_p_1,C,6"])
fig_scatter1.update_layout(
    title="Hospitalisierung, Anteil der über 65-Jährigen und Covid-19 Fälle (color)",
    xaxis_title="Anteil der über 65-Jährigen [%]",
    yaxis_title="Anteil der belgten Intensivbetten [%]",
    legend_title="Covid-19 Fälle",
)
#Figure Bubbles
fig_bubbles1 = px.scatter(x=bl_df_data.Anteil, y=bl_df_data.Impfquote_60plus_voll,
                          size=bl_df_data.Verh_betten_belegt, color=bl_df_data.Verh_betten_belegt,
                          hover_name=bl_df_data.Name, log_x=True, size_max=50)
fig_bubbles1.update_layout(
    title="Hospitalisierung (size und color) der einzelnen Bundesländer in Abhängigkeit vom Anteil der über 65-Jährigen und Impfquoteder über 60-Jährigen",
    xaxis_title="Anteil der über 65-Jährigen [%]",
    yaxis_title="Impfquote 60plus voll [%]",
    legend_title="Covid-19 Fälle",
)
#Figure Map1
m = folium.Map(location=[51.165691, 10.451526],
               tiles=f"https://api.mapbox.com/styles/v1/geonie/ckwncbbrd0yrr14s9jxw55m7f/tiles/256/{{z}}/{{x}}/{{y}}@2x?access_token=pk.eyJ1IjoiZ2VvbmllIiwiYSI6ImNrd25ieHlvczJpbngycG52djFybmpwbmoifQ.IipoXG1Ioqw4iGxjGeXLWA",
               attr='My Data Attribution',
               zoom_start=6
)
#1. Choroplathenkarte zu Fig1
choropleth1 = folium.Choropleth(
    geo_data=de_lk,
    name="Altersgruppen",
    data=de_demo_alt_data,
    columns=["A","Anteil ueber 65-Jaehrigen"],
    key_on="feature.properties.AdmUnitId",
    fill_color="YlOrRd",
    fill_opacity=0.9,
    line_opacity=0.2,
    legend_name="Altersgruppen",
    bins=bins1,
    reset=True
).add_to(m)
choropleth2 = folium.Choropleth(
    geo_data=de_lk,
    name="Altersgruppen DIVI",
    data=de_divi_data,
    columns=["gemeindeschluessel","verh_frei_belegt"],
    key_on="feature.properties.AdmUnitId",
    fill_color="YlGnBu",
    fill_opacity=0.9,
    line_opacity=0.2,
    legend_name="Altersgruppen DIVI",
    bins=bins2,
    reset=True
).add_to(m)
folium.LayerControl().add_to(m)
location_map = m
location_map.save('Covid.html')
#Figure Map2 Bivaraite
m2 = folium.Map(location=[51.165691, 10.451526],
               tiles=f"https://api.mapbox.com/styles/v1/geonie/ckwncbbrd0yrr14s9jxw55m7f/tiles/256/{{z}}/{{x}}/{{y}}@2x?access_token=pk.eyJ1IjoiZ2VvbmllIiwiYSI6ImNrd25ieHlvczJpbngycG52djFybmpwbmoifQ.IipoXG1Ioqw4iGxjGeXLWA",
               attr='My Data Attribution',
               zoom_start=6
)
#Liste für jeden Farbcode mit den LK_Nummern
df_1=df.facecolor_id == 1
df_1_data = df[df_1]
df_2=df.facecolor_id == 2
df_2_data = df[df_2]
df_3=df.facecolor_id == 3
df_3_data = df[df_3]
df_4=df.facecolor_id == 4
df_4_data = df[df_4]
df_5=df.facecolor_id == 5
df_5_data = df[df_5]
df_6=df.facecolor_id == 6
df_6_data = df[df_6]
df_7=df.facecolor_id == 7
df_7_data = df[df_7]
df_8=df.facecolor_id == 8
df_8_data = df[df_8]
df_9=df.facecolor_id == 9
df_9_data = df[df_9]
jstevens = ["#e8e8e8", "#ace4e4", "#5ac8c8", "#dfb0d6", "#a5add3",
            "#5698b9", "#be64ac", "#8c62aa", "#3b4994"]
jstevens_id = ["1", "2", "3", "4", "5",
                "6", "7", "8", "9"]
def getcolor(feature):
    if feature['properties']['AdmUnitId'] in list(df_1_data.admin_unit):
        return jstevens[0]
    if feature['properties']['AdmUnitId'] in list(df_2_data.admin_unit):
        return jstevens[1]
    if feature['properties']['AdmUnitId'] in list(df_3_data.admin_unit):
        return jstevens[2]
    if feature['properties']['AdmUnitId'] in list(df_4_data.admin_unit):
        return jstevens[3]
    if feature['properties']['AdmUnitId'] in list(df_5_data.admin_unit):
        return jstevens[4]
    if feature['properties']['AdmUnitId'] in list(df_6_data.admin_unit):
        return jstevens[5]
    if feature['properties']['AdmUnitId'] in list(df_7_data.admin_unit):
        return jstevens[6]
    if feature['properties']['AdmUnitId'] in list(df_8_data.admin_unit):
        return jstevens[7]
    if feature['properties']['AdmUnitId'] in list(df_9_data.admin_unit):
        return jstevens[8]
    else:
        return 'gray'
folium.GeoJson(geojson, smooth_factor = 1, style_function = lambda feature: {
        'fillColor': getcolor(feature),
        'weight': 0,
        'fillOpacity': 0.8,
}).add_to(m2)
folium.LayerControl().add_to(m2)
bi_map = m2
bi_map.save('CovidBivariate.html')
#Figure Bivariate Legend
def colorsquare(text_x, text_y, colorscale, n=3, xaxis='x2', yaxis='y2'):
    z = [[j + n * i for j in range(n)] for i in range(n)]
    n = len(text_x)
    if len(text_x) != n or len(text_y) != n or len(colorscale) != 2 * n ** 2:
        raise ValueError('Your lists of strings  must have the length {n} and the colorscale, {n**2}')
    text = [[text_x[j] + '' + text_y[i] for j in range(len(text_x))] for i in range(len(text_y))]
    return go.Heatmap(x=list(range(n)),
                      y=list(range(n)),
                      z=z,
                      xaxis=xaxis,
                      yaxis=yaxis,
                      text=text,
                      hoverinfo='text',
                      colorscale=colorscale,
                      showscale=False)
def colors_to_colorscale(biv_colors):
    n = len(biv_colors)
    biv_colorscale = []
    for k, col in enumerate(biv_colors):
        biv_colorscale.extend([[round(k / n, 2), col], [round((k + 1) / n, 2), col]])
    return biv_colorscale
text_x = ['Intensiv_ratio<P_33', 'Intensiv_33<=Intensiv_ratio<=P_66', 'Intensiv_ratio>P_66']
text_y = ['Alter_ratio<P_33', 'Alter_33<=Alter_ratio<=P_66', 'Alter_ratio>P_66']
legend = colorsquare(text_x, text_y, colors_to_colorscale(jstevens))
figL = go.Figure(data=go.Heatmap({
    'colorscale': [[0.0, '#e8e8e8'], [0.11, '#e8e8e8'], [0.11, '#ace4e4'], [0.22,
                   '#ace4e4'], [0.22, '#5ac8c8'], [0.33, '#5ac8c8'], [0.33,
                   '#dfb0d6'], [0.44, '#dfb0d6'], [0.44, '#a5add3'], [0.56,
                   '#a5add3'], [0.56, '#5698b9'], [0.67, '#5698b9'], [0.67,
                   '#be64ac'], [0.78, '#be64ac'], [0.78, '#8c62aa'], [0.89,
                   '#8c62aa'], [0.89, '#3b4994'], [1.0, '#3b4994']],
    'hoverinfo': 'text',
    'showscale': False,
    'text': [['Intensiv_ratio<P_33<br>Alter_ratio<P_33',
             'Intensiv_33<=Intensiv_ratio<=P_66<br>Alter_ratio<P_33',
             'Intensiv_ratio>P_66<br>Alter_ratio<P_33'],
             ['Intensiv_ratio<P_33<br>Alter_33<=Alter_ratio<=P_66',
             'Intensiv_33<=Intensiv_ratio<=P_66<br>Alter_33<=Alter_ratio<=P_66',
             'Intensiv_ratio>P_66<br>Alter_33<=Alter_ratio<=P_66'],
             ['Intensiv_ratio<P_33<br>Alter_ratio>P_66',
             'Intensiv_33<=Intensiv_ratio<=P_66<br>Alter_ratio>P_66',
             'Intensiv_ratio>P_66<br>Alter_ratio>P_66']],
    'x': [0, 1, 2],
    'xaxis': 'x2',
    'y': [0, 1, 2],
    'yaxis': 'y2',
    'z': [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
}))
figL.update_layout(title="Legende Bivariate Choroplethenkarte",
                  yaxis={"title": 'Anteil der über 65-Jährigen'},
                  xaxis={"title": 'Anteil der belegten Intensivbetten'},
                  )

app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
color_text1 = {'color' : '#25938c', 'white-space': 'pre', 'textAlign': 'center'}
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1("Covid Dashboard Altersstruktur"),
        ]),
    #Map1
    html.Iframe(id='map', srcDoc=open('Covid.html', 'r').read(), width='100%', height='600'),
    html.Iframe(id='map2', srcDoc=open('CovidBivariate.html', 'r').read(), width='100%', height='600'),
    dcc.Graph(id='bivariatelegend', figure=figL),
    #Allgemein
    dcc.Graph(id='allgemein1', figure=fig_allgemein1),
    dcc.Graph(id='allgemein2', figure=fig_allgemein2),
    dcc.Graph(id='allgemein3', figure=fig_allgemein3),
    ]),
    #Windrose
    dcc.Dropdown(id='dropdown_windrose',
                options=[
                    {'label': 'Schleswig-Holstein', 'value': 1},
                    {'label': 'Hamburg', 'value': 2},
                    {'label': 'Niedersachsen', 'value': 3},
                    {'label': 'Bremen', 'value': 4},
                    {'label': 'Nordrhein-Westfalen', 'value': 5},
                    {'label': 'Hessen', 'value': 6},
                    {'label': 'Rheinland-Pfalz', 'value': 7},
                    {'label': 'Baden-Württemberg', 'value': 8},
                    {'label': 'Bayern', 'value': 9},
                    {'label': 'Saarland', 'value': 10},
                    {'label': 'Berlin', 'value': 11},
                    {'label': 'Brandenburg', 'value': 12},
                    {'label': 'Mecklenburg-Vorpommern', 'value': 13},
                    {'label': 'Sachsen', 'value': 14},
                    {'label': 'Sachsen-Anhalt', 'value': 15},
                    {'label': 'Thüringen', 'value': 16},
                ],
                optionHeight=35,
                value=1,
                disabled=False,
                multi=False,
                searchable=True,
                search_value='',
                placeholder='Please select...',
                clearable=True,
                style={'width': "100%", 'color': 'black', 'border-bottom': 'solid 3px',
                        'border-color': '#ffffff', 'padding-top': '6px'},
                ),
    dcc.Graph(id='windrose'),
    #Säulendiagramm Hospitalisierung
    dcc.Dropdown(id='dropdown_saeulen_hospi',
                 options=[
                     {'label': 'Schleswig-Holstein', 'value': 1},
                     {'label': 'Hamburg', 'value': 2},
                     {'label': 'Niedersachsen', 'value': 3},
                     {'label': 'Bremen', 'value': 4},
                     {'label': 'Nordrhein-Westfalen', 'value': 5},
                     {'label': 'Hessen', 'value': 6},
                     {'label': 'Rheinland-Pfalz', 'value': 7},
                     {'label': 'Baden-Württemberg', 'value': 8},
                     {'label': 'Bayern', 'value': 9},
                     {'label': 'Saarland', 'value': 10},
                     {'label': 'Berlin', 'value': 11},
                     {'label': 'Brandenburg', 'value': 12},
                     {'label': 'Mecklenburg-Vorpommern', 'value': 13},
                     {'label': 'Sachsen', 'value': 14},
                     {'label': 'Sachsen-Anhalt', 'value': 15},
                     {'label': 'Thüringen', 'value': 16},
                 ],
                 optionHeight=35,
                 value=1,
                 disabled=False,
                 multi=False,
                 searchable=True,
                 search_value='',
                 placeholder='Please select...',
                 clearable=True,
                 style={'width': "100%", 'color': 'black', 'border-bottom': 'solid 3px',
                        'border-color': '#ffffff', 'padding-top': '6px'},
                 ),
    dcc.Graph(id='saeulen_hospi'),
    # Heatmap
    dcc.Graph(id='heatmap1', figure=fig_heatmap1),
    #Scatterplot
    dcc.Graph(id='scatter1', figure=fig_scatter1),
    # Bubbles
    dcc.Graph(id='bubbles1', figure=fig_bubbles1),
    #Balken
    dcc.Dropdown(de_lk_nr_data["AdmUnitId,N,5,0"],
                 id='balken_dropdown1',
                 value=1001,
                 searchable=True,),
    dcc.Graph(id='balken1'),
    dcc.Dropdown(de_lk_nr_data["AdmUnitId,N,5,0"], id='balken_dropdown2', value=1001, searchable=True,),
    dcc.Dropdown(de_lk_nr_data["AdmUnitId,N,5,0"], id='balken_dropdown3', value=1002, searchable=True,),
    dcc.Graph(id='balken2'),
])

#Callback Windrose
@app.callback([Output(component_id='windrose', component_property='figure'),
               ],
              [Input('dropdown_windrose', 'value'),
               ])
def fkt(chosen_windrose):
    bl_altersgruppen = lk_altersstruktur_icu_data.bundesland == chosen_windrose
    x = lk_altersstruktur_icu_data[bl_altersgruppen]
    fig_windrose = px.bar_polar(lk_altersstruktur_icu_data[bl_altersgruppen], r="verh_frei_belegt", theta="%s"%("gemeindeschluessel"), color="Anteil ueber 65-Jaehrigen",
                                color_discrete_sequence= px.colors.sequential.Plasma_r,
                                title="Verhältnis freie und belegte Intensivbetten der Landkreise sortiert nach demographischen Alterung"
                                )
    return [go.Figure(data=fig_windrose)]

# Callback Säulen Hospi
@app.callback([Output(component_id='saeulen_hospi', component_property='figure'),
               ],
              [Input('dropdown_saeulen_hospi', 'value'),
               ])
def fkt(chosen_hospi):
    bl_altersgruppen = lk_altersstruktur_icu_data.bundesland == chosen_hospi
    x = lk_altersstruktur_icu_data[bl_altersgruppen]
    fig_sauelen_hospi1 = px.bar(lk_altersstruktur_icu_data[bl_altersgruppen], y="verh_frei_belegt", x="%s"%("gemeindeschluessel"), color="Anteil ueber 65-Jaehrigen",
                       #color_discrete_sequence= px.colors.sequential.Plasma_r,
                       title="Verhältnis freie und belegte Intensivbetten der Landkreise sortiert nach demographischen Alterung"
                      )
    fig_sauelen_hospi1.update_layout(
        title="Verhältnis freie und belegte Intensivbetten der Landkreise sortiert nach demographischen Alterung",
        xaxis_title="Gemeindeschlüssel",
        yaxis_title="Belegte Intensivbetten [%]",
        legend_title="Legend Title",
    )
    return [go.Figure(data=fig_sauelen_hospi1)]

#Balken1
@app.callback(
    Output('balken1', 'figure'),
    Input('balken_dropdown1', 'value')
)
def update_output(lk_nummer):
    lk_altersgruppen = de_altersgruppen_data.A == lk_nummer
    lk_data = de_altersgruppen_data[lk_altersgruppen]
    fig = make_subplots(rows=1, cols=2, shared_yaxes=True, subplot_titles=("Todesfälle", "Coronafälle"),
                        horizontal_spacing=0)
    fig.add_trace(go.Bar(
        name='Corona Todesfälle',
        x=lk_data['AnzTodesfall100kM'],
        y=lk_data['Altersgruppe'],
        marker_color='indianred',
        # color=lk_data['Altersgruppe'],
        # olor_continuous_scale='Bluered_r',
        orientation='h'),
        1, 1)
    fig.add_trace(go.Bar(
        name='Coronafälle',
        x=lk_data['AnzFall100kM'],
        y=lk_data['Altersgruppe'],
        marker_color='MediumPurple',
        orientation='h'),
        1, 2)
    fig.update_layout(barmode="relative", yaxis_visible=True)
    fig.update_layout(
        xaxis=dict(showgrid=False),
        xaxis2=dict(showgrid=True)
    )
    fig.update_xaxes(title_text="Anzahl Todesfälle", row=1, col=1, autorange='reversed')
    fig.update_xaxes(title_text="Anzahl Coronafälle", row=1, col=2)

    return fig


@app.callback(
    Output('balken2', 'figure'),
    [Input('balken_dropdown2', 'value'),
     Input('balken_dropdown3', 'value')]
)
def update_output(lk_nummer1, lk_nummer2):
    lk_altersgruppen1 = de_altersgruppen_data.A == lk_nummer1
    lk_data1 = de_altersgruppen_data[lk_altersgruppen1]
    lk_altersgruppen2 = de_altersgruppen_data.A == lk_nummer2
    lk_data2 = de_altersgruppen_data[lk_altersgruppen2]
    fig = make_subplots(rows=1, cols=2, shared_yaxes=True, subplot_titles=("Landkreis1", "Landkreis2"),
                        horizontal_spacing=0)
    fig.add_trace(go.Bar(
        name='Corona Todesfälle',
        x=lk_data1['AnzTodesfall100kM'],
        y=lk_data1['Altersgruppe'],
        marker_color='indianred',
        # color=lk_data['Altersgruppe'],
        # olor_continuous_scale='Bluered_r',
        orientation='h'),
        1, 1)
    fig.add_trace(go.Bar(
        name='Corona Todesfälle',
        x=lk_data2['AnzTodesfall100kM'],
        y=lk_data2['Altersgruppe'],
        marker_color='MediumPurple',
        orientation='h'),
        1, 2)
    fig.update_layout(barmode="relative", yaxis_visible=True)
    fig.update_layout(
        xaxis=dict(showgrid=False),
        xaxis2=dict(showgrid=False)
    )
    fig.update_xaxes(title_text="Anzahl Todesfälle", row=1, col=1, autorange='reversed')
    fig.update_xaxes(title_text="Anzahl Coronafälle", row=1, col=2)

    return fig

if __name__ == '__main__':
    app.run(debug=True)