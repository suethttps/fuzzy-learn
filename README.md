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

## 🚢 Deploy AWS ECS Fargate

Este projeto está preparado para deploy profissional na AWS usando containers, sem Terraform, sem Kubernetes, sem EC2 e sem AWS CLI local.

### Arquitetura

```text
GitHub Actions → Amazon ECR → Amazon ECS Fargate → Application Load Balancer → Usuário
                                      ↓
                              CloudWatch Logs
```

### Estrutura de pastas para produção

```text
fuzzy-learn/
├── .github/
│   └── workflows/
│       └── deploy-ecs.yml          # Pipeline de build, push e deploy no ECS
├── infra/
│   └── ecs/
│       └── task-definition.json    # Template da task definition ECS/Fargate
├── src/
│   └── app.py                      # Aplicação Streamlit
├── utils/
│   └── fuzzy_logic.py              # Regras e funções de lógica fuzzy
├── .dockerignore                   # Reduz contexto de build Docker
├── Dockerfile                      # Imagem de produção
├── docker-compose.yml              # Execução local
├── requirements.txt                # Dependências Python
└── README.md
```

### Nomes usados pela pipeline

| Recurso | Valor padrão |
|---|---|
| Região AWS | `us-east-1` |
| ECR Repository | `fuzzy-learn` |
| ECS Cluster | `fuzzy-learn-cluster` |
| ECS Service | `fuzzy-learn-service` |
| ECS Task Family | `fuzzy-learn-task` |
| Container | `fuzzy-learn-app` |
| Container Port | `8501` |
| CloudWatch Log Group | `/ecs/fuzzy-learn` |

Se usar outra região ou outros nomes, atualize o bloco `env` em `.github/workflows/deploy-ecs.yml` e mantenha os mesmos nomes no Console da AWS.

### GitHub Secrets obrigatórios

Crie estes secrets em `Settings` → `Secrets and variables` → `Actions` → `New repository secret`:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_ACCOUNT_ID
```

Nunca versione chaves, tokens, arquivos `.env`, credenciais IAM ou dados reais da conta AWS. O arquivo `infra/ecs/task-definition.json` usa apenas os placeholders públicos `AWS_ACCOUNT_ID_PLACEHOLDER` e `AWS_REGION_PLACEHOLDER`.

### Como a pipeline funciona

O workflow `.github/workflows/deploy-ecs.yml` executa automaticamente em push para `main` ou `master`, e também pode ser executado manualmente por `workflow_dispatch`.

Fluxo executado:

1. Faz checkout do repositório.
2. Autentica na AWS usando GitHub Secrets.
3. Faz login no Amazon ECR.
4. Cria a imagem Docker de produção.
5. Publica a imagem no ECR com a tag do commit SHA e também com `latest`.
6. Substitui os placeholders públicos da task definition.
7. Renderiza a task definition com a nova imagem.
8. Registra uma nova revisão da task definition.
9. Atualiza o ECS Service.
10. Aguarda o ECS Service ficar estável.

## Tutorial AWS Console sem CLI

Todos os passos abaixo são feitos pelo painel da AWS. Não é necessário usar Terraform, Kubernetes, EC2 ou AWS CLI local.

Observação: alguns recursos como Load Balancer, Target Groups e Security Groups ficam no menu `EC2` do Console da AWS, mas nenhuma instância EC2 deve ser criada.

### 1. Escolher região

Use a mesma região configurada no workflow. O padrão deste repositório é `us-east-1`.

### 2. Criar ECR Repository

1. Acesse `Amazon ECR` → `Repositories` → `Create repository`.
2. Escolha `Private`.
3. Nome do repositório: `fuzzy-learn`.
4. Ative `Scan on push` se disponível.
5. Crie o repositório.
6. Opcional para custo: adicione lifecycle policy para manter apenas as últimas 10 imagens.

### 3. Criar IAM Role da task ECS

1. Acesse `IAM` → `Roles` → `Create role`.
2. Trusted entity: `AWS service`.
3. Use case: `Elastic Container Service Task`.
4. Adicione a policy gerenciada `AmazonECSTaskExecutionRolePolicy`.
5. Nome da role: `ecsTaskExecutionRole`.
6. Crie a role.

Essa role permite que o ECS Fargate baixe a imagem do ECR e envie logs para o CloudWatch.

### 4. Criar usuário IAM para GitHub Actions

1. Acesse `IAM` → `Users` → `Create user`.
2. Nome sugerido: `github-actions-fuzzy-learn`.
3. Crie uma access key para `Application running outside AWS`.
4. Salve o `Access key ID` e o `Secret access key` apenas nos GitHub Secrets.
5. Anexe uma policy com permissões mínimas para ECR, ECS e PassRole.

Policy sugerida, substituindo os placeholders antes de salvar no Console:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ecr:GetAuthorizationToken",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecr:BatchCheckLayerAvailability",
        "ecr:BatchGetImage",
        "ecr:CompleteLayerUpload",
        "ecr:DescribeRepositories",
        "ecr:InitiateLayerUpload",
        "ecr:PutImage",
        "ecr:UploadLayerPart"
      ],
      "Resource": "arn:aws:ecr:AWS_REGION_PLACEHOLDER:AWS_ACCOUNT_ID_PLACEHOLDER:repository/fuzzy-learn"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecs:DescribeServices",
        "ecs:DescribeTaskDefinition",
        "ecs:RegisterTaskDefinition",
        "ecs:UpdateService"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "arn:aws:iam::AWS_ACCOUNT_ID_PLACEHOLDER:role/ecsTaskExecutionRole",
      "Condition": {
        "StringEquals": {
          "iam:PassedToService": "ecs-tasks.amazonaws.com"
        }
      }
    }
  ]
}
```

Para uma entrevista técnica, explique que o próximo passo recomendado é trocar access keys por OIDC com trust policy do GitHub Actions.

### 5. Criar CloudWatch Logs

1. Acesse `CloudWatch` → `Logs` → `Log groups` → `Create log group`.
2. Nome: `/ecs/fuzzy-learn`.
3. Retention: `7 days` ou `14 days` para controlar custo.
4. Crie o log group.

### 6. Criar ECS Cluster

1. Acesse `Amazon ECS` → `Clusters` → `Create cluster`.
2. Nome: `fuzzy-learn-cluster`.
3. Infrastructure: `AWS Fargate`.
4. Crie o cluster.

### 7. Criar Security Groups

Use a VPC padrão ou uma VPC já existente. Para baixo custo e simplicidade, use subnets públicas com `Assign public IP` habilitado nas tasks e bloqueie acesso direto ao container pelo Security Group.

Security Group do Load Balancer:

```text
Nome: fuzzy-learn-alb-sg
Inbound: HTTP TCP 80 de 0.0.0.0/0
Outbound: All traffic
```

Security Group das tasks ECS:

```text
Nome: fuzzy-learn-ecs-sg
Inbound: TCP 8501 com origem no Security Group fuzzy-learn-alb-sg
Outbound: All traffic
```

### 8. Criar Target Group

1. Acesse `EC2` → `Target Groups` → `Create target group`.
2. Target type: `IP addresses`.
3. Nome: `fuzzy-learn-tg`.
4. Protocol: `HTTP`.
5. Port: `8501`.
6. VPC: a mesma usada pelo ECS.
7. Health check path: `/_stcore/health`.
8. Success codes: `200-399`.
9. Crie sem registrar targets manualmente. O ECS fará isso pelo service.

### 9. Criar Application Load Balancer

1. Acesse `EC2` → `Load Balancers` → `Create load balancer`.
2. Tipo: `Application Load Balancer`.
3. Nome: `fuzzy-learn-alb`.
4. Scheme: `Internet-facing`.
5. IP address type: `IPv4`.
6. Selecione pelo menos duas subnets públicas.
7. Security Group: `fuzzy-learn-alb-sg`.
8. Listener: `HTTP:80` encaminhando para `fuzzy-learn-tg`.
9. Crie o load balancer.

### 10. Criar Task Definition

1. Acesse `Amazon ECS` → `Task definitions` → `Create new task definition`.
2. Launch type: `AWS Fargate`.
3. Task definition family: `fuzzy-learn-task`.
4. CPU: `1 vCPU`.
5. Memory: `2 GB`.
6. Task execution role: `ecsTaskExecutionRole`.
7. Container name: `fuzzy-learn-app`.
8. Image URI: `AWS_ACCOUNT_ID.dkr.ecr.AWS_REGION.amazonaws.com/fuzzy-learn:latest`.
9. Container port: `8501`.
10. Log driver: `awslogs`.
11. Log group: `/ecs/fuzzy-learn`.
12. Stream prefix: `ecs`.

O arquivo `infra/ecs/task-definition.json` é a fonte versionada do template usado pela pipeline. No Console, substitua manualmente `AWS_ACCOUNT_ID` e `AWS_REGION` pelos valores reais apenas no painel da AWS, nunca no repositório.

### 11. Criar ECS Service

1. Acesse o cluster `fuzzy-learn-cluster`.
2. Clique em `Create` em `Services`.
3. Launch type: `Fargate`.
4. Task definition family: `fuzzy-learn-task`.
5. Service name: `fuzzy-learn-service`.
6. Desired tasks: `1`.
7. Networking: escolha as mesmas subnets públicas do ALB.
8. Public IP: `Enabled`.
9. Security Group: `fuzzy-learn-ecs-sg`.
10. Load balancer: selecione `Application Load Balancer`.
11. Container: `fuzzy-learn-app:8501`.
12. Target group: `fuzzy-learn-tg`.
13. Crie o service.

Se a imagem `latest` ainda não existir no ECR no primeiro setup, crie o service com `Desired tasks = 0`, execute o workflow do GitHub Actions para publicar a imagem e registrar a nova revisão, depois volte ao Console e ajuste `Desired tasks = 1`. A partir daí, todo push para `main` ou `master` faz deploy automaticamente.

### 12. Testar o acesso

1. Acesse `EC2` → `Load Balancers`.
2. Copie o DNS do `fuzzy-learn-alb`.
3. Abra no navegador usando `http://DNS_DO_LOAD_BALANCER`.
4. Confira os logs em `CloudWatch` → `Log groups` → `/ecs/fuzzy-learn`.

### Melhorias opcionais futuras

1. Domínio customizado no Route 53.
2. HTTPS com AWS Certificate Manager e listener `443` no ALB.
3. OIDC do GitHub Actions no lugar de `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY`.
4. Autoscaling do ECS Service por CPU ou memória.
5. Blue/Green deploy com CodeDeploy.
6. ECS tasks em subnets privadas com NAT Gateway ou VPC endpoints para ECR/CloudWatch.
7. Alarmes no CloudWatch para erro de health check, CPU, memória e reinícios.
8. Lifecycle policy no ECR para reduzir custo de armazenamento.

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
├── .github/workflows/
│   └── deploy-ecs.yml       # Deploy automatizado AWS ECS Fargate
├── infra/ecs/
│   └── task-definition.json # Template da task definition ECS
├── src/
│   └── app.py               # Aplicativo Streamlit principal
├── utils/
│   └── fuzzy_logic.py       # Lógica fuzzy (FuzzySystem, HeightPersistenceSystem)
├── .dockerignore            # Arquivos ignorados no build Docker
├── Dockerfile               # Imagem de produção
├── docker-compose.yml       # Execução local com Docker
├── requirements.txt         # Dependências Python
├── .gitignore               # Arquivos ignorados pelo Git
└── README.md                # Este arquivo
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
