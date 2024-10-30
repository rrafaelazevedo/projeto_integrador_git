import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from query import * 

# consulta no database
query = 'SELECT * FROM tb_registro'

# carregar os dados do mysql
df = conexao(query)

# botao para atualizar dados
if st.button('Atualizar Dados'):
    df = conexao(query)

# menu lateral
st.sidebar.header('Selecione a informação para gerar gráfico')


# selecao de eixos, eixo das abscissas ou dominio x, e eixo das ordenadas y
# selectbox -> cria uma caixa de seleção na barra lateral
eixo_x = st.sidebar.selectbox(
    'Eixo X',
    options=['umidade', 'temperatura', 'pressao', 'altitude', 'co2', 'poeira'],
    index=0   
)

eixo_y = st.sidebar.selectbox(
    'Eixo Y',
    options=['umidade', 'temperatura', 'pressao', 'altitude', 'co2', 'poeira'],
    index=1   
)

# verifica quais os atributos do filtro de seleção
def filtros(atributo):
    return atributo in [eixo_x, eixo_y]


# filtro de range -> slider
st.sidebar.header('Seleciona o Filtro')

# temperatura
if filtros('temperatura'):
    temperatura_range = st.sidebar.slider(
        'Temperatura (°C)',
        min_value=float(df['temperatura'].min()),
        max_value=float(df['temperatura'].max()),
        # faixa de valores selecionados
        value=(float(df['temperatura'].min()), float(df['temperatura'].max())),
        # incremento para cada movimento do slider
        step = 1.0
    )


# pressao
if filtros('pressao'):
    pressao_range = st.sidebar.slider(
        'Pressao',
        min_value=float(df['pressao'].min()),
        max_value=float(df['pressao'].max()),
        # faixa de valores selecionados
        value=(float(df['pressao'].min()), float(df['pressao'].max())),
        # incremento para cada movimento do slider
        step = 1.0
    )


# altitude
if filtros('altitude'):
    altitude_range = st.sidebar.slider(
        'Altitude',
        min_value=float(df['altitude'].min()),
        max_value=float(df['altitude'].max()),
        # faixa de valores selecionados
        value=(float(df['altitude'].min()), float(df['altitude'].max())),
        # incremento para cada movimento do slider
        step = 1.0
    )


# umidade
if filtros('umidade'):
    umidade_range = st.sidebar.slider(
        'Umidade',
        min_value=float(df['umidade'].min()),
        max_value=float(df['umidade'].max()),
        # faixa de valores selecionados
        value=(float(df['umidade'].min()), float(df['umidade'].max())),
        # incremento para cada movimento do slider
        step = 1.0
    )


# co2
if filtros('co2'):
    co2_range = st.sidebar.slider(
        'Co2',
        min_value=float(df['co2'].min()),
        max_value=float(df['co2'].max()),
        # faixa de valores selecionados
        value=(float(df['co2'].min()), float(df['co2'].max())),
        # incremento para cada movimento do slider
        step = 1.0
    )


# poeira
if filtros('poeira'):
    poeira_range = st.sidebar.slider(
        'Poeira',
        min_value=float(df['poeira'].min()),
        max_value=float(df['poeira'].max()),
        # faixa de valores selecionados
        value=(float(df['poeira'].min()), float(df['poeira'].max())),
        # incremento para cada movimento do slider
        step = 1.0
    )

df_selecionado = df.copy()

if filtros('temperatura'):
    df_selecionado = df_selecionado[
        (df_selecionado['temperatura'] >= temperatura_range[0]) &
        (df_selecionado['temperatura'] <= temperatura_range[1])
    ]

if filtros('pressao'):
    df_selecionado = df_selecionado[
        (df_selecionado['pressao'] >= pressao_range[0]) &
        (df_selecionado['pressao'] <= pressao_range[1])
    ]

if filtros('altitude'):
    df_selecionado = df_selecionado[
        (df_selecionado['altitude'] >= altitude_range[0]) &
        (df_selecionado['altitude'] <= altitude_range[1])
    ]

if filtros('umidade'):
    df_selecionado = df_selecionado[
        (df_selecionado['umidade'] >=umidade_range[0]) &
        (df_selecionado['umidade'] <= umidade_range[1])
    ]

if filtros('co2'):
    df_selecionado = df_selecionado[
        (df_selecionado['co2'] >= co2_range[0]) &
        (df_selecionado['co2'] <= co2_range[1])
    ]

if filtros('poeira'):
    df_selecionado = df_selecionado[
        (df_selecionado['poeira'] >= poeira_range[0]) &
        (df_selecionado['poeira'] <= poeira_range[1])
    ]

# graficos
def home():
    with st.expander('Tabela'):
        mostrar_dados = st.multiselect(
            'Filtro: ',
            df_selecionado.columns,
            default=[],
            key = 'showData_home'
        )

        if mostrar_dados:
            st.write(df_selecionado[mostrar_dados])
            
   # se o dataframe não estiver vázio, teremos estatísticas fundamentas 
    if not df_selecionado.empty:
        umidade_media = df_selecionado['umidade'].mean()
        temperatura_media = df_selecionado['temperatura'].mean()
        co2_media = df_selecionado['co2'].mean()

        media_u, media_t, media_c = st.columns(3, gap='large')

        with media_u:
            st.info('Média de Registros de Umidade')
            st.metric(label='Média', value=f'{umidade_media:.2f}')
        
        with media_t:
            st.info('Média de Registros de Temperatura')
            st.metric(label='Média', value=f'{temperatura_media:.2f}')

        with media_c:
            st.info('Média de Registros de CO2')
            st.metric(label='Média', value=f'{co2_media:.2f}')

        st.markdown("""---------""")

def graficos():
    st.title('Dashboard Monitoramento')
    #aba_a, aba_b = st.tabs(['Gráfico de Linha', 'Gráfico de Dispersão'])
    aba_a = st.info['Gráfico de Barras']

    with aba_a:
        if df_selecionado.empty:
            st.write('Nenhum dado disponível para geração de gráfico')
            return
        
        if eixo_x == eixo_y:
            st.warning('Selecione uma opção diferente para os eixos perpendiculares, X e Y')
            return
        
        try:
            grupo_a = df_selecionado.groupby(by=[eixo_x]).size().reset_index(name='contagem')
            fig_valores = px.bar(
                grupo_a,
                x=eixo_x,
                y='contagem',
                orientation='h',
                title=f'Contagem de Registros por {eixo_x}',
                color_discrete_sequence=['#0083b8'],
                template='plotly_white'
            )

        except Exception as e:
            st.error(f'ERRO ao criar gráfico de barras: {e}')

            st.plotly_chart(fig_valores, use_container_width=True)
    

