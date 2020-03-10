# 设计思路

## 需求
* 根据作品tag爬图（默认1000users收藏）<br>
```eg: crawl_by_tag やがて君になる nums```
    
* 根据作者id爬图（默认all）<br>
```eg: crawl_by_author authorID [nums]```

## 新的路线
主要是搜索信息，比如前1000作者分布
python爬出json再用matlab可视化？python直接可视化？

通过tag爬取到某tag下所有作品的信息，储存到json里

做成直方图(x:作者 y:作品数)