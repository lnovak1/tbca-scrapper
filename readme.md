O intuito desse script é produzir de um forma facil a criacao de tabelas auxiliares de nutrientes.

para roda-lo é necessário ter o python 3 em sua maquina(https://www.python.org/)

na pasta do projeto abra o terminal e digite ```pip install -r requirements.txt```

para buscar os dados das tabelas do TBCA use ```python tbca_scrapper.py```
(PS.: esse processo e lento e pode demorar de minutos a horas dependendo da velocidade de resposta do servidor)

para criar a planilha altere a variavel *ALIMENT_INTAKE* dentro de table_generator.py com os valores desejados salve e use no terminal ```python table_generator.py```