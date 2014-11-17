mojibakeFix
===========

UTF-8で書かれたテキストをShift_JISで読み込んだ際に生じる文字化けを修正する


## Requirement
* python3


## Usage
    python .\mojibakeFix.py -f sample.txt


### Demo
    >> cat sample.txt
    譁・ｭ怜喧縺代＠縺滓枚蟄励・蠕ｩ蜈・ｒ陦後＞縺ｾ縺・
    >> python .\mojibakeFix.py -f sample.txt
    文字化けした文字の復元を行います