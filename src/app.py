import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import sys
sys.path.insert(0, '/home/soethe/codeneed_workspace/fuzzy-learn')

from utils.fuzzy_logic import FuzzySystem, HeightPersistenceSystem

st.set_page_config(page_title="Fuzzy Logic Explorer", layout="wide", initial_sidebar_state="expanded")

st.title("🎯 Explorador de Lógica Fuzzy")
st.markdown("""
Aprenda sobre conjuntos fuzzy, funções de pertencimento e sistemas de classificação com exemplos interativos.
""")

# Menu principal
menu = st.sidebar.radio(
    "Escolha um tópico:",
    ["Conjuntos Fuzzy", "Funções de Pertencimento", "Sistema de Altura e Persistência"]
)

if menu == "Conjuntos Fuzzy":
    st.header("📊 Entendendo Conjuntos Fuzzy")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### O que é um Conjunto Fuzzy?
        
        Ao contrário da lógica clássica (0 ou 1), os conjuntos fuzzy permitem **graus de pertencimento** entre 0 e 1.
        
        **Exemplo Clássico:**
        - Lógica clássica: Uma pessoa com 1.80m é "alta" (1) ou "não alta" (0)
        - Lógica fuzzy: Uma pessoa com 1.80m tem grau de pertencimento 0.7 para "alta"
        """)
    
    with col2:
        # Visualização de conjunto fuzzy
        x = np.arange(150, 210, 1)
        baixa = np.maximum(1 - np.abs(x - 160) / 15, 0)
        media = np.maximum(1 - np.abs(x - 175) / 15, 0)
        alta = np.maximum(1 - np.abs(x - 190) / 15, 0)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(x, baixa, label='Baixa', linewidth=2, color='#FF6B6B')
        ax.plot(x, media, label='Média', linewidth=2, color='#4ECDC4')
        ax.plot(x, alta, label='Alta', linewidth=2, color='#45B7D1')
        ax.fill_between(x, baixa, alpha=0.3, color='#FF6B6B')
        ax.fill_between(x, media, alpha=0.3, color='#4ECDC4')
        ax.fill_between(x, alta, alpha=0.3, color='#45B7D1')
        ax.set_xlabel('Altura (cm)', fontsize=12)
        ax.set_ylabel('Grau de Pertencimento', fontsize=12)
        ax.set_title('Conjuntos Fuzzy: Classificação de Altura', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
    
    # Teste interativo
    st.divider()
    st.subheader("🧪 Teste Interativo")
    
    altura_teste = st.slider("Selecione uma altura (cm):", 150, 210, 175)
    
    col1, col2, col3 = st.columns(3)
    
    pertencimento_baixa = max(1 - abs(altura_teste - 160) / 15, 0)
    pertencimento_media = max(1 - abs(altura_teste - 175) / 15, 0)
    pertencimento_alta = max(1 - abs(altura_teste - 190) / 15, 0)
    
    with col1:
        st.metric("Pertencimento em 'Baixa'", f"{pertencimento_baixa:.2%}")
    with col2:
        st.metric("Pertencimento em 'Média'", f"{pertencimento_media:.2%}")
    with col3:
        st.metric("Pertencimento em 'Alta'", f"{pertencimento_alta:.2%}")
    
    # Gráfico interativo
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x, y=baixa,
        mode='lines', name='Baixa',
        line=dict(color='#FF6B6B', width=3),
        fill='tozeroy', fillcolor='rgba(255, 107, 107, 0.3)'
    ))
    fig.add_trace(go.Scatter(
        x=x, y=media,
        mode='lines', name='Média',
        line=dict(color='#4ECDC4', width=3),
        fill='tozeroy', fillcolor='rgba(78, 205, 196, 0.3)'
    ))
    fig.add_trace(go.Scatter(
        x=x, y=alta,
        mode='lines', name='Alta',
        line=dict(color='#45B7D1', width=3),
        fill='tozeroy', fillcolor='rgba(69, 183, 209, 0.3)'
    ))
    
    fig.add_vline(x=altura_teste, line_dash="dash", line_color="red", 
                  annotation_text=f"Altura: {altura_teste}cm")
    
    fig.update_layout(
        title="Graus de Pertencimento por Altura",
        xaxis_title="Altura (cm)",
        yaxis_title="Grau de Pertencimento",
        height=500,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)


elif menu == "Funções de Pertencimento":
    st.header("📈 Tipos de Funções de Pertencimento")
    
    st.markdown("""
    As funções de pertencimento definem como um valor é mapeado para um grau de pertencimento (0 a 1).
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        funcao_tipo = st.selectbox(
            "Escolha o tipo de função:",
            ["Triangular", "Trapezoidal", "Gaussiana", "Sigmoide"]
        )
    
    x = np.arange(0, 100, 0.1)
    
    if funcao_tipo == "Triangular":
        y = np.maximum(1 - np.abs(x - 50) / 25, 0)
        descricao = "**Triangular**: Forma de triângulo. Simples e computacionalmente eficiente."
        params = "Parâmetros: mín, pico, máx"
        
    elif funcao_tipo == "Trapezoidal":
        y = np.maximum(1 - np.maximum(
            np.maximum(40 - x, 0) / 15,
            np.maximum(x - 60, 0) / 15
        ), 0)
        descricao = "**Trapezoidal**: Forma de trapézio. Representa valores com patamar constante."
        params = "Parâmetros: a, b, c, d (onde b-a e d-c são os lados)"
        
    elif funcao_tipo == "Gaussiana":
        sigma = 15
        y = np.exp(-((x - 50) ** 2) / (2 * sigma ** 2))
        descricao = "**Gaussiana**: Forma de sino. Suave e simétrica."
        params = f"Parâmetros: média ({50}), desvio padrão ({sigma})"
        
    elif funcao_tipo == "Sigmoide":
        y = 1 / (1 + np.exp(-(x - 50) / 10))
        descricao = "**Sigmoide**: Forma de S. Representa transição gradual."
        params = "Parâmetros: ponto de inflexão (x₀), inclinação (a)"
    
    with col2:
        st.markdown(descricao)
        st.info(f"ℹ️ {params}")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='lines',
            name=funcao_tipo,
            line=dict(color='#45B7D1', width=3),
            fill='tozeroy', fillcolor='rgba(69, 183, 209, 0.3)'
        ))
        
        fig.update_layout(
            title=f"Função {funcao_tipo}",
            xaxis_title="Valor",
            yaxis_title="Grau de Pertencimento",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Comparação de funções
    st.divider()
    st.subheader("📊 Comparação de Todas as Funções")
    
    y_tri = np.maximum(1 - np.abs(x - 50) / 25, 0)
    y_trap = np.maximum(1 - np.maximum(
        np.maximum(40 - x, 0) / 15,
        np.maximum(x - 60, 0) / 15
    ), 0)
    sigma = 15
    y_gauss = np.exp(-((x - 50) ** 2) / (2 * sigma ** 2))
    y_sig = 1 / (1 + np.exp(-(x - 50) / 10))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y_tri, mode='lines', name='Triangular', 
                            line=dict(width=2, color='#FF6B6B')))
    fig.add_trace(go.Scatter(x=x, y=y_trap, mode='lines', name='Trapezoidal', 
                            line=dict(width=2, color='#4ECDC4')))
    fig.add_trace(go.Scatter(x=x, y=y_gauss, mode='lines', name='Gaussiana', 
                            line=dict(width=2, color='#45B7D1')))
    fig.add_trace(go.Scatter(x=x, y=y_sig, mode='lines', name='Sigmoide', 
                            line=dict(width=2, color='#FFA07A')))
    
    fig.update_layout(
        title="Comparação de Funções de Pertencimento",
        xaxis_title="Valor",
        yaxis_title="Grau de Pertencimento",
        height=500,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)


elif menu == "Sistema de Altura e Persistência":
    st.header("🎓 Sistema Fuzzy: Classificação por Altura e Persistência")
    
    st.markdown("""
    Este sistema classifica em grupos (Inicial, Intermediário, Avançado) baseado em:
    - **Altura**: Característica física
    - **Persistência**: Dedicação do aluno (0-10)
    """)
    
    system = HeightPersistenceSystem()
    
    col1, col2 = st.columns(2)
    
    with col1:
        altura = st.slider("Altura (cm):", 130, 210, 175)
    
    with col2:
        persistencia = st.slider("Persistência (0-10):", 0.0, 10.0, 5.0, step=0.5)
    
    resultado = system.evaluate(altura, persistencia)
    
    # Mostrar resultados
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    grupo_inicial_score = resultado['resultado']
    if grupo_inicial_score < 3.5:
        grupo = "🟢 INICIAL"
        cor = "#FF6B6B"
    elif grupo_inicial_score < 7:
        grupo = "🟡 INTERMEDIÁRIO"
        cor = "#4ECDC4"
    else:
        grupo = "🔵 AVANÇADO"
        cor = "#45B7D1"
    
    with col1:
        st.markdown(f"### {grupo}")
        st.metric("Score", f"{grupo_inicial_score:.1f}/10")
    
    with col2:
        st.metric("Altura", f"{altura} cm")
        if resultado['altura_a'] > resultado['altura_m'] > resultado['altura_b']:
            st.caption("📊 Classificação: Alta")
        elif resultado['altura_m'] >= max(resultado['altura_a'], resultado['altura_b']):
            st.caption("📊 Classificação: Média")
        else:
            st.caption("📊 Classificação: Baixa")
    
    with col3:
        st.metric("Persistência", f"{persistencia:.1f}/10")
        if resultado['persist_a'] > resultado['persist_m'] > resultado['persist_b']:
            st.caption("📊 Classificação: Alta")
        elif resultado['persist_m'] >= max(resultado['persist_a'], resultado['persist_b']):
            st.caption("📊 Classificação: Média")
        else:
            st.caption("📊 Classificação: Baixa")
    
    # Gráficos de pertencimento
    st.divider()
    st.subheader("📊 Análise de Pertencimento")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico da entrada altura
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=system.altura, y=system.altura_baixa,
            mode='lines', name='Baixa',
            line=dict(color='#FF6B6B', width=2)
        ))
        fig1.add_trace(go.Scatter(
            x=system.altura, y=system.altura_media,
            mode='lines', name='Média',
            line=dict(color='#4ECDC4', width=2)
        ))
        fig1.add_trace(go.Scatter(
            x=system.altura, y=system.altura_alta,
            mode='lines', name='Alta',
            line=dict(color='#45B7D1', width=2)
        ))
        
        fig1.add_vline(x=altura, line_dash="dash", line_color="red")
        
        fig1.update_layout(
            title="Funções de Pertencimento: Altura",
            xaxis_title="Altura (cm)",
            yaxis_title="Grau de Pertencimento",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Gráfico da entrada persistência
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=system.persistencia, y=system.persistencia_baixa,
            mode='lines', name='Baixa',
            line=dict(color='#FF6B6B', width=2)
        ))
        fig2.add_trace(go.Scatter(
            x=system.persistencia, y=system.persistencia_media,
            mode='lines', name='Média',
            line=dict(color='#4ECDC4', width=2)
        ))
        fig2.add_trace(go.Scatter(
            x=system.persistencia, y=system.persistencia_alta,
            mode='lines', name='Alta',
            line=dict(color='#45B7D1', width=2)
        ))
        
        fig2.add_vline(x=persistencia, line_dash="dash", line_color="red")
        
        fig2.update_layout(
            title="Funções de Pertencimento: Persistência",
            xaxis_title="Persistência (0-10)",
            yaxis_title="Grau de Pertencimento",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # Gráfico de saída
    st.subheader("🎯 Saída do Sistema")
    
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=system.output, y=resultado['output'],
        mode='lines', name='Saída Fuzzy',
        line=dict(color='#FFB627', width=3),
        fill='tozeroy', fillcolor='rgba(255, 182, 39, 0.3)'
    ))
    
    fig3.add_vline(x=resultado['resultado'], line_dash="dash", line_color="green",
                   annotation_text=f"Output: {resultado['resultado']:.1f}")
    
    fig3.update_layout(
        title="Função de Pertencimento da Saída",
        xaxis_title="Score de Classificação",
        yaxis_title="Grau de Pertencimento",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # Regras aplicadas
    st.divider()
    st.subheader("⚙️ Regras Fuzzy Aplicadas")
    
    regra1_score = min(resultado['altura_a'], resultado['persist_a'])
    regra2_score = min(resultado['altura_b'], resultado['persist_b'])
    regra3_score = max(
        min(resultado['altura_m'], resultado['persist_m']),
        min(resultado['altura_a'], resultado['persist_b'])
    )
    
    cols = st.columns(3)
    
    with cols[0]:
        st.info(f"""
        **Regra 1: Avançado**
        
        SE altura = Alta E persistência = Alta
        
        Ativação: {regra1_score:.2%}
        """)
    
    with cols[1]:
        st.warning(f"""
        **Regra 2: Inicial**
        
        SE altura = Baixa E persistência = Baixa
        
        Ativação: {regra2_score:.2%}
        """)
    
    with cols[2]:
        st.info(f"""
        **Regra 3: Intermediário**
        
        SE (altura = Média E persistência = Média) OU
        (altura = Alta E persistência = Baixa)
        
        Ativação: {regra3_score:.2%}
        """)
    
    # Matriz de decisão
    st.divider()
    st.subheader("📋 Matriz de Decisão")
    
    alturas_teste = [140, 160, 175, 190, 205]
    persistencias_teste = [1, 3, 5, 7, 9]
    
    matriz_resultados = np.zeros((len(persistencias_teste), len(alturas_teste)))
    
    for i, p in enumerate(persistencias_teste):
        for j, a in enumerate(alturas_teste):
            res = system.evaluate(a, p)
            matriz_resultados[i, j] = res['resultado']
    
    fig_matriz = go.Figure(data=go.Heatmap(
        z=matriz_resultados,
        x=[f"{a}cm" for a in alturas_teste],
        y=[f"{p}/10" for p in persistencias_teste],
        colorscale='RdYlGn',
        text=np.round(matriz_resultados, 1),
        texttemplate='%{text}',
        textfont={"size": 12},
        colorbar=dict(title="Score")
    ))
    
    fig_matriz.update_layout(
        title="Matriz de Classificação: Altura vs Persistência",
        xaxis_title="Altura",
        yaxis_title="Persistência",
        height=500
    )
    
    st.plotly_chart(fig_matriz, use_container_width=True)
    
    st.info("""
    💡 **Como ler:**
    - **Vermelho**: Classificação Inicial (baixo score)
    - **Amarelo**: Classificação Intermediária
    - **Verde**: Classificação Avançada (alto score)
    """)

st.sidebar.divider()
st.sidebar.markdown("""
### 📚 Conceitos-Chave

**Lógica Fuzzy:**
- Permite valores entre 0 e 1
- Reflete melhor o mundo real
- Mais humana e intuitiva

**Funções de Pertencimento:**
- Definem como valores são mapeados
- Formas: Triangular, Trapezoidal, Gaussiana, Sigmoide

**Operações Fuzzy:**
- AND (mínimo)
- OR (máximo)
- NOT (complemento)

**Defuzzificação:**
- Converte saída fuzzy em valor crisp
- Métodos: Centroide, Bissetor, Meio do Máximo
""")

st.sidebar.divider()
st.sidebar.markdown("🎯 **Criado com ❤️ para aprender Fuzzy Logic**")
