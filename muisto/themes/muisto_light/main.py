#!/usr/bin/python
#Muisto : A useful satatic website generator
#Developer : Mamoru Itoi
    #Website : https://mamoruitoi.github.io/
    #Twitter : @MamoruItoi
    #GitHub : mamoruitoi

import codecs
import glob
import MeCab
import os
import re
import sys


isInCode = None
language = None
lines = []
muistoFlag = False
url = ""

#メイン処理
def main(fileName, config, mode="normal"):
    if mode == "normal":
        with codecs.open(fileName, "r", "utf-8") as f:
            global lines
            lines = f.readlines()
        HTMLFileName = re.sub("md$", "html", fileName.replace("../_post/", "../"))
        with codecs.open(HTMLFileName, "w", "utf-8") as f:
            head = """
<html>
<head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
<script src="https://cdn.rawgit.com/google/code-prettify/master/loader/run_prettify.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Swiper/3.4.1/css/swiper.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Swiper/4.5.1/js/swiper.min.js">
<link rel="stylesheet" href="./muisto/themes/muisto_light/prettify.css">
<link rel="stylesheet" type="text/css" href="./muisto/themes/muisto_light/main.css">
<link href="https://use.fontawesome.com/releases/v5.6.1/css/all.css" rel="stylesheet">
<link rel="shortcut icon" href="img/favicon.ico" type="image/vnd.microsoft.icon">
<link rel="icon" href="img/favicon.ico" type="image/vnd.microsoft.icon">
<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
<title>Oblivion-学生Pythonプログラマの日常</title>
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
<div class="main">
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
{0}
</ul>
</div>
"""
            url = config["top"]["url"]
            f.write(head.replace("{0}", generateLinks(config)))
            for i, line in enumerate(lines):
                f.write(generateHTML(i, line))
            f.write("""
</div>
<footer>
<p>©2020 Mamoru Itoi<br><a href="https://twitter.com/MamoruItoi" target="_blank">Twitter</a></p>
</footer>
<script type="text/javascript">
var swiper = new Swiper('.swiper-container', {
navigation: {
nextEl: '.swiper-button-next',
prevEl: '.swiper-button-prev',
},
});
</script>
</body>
</html>
""")
        print(HTMLFileName)
    elif mode == "index":
        pass

#MarkdownからHTMLへの変換
def generateHTML(i, md):
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
    global isInCode, muistoFlag
    #Muisto Codeは仮変換する
    if muistoCode:
        if muistoFlag:
            return ""
        else:
            muistoFlag = True
            return "@muisto\n"
    elif link:
        return link.group(0) + "\n"
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
def convertMuistoCodes(fileName, muistoCodesDict):
    cover = muistoCodesDict["cover"]
    title = span(muistoCodesDict["title"])
    #このソフトウェアは西暦10000年問題に対応しています。
    date = translate(muistoCodesDict["date"][5:7]) + " " + muistoCodesDict["date"][7:9] + ", " + muistoCodesDict["date"][10:]
    place = muistoCodesDict["place"]
    writer = muistoCodesDict["writer"]
    mode = muistoCodesDict["mode"]
    tags = generateTags(muistoCodesDict["tags"])
    templateOfData = """
<img src="img/{0}" width="95%" height="auto">
<h1>{1}</h1>
<p class="data"><span class="date">{2}</span><span class="place"><i class="tiny material-icons">location_on</i>{3}</span><span class="writer"><i class="tiny material-icons">create</i>{4}</span><br>
<a href="https://mamoruitoi.github.io/"><span class="mode">{5}</span></a>{6}
<hr color="#103670">
<ul class="shareList">
<li class="shareList-item"><i class="small material-icons">share</i></li>
<li class="shareList-item"><a class="icon icon-twitter" href="https://twitter.com/intent/tweet?text=今日はいい天気なので自作SSGでカッコいいWebサイトを作ってみた%20-%20daydream%20糸井主歩のWebサイト%0Ahttps://mamoruitoi.github.io/" target="_blank" title="Twitter"><i class="fab fa-twitter"></i></a></li>
<li class="shareList-item"><a class="icon icon-facebook" href="https://www.facebook.com/sharer/sharer.php?u=https://mamoruitoi.github.io/" target="_blank" title="Facebook"><i class="fab fa-facebook"></i></a></li>
</ul>
    """.format(cover, title, date, place, writer, mode, tags)
    HTMLFileName = re.sub("md$", "html", fileName.replace("../_post/", "../"))
    with codecs.open(HTMLFileName, "r", "utf-8") as f:
        lines = f.read()
    lines = lines.replace("@muisto", templateOfData)
    with open(HTMLFileName, mode="w", encoding="utf-8") as f:
        f.write(lines)

#タグのインデックスページへのリンクのHTMLを生成
def generateTags(tags):
    result = ""
    for tag in tags:
        result += "<a href=\"{0}tags/{1}.html\"><span class=\"tag\">{1}</span></a>".format(url, tag)
    return result

#フローティングボタンのリンクを生成
def generateLinks(config):
    result = ""
    for k, v in config.items():
        result += "<li><a href=\"{0}/mode/{1}.html\" class=\"btn-floating {2}\"><i class=\"material-icons\">{3}</i></a></li>\n".format(url, k, v["color"], v["icon"])
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
