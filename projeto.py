import  streamlit as st
import pandas as pd
import altair as alt
import json
import requests

headers = {'Content-Type': 'application/json'}
def get_dados_brasil_por_data(data):
    url = 'https://covid19-brazil-api.now.sh/api/report/v1/brazil/' + str(data) 
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        st.text('Não há dados para essa data no Brasil')
        return None

def get_dados_paises():
    url = 'https://covid19-brazil-api.now.sh/api/report/v1/countries'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        
        return None

coordenadas = {'RS':{
            'latitude':-30.033914,
            'longitude':-51.229154,
            'uf':'RS'
        },
         'SC':{
             'latitude':-27.593237,
             'longitude':-48.543736,
             'uf':'SC'
        },
        'PR':{
            'latitude':-25.433171,
            'longitude':-49.27147,
            'uf':'PR'
        },
        'MS':{
            'latitude':-20.461719,
            'longitude':-54.612237,
            'uf':'MS'
        },
        'MT':{
            'latitude':-15.598917,
            'longitude':-56.094894,
            'uf':'MT'
        },
        'GO':{
            'latitude':-16.67992,
            'longitude':-49.255032,
            'uf':'GO'
        },
        'DF':{
            'latitude':-15.79983,
            'longitude':-47.863711,
            'uf':'DF'
        },
        'MG':{
            'latitude':-19.918339,
            'longitude':-43.940102,
            'uf':'MG'
        },
        'ES':{
            'latitude':-20.319933,
            'longitude':-40.336296,
            'uf':'ES'
        },
        'RJ':{
            'latitude':-22.908892,
            'longitude':-43.177138,
            'uf':'RJ'
        },
        'SP':{
            'latitude':-23.550483,
            'longitude':-46.633106,
            'uf':'SP'
        },
        'MA':{
            'latitude':-2.532066,
            'longitude':-44.299996,
            'uf':'MA'
        },
        'PI':{
            'latitude':-5.092628,
            'longitude':-42.810155,
            'uf':'PI'
        },
        'CE':{
            'latitude':-3.730536,
            'longitude':-38.521777,
            'uf':'CE'
        },
        'RN':{
            'latitude':-5.786403,
            'longitude':-35.207978,
            'uf':'RN'
        },
        'PB':{
            'latitude':-7.120034,
            'longitude':-34.876211,
            'uf':'PB'
        },
        'PE':{
            'latitude':-8.054278,
            'longitude':-34.881256,
            'uf':'PE'
        },
        'AL':{
            'latitude':-9.667137,
            'longitude':-35.737958,
            'uf':'AL'
        },
        'SE':{
            'latitude':-10.912647,
            'longitude':-37.053451,
            'uf':'SE'
        },
        'BH':{
            'latitude':-12.970382,
            'longitude':-38.512382,
            'uf':'BH'
        },
        'RO':{
            'latitude':-8.764597,
            'longitude':-63.903943,
            'uf':'RO'
        },
        'AC':{
            'latitude':-9.972463,
            'longitude':-67.812749,
            'uf':'AC'
        },
        'AM':{
            'latitude':-3.133842,
            'longitude':-60.020165,
            'uf':'AM'
        },
        'RR':{
            'latitude':2.821734,
            'longitude':-60.672061,
            'uf':'RR'
        },
        'PA':{
            'latitude':-1.452005,
            'longitude':-48.503072,
            'uf':'PA'
        },
        'AP':{
            'latitude':0.039045,
            'longitude':-51.050099,
            'uf':'AP'
        },
        'TO':{
            'latitude':-10.184567,
            'longitude':-48.333654,
            'uf':'TO'
        }
    }
coordenadas_df = pd.DataFrame(coordenadas)

from datetime import datetime
now = datetime.now()
datastime = pd.date_range(start='2020-01-01', end=now, closed="left")
datas = []
for data in reversed(datastime):
    data2 = data.strftime('%d/%m/%Y')
    datas.append(data2)

def main():
    st.text('Este aplicativo utiliza as informações atualizadas contidas no site Covid19Brazil')
    st.write('https://covid19-brazil-api.now.sh/')
    st.title('Covid pelo Brasil')

    data = st.selectbox('Escolha a data que deseja visualizar', datas)
    data_aux = data.split('/')
    data = ''.join(data_aux[::-1])
    dados_brasil = get_dados_brasil_por_data(data)
    
    df = pd.DataFrame(dados_brasil['data'])
    if len(df) == 0:
        st.text('Não há dados para essa data no Brasil')
    else:
        df.merge(coordenadas_df.T)

        # html_temp = """
        # <div style="display:flex;margin-bottom:20px">
        #     <div style="background-color:lightgray;width:150px;height:100px;margin-right:10px">{{df['deaths'].sum()}}</div>
        #     <div style="background-color:lightgray;width:150px;height:100px">Teste</div>
        # </div>
        # """
        # st.write(html_temp, unsafe_allow_html=True)
        
        bar = alt.Chart(df).mark_bar().encode(
        alt.X('state:O',title='Estados'),
        alt.Y('deaths:Q'),
        color = alt.condition(alt.datum.deaths > 2072,
                alt.value('red'),
                alt.value('black'))
        ).properties(
            title='Mortes por Estado e linha de média de morte'
        )
        
        rule = alt.Chart(df).mark_rule(color='red').encode(
            alt.Y('mean(deaths):Q', title='Quantidade de Mortes')
        )

        text = bar.mark_text(
            align='center',
            color='black',
            baseline='bottom',
            dx=3  # Nudges text to right so it doesn't appear on top of the bar
        ).encode(
            text='deaths:Q'
        )

        st.write((bar + rule + text).properties(width=600, height=400))

        st.subheader('Números do Brasil')
        st.text('Total de Casos Confirmados')
        st.text(df['cases'].sum())
        
        st.text('Total de Suspeitas')
        st.text(df['suspects'].sum())
        st.text('Total de Mortes')
        st.text(df['deaths'].sum())

        estados = list(df['state'])
        st.selectbox('Escolha o estado que deseja visualizar', estados)

    #sidebar
    dados_paises = get_dados_paises()
    dados_paises_df = pd.DataFrame(dados_paises['data'])
    paises = list(dados_paises_df['country'])
    
    st.sidebar.title('Números do Mundo')
    st.sidebar.subheader('Total de Casos Confirmados')
    st.sidebar.text(dados_paises_df['confirmed'].sum())
    st.sidebar.subheader('Total de Mortes')
    st.sidebar.text(dados_paises_df['deaths'].sum())
    st.sidebar.subheader('Total de Recuperações')
    st.sidebar.text(dados_paises_df['recovered'].sum())

   
    st.sidebar.title('Covid pelos Países')
    pais = st.sidebar.selectbox('Escolha o País', paises)

    st.sidebar.subheader('Total de Casos Confirmados')
    st.sidebar.text(dados_paises_df[dados_paises_df['country']==pais]['confirmed'].sum())
    
    st.sidebar.subheader('Total de Mortes')
    st.sidebar.text(dados_paises_df[dados_paises_df['country']==pais]['deaths'].sum())
    st.sidebar.subheader('Total de Recuperações')
    st.sidebar.text(dados_paises_df[dados_paises_df['country']==pais]['recovered'].sum())




if __name__ == '__main__':
    main()
