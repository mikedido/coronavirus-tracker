# COVID-19 chart

## About

An app to analysis data about the corona virus / COVID-19 on the world of the number of deaths, confirmed and recovered person. 

Charts of evolution of deaths, confirmed and recovered person by country.

![iOS](https://img.shields.io/badge/iOS-10%20-blue)
![macOS](https://img.shields.io/badge/macOS-10.15-blue)
![Swift](https://img.shields.io/badge/Swift-5-orange?logo=Swift&logoColor=white)

![python]
![flask]


## Screenshot
<img src="https://user-images.githubusercontent.com/121827/76558431-5e747900-64ae-11ea-9168-2091a431773a.png" width="127">

![image](https://user-images.githubusercontent.com/121827/77246699-e25efb80-6c3a-11ea-8a49-30bd87ff33c0.png)

## Features
* __Live data__: Shows the most recent data, and updates automatically.
* __Distribution map__ with two levels of details:
  * __Countries__: When the user zooms out. Fewer details and reduced clutter.
  * __Cities__: When the user zooms in. More details.
* __Charts__:
   * __Current state chart__ for all countries (and cities).
   * __Timeline chart__ for all countries (and cities).
   * __Top affected countries__ chart with info about every country.
  * Option for using a __logarithmic__ scale.
* __Search__ for countries & cities.
* __Share__ stats & charts as images.
* __Today widget__ for worldwide stats (Contributed by [Piotr Ożóg](https://github.com/pbeo)).
* __Red color scale__: Reflects the number of confirmed cases. In addition to increasing circle size.
* __Statistics__: Including the number of confirmed, recovered, and deaths, in addition to percents.
* __iPad__ & __macOS__ support.

## How to Use
#### Build from source code
1. Clone/Download the repo.
2. Open `Corona.xcodeproj` in Xcode.
3. Choose the right target (iOS or macOS).
4. Build & run!

`python3 run.py`

## TODO

 * Add key to global view
 * Convert disparate data sources in to singular SQLite database
 * Add cities (needs an improved visualization system)
 * More visualization options:
   * [amcharts](https://www.amcharts.com/demos/map-with-curved-lines/?theme=dark) (icky licensing but looks cool)
   * [d3.js](https://d3js.org/) and [d3-china-map](https://github.com/clemsos/d3-china-map) (good option but possibly overkill)
   * [jvectormap](https://jvectormap.com/) and [jvectormap china](https://jvectormap.com/maps/countries/china/) (good option but no cities)
   * [kartograph](http://kartograph.org/) (good option)
 * Add other sources, eg.
   * [WHO situation reports](https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports)
   * [National Health Commission daily reports](http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml)
   * [Tencent live monitoring page](https://news.qq.com//zt2020/page/feiyan.htm)
   * [English Wikipedia](https://en.wikipedia.org/wiki/2019%E2%80%9320_Wuhan_coronavirus_outbreak) (although it generally lags DXY on updates, the summary table is good for international data citations)
   * [Fuuuuuuu's map](https://maphub.net/Fuuuuuuu/map) which seems to have many international cases missed by BNO
 * Potential for different source SVGs, eg. [naturalearthdata](https://www.naturalearthdata.com/downloads/)

 ## Data

 The data of coronavirus was getted by the api of the project : ....


## Contribute
Please feel free to contribute pull requests or create issues for bugs and feature requests.

## License
The app is available for personal/non-commercial use. It's not allowed to publish, distribute, or use the app in a commercial way.

## Author
Mahdi Gueffaz (mahdi.gueffaz@gmail.com)

### Libraries
* [CSV.swift](https://github.com/yaslab/CSV.swift): For parsing the CSV data file.
* [Charts](https://github.com/danielgindi/Charts): Beautiful and powerful charts.
* [FloatingPanel](https://github.com/SCENEE/FloatingPanel): For the bottom sheet.
* [Disk](https://github.com/saoudrizwan/Disk): Simplifies loading/saving files.