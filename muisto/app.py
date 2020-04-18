#!/usr/bin/python
#Muisto : A useful satatic website generator
#Developer : Mamoru Itoi
    #Website : https://mamoruitoi.github.io/
    #Twitter : @MamoruItoi
    #GitHub : mamoruitoi


import codecs
import glob
import os
import re
import sys

from themes.muisto_light import main as muisto_light


aboutLines = ""
configLines = []
config = {}
muistoCodesDict = {}
dataOfFiles = {}
dataOfModes = {}
dataOfTags = {}
indexLines = []
defaultAbout = """
<div class="about">
<div class="icon">
<img src="img/icon.png" width="100px" height="100px">
</div>
<div class="name">
<h1><span class="japan">糸井主歩</span><span class="english">Mamoru Itoi</span></h1>
</div>
<div class="outline">
<p>東京の端っこでちまちまとPythonを書く人間的何かです。</p>
</div>
</div>
"""
defaultConfig = """
@theme: "muisto-light"
@cover: "muisto-logo.png"
@title: "モダンながらどこか懐かしい静的サイトジェネレータ"
"""
defaultIndex = """

"""
indexHeader = """
<html>
<head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
<script src="https://cdn.rawgit.com/google/code-prettify/master/loader/run_prettify.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Swiper/4.5.1/css/swiper.css" integrity="sha256-eN7gD6kRzzeXS87cycVGlO3smXA9o+yeN0BDkTVaOc0=" crossorigin="anonymous">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Swiper/4.5.1/js/swiper.js" integrity="sha256-2AzmZuC/JWSxd9zvzxqNIBQIoB/uSRsSYtXJBhAkfjY=" crossorigin="anonymous"></script>
<link rel="stylesheet" href="./muisto/themes/muisto_light/prettify.css">
<link rel="stylesheet" type="text/css" href="./muisto/themes/muisto_light/main.css">
<link href="https://use.fontawesome.com/releases/v5.6.1/css/all.css" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
<title>Mamoru's Website</title>
<script>(function(d){var config = {kitId: 'hdm7ghc',scriptTimeout: 3000,async: true},h=d.documentElement,t=setTimeout(function(){h.className=h.className.replace(/wf-loading/g,"")+" wf-inactive";},config.scriptTimeout),tk=d.createElement("script"),f=false,s=d.getElementsByTagName("script")[0],a;h.className+=" wf-loading";tk.src='https://use.typekit.net/'+config.kitId+'.js';tk.async=true;tk.onload=tk.onreadystatechange=function(){a=this.readyState;if(f||a&&a!="complete"&&a!="loaded")return;f=true;clearTimeout(t);try{Typekit.load(config)}catch(e){}};s.parentNode.insertBefore(tk,s)})(document);</script>
<link href="https://fonts.googleapis.com/css?family=Lato&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=1.0">
</head>
<body>
<header>
<div class="nav">
<div class="left">
<div class="logo">
<a href="https://mamoruitoi.github.io/" target="_blank"><img src="img/oblivion-logo.png" width="auto" height="100%"></a>
</div>
<div class="title">
<h1>学生Pythonプログラマの日常</h1>
</div>
</div>
<div class="right">
<ul class="sns">
<li><a href="https://twitter.com/MamoruItoi" target="_blank"><img src="img/twitter.png" width="auto" height="70%"></a></li>
<li><a href="https://github.com/mamoruitoi" target="_blank"><img src="img/github.png" width="auto" height="70%"></a></li>
<li><a href="https://qiita.com/MamoruItoi" target="_blank"><img src="img/qiita.png" width="auto" height="70%"></a></li>
</ul>
</div>
</div>
</header>
<div class="nav-button">
<div class="fixed-action-btn">
<a class="btn-floating btn-large blue"><i class="material-icons button-color">bubble_chart</i></a>
<script>
document.addEventListener("DOMContentLoaded", function() {
var elems = document.querySelectorAll(".fixed-action-btn");
var instances = M.FloatingActionButton.init(elems, {
direction: "top"
});
});
</script>
<ul class="google">
<li><a href="#" class="btn-floating red lighten-2"><i class="material-icons">home</i></a></li>
<li><a href="https://qiita.com/itoppy18" class="btn-floating amber lighten-2"><i class="material-icons">account_circle</i></a></li>
<li><a href="https://twitter.com/shinkaimakoto" class="btn-floating teal lighten-2"><i class="material-icons">build</i></a></li>
<li><a href="https://krunker.io/" class="btn-floating blue lighten-2"><i class="material-icons">event</i></a></li>
<li><a href="https://tenkinoko.com/" class="btn-floating purple lighten-3"><i class="material-icons">explore</i></a></li>
</ul>
</div>
<div class="muisto-header">
<img src="img/header.png" width="95%" height="auto">
<h1>{0}:{1}</h1>
</div>
<div class="main">
"""


#メイン関数
def main():
    try:
        fileName = sys.argv[1]
        if fileName == ".":
            generateRequiredFiles()
            convertConfigFileToPython()
            generate()
        elif fileName == "418":
            print("\033[1;31m[Error!]\033[1;m I'm a tea pot.")
        else:
            print("\033[1;31m[Error!]\033[1;m What's that?")
    except IndexError:
        print("\033[1;31m[Error!]\033[1;m Not found the file.")

#生成に必要なconfig.md、_about.md、index.mdの存在を確認し、もし存在しなければデフォルト内容で生成する
def generateRequiredFiles():
    global about, configLines, indexLines
    if os.path.isfile("about.html"):
        with open("about.html") as f:
            about = f.read()
    else:
        with open("about.html", "w") as f:
            f.write(defaultAbout)
    if os.path.isfile("config.md"):
        with open("config.md") as f:
            configLines = f.readlines()
    else:
        with open("config.md", "w") as f:
            f.write(defaultConfig)
    if os.path.isfile("index.md"):
        with open("index.md") as f:
            indexLines = f.readlines()
    else:
        with open("index.md", "w") as f:
            f.write(defaultIndex)

#Markdown形式の設定ファイル(config.md)をPythonの辞書型に変換する
def generateConfigFiles():
    global config, configLines
    mode = "top"
    config[mode] = {}
    for i, line in enumerate(configLines):
        isModeDeclaration = re.search("^# (.+)", line)
        isMuistoCode = re.search("^@(cover|place|tags|theme|title|writer|icon|color|url|name|fav): \"(.+)\"", line)
        if isModeDeclaration:
            mode = isModeDeclaration.group(1)
            config[mode] = {}
        elif isMuistoCode:
            code = isMuistoCode.group(1)
            parameter = isMuistoCode.group(2)
            config[mode][code] = parameter

#静的サイトを生成する
def generate():
    files = [p for p in glob.glob("../_post/**") if os.path.isfile(p)]
    for file in files:
        convertMarkdownToHTML(file)
        generateIndexPages()
        generateIndexesAndLinks()

#MarkdownをHTMLに変換する
def convertMarkdownToHTML(fileName, mode="normal"):
    generateBody(fileName, muistoCodesDict["theme"], mode, about, config)
    convertMuistoCodes(fileName, muistoCodesDict)

#ファイル内のMuistoCodes（日付・モード・タグなど）を取得する
def getMuistoCodes(fileName):
    global muistoCodesDict, dataOfFiles
    muistoCodesDict = {
    "cover": "",
    "date": "",
    "mode": "",
    "place": "",
    "tags": "",
    "theme": "",
    "title": "",
    "writer": ""
    }
    with open(fileName) as f:
        lines = f.readlines()
    for line in lines:
        isMuistoCode = re.search("^@(cover|date|mode|place|tags|theme|title|writer): \"(.+)\"", line)
        if isMuistoCode:
            code = isMuistoCode.group(1)
            parameter = isMuistoCode.group(2)
            if code == "tags":
                muistoCodesDict[code] = parameter.split("|")
            else:
                muistoCodesDict[code] = parameter
    #muistoCodesDict = {'cover': 'muisto-logo.png', 'date': '0900-0215-2020', 'mode': 'blog', 'place': 'Tokyo', 'tags': [Muisto, Web, Design], 'theme': '', 'title': '今日はいい天気なので自作SSGでかっこいいWebサイトを作ってみた', 'writer': ''}
    #config = {'top': {'theme': 'muisto-light', 'cover': 'muisto-logo.png', 'title': '学生Pythonプログラマの日常', 'icon': 'home', 'color': '#2792ca'}, 'about': {'icon': 'account_circle', 'color': '#2792ca', 'cover': 'muisto-logo.png'}, 'code': {'icon': 'build', 'color': '#2792ca', 'cover': 'muisto-logo.png'}, 'blog': {'icon': 'event', 'color': '#2792ca', 'cover': 'muisto-logo.png'}, 'news': {'icon': 'explore', 'color': '2792ca', 'cover': 'muisto-logo.png'}}
    for code, parameter in muistoCodesDict.items():
        if parameter != "":
            continue
        else:
            #modeを取得→なければトップ
            #configを確認
            #configのモードになければ（if key in dict）トップのを参照、それでもなければ知らんがな。
            if "mode" in muistoCodesDict:
                if muistoCodesDict["mode"] in config and code in config[muistoCodesDict["mode"]]:
                    muistoCodesDict[code] = config[muistoCodesDict["mode"]][code]
                else:
                    try:
                        muistoCodesDict[code] = config["top"][code]
                    except KeyError:
                        pass
    name = fileName.replace("../_post/", "").replace(".md", "")
    dataOfFiles[name] = muistoCodesDict


#HTML部分を生成する
def generateBody(fileName, theme, mode, about, config):
    if theme == "muisto-light":
        muisto_light.main(fileName, config, mode)
    #テーマ以外の設定はmuistoCodesDictから読み込む
    #@indexと@linkは<p>に変換せず、そのままの形で保存しておく

#Muisto CodesをHTMLに変換する
def convertMuistoCodes(fileName, muistoCodesDict):
    if muistoCodesDict["theme"] == "muisto-light":
        muisto_light.convertMuistoCodes(fileName, muistoCodesDict)

#dataOfFilesを使って、その中に含まれるすべてのモードとタグのインデックスページを生成する
def generateIndexPages():
    global dataOfModes, dataOfTags
    #いろいろ生成
    for k, v in config.items():
        if k == "top":
            continue
        dataOfModes[k] = {}
    for k, v in dataOfFiles.items():
        for tag in v["tags"]:
            if not tag in dataOfModes[v["mode"]]:
                dataOfModes[v["mode"]][tag] = []
            dataOfModes[v["mode"]][tag].append(k)
    for k1, v1 in dataOfModes.items():
        for k2, v2 in v1.items():
            if not k2 in dataOfTags:
                dataOfTags[k2] = {}
            if not k1 in dataOfTags[k2]:
                dataOfTags[k2][k1] = []
            for article in v2:
                dataOfTags[k2][k1].append(article)


#dataOfFilesを使って、ファイル内の@linkを生成する
def generateIndexesAndLinks():
    files = [p for p in glob.glob("../**.html") if os.path.isfile(p)]
    print(files)
    for file in files:
        with codecs.open(file, "r", "utf-8") as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            link = re.search("^@link: \"([^\"]*)\"$", line)
            if link:
                fileName = link.group(1)
                cover = dataOfFiles[fileName]["cover"]
                title = dataOfFiles[fileName]["title"]
                mode = dataOfFiles[fileName]["mode"]
                date = muisto_light.translate(muistoCodesDict["date"][5:7]) + " " + muistoCodesDict["date"][7:9] + ", " + muistoCodesDict["date"][10:]
                templateOfLink = """
<a href="{0}.html">
<div class="link">
<div class="img">
<img src="img/{1}" width="auto" height="100%">
</div>
<div class="title">
<p>{2}</p>
<p class="data">{3} / {4}</p>
</div>
</div>
</a>""".format(fileName, cover, title, mode, date)
                lines[i] = templateOfLink
        with codecs.open(file, "w", "utf-8") as f:
            f.write("".join(lines))
