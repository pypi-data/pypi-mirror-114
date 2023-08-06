# WordHuntAnagram
 Play iMessage Anagram and wordhunt or any search word game using this `module`.

# Example

`
    
    from wordhuntanagram.wordhunt import WordHunt

    word = WordHunt(4, 4, args='yiuonhjnhffhggdb')
    word.hunt()
    print(word.words)

`

`
    
    from wordhuntanagram.anagram import Anagram

    anagram = Anagram(6, args='ioijbf')
    anagram.hunt()
    print(anagram.words)

`

---
Note that you have to be quick in doing all this. Its advisable to use a while loop.

---

`

    run = True
    while run:
        type_ = input("Choose type: (wordhunt-w/anagram-a)")
        if type_ == 'w' or type_ == 'wordhunt':
            word = WordHunt(4, 4)
            word.hunt()
            for item in word.words:
                print(item, '', word.words[item])
        elif type_ == 'a' or type_ == 'anagram':
            anagram = Anagram(6)
            anagram.hunt()
            for item in word.words:
                print(item, '', word.words[item])
        else:
            print("Input valid type")
        continuation = input("Press y to continue, any key to exit")
        if continuation != 'y':
            run = False
        else:
            ### you can clear the terminal here
            pass

`

**Enjoy!**