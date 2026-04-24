# 🎯 Fuzzy Logic Explorer

Um aplicativo interativo para aprender e explorar **Lógica Fuzzy** usando Python, Streamlit e Scikit-Fuzzy.

## 📋 Características

✅ **Conjuntos Fuzzy** - Entenda como funcionam valores entre 0 e 1  
✅ **Funções de Pertencimento** - Triangular, Trapezoidal, Gaussiana, Sigmoide  
✅ **Sistema de Classificação** - Altura + Persistência → Grupo (Inicial/Intermediário/Avançado)  
✅ **Gráficos Interativos** - Plotly para visualizações dinâmicas  
✅ **Matriz de Decisão** - Veja como o sistema classifica diferentes combinações  
✅ **Análise em Tempo Real** - Ajuste valores e veja as mudanças instantaneamente  

## 🚀 Quick Start

### 1. Clone o repositório
```bash
cd /home/soethe/codeneed_workspace/fuzzy-learn
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Execute o Streamlit
```bash
streamlit run src/app.py
```

O aplicativo abrirá em `http://localhost:8501`

## 📖 Como Usar

### 1. **Conjuntos Fuzzy**
- Ajuste a altura no slider
- Veja em tempo real como o valor pertence aos conjuntos "Baixa", "Média" e "Alta"
- Entenda o conceito de pertencimento parcial

### 2. **Funções de Pertencimento**
- Escolha diferentes tipos de funções
- Veja a fórmula e os parâmetros
- Compare todas as funções lado a lado

### 3. **Sistema de Altura e Persistência**
- **Entrada 1**: Altura (130-210 cm)
- **Entrada 2**: Persistência (0-10)
- **Saída**: Score de classificação (0-10)
  - 0-3.5: 🟢 INICIAL
  - 3.5-7: 🟡 INTERMEDIÁRIO
  - 7-10: 🔵 AVANÇADO

## 🧠 Conceitos-Chave

### Lógica Fuzzy vs Clássica

**Clássica:**
```
SE altura >= 180 ENTÃO "Alto"
SENÃO "Não Alto"
```

**Fuzzy:**
```
SE altura = "Alto" (grau: 0.7)
   E persistência = "Alta" (grau: 0.8)
ENTÃO classificação = "Avançado" (grau: min(0.7, 0.8) = 0.7)
```

### Operações Fuzzy

- **AND**: Mínimo entre os graus
- **OR**: Máximo entre os graus
- **NOT**: 1 - grau

### Defuzzificação

Converte a saída fuzzy em um valor crisp (número):
- **Centroide**: Centro de massa da área
- **Bissetor**: Valor que divide a área em dois
- **Meio do Máximo**: Ponto médio dos valores máximos

## 📁 Estrutura do Projeto

```
fuzzy-learn/
├── src/
│   └── app.py              # Aplicativo Streamlit principal
├── utils/
│   └── fuzzy_logic.py      # Lógica fuzzy (FuzzySystem, HeightPersistenceSystem)
├── requirements.txt         # Dependências Python
├── .gitignore              # Arquivos ignorados pelo Git
└── README.md               # Este arquivo
```

## 🛠️ Tecnologias

| Tecnologia | Propósito |
|---|---|
| **Streamlit** | Framework web interativo |
| **Scikit-Fuzzy** | Biblioteca de lógica fuzzy |
| **NumPy** | Computação numérica |
| **Matplotlib** | Gráficos estáticos |
| **Plotly** | Gráficos interativos |
| **Pandas** | Manipulação de dados |

## 📚 Referências

- [Scikit-Fuzzy Documentation](https://scikit-fuzzy.github.io/)
- [Fuzzy Logic Introduction](https://en.wikipedia.org/wiki/Fuzzy_logic)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 💡 Exemplos de Uso

### Exemplo 1: Classificar um aluno
1. Altura: 185 cm
2. Persistência: 8/10
3. **Resultado**: Avançado ✅

### Exemplo 2: Matriz de decisão
Veja como o sistema classifica **todas as combinações** de altura e persistência

## 🎓 Aprendizado

Use este projeto para entender:
- ✅ Como trabalham sistemas fuzzy em tempo real
- ✅ Diferença entre lógica clássica e fuzzy
- ✅ Como visualizar dados fuzzy
- ✅ Aplicações práticas de lógica fuzzy

## 📝 Notas

- Não requer login ou autenticação
- Todos os dados são processados localmente
- Interface simples e intuitiva
- Gráficos interativos em tempo real

## 🤝 Contribuições

Melhorias sugeridas:
- Adicionar mais sistemas fuzzy (controle de temperatura, etc.)
- Novos tipos de funções de pertencimento
- Exportar gráficos em PDF
- Adicionar exemplos de casos reais

---

**Criado com ❤️ para aprender Fuzzy Logic**
