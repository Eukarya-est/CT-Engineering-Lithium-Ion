2025.10.15

# Components; 構成ファイル
1. session-extractor.py
2. README.md
3. config/search_key.json
    - The list of Scan settings to search
4. config/dictionary.json
    - The dictionary of values of scansettings
5. config/subrecon.py
    - The configuration for number of subrecon
6. config/path.py
    - The configuration for the path of target directory
7. config/name.py
    - The configuration for the name of output file

# How to Use; 使用方法
## 1. Unzip the ‘session-extractor.zip’  \ 「session-extractor.zip」を解凍する
## 2. Set the path of ‘Site’ via ‘/config/path.py' \ 「/config/path.py」で'Site’のパスを設定する
## 3. Set the name of output file via ‘/config/name.py' \ 「/config/name.py」で出力ファイルの名前を設定する
- Example) Name: str = 'CT_Engineering' → CT_Engineering_20251016023221.txt, CT_Engineering_20251016023221.csv
## 4. Set the other configuration in ‘config' directory (Refer to ‘How to set details’) \ 「config」フォルダにて他の設定を行う。(「詳細設定方法」 参照)
## 5. execute the 'session-extractor.py' script \ 「session-extractor.py」を実行する。
```shell
    python3 session-extractor.py 
```
## 6. Get the text result file \ 結果ファイルを得る。
- Example) Site_20251015013919.txt, Site_20251015013919.csv

# How to set details \ 詳細設定方法
## 1. Search Key Setting \ Search Key 設定
- ‘Search key' is keyword to search in .xml file \ 「Search key」は .xmlファイルから探すキーワードなります。
- There is NOT ‘Search key', then the extractor does NOT search the element \ 「Search key」がない場合、extractorが該当要素を探索しません。
- ‘Search key' setting is from ‘/config/search_key.json’ \ 「/config/search_key.json」から「Search key」を設定することが可能です。
- Example)
    - The ‘kiloVolts’ element in .xml file is for ‘kV’ scan setting. \ 「kiloVolts」 要素は「kV」スキャン設定の指している。
    - Input “kiloVolts”:”kV” into ‘group' key in /config/search_key.json, Then the Extractor searches ‘kiloVolts’ in .xml file and transform the name to ‘kV’ \ 「“kiloVolts”:”kV”」を「/config/search_key.json」の中身 ‘group’ キーに追加すると、Extractorが.xmlファイルにで「kiloVolts」要素を見つかり「kV」に変換する。
## 2. Dictionary for value of search key \ Search Keyのvalue字引設定
- ‘Dictionary' is reference for translating value of a specific ‘Search Key' in .xml file \ 「Dictionary」は 特定「Search Key」に対するvalue字引になります。
- Example)
    - The ‘groupType’ element in .xml file is for ‘Scan Type’ scan setting and value ‘4' of the ‘groupType’ is for ‘Scout’ Scan Type   \ 「groupType」要素は「Scan Type」スキャン設定、値「4」は「Scout」Scan Typeをの指している。
    - Input “groupType”:”Scan Type” into ‘group' key in /config/search_key.json, Then the Extractor searches ‘groupType’ in .xml file and transform the name to ‘Scan Type’ \ 「“groupType”:”Scan Type”」を「/config/search_key.json」の中身 「group」 キーに追加すると、Extractorが.xmlファイルにで「groupType」要素を見つかり「Scan Type」に変換する。
    - In ‘/config/dicitionary.json’, input ‘Scan Type' key and “4”:”Scout” into the ‘Scan Type' key,  Then the Extractor searches transform the value ’4' to ‘Scout’ \ 「/config/dicitionary.json」に「Scan Type」キーを追加してその中に 「”4”:”Scout”」を追加すると、Extractorが「4」値を「Scout」に変換する。
## 3. Subrecon Setting (The number of Subrecon) \ Subrecon 設定 (Subrecon出力個数設定)
- The number of subrecon depend on ‘Subrecon’ of /config/subrecon.py (Default: 1, Range: 0 - ) \ 「/config/subrecon.py」中に「Subrecon」の値で出力されるSubreconの数を調整することができます。「Subrecon」の値で出力されるSubreconの数が固定されます。(基本値: '1', 範囲: 0 ~ )