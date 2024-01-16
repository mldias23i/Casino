Desafio Técnico - Platform Casino Integration API

Este documento descreve a solução que implementei para o desafio técnico proposto:

 - Implementação dos endpoints getGames, GameLaunch, Bet, Win e Refund
 - Transações Bet, Win e Refund registadas num banco de dados em Postgres  
 - Implementação de 2 ou 3 códigos de erro da API  - Uso da autenticação dos pedidos conforme descrito no documento

Estrutura do Projeto

O projeto é uma API desenvolvida em Django, que fornece endpoints para realizar várias operações. A estrutura geral do projeto é a seguinte:

casino - App do projeto que contém as views e a lógica do projeto
utils.py - Contém as funções utilitárias ao projeto 
betLogic.py - Lógica relacionada com as apostas, separada do ficheiro views.py, para mostrar que há escolha entre implementar tudo no ficheiro views.py ou em vários ficheiros com diferentes classes. 
models.py - Definição dos modelos de dados da base de dados. 
tests.py - Testes unitários para os endpoints bet, win e refund. 
views.py - As views da API, que respondem às solicitações.

Execução do projeto

Para executar o projeto é necessário:  
 - Ter o python instalado  
 - Executar as migrações:  
    - python manage.py makemigrations  
    - python manage.py migrate
 - Iniciar o servidor de desenvolvimento:  
    - python manage.py runserver

A API estará acessível em http://localhost:8000. 
No ficheiro settings.py é possível fazer alterações a algumas configurações, como por exemplo, a
base de dados que está a ser utilizada. Neste projeto é utilizada uma base de dados PostgreSQL e devem ser alterados os dados de autenticação no ficheiro settings.py.

Endpoints da API

 - '/getGames': Obtém a lista de jogos disponíveis  
 - '/gameLaunch': Fornece um URL para lançar um jogo  
 - '/bet': Processa uma aposta  
 - '/win': Processa um ganho  
 - '/refund': Processa um reembolso

Para testar estes endpoints pode ser utilizada a ferramenta Postman. Os requests devem ser feitos com o método POST.
O url para teste deve ser: http://127.0.0.1:8000/ seguido do endpoint a ser testado.
Os tokens e chaves secretas foram adicionados hardcoded. Num ambiente de produção real devem ser utilizados os valores reais.

Testes Unitários

O projeto inclui testes unitários para as funcionalidades principais.
Podem ser executados da seguinte forma:
    
    - python manage.py test casino

Conclusão

Este projeto é uma solução para o desafio técnico proposto.
