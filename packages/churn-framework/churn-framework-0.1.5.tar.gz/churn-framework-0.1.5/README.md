# Churn Framework
Encontre métricas que melhor separam clientes recorrentes de clientes que cancelaram o contrato durante a joranada de uso do produto/serviço.

Auxílio na definição de possíveis pontos de corte para potenciais métricas de um possível indício de Churn durante a jornada de um cliente.

- Identificação de pontos de corte que melhor diferenciam clientes de sucesso de clientes que sofreram um churn prematuro
- Identificação de métricas cujo ponto de corte determinam um alerta para Churn nos primeiros meses da jornada do cliente


## Instalação

##### Dependências:
- Python (>=3.6)
- Seaborn
- Tqdm 
##### Instalar:

```sh
pip install churn-framework

```

## Documentação

Descrição das funcionalidades de cada função presente no script churn_framework:

### Funções
-   **get_great_value** - Função que encontra o valor ideal para um ou mais features com base em restrições definidas que melhor dividem clientes recorrentes de clientes que sofreram Churn, para cada mês da jornada do cliente.
-   **plot_metrics**  - Método que plota métricas de avaliação para cada valor testado no framework em um determinado mês, enfatizando o ponto ótimo encontrado.

![](images/metrics.png)

-   **get_confusion_matrix**  - Método que retorna valores de matriz de confusão Cliente / Churn para um mês específico.
-   **plot_matrix**  - Método que traça a matriz de confusão Cliente / Churn.

![](images/matrix.png)

Também fornecemos um bloco de notas passo a passo. Para visualizá-lo, basta digitar jupyter notebook dentro do diretório
`/src/notebooks`.



## License

MIT


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
