#---¡import-libraries!
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import streamlit as st 
import pydeck
from datetime import datetime


#---¡cargamos-la-data!
@st.cache_data
def load_data():
    data = pd.read_csv('data/uspvdb_v2_0_20240807.csv')
    return data

df = load_data()
#---¡vemos-la-informacion!
print(df.info())

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Data", "Renowables",
 "Agrivoltaics", "Maps USA", "AC capacity", "DC capacity", "Antioquia Potentials", "Antioquia map"])

with tab1:
    #---¡st.checkbox¡
    #--¡para-desplregar-dataframe-,-tambien-se-puede-usar-st.toggle!
    description = '''
    In this APP we can analized a data base with agrivaoltaics proyects in USA 
    to determine the viability of this same type proyects 
    on Antioquia and your municipalities. The data base was take of Sciencebase
    '''
    st.write(description)
    view_df = st.checkbox('View Data Frame')
    if view_df:
        st.write(df)

with tab2:
    #---¡proyectos-renovables-en-USA-por-estados!
    with st.container(border=True):
        #---el-numero-de-proyecos-por-estado!
        df_state = df.groupby(df['p_state']).count()['case_id']
        #---graficamos-el-numero-de-proyectos-por-estado!
        st.header('Renewable energy projects in the United States of America')
        st.bar_chart(df_state, horizontal=True)
with tab3:
    #---¡granjas-agrivoltaicas-por-estados!
    with st.container(border = True):
        #---¡creamos-la-columan-fil_agv-para-almacenar-allí-los-datos-no-agrivolt!
        df['fil_agv'] = df[df['p_agrivolt'] == 'non-agrivoltaic']['p_agrivolt']
        #---¡ahora-filtramos-unicamente-los-datos-agrivoltaicos-utilizando-la-columna-creada-file_agv!
        df_agrivolt = df[df['p_agrivolt'] != df['fil_agv']]
        print(df_agrivolt.info())
        #---¡filtramos-por-estado!
        filtred_agrivolt_state = df_agrivolt.groupby(df_agrivolt['p_state']).count()['case_id']
        #---¡graficamos-el-numero-de-granjas-agrivoltaicas-por-estado!
        st.header('Agrivoltaic projects in the United States of America')
        st.bar_chart(filtred_agrivolt_state, horizontal=True)

with tab4:
    #---¡filtramos-los-proyectos-por-latitud-y-longitug!
    df_agrivoltaic_state_map = df_agrivolt.groupby(by=['p_state', 'ylat','xlong'], as_index=False).case_id.count()
    df_agrivoltaic_state_map['size'] = df_agrivoltaic_state_map['case_id'] * 300
    capas=pydeck.Layer(
        "ScatterplotLayer",
        data=df_agrivoltaic_state_map,
        get_position=["xlog", "ylat"],
        get_color="[255, 75, 75]",
        pickable=True,
        auto_highlight=True,
        get_radius="size"
        )
    vista_inicial=pydeck.ViewState(latitude=4,longitude=-74,zoom=4.5)
    #---¡creamos-el-mapa-de-los proyectos-en-USA!
    with st.container(border=True):
        st.header('Agrivoltaic map states')
        st.map(df_agrivoltaic_state_map,latitude='ylat', longitude='xlong', size='size')

with tab5:
    with st.container(border=True):
        st.header('AC Capacity')
        #vamos-a-filtrar-por-capacidad-en-corriente-alterna-ac
        agrivolt_ac_capacity = df_agrivolt.groupby(df_agrivolt['p_state']).count()['p_cap_ac']
        #agrivolt_ac_capacity.plot(kind = 'scatter')
        #---¡statistics-of-ac-capacity!
        count_agrivolt_ac = df_agrivolt['p_cap_ac'].describe()[0]
        mean_agrivolt_ac = df_agrivolt['p_cap_ac'].describe()[1]
        min_agrivolt_ac = df_agrivolt['p_cap_ac'].describe()[3]
        max_agrivolt_ac = df_agrivolt['p_cap_ac'].describe()[7]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label="Total agrivoltaic proyects", value=round(count_agrivolt_ac, 2))
        col2.metric(label="Mean capacity [MW]", value=round(mean_agrivolt_ac, 2))
        col3.metric(label="Minim capacity [MW]", value=round(min_agrivolt_ac, 2))
        col4.metric(label="Maxim capacity [MW]", value=round(max_agrivolt_ac, 2))
    
        fig, ax = plt.subplots()
        sns.scatterplot(x = 'p_cap_ac', y = 'p_state', data = df_agrivolt)
        ax.set_title('AC capacity proyects')
        ax.set_xlabel('Capacity [MW]')
        ax.set_ylabel('State')
        #ax.tick_params(axis='x', labelrotation=90, labelsize=6)
        st.pyplot(fig)


with tab6:
    with st.container(border=True):
        st.header('DC Capacity')
        #---¡vamos-a-filtrar-por-capacidad-en-corriente-alterna-dc!
        agrivolt_dc_capacity = df_agrivolt.groupby(df_agrivolt['p_state']).count()['p_cap_ac']
        #agrivolt_ac_capacity.plot(kind = 'scatter')
        #num_columns = ['p_cap_dc']
        #cat_columns = [None, 'p_state', 'p_county']
        count_agrivolt_dc = df_agrivolt['p_cap_dc'].describe()[0]
        mean_agrivolt_dc = df_agrivolt['p_cap_dc'].describe()[1]
        min_agrivolt_dc = df_agrivolt['p_cap_dc'].describe()[3]
        max_agrivolt_dc = df_agrivolt['p_cap_dc'].describe()[7]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label="Total agrivoltaic proyects", value=round(count_agrivolt_dc, 2))
        col2.metric(label="Mean capacity [MW]", value=round(mean_agrivolt_dc, 2))
        col3.metric(label="Minim capacity [MW]", value=round(min_agrivolt_dc, 2))
        col4.metric(label="Maxim capacity [MW]", value=round(max_agrivolt_dc, 2))
    
        fig, ax = plt.subplots()
        sns.scatterplot(x = 'p_cap_dc', y = 'p_state', data = df_agrivolt)
        ax.set_title('DC capacity proyects')
        ax.set_xlabel('Capacity [MW]')
        ax.set_ylabel('State')
        #ax.tick_params(axis='x', labelrotation=90, labelsize=6)
        st.pyplot(fig)

with tab7:
    #---¡cargamos-los-datos-de-Antioquia!
    df_Antioquia = pd.read_excel('data/3.1.1.xlsx')
    print(df_Antioquia.info())
    print(df_Antioquia)
    #---¡vamos-a-eliminar-las-primeras-filas-porque-no-aportan-mucho-y-también-la-ultima-fila!
    df_Antioquia = df_Antioquia[6:]
    df_Antioquia.columns = ['cod_dane', 'subregion', 'esq_asociatvo', 'municipios', 'pob_urbana',
    'pob_urb_%depar', 'pob_rural', 'pob_rur_%depar', 'pob_total', '%_total_depar' ]
    df_Antioquia = df_Antioquia.reset_index(drop=True)
    df_Antioquia = df_Antioquia.drop(df_Antioquia.index[[134]])
    print(df_Antioquia.info())

    #---¡cargamos-el-dataframe-con-la-poblacion-de-usa!
    df_populations_usa = pd.read_csv('data/pop_co_est2023_alldata.csv')
    print(df_populations_usa.info())
    print(df_populations_usa)

    #---¡vamos-a-escorger-condados-de-USA-que-tengan-la-misma-poblacion-que-algunos-municipios-de-Antioquia!
    populations_same_county_ant_usa = []
    for population_usa in df_populations_usa['POPESTIMATE2023']:
        for population_ant in df_Antioquia['pob_total']:
            if population_usa == population_ant:
                populations_same_county_ant_usa.append(population_usa)
    
    print(populations_same_county_ant_usa)

    #---¡filtramos-en-un-dataframe-los-municipios-de-Antioquia-con-el-numero-de-poblacion!
    filtered_Ant_Usa_pob = df_Antioquia[df_Antioquia.pob_total.isin(populations_same_county_ant_usa)].sort_values('pob_total')
    filtered_Ant_Usa_pob = filtered_Ant_Usa_pob.reset_index(drop=True)
    print(filtered_Ant_Usa_pob)

    #---¡filtramos-en-un-dataframe-los-condaddos-de-USA-con-el-numero-de-poblacion!
    filtered_Usa_Ant_pob = df_populations_usa[df_populations_usa.POPESTIMATE2023.isin(populations_same_county_ant_usa)].sort_values('POPESTIMATE2023')
    filtered_Usa_Ant_pob  = filtered_Usa_Ant_pob.reset_index(drop=True)
    print(filtered_Usa_Ant_pob)

    #---¡creamos-un-dataframe-con-los-municipios-de-Antioquia-y-los-condados-de-USA-que-tienen-la-misma-poblacion!
    df_Ant_Usa = pd.DataFrame(filtered_Usa_Ant_pob['STNAME'])
    df_Ant_Usa['CTYNAME'] = filtered_Usa_Ant_pob['CTYNAME']
    df_Ant_Usa['MUN_ANTIOQUIA'] = filtered_Ant_Usa_pob['municipios']
    df_Ant_Usa['POPULATION'] = filtered_Usa_Ant_pob['POPESTIMATE2023']
    #---¡cargamos-las-coordenadas-de-los-municipios!
    df_coor_ant = pd.read_csv('data/coord_muni.csv')
    df_Ant_Usa['MUN_LAT'] = df_coor_ant['mun_ant_lat']
    df_Ant_Usa['MUN_LONG'] = df_coor_ant['mun_ant_long']
    print(df_Ant_Usa.info())
    print(df_Ant_Usa)

    #---¡graficamos-los-municipios-de-Antioquia!
    with st.container(border=True):
        st.header('Municipalities candidates')
        #sns.set_style("whitegrid")
        #df['sepal_length_mayor5'] = np.where(df['sepal_length'] > 5,"Si", "No")
        fig, ax = plt.subplots(figsize = (8,6))
        sns.barplot(x='MUN_ANTIOQUIA', y='POPULATION', hue=None, data=df_Ant_Usa)
        #sns.barplot(x='CTYNAME', y='POPULATION', hue=None, data=dfgh)
        ax.bar_label(ax.containers[0], fontsize=10);
        ax.tick_params(axis='x', labelrotation=45)
        ax.set_title('Municipalities of Antioquia with population potential')
        ax.set_xlabel('Municipalities')
        ax.set_ylabel('Population')
        #ax.tick_params(axis='x', labelrotation=90, labelsize=6)
        plt.show()
        st.pyplot(fig)

with tab8:
    #---¡filtramos-los-proyectos-por-latitud-y-longitug!
    df_Ant_Usa_map = df_Ant_Usa.groupby(by=['MUN_ANTIOQUIA', 'MUN_LAT','MUN_LONG'], as_index=False).STNAME.count()
    df_Ant_Usa_map['size'] = df_Ant_Usa_map['STNAME'] * 100
    capas=pydeck.Layer(
        "ScatterplotLayer",
        data=df_Ant_Usa_map,
        get_position=["MUN_LONG", "MUN_LAT"],
        get_color="[255, 75, 75]",
        pickable=True,
        auto_highlight=True,
        get_radius="size"
        )
    vista_inicial=pydeck.ViewState(latitude=4,longitude=-74,zoom=4.5)
    #---¡creamos-el-mapa-de-los proyectos-en-USA!
    with st.container(border=True):
        st.header('Municipalities candidates map')
        st.map(df_Ant_Usa_map, latitude='MUN_LAT', longitude='MUN_LONG', size='size')