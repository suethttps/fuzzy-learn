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

### 2. Criar um ambiente virtual Python (venv)

**No Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**No Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

Você saberá que o venv está ativo quando a linha de comando mostrar `(.venv)` no início.

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute o Streamlit
```bash
streamlit run src/app.py
```

O aplicativo abrirá em `http://localhost:8501`

### 5. Desativar o venv (quando terminar)
```bash
deactivate
```

## 🐳 Alternativa: Executar com Docker

Se preferir usar Docker, siga os passos abaixo:

### 1. Build e execute:
```bash
docker-compose up --build
```

### 2. Acesse em seu navegador:
```
http://localhost:8501
```

### 3. Para parar:
```bash
docker-compose down
```

### Comandos úteis com Docker:

- **Logs em tempo real:**
  ```bash
  docker-compose logs -f
  ```

- **Rebuild sem cache:**
  ```bash
  docker-compose up --build --no-cache
  ```

- **Remover volumes:**
  ```bash
  docker-compose down -v
  ```

- **Executar bash no container:**
  ```bash
  docker-compose exec fuzzy-learn bash
  ```

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

## 🔧 Troubleshooting

### Problemas com venv

**Problema**: `python3 command not found` / `python command not found`  
**Solução**: Verifique se Python está instalado: `python --version` ou `python3 --version`

**Problema**: venv já criado mas não ativa  
**Solução**: Remova e recrie:
```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
```

**Problema**: Ainda recebe "command not found" após ativar venv  
**Solução**: Certifique-se de que o comando foi executado corretamente:
```bash
# Verifique se você está no diretório correto
pwd

# Tente novamente
source .venv/bin/activate
```

### Problemas com dependências

**Problema**: `pip: command not found`  
**Solução**: O venv não está ativado. Execute:
```bash
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

**Problema**: Erro ao instalar scikit-fuzzy  
**Solução**: Atualize pip primeiro:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Executar novamente após fechar o terminal

```bash
# 1. Navegue para o diretório do projeto
cd /home/soethe/codeneed_workspace/fuzzy-learn

# 2. Ative o venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# 3. Execute a aplicação
streamlit run src/app.py
```

## 🤝 Contribuições

Melhorias sugeridas:
- Adicionar mais sistemas fuzzy (controle de temperatura, etc.)
- Novos tipos de funções de pertencimento
- Exportar gráficos em PDF
- Adicionar exemplos de casos reais

---

**Criado com ❤️ para aprender Fuzzy Logic**
