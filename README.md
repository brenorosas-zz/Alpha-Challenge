# Alpha-Challenge

Esse projeto do processo seletivo para estágio na Inoa sistemas.

# Requisitos

Criar um sistema que auxilie um investidor nas decisões de compra e venda de ativos. Registrando periodicamente a cotação atual de ativos da B3 e avisando via e-mail caso haja oportunidade de negociação.

O tempo para periodicidade do registro será informado pelo investidor, sendo único para cada ativo que o mesmo escolher. O mesmo também poderá setar um limite superior e um inferior, que ao serem cruzados um aviso será enviado para e-mail registrado.

O sistema foi feito em Python com Django visando conhecer as tecnologias usadas na empresa.

## Instalação

```bash
git clone https://github.com/brenorosas/Alpha-Challenge.git
cd Alpha-Challenge
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Após instalação, é necessário usar o .env.example como base para criar um novo arquivo .env como mostrado abaixo:

```bash
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DJANGO_KEY=Your django secret key
EMAIL_ADDRESS="example@gmail.com"
EMAIL_PASSWORD=Your gmail password
```

Se seu gmail tiver identificação por dois fatores, use um [app password](https://support.google.com/accounts/answer/185833).

Possivelmente será preciso alterar as permissões no seu gmail para permitir acesso de aplicativos com menor segurança.

## Requisitos para funcionamento do sistema.

Para rodar a aplicação, 'docker' e 'docker-compose' precisam estar instalados em seu sistema.
Siga as instruções no docs do docker para instalação [docs](https://docs.docker.com/compose/install/).

#### Compose

Para rodar a aplicação apenas execute:

```bash
docker-compose up
```

Para remover todos os containers em execução use:

```bash
docker-compose down -v
```

Você pode ver o website no seu navegador acessando o link [link](localhost:8000)

## Funcionalidades
#### Home Page
Mostra apenas o nome do projeto.

#### Registro de conta.
Clique em "Register", insira seus dados e submeta, se tudo ocorrer bem você será redirecionado para a home page.

#### Logando no site.
Clique em "Login", insira os dados que foram registrados e submeta, se tudo ocrrer bem você será redirecionado para seu perfil.

#### Visualização do perfil.
Já logado, o nome e sobrenome informados no registro aparecerá no topo do site e haverá algumas opções na barra superior:

Assets, Monitoring Assets e Logout.

#### Visualização dos assets.
Estando logado, clique em "Assets", vários tickers de ativos serão listados, ao clicar em algum em um dos tickers maiores detalhes do mesmo serão exibidas junto com um formulário para monitoramento.

#### Monitorar ativo.
Na página de visualização dos assets, clique no ativo que deseja monitorar, na página de detalhes do mesmo terá um formulário, preencha o mesmo e submeta para começar o monitoramento.

#### Visualizando ativos monitorados.
Na página de perfil clique na opção "Monitoring Assets", lá haverá todos os ativos que estão sendo monitorados no momento:

Ticker, a periodicidade, o limite superior e inferior de cada um. 

Ao clicar no botão "Remove Asset" o mesmo irá parar de ser monitorado e sairá da lista.

#### Deslogando do site.
Estando logado, no canto superior direito haverá um botão de "Logout", apenas clique no mesmo e você será redirecionado para home page.