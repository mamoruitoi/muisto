#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Muisto: A Nostalgic Modern Static Site Generator
#Developer: Mamoru Itoi(@MamoruItoi)


import codecs
import glob
import MeCab
import os
import re
import sys


#各種グローバル変数
#config.mdの中身
config = {}
data = {}
dataOfModes = {}
dataOfTags = {}
muistoFlag = False
isInCode = False
lines = []

def main():
    about, configLines = generateRequiredFiles()
    convertConfig(configLines)
    getData()
    generateFiles()
    generateIndexPages()

#生成に必要な設定ファイルがあるかどうかを確認し、なければデフォルト内容で生成
def generateRequiredFiles():
    #ファイルがなければデフォルト内容で生成
    if not os.path.isfile("about.html"):
        with open("about.html", "w") as f:
            f.write(defaultAbout)
    if not os.path.isfile("config.md"):
        with open("config.md", "w") as f:
            f.write(defaultConfig)
    #ファイルを開いて中身を変数に代入
    with open("about.html") as f:
        about = f.read()
    with open("config.md") as f:
        configLines = f.readlines()
    return about, configLines

#設定ファイルをPythonの辞書形式に変換
def convertConfig(configLines):
    global config
    mode = "top"
    config[mode] = {}
    for i, line in enumerate(configLines):
        isModeDeclaration = re.search("^# (.+)", line)
        isMuistoCode = re.search("^@(cover|place|tags|theme|title|writer|icon|color|url|name|fav|twitter|github|logo): \"(.+)\"", line)
        if isModeDeclaration:
            mode = isModeDeclaration.group(1)
            config[mode] = {}
        elif isMuistoCode:
            code = isMuistoCode.group(1)
            parameter = isMuistoCode.group(2)
            config[mode][code] = parameter

#Markdownファイルのデータ（日付やタイトルなど）を取得して辞書形式にまとめる
def getData():
    global data, dataOfModes, dataOfTags
    files = [p for p in glob.glob("../_post/**") if os.path.isfile(p)]
    for file in files:
        fileData = {
        "cover": "",
        "date": "",
        "mode": "",
        "place": "",
        "tags": "",
        "theme": "",
        "title": "",
        "writer": ""
        }
        with open(file) as f:
            lines = f.readlines()
        for line in lines:
            isMuistoCode = re.search("^@(cover|date|mode|place|tags|theme|title|writer): \"(.+)\"", line)
            if isMuistoCode:
                code = isMuistoCode.group(1)
                parameter = isMuistoCode.group(2)
                if code == "tags":
                    fileData[code] = parameter.split("|")
                else:
                    fileData[code] = parameter
        for code, parameter in fileData.items():
            if parameter != "":
                continue
            else:
                if "mode" in fileData:
                    if fileData["mode"] in config and code in config[fileData["mode"]]:
                        fileData[code] = config[fileData["mode"]][code]
                    else:
                        try:
                            fileData[code] = config["top"][code]
                        except KeyError:
                            pass
        name = file.replace("../_post/", "").replace(".md", "")
        data[name] = fileData
    for k, v in config.items():
        if k == "top":
            continue
        dataOfModes[k] = {}
    for k, v in data.items():
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

#MarkdownファイルからHTMLファイルを生成
def generateFiles():
    files = [p for p in glob.glob("../_post/**") if os.path.isfile(p)]
    for file in files:
        with codecs.open(file, "r", "utf-8") as f:
            global lines
            lines = f.readlines()
        htmlFileName = re.sub("md$", "html", file.replace("../_post/", "../"))
        with codecs.open(htmlFileName, "w", "utf-8") as f:
            url = config["top"]["url"]
            fav = config["top"]["fav"]
            twitter = config["top"]["twitter"]
            github = config["top"]["github"]
            fileName = htmlFileName.replace("../", "").replace(".html", "")
            title = data[fileName]["title"]
            cover = data[fileName]["cover"]
            logo = config["top"]["logo"]
            css = f"""
<link rel="stylesheet" href="./muisto/themes/{data[fileName]["theme"]}/main.css" type="text/css">
"""
            fav = f"""
<link rel="shortcut icon" href="img/{fav}" type="image/vnd.microsoft.icon">
<link rel="icon" href="img/{fav}" type="image/vnd.microsoft.icon">"""
            templateOfHead1 = f"""
<html>
<head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
<link rel="stylesheet" href="./muisto/prettify.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
<script src="https://cdn.rawgit.com/google/code-prettify/master/loader/run_prettify.js"></script>
{css}
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Noto+Sans+JP:400,500,600,700|Lato&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.6.1/css/all.css">
{fav}
<title>{title}</title>
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@{twitter}">
<meta property="og:url" content="{url}{fileName}.html">
<meta property="og:title" content="{title}">
<meta property="og:image" content="{url}img/{cover}">
<meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=1.0">
</head>
<body>
<header>
<div class="nav">
<div class="left">
<div class="logo">
<a href="{url}"><img src="img/{logo}" width="auto" height="100%"></a>
</div>
<div class="title">
<h1>{config["top"]["title"]}</h1>
</div>
</div>
<div class="right">
<ul class="sns">
<li><a href="https://twitter.com/{twitter}" target="_blank"><img src="{url}img/twitter.png" width="auto" height="70%"></a></li>
<li><a href="https://github.com/{github}" target="_blank"><img src="{url}img/github.png" width="auto" height="70%"></a></li>
</ul>
</div>
</div>
</header>
<div class="main">
<div class="fixed-action-btn">
<a class="btn-floating btn-large blue"><i class="material-icons button-color">bubble_chart</i></a>"""
            script = """
<script>
document.addEventListener("DOMContentLoaded", function() {
var elems = document.querySelectorAll(".fixed-action-btn");
var instances = M.FloatingActionButton.init(elems, {
direction: "top"
});
});
</script>"""
            templateOfHead2 = """
<ul class="google">
{0}
</ul>
</div>"""

            f.write(templateOfHead1)
            f.write(script)
            f.write(templateOfHead2.replace("{0}", generateButtons(config)))
            global muistoFlag
            muistoFlag = False
            for i, line in enumerate(lines):
                f.write(generateHTML(i, line, fileName))
            f.write(f"""
</div>
<footer>
<p>©2020 {data[fileName]["writer"]}<br><a href="https://twitter.com/{twitter}" target="_blank">Twitter</a></p>
</footer>
</body>
</html>""")
        print(htmlFileName)

#MarkdownからHTMLへの変換
def generateHTML(i, md, fileName):
    global muistoFlag, isInCode
    muistoCode = re.search("^@(cover|date|mode|place|tags|theme|title|writer): \"(.+)\"$", md)
    link = re.search("^@link: \"([^\"]*)\"$", md)
    h2 = re.search("^# (.+)$", md)
    h3 = re.search("^## (.+)$", md)
    h4 = re.search("^### (.+)$", md)
    h5 = re.search("^#### (.+)$", md)
    h6 = re.search("^##### (.+)$", md)
    horizontalRule = re.search("^(-|\*|_){3,}$", md)
    discList = re.search("^(\*|\+|-) (.+)$", md)
    decimalList = re.search("\d\. (.+)$", md)
    p = re.search("(.+)", md)
    #Muisto Codes
    if muistoCode:
        if muistoFlag:
            return ""
        else:
            muistoFlag = True
            return convertMuistoCodes(fileName)
    #@link
    elif link:
        return generateLink(link.group(1))
    #コード・リストの開始・終了処理
    elif md == "\n":
        result = ""
        #コード・リストの終了処理
        #コード終了
        if re.search("^```", lines[i-1]):
            isInCode = False
            result += "</code></pre>\n"
        #disc型リスト終了
        if re.search("^(\*|\+|\-) (.+)", lines[i-1]):
            result += "</ul>\n"
        #decimal型リスト終了
        if re.search("\d\. (.+)", lines[i-1]):
            result += "</ol>\n"
        #コード・リストの開始処理
        #コードの開始処理
        code = re.search("^(`){3}([^\:]*)\:", lines[i+1])
        if code:
            isInCode = True
            result += "<pre class=\"prettyprint linenums\"><code class=\"lang-" + code.group(2) +"\">\n"
        #disc型リスト開始
        if re.search("^(\*|\+|\-) (.+)", lines[i+1]):
            result += "<ul>\n"
        #decimal型リスト開始
        if re.search("\d\. (.+)", lines[i+1]):
            result += "<ol>\n"
        #コード内の改行は維持
        if isInCode:
            result += "\n\n"
        return result
    #コード・リスト
    #コード
    elif isInCode:
        if not re.search("^`", md):
            return md
        else:
            return ""
    #disc型リスト
    elif discList:
        return "<li>" + discList.group(2) + "</li>\n"
    #decimal型リスト
    elif decimalList:
        return "<li>" + decimalList.group(1) + "</li>\n"
    #H2
    elif h2:
        return "<h2>" + span(h2.group(1)) + "</h2>\n"
    #H3
    elif h3:
        return "<h3>" + span(h3.group(1)) + "</h3>\n"
    #H4
    elif h4:
        return "<h4>" + span(h4.group(1)) + "</h4>\n"
    #H5
    elif h5:
        return "<h5>" + span(h5.group(1)) + "</h5>\n"
    #H6
    elif h6:
        return "<h6>" + span(h6.group(1)) + "</h6>\n"
    #水平線
    elif horizontalRule:
        return "<hr color=\"#333\">\n"
    #本文
    elif p:
        result = "<p>" + p.group(1) + "</p>\n"
        #ボールド
        result = re.sub("\*\*([^\*]*)\*\*", "<strong>\\1</strong>", result)
        #イタリック
        result = re.sub("\*([^\*]*)\*", "<em>\\1</em>", result)
        #取り消し線
        result = re.sub("~~([^~]*)~~", "<strike>\\1</strike>", result)
        #インラインコード
        result = re.sub("`([^`]*)`", "<span class=\"inline-code\">\\1</span>", result)
        #画像
        result = re.sub("!\[([^\)]*)\]\(([^\]]*)\)", "<img alt=\"\\1\" src=\"img/\\2\" width=\"95%\" height=\"auto\">", result)
        #リンク
        result = re.sub("\[([^\)]*)\]\(([^\]]*)\)", "<a href=\"\\2\" target=\"_blank\">\\1</a>", result)
        #ダッシュがつながって見えるように処理
        result = re.sub("(——)", "<span style=\"letter-spacing: -0.2em;\">\\1&ensp;</span>", result)
        return result
    return ""

#Muisto Codesを変換
def convertMuistoCodes(fileName):
    cover = data[fileName]["cover"]
    title = span(data[fileName]["title"])
    #このソフトウェアは西暦10000年問題に対応しています。
    date = translate(data[fileName]["date"][5:7]) + " " + data[fileName]["date"][7:9] + ", " + data[fileName]["date"][10:]
    place = data[fileName]["place"]
    writer = data[fileName]["writer"]
    mode = "<a href=\"{0}modes/{1}.html\"><span class=\"mode\">{1}</span></a>".format(config["top"]["url"], data[fileName]["mode"])
    tags = generateTags(data[fileName]["tags"])
    templateOfData = """
<img src="img/{0}" width="95%" height="auto">
<h1>{1}</h1>
<p class="data"><span class="date">{2}</span><span class="place"><i class="tiny material-icons">location_on</i>{3}</span><span class="writer"><i class="tiny material-icons">create</i>{4}</span><br>{5}</span></a>{6}
<hr color="#103670">
<ul class="shareList">
<li class="shareList-item"><i class="small material-icons">share</i></li>
<li class="shareList-item"><a class="icon icon-twitter" href="https://twitter.com/intent/tweet?text={7}%20-%20{8}%20{9}%0A{10}.html" target="_blank" title="Twitter"><i class="fab fa-twitter"></i></a></li>
<li class="shareList-item"><a class="icon icon-facebook" href="https://www.facebook.com/sharer/sharer.php?u=https://mamoruitoi.github.io/" target="_blank" title="Facebook"><i class="fab fa-facebook"></i></a></li>
</ul>""".format(cover, title, date, place, writer, mode, tags, data[fileName]["title"], config["top"]["name"], config["top"]["title"], config["top"]["url"]+fileName)
    return templateOfData

def generateIndexPages():
    for k1, v1 in dataOfModes.items():
        htmlFileName = f"../modes/{k1}.html"
        with codecs.open(htmlFileName, "w", "utf-8") as f:
            url = config["top"]["url"]
            fav = config["top"]["fav"]
            twitter = config["top"]["twitter"]
            github = config["top"]["github"]
            fileName = htmlFileName.replace("../", "").replace(".html", "")
            title = k1
            cover = config[k1]["cover"]
            logo = config["top"]["logo"]
            css = f"""
<link rel="stylesheet" href="../muisto/themes/{config[k1]["theme"]}/main.css" type="text/css">"""
            fav = f"""
<link rel="shortcut icon" href="../img/{fav}" type="image/vnd.microsoft.icon">
<link rel="icon" href="../img/{fav}" type="image/vnd.microsoft.icon">"""
            templateOfHead1 = f"""
<html>
<head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
<link rel="stylesheet" href="../muisto/prettify.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
<script src="https://cdn.rawgit.com/google/code-prettify/master/loader/run_prettify.js"></script>
{css}
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Noto+Sans+JP:400,500,600,700|Lato&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.6.1/css/all.css">
{fav}
<title>{title}</title>
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@{twitter}">
<meta property="og:url" content="{url}{fileName}.html">
<meta property="og:title" content="{title}">
<meta property="og:image" content="{url}img/{cover}">
<meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=1.0">
</head>
<body>
<header>
<div class="nav">
<div class="left">
<div class="logo">
<a href="{url}"><img src="../img/{logo}" width="auto" height="100%"></a>
</div>
<div class="title">
<h1>{config["top"]["title"]}</h1>
</div>
</div>
<div class="right">
<ul class="sns">
<li><a href="https://twitter.com/{twitter}" target="_blank"><img src="{url}img/twitter.png" width="auto" height="70%"></a></li>
<li><a href="https://github.com/{github}" target="_blank"><img src="{url}img/github.png" width="auto" height="70%"></a></li>
</ul>
</div>
</div>
</header>
<div class="fixed-action-btn">
<a class="btn-floating btn-large blue"><i class="material-icons button-color">bubble_chart</i></a>"""
            script = """
<script>
document.addEventListener("DOMContentLoaded", function() {
var elems = document.querySelectorAll(".fixed-action-btn");
var instances = M.FloatingActionButton.init(elems, {
direction: "top"
});
});
</script>"""
            templateOfHead2 = f"""
<ul class="google">
{generateButtons(config)}
</ul>
</div>
<div class="muisto-header">
    <img src="../img/{config[k1]["cover"]}" width="95%" height="auto">
    <h1>Mode:{k1}</h1>
</div>
<div class="main">"""

            f.write(templateOfHead1)
            f.write(script)
            f.write(templateOfHead2)
            for k2, v2 in v1.items():
                if v1 == {}:
                    continue
                f.write(f"<h2>{k2}</h2>")
                for i in v2:
                    f.write(generateLink(i))
            f.write(f"""
</div>
<footer>
<p>©2020 {config[k1]["writer"]}<br><a href="https://twitter.com/{twitter}" target="_blank">Twitter</a></p>
</footer>
</body>
</html>""")
        print(htmlFileName)
    for k1, v1 in dataOfTags.items():
        htmlFileName = f"../tags/{k1}.html"
        with codecs.open(htmlFileName, "w", "utf-8") as f:
            url = config["top"]["url"]
            fav = config["top"]["fav"]
            twitter = config["top"]["twitter"]
            github = config["top"]["github"]
            fileName = htmlFileName.replace("../", "").replace(".html", "")
            title = k1
            cover = config["top"]["cover"]
            logo = config["top"]["logo"]
            css = f"""
<link rel="stylesheet" href="../muisto/themes/{config["top"]["theme"]}/main.css" type="text/css">"""
            fav = f"""
<link rel="shortcut icon" href="../img/{fav}" type="image/vnd.microsoft.icon">
<link rel="icon" href="../img/{fav}" type="image/vnd.microsoft.icon">"""
            templateOfHead1 = f"""
<html>
<head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
<link rel="stylesheet" href="../muisto/prettify.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
<script src="https://cdn.rawgit.com/google/code-prettify/master/loader/run_prettify.js"></script>
{css}
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Noto+Sans+JP:400,500,600,700|Lato&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.6.1/css/all.css">
{fav}
<title>{title}</title>
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@{twitter}">
<meta property="og:url" content="{url}{fileName}.html">
<meta property="og:title" content="{title}">
<meta property="og:image" content="{url}img/{cover}">
<meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=1.0">
</head>
<body>
<header>
<div class="nav">
<div class="left">
<div class="logo">
<a href="{url}"><img src="../img/{logo}" width="auto" height="100%"></a>
</div>
<div class="title">
<h1>{config["top"]["title"]}</h1>
</div>
</div>
<div class="right">
<ul class="sns">
<li><a href="https://twitter.com/{twitter}" target="_blank"><img src="{url}img/twitter.png" width="auto" height="70%"></a></li>
<li><a href="https://github.com/{github}" target="_blank"><img src="{url}img/github.png" width="auto" height="70%"></a></li>
</ul>
</div>
</div>
</header>
<div class="fixed-action-btn">
<a class="btn-floating btn-large blue"><i class="material-icons button-color">bubble_chart</i></a>"""
            script = """
<script>
document.addEventListener("DOMContentLoaded", function() {
var elems = document.querySelectorAll(".fixed-action-btn");
var instances = M.FloatingActionButton.init(elems, {
direction: "top"
});
});
</script>"""
            templateOfHead2 = f"""
<ul class="google">
{generateButtons(config)}
</ul>
</div>
<div class="muisto-header">
    <img src="../img/{config["top"]["cover"]}" width="95%" height="auto">
    <h1>Tag:{k1}</h1>
</div>
<div class="main">"""

            f.write(templateOfHead1)
            f.write(script)
            f.write(templateOfHead2)
            for k2, v2 in v1.items():
                if v1 == {}:
                    continue
                f.write(f"<h2>{k2}</h2>")
                for i in v2:
                    f.write(generateLink(i))
            f.write(f"""
</div>
<footer>
<p>©2020 {config["top"]["writer"]}<br><a href="https://twitter.com/{twitter}" target="_blank">Twitter</a></p>
</footer>
</body>
</html>""")
        print(htmlFileName)

#dataOfFilesを使って、ファイル内の@linkを生成する
def generateLink(fileName):
    url = config["top"]["url"]
    cover = data[fileName]["cover"]
    title = data[fileName]["title"]
    mode = data[fileName]["mode"]
    date = translate(data[fileName]["date"][5:7]) + " " + data[fileName]["date"][7:9] + ", " + data[fileName]["date"][10:]
    templateOfLink = """
<a href="{0}{1}.html">
<div class="link">
<div class="img">
<img src="{0}img/{2}" width="auto" height="100%">
</div>
<div class="title">
<p>{3}</p>
<p class="data">{4} / {5}</p>
</div>
</div>
</a>""".format(url, fileName, cover, title, mode, date)
    return templateOfLink

#タグのインデックスページへのリンクのHTMLを生成
def generateTags(tags):
    result = ""
    for tag in tags:
        result += f"<a href=\"./tags/{tag}.html\"><span class=\"tag\">{tag}</span></a>"
    return result

#フローティングボタンのリンクを生成
def generateButtons(config):
    result = ""
    for k, v in config.items():
        if k == "top":
            result += "<li><a href=\"{0}index.html\" class=\"btn-floating {1}\"><i class=\"material-icons\">{2}</i></a></li>\n".format(config["top"]["url"], v["color"], v["icon"])
        else:
            result += "<li><a href=\"{0}modes/{1}.html\" class=\"btn-floating {2}\"><i class=\"material-icons\">{3}</i></a></li>\n".format(config["top"]["url"], k, v["color"], v["icon"])
    return result

#01から12までの数字を英語名に変換
def translate(month):
    if month == "01":
        return "January"
    elif month == "02":
        return "February"
    elif month == "03":
        return "March"
    elif month == "04":
        return "April"
    elif month == "05":
        return "May"
    elif month == "06":
        return "June"
    elif month == "07":
        return "July"
    elif month == "08":
        return "August"
    elif month == "09":
        return "September"
    elif month == "10":
        return "October"
    elif month == "11":
        return "November"
    elif month == "12":
        return "December"
    else:
        return ""

#形態素解析
def tokenize(text):
    t = MeCab.Tagger("")
    #mecab-ipadic-neologdを使用する際には前の行をコメントアウトし、代わりに次の行を挿入
    #t = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")
    t.parse("")
    m = t.parseToNode(text)
    tokens = []
    while m:
        tokenData = m.feature.split(",")
        token = [m.surface]
        for data in tokenData:
            token.append(data)
        tokens.append(token)
        m = m.next
    #EOSなどを削除
    tokens.pop(0)
    tokens.pop(-1)
    return tokens

#文節分け
def separatePhrases(text):
    #形態素解析
    tokens = tokenize(text)
    #文節リスト
    phrases = []
    #一つの文節のトークンリスト
    phrase = []
    #特別処理中フラグ
    isSpecialAnalyzing = False
    #自立語リスト
    independentParts = ["名詞", "動詞", "形容詞", "副詞", "連体詞", "感動詞", "接続詞", "接頭詞", "記号"]
    #トークンごとの処理
    for i, token in enumerate(tokens):
        #見出し
        surface = token[0]
        #品詞
        part = token[1]
        #品詞細分類1
        typeOfPart = token[2]
        #半角スペースがMeCabの辞書に登録されていない問題を解決
        try:
            if surface == "　" and re.match("\w", tokens[i-1][0]) and re.match("\w", tokens[i+1][0]):
                tokens[i][0] = "&nbsp;"
        except IndexError:
            pass
        #文節内のトークンをまとめる処理
        if part in independentParts and i != 0:
            isSpecialAnalyzing = False
            if phrase != []:
                phrases.append(phrase)
                phrase = []
        #漢語サ変動詞の処理
        if i != 0 and token[5] == "サ変・スル" or typeOfPart == "接尾" or tokens[i-1][1] == "接頭詞" or (tokens[i-1][2] == "括弧開") or typeOfPart == "読点":
            isSpecialAnalyzing = True
        if isSpecialAnalyzing:
            if phrases == []:
                phrase.append(token)
            else:
                phrases[-1].append(token)
        else:
            phrase.append(token)
    if phrase != []:
        phrases.append(phrase)
    for i, phrase in enumerate(phrases):
        for token in phrase:
            if token[2] == "括弧閉":
                for token2 in phrase:
                    phrases[i-1].append(token2)
                phrases.pop(i)
    return phrases

#見出しをspanタグで分けて見やすくする関数
def span(text):
    phrases = separatePhrases((lambda t:(re.sub(" ", "　", t)))(text))
    result = ""
    phraseResult = ""
    for phrase in phrases:
        result += "<span>"
        for token in phrase:
            phraseResult += token[0]
        result += phraseResult + "</span>"
        phraseResult = ""
    return result

main()