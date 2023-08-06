## mofid singular finder

A simple library for finding words with Second person singular pronouns.
for example:
* ماشینم : False
* ماشینت : True
* رفتم : False
* رفتی : True

***
### Installation
### Usage
    from mofid_singular_finder import SingularDetector
    word = SingularDetector()
    word = word.singular_checker("حسابت")
    print(word)
#### input
should be string
#### output
Boolean:

    True, If the word is in the second person singular.
    Flase, otherwise.
