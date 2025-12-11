2025.12.11

[TOC]

# Ⅰ. Components; 構成ファイル
1. session-extractor.py
2. README.md
3. config/search_key.json
    - The list of Scan settings to search
4. config/dictionary.json
    - The dictionary of values of scansettings
5. config/addOn.py
    - The parameter dependency controller
6. config/subrecon.py
    - The configuration for number of subrecon
7. config/path.py
    - The configuration for the path of target directory
8. config/name.py
    - The configuration for the name of output file

# Ⅱ. How to Use
### (1) Unzip the ‘session-extractor.zip’ 
```shell
    unzip -d ./session-extractor session-extractor.zip
```
### (2) Set the path of ‘Site’ via ‘/config/path.py'
### (3) Set the name of output file via ‘/config/name.py'
> Example) <br> 
> Name: str = 'CT_Engineering' → CT_Engineering_20251016023221.csv
### (4) Set the other configuration in ‘config' directory (Refer to ‘How to set details’)
### (5) execute the 'session-extractor.py' script
```shell
    python3 session-extractor.py 
```
### (6) Get the text result file
> Example) <br> 
> Site_20251015013919.csv

# Ⅱ. 使用方法
### (1) 「session-extractor.zip」を解凍する
```shell
    unzip -d ./session-extractor session-extractor.zip
```
### (2) 「/config/path.py」で'Site’のパスを設定する
### (3) 「/config/name.py」で出力ファイルの名前を設定する
> 例) Name: str = 'CT_Engineering' → CT_Engineering_20251016023221.csv
### (4) 「config」フォルダにて他の設定を行う。(「詳細設定方法」 参照)
### (5) 「session-extractor.py」を実行する。
```shell
    python3 session-extractor.py 
```
### (6) 結果ファイルを得る。
> 例) Site_20251015013919.csv

# Ⅲ. How to set details
## 1. Search Key Setting
1) ‘Search key' is keyword to search in .xml file
2) There is NOT ‘Search key', then the extractor does NOT search the element
3) ‘Search key' setting is from ‘/config/search_key.json’
> Example) <br>
> (1) The ‘kiloVolts’ element in .xml file is for ‘kV’ scan setting. <br>
> (2) Input “kiloVolts”:”kV” into ‘group' key in /config/search_key.json, Then the Extractor searches ‘kiloVolts’ in .xml file and transform the name to ‘kV’ <br>

## 2. Dictionary for value of search key
- ‘Dictionary' is reference for translating value of a specific ‘Search Key' in .xml file
> Example) <br>
> (1) The ‘groupType’ element in .xml file is for ‘Scan Type’ scan setting and value ‘4' of the ‘groupType’ is for ‘Scout’ Scan Type <br>
> (2) Input “groupType”:”Scan Type” into ‘group' key in /config/search_key.json, Then the Extractor searches ‘groupType’ in .xml file and transform the name to ‘Scan Type’ <br>
> (3) In ‘/config/dicitionary.json’, input ‘Scan Type' key and “4”:”Scout” into the ‘Scan Type' key,  Then the Extractor searches transform the value ’4' to ‘Scout’ <br>

## 3. Subrecon Setting (The number of Subrecon) \
- The number of subrecon depend on ‘Subrecon’ of /config/subrecon.py (Default: 1, Range: 0 - )

# Ⅲ. 詳細設定方法
## 1. Search Key 設定
1) 「Search key」は .xmlファイルから探すキーワードなります。
2) 「Search key」がない場合、extractorが該当要素を探索しません。
3) 「/config/search_key.json」から「Search key」を設定することが可能です。
> 例) <br>
> (1)「kiloVolts」 要素は「kV」スキャン設定の指している。 <br>
> (2) “kiloVolts”:”kV”」を「/config/search_key.json」の中身 ‘group’ キーに追加すると、Extractorが.xmlファイルにで「kiloVolts」要素を見つかり「kV」に変換する。 <br>

## 2. Search Keyのvalue字引設定
-「Dictionary」は 特定「Search Key」に対するvalue字引になります。
> 例) <br>
> (1)「groupType」要素は「Scan Type」スキャン設定、値「4」は「Scout」Scan Typeをの指している。 <br>
> (2)「“groupType”:”Scan Type”」を「/config/search_key.json」の中身 「group」 キーに追加すると、Extractorが.xmlファイルにで「groupType」要素を見つかり「Scan Type」に変換する。 <br>
> (3)「/config/dicitionary.json」に「Scan Type」キーを追加してその中に 「”4”:”Scout”」を追加すると、Extractorが「4」値を「Scout」に変換する <br>

## 3. Subrecon 設定 (Subrecon出力個数設定)
- 「/config/subrecon.py」中に「Subrecon」の値で出力されるSubreconの数を調整することができます。「Subrecon」の値で出力されるSubreconの数が固定されます。(基本値: '1', 範囲: 0 ~ )