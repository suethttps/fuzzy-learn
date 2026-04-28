import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.fuzzy_logic import FuzzySystem, HeightPersistenceSystem


class ConjuntoFuzzy:
    def __init__(self, nome: str, elementos: dict):
        self.nome = nome
        self.elementos = elementos
    
    def __str__(self):
        items = [f"{grau}/{elem}" for elem, grau in self.elementos.items()]
        return f"{self.nome} = {{ {', '.join(items)} }}"
    
    def suporte(self):
        return [elem for elem, grau in self.elementos.items() if grau > 0]
    
    def nucleo(self):
        return [elem for elem, grau in self.elementos.items() if grau == 1]
    
    def cardinalidade(self):
        return sum(self.elementos.values())
    
    def cardinalidade_escalar(self):
        if len(self.elementos) == 0:
            return 0
        return self.cardinalidade() / len(self.elementos)
    
    def complemento(self):
        novo_elementos = {elem: 1 - grau for elem, grau in self.elementos.items()}
        return ConjuntoFuzzy(f"{self.nome}'", novo_elementos)
    
    def uniao(self, outro):
        todos_elems = set(self.elementos.keys()) | set(outro.elementos.keys())
        novo_elementos = {}
        for elem in todos_elems:
            grau_a = self.elementos.get(elem, 0)
            grau_b = outro.elementos.get(elem, 0)
            novo_elementos[elem] = max(grau_a, grau_b)
        return ConjuntoFuzzy(f"({self.nome} ∪ {outro.nome})", novo_elementos)
    
    def intersecao(self, outro):
        todos_elems = set(self.elementos.keys()) | set(outro.elementos.keys())
        novo_elementos = {}
        for elem in todos_elems:
            grau_a = self.elementos.get(elem, 0)
            grau_b = outro.elementos.get(elem, 0)
            novo_elementos[elem] = min(grau_a, grau_b)
        return ConjuntoFuzzy(f"({self.nome} ∩ {outro.nome})", novo_elementos)
    
    def potencia(self, p):
        novo_elementos = {elem: grau ** p for elem, grau in self.elementos.items()}
        return ConjuntoFuzzy(f"{self.nome}^{p}", novo_elementos)
    
    def multiplicacao_escalar(self, k):
        novo_elementos = {elem: min(k * grau, 1.0) for elem, grau in self.elementos.items()}
        return ConjuntoFuzzy(f"{k}×{self.nome}", novo_elementos)
    
    def alfa_corte(self, alfa):
        novo_elementos = {elem: grau for elem, grau in self.elementos.items() if grau >= alfa}
        return ConjuntoFuzzy(f"A_{{{alfa}}}", novo_elementos)

st.set_page_config(page_title="Fuzzy Logic Explorer", layout="wide", initial_sidebar_state="expanded")

st.title("🎯 Explorador de Lógica Fuzzy")
st.markdown("""
Aprenda sobre conjuntos fuzzy, funções de pertencimento e sistemas de classificação com exemplos interativos.
""")

# Menu principal
menu = st.sidebar.radio(
    "Escolha um tópico:",
    ["Conjuntos Fuzzy", "Funções de Pertencimento", "Sistema de Altura e Persistência", "Exercícios Interativos"]
)

if menu == "Exercícios Interativos":
    st.header("🧮 Exercícios: Operações com Conjuntos Fuzzy")
    st.markdown("""
    Aprenda a realizar operações com conjuntos fuzzy. Defina os elementos e seus graus de pertencimento para cada conjunto.
    """)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📥 Definir Conjunto A")
        elementos_a_input = st.text_area(
            "Elementos do Conjunto A (formato: elemento:grau, ex: a:0.2, b:0.4)",
            value="a:0.2, b:0.4, c:1.0, d:0.8, e:0.0",
            height=100,
            key="conjunto_a"
        )
    
    with col2:
        st.subheader("📥 Definir Conjunto B")
        elementos_b_input = st.text_area(
            "Elementos do Conjunto B (formato: elemento:grau, ex: a:0.0, b:0.9)",
            value="a:0.0, b:0.9, c:0.3, d:0.2, e:0.1",
            height=100,
            key="conjunto_b"
        )
    
    def parse_conjunto(input_str, nome):
        elementos = {}
        try:
            for item in input_str.split(','):
                item = item.strip()
                if ':' in item:
                    elem, grau = item.split(':')
                    elementos[elem.strip()] = float(grau.strip())
            return elementos
        except:
            st.error(f"Erro ao analisar {nome}. Use o formato: elemento:grau")
            return {}
    
    elementos_a = parse_conjunto(elementos_a_input, "Conjunto A")
    elementos_b = parse_conjunto(elementos_b_input, "Conjunto B")
    
    if elementos_a and elementos_b:
        A = ConjuntoFuzzy("A", elementos_a)
        B = ConjuntoFuzzy("B", elementos_b)
        
        st.divider()
        st.subheader("📊 Conjuntos Definidos")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Conjunto A:**")
            for elem, grau in A.elementos.items():
                st.write(f"  μ_A({elem}) = {grau}")
        
        with col2:
            st.markdown(f"**Conjunto B:**")
            for elem, grau in B.elementos.items():
                st.write(f"  μ_B({elem}) = {grau}")
        
        st.divider()
        
        operacao = st.selectbox(
            "Selecione a operação:",
            [
                "Análise do Conjunto A",
                "Análise do Conjunto B",
                "União (A ∪ B)",
                "Interseção (A ∩ B)",
                "Complemento de A (A')",
                "Complemento de B (B')",
                "Potência (A²)",
                "Multiplicação Escalar (k × B)",
                "Alfa-Corte (A_α)",
                "Ver Todas as Operações"
            ]
        )
        
        st.divider()
        
        if operacao == "Análise do Conjunto A":
            st.subheader("🔍 Análise do Conjunto A")
            
            suporte_a = A.suporte()
            nucleo_a = A.nucleo()
            card_a = A.cardinalidade()
            card_escalar_a = A.cardinalidade_escalar()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Suporte", f"{{{', '.join(suporte_a)}}}")
                st.caption("Elementos com grau > 0")
            with col2:
                st.metric("Núcleo", f"{{{', '.join(nucleo_a)}}}" if nucleo_a else "∅")
                st.caption("Elementos com grau = 1")
            
            st.metric("Cardinalidade", f"{card_a:.2f}")
            st.caption("Soma de todos os graus de pertencimento")
            
            st.subheader("📝 Complemento de A (A')")
            A_complemento = A.complemento()
            for elem, grau in A_complemento.elementos.items():
                grau_original = A.elementos[elem]
                st.write(f"μ_A'({elem}) = 1 - {grau_original} = {grau}")
        
        elif operacao == "Análise do Conjunto B":
            st.subheader("🔍 Análise do Conjunto B")
            
            suporte_b = B.suporte()
            nucleo_b = B.nucleo()
            card_b = B.cardinalidade()
            card_escalar_b = B.cardinalidade_escalar()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Suporte", f"{{{', '.join(suporte_b)}}}")
                st.caption("Elementos com grau > 0")
            with col2:
                st.metric("Núcleo", f"{{{', '.join(nucleo_b)}}}" if nucleo_b else "∅")
                st.caption("Elementos com grau = 1")
            
            st.metric("Cardinalidade", f"{card_b:.2f}")
            st.caption("Soma de todos os graus de pertencimento")
            
            st.subheader("📝 Complemento de B (B')")
            B_complemento = B.complemento()
            for elem, grau in B_complemento.elementos.items():
                grau_original = B.elementos[elem]
                st.write(f"μ_B'({elem}) = 1 - {grau_original} = {grau}")
        
        elif operacao == "União (A ∪ B)":
            st.subheader("🔗 União: A ∪ B")
            st.markdown("**Fórmula:** μ_(A∪B)(x) = max(μ_A(x), μ_B(x))")
            
            uniao = A.uniao(B)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Resultado:**")
                for elem, grau in uniao.elementos.items():
                    grau_a = A.elementos.get(elem, 0)
                    grau_b = B.elementos.get(elem, 0)
                    st.write(f"{elem}: max({grau_a}, {grau_b}) = {grau}")
            with col2:
                st.markdown("**Expressão:**")
                st.code(f"{uniao}")
        
        elif operacao == "Interseção (A ∩ B)":
            st.subheader("🔗 Interseção: A ∩ B")
            st.markdown("**Fórmula:** μ_(A∩B)(x) = min(μ_A(x), μ_B(x))")
            
            intersecao = A.intersecao(B)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Resultado:**")
                for elem, grau in intersecao.elementos.items():
                    grau_a = A.elementos.get(elem, 0)
                    grau_b = B.elementos.get(elem, 0)
                    st.write(f"{elem}: min({grau_a}, {grau_b}) = {grau}")
            with col2:
                st.markdown("**Expressão:**")
                st.code(f"{intersecao}")
        
        elif operacao == "Complemento de A (A')":
            st.subheader("📝 Complemento: A'")
            st.markdown("**Fórmula:** μ_A'(x) = 1 - μ_A(x)")
            
            A_complemento = A.complemento()
            
            for elem, grau in A_complemento.elementos.items():
                grau_original = A.elementos[elem]
                st.write(f"μ_A'({elem}) = 1 - {grau_original} = {grau}")
        
        elif operacao == "Complemento de B (B')":
            st.subheader("📝 Complemento: B'")
            st.markdown("**Fórmula:** μ_B'(x) = 1 - μ_B(x)")
            
            B_complemento = B.complemento()
            
            for elem, grau in B_complemento.elementos.items():
                grau_original = B.elementos[elem]
                st.write(f"μ_B'({elem}) = 1 - {grau_original} = {grau}")
        
        elif operacao == "Potência (A²)":
            st.subheader("⚡ Potência: A²")
            st.markdown("**Fórmula:** μ_A²(x) = (μ_A(x))²")
            
            C = A.potencia(2)
            
            for elem, grau in C.elementos.items():
                grau_a = A.elementos[elem]
                st.write(f"μ_A²({elem}) = ({grau_a})² = {grau}")
        
        elif operacao == "Multiplicação Escalar (k × B)":
            st.subheader("✖️ Multiplicação Escalar")
            
            k = st.slider("Valor de k:", 0.1, 2.0, 0.5, step=0.1)
            st.markdown(f"**Fórmula:** μ_{{k×B}}(x) = min(k × μ_B(x), 1)")
            
            D = B.multiplicacao_escalar(k)
            
            for elem, grau in D.elementos.items():
                grau_b = B.elementos[elem]
                st.write(f"μ_{{ {k}×B }}({elem}) = min({k} × {grau_b}, 1) = {grau}")
        
        elif operacao == "Alfa-Corte (A_α)":
            st.subheader("✂️ Alfa-Corte: A_α")
            
            alfa = st.slider("Valor de α (alfa):", 0.0, 1.0, 0.5, step=0.1)
            st.markdown(f"**Fórmula:** A_α = {{x ∈ X | μ_A(x) ≥ {alfa}}}")
            
            E = A.alfa_corte(alfa)
            
            st.markdown("**Elementos incluídos (grau ≥ α):**")
            for elem in sorted(A.elementos.keys()):
                grau = A.elementos[elem]
                status = "✓" if grau >= alfa else "✗"
                st.write(f"{status} {elem}: {grau} ({'incluído' if grau >= alfa else 'excluído'})")
        
        elif operacao == "Ver Todas as Operações":
            st.subheader("📋 Resumo de Todas as Operações")
            
            suporte_a = A.suporte()
            nucleo_a = A.nucleo()
            card_a = A.cardinalidade()
            suporte_b = B.suporte()
            nucleo_b = B.nucleo()
            card_b = B.cardinalidade()
            uniao = A.uniao(B)
            intersecao = A.intersecao(B)
            A_comp = A.complemento()
            B_comp = B.complemento()
            C = A.potencia(2)
            
            with st.expander("📊 CONJUNTO A", expanded=True):
                st.write(f"**Suporte:** {{{', '.join(suporte_a)}}}")
                st.write(f"**Núcleo:** {{{', '.join(nucleo_a)}}}")
                st.write(f"**Cardinalidade:** {card_a:.2f}")
                st.write(f"**Complemento:** {A_comp}")
            
            with st.expander("📊 CONJUNTO B", expanded=True):
                st.write(f"**Suporte:** {{{', '.join(suporte_b)}}}")
                st.write(f"**Núcleo:** {{{', '.join(nucleo_b) if nucleo_b else 'vazio'}}}")
                st.write(f"**Cardinalidade:** {card_b:.2f}")
                st.write(f"**Complemento:** {B_comp}")
            
            with st.expander("🔗 OPERAÇÕES", expanded=True):
                st.write(f"**União (A ∪ B):** {uniao}")
                st.write(f"**Interseção (A ∩ B):** {intersecao}")
                st.write(f"**A²:** {C}")
                st.write(f"**0.5 × B:** {B.multiplicacao_escalar(0.5)}")
                st.write(f"**A₀.₅ (corte):** {A.alfa_corte(0.5)}")
    
    else:
        st.warning("⚠️ Defina ambos os conjuntos A e B para continuar.")

elif menu == "Conjuntos Fuzzy":
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
