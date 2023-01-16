

# LIDAR PROCESSING

 O LIDAR é um equipamento cuja finalidade é nos fornecer um conjunto de pontos que descreve o ambiente a sua volta com precisão. O nosso objetivo é, a partir de um conjunto de pontos(denominado de Point Cloud) da pista de corrida, conseguir reconhecer onde estão posicionados os cones.

## Funcionamento

Para reconhecer cones em uma Point Cloud são utilizados 2 principais algoritimos: o RANSAC e o DBSCAN. Esses algoritimos, juntamente com uma filtragem básica, servem para tratar a Point Cloud de modo que apenas os pontos desejados(aqueles que representam os cones) permaneçam.

### RANSAC
A função do RANSAC(RANdom SAmple Consensus) é encontrar os pontos que pertencem ao chão e removê-los, e sabemos que o chão pode ser aproximado por um plano. Dessa forma nós conseguimos remover uma grande quantidade de pontos que não nos interessam de uma só vez.

O algoritimo divide todos os pontos de uma amostragem em inliers e outliers. Os inliers são os pontos que atendem determinada condição enquanto que os outliers não o fazem. O RANSAC busca, dentro dessa amostragem, um modelo que contém a maior quantidade de inliers, e devolve como sendo o modelo ótimo.

Se o objetivo for traçar uma linha que melhor descreve determinado conjunto de pontos (a), por exemplo, o algoritimo irá pegar uma linha descrita por dois pontos aleatórios (b) e separar todos os outros pontos em inliers e outliers, dependendo da distância δ na qual os outros pontos se encontram da reta. Na figura abaixo, em (c), os pontos em azul são os inliers, aqueles que se encontram dentro do limite δ no qual o ponto pode ser considerado inlier.
O algoritimo então seleciona outros dois pontos e repete o processo. Por fim, retorna o modelo com a maior quantidade de inliers (d).

(/Screenshot_5.png "RANSAC")



No nosso caso, o RANSAC não trabalha com retas, mas sim com planos. O algoritimo seleciona três pontos aleatórios, e, a partir do plano determinado por eles, classifica todos os outros pontos como inliers e outliers com base na distancia do ponto ao plano. Se esse distancia for menor  ou igual ao threshold (δ) escolhido, o ponto é um inlier. O processo é repetido para diversos conjuntos de três pontos e o modelo que melhor descreve o chão é encontrado. Por fim, todos os pontos desse modelo são removidos e, portanto, é realizada a remoção do chão da Point Cloud.  

### DBSCAN

Na pista teremos, teoricamente, apenas os cones e o chão. Após a remoção do chão pelo RANSAC, poderiamos tratar um conjunto agrupado de pontos como os cones. E a partir desse conjunto de pontos estimar a posicao dos cones naquela Point Cloud.

Para conseguir estimar com precisão quais conjuntos de pontos representam os cones, nós utilizamos o DBSCAN

Esse algoritmo reconhece os Clusters – região com alta de densidade de pontos separada de outra por uma região com baixa densidade de pontos – com grande precisão.

O DBSCAN separa os pontos de uma Point Cloud em três categorias: Core, Border e Noise.
Para categoriza-los, o algoritimo trabalha com dois parametros, definidos pelo usuário: Quantidade de pontos necessários para um Core Point e Raio.

Para explicar o funcionamento do algoritimo e como cada Ponto é caracterizado, vamos para um exemplo:

Supondo que tenha sido escolhido um Raio R = 3 cm e que a quantidade de pontos necessários para um Core Point seja 3, trabalharemos com o conjunto de pontos abaixo:

Para cada ponto, o algoritimo irá traçar um região de raio R = 3 cm a partir desse ponto, e se, dentro dessa região, tiver uma quantidade de pontos vizinhos maior ou igual a 3, esse ponto será um Core Point.
 Na imagem, o ponto em laranja é um Core Point, já que possui 3 ou mais outros pontos  na região de raio R ao seu redor.

Caso a região de raio R não possua a quantidade de pontos necessária para um Core Point, o ponto pode ser caracterizado como Border Point ou Noise Point.

Se o ponto, apesar de não atingir a condição, estiver dentro da região de raio R de um Core Point, esse ponto se torna um Border Point.

Na imagem acima, os pontos em laranja são os Core Points, e o ponto rosa representa um Border Point, que, apesar de não possuir três ou mais pontos dentro de sua região de raio R, possui um Core Point.

Por fim, os pontos que não antigem a condição necessária para Core Points e nem possuem Core Points dentro de sua região de raio R, se encaixam como Noise Points.
Na imagem acima, os pontos em laranja são os Core Poins, ou rosas são os Border Points e s pontos pretos são os Noise Points.

Desse modo, o DBSCAN é capaz de reconhecer os clusters e, consequentemente, os cones com alta precisão.
