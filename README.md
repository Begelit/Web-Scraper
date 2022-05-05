# test_AVsoft
Project with Script that should create a tree of links and generate a sitemap based on this tree.
Первичный результат таков:
##    Результат выполнения скрипта веб-краулера
![](https://github.com/ZeroIsntNull/test_AVsoft/blob/master/images/results_1.jpeg)
###   Где файл set_url.csv соответствует набору уникальных ссылок, количество которых указано в результирующей таблице, которые были получены в результате выполнения запросов, а также использованные в качестве дальнейших запросов.
###   В то же время файл tree_json.json содержит в себе эти ссылки, но в древовидной структуре, имея связи между родительскими и дочерними ссылками. Среди уникальных ссылок, соответствующих основному домену, в этом файле содержатся так же ссылки на возможние сторонние ссылки других доменов, которые были получены в результате запросов по ссылкам основного домена.
##    Файл tree_json.json имеет структуру следующего вида:
![](https://github.com/ZeroIsntNull/test_AVsoft/blob/master/images/tree_structure.jpeg)
##    Структура tree_json.json такова, что "parent_id" ссылки высокого уровня соответсвует "id" предшествующего уровня.
###   В приведенном псевдопримере структуры tree_json.json рассмотрим ссылку "url_2_1" из второго уровня "2_level". Значение "parent_id" равное "2" говорит о том, что ссылка принадлежит списку ссылок "list", полученный в результате запроса по ссылке "url_2" первого уровня "1_level".

