from collections import Counter

text = """
Jak to jest być skrybą, dobrze.
Moim zdaniem to nie ma tak, że dobrze albo że nie dobrze.
Gdybym miał powiedzieć, co cenię w życiu najbardziej, powiedziałbym, że ludzi.
Ekhm Ludzi, którzy podali mi pomocną dłoń, kiedy sobie nie radziłem, kiedy byłem sam.
I co ciekawe, to właśnie przypadkowe spotkania wpływają na nasze życie.
Chodzi o to, że kiedy wyznaje się pewne wartości, nawet pozornie uniwersalne, bywa, że nie znajduje się zrozumienia, które by tak rzec, które pomaga się nam rozwijać.
Ja miałem szczęście, by tak rzec, ponieważ je znalazłem.
I dziękuję życiu.
Dziękuję mu, życie to śpiew, życie to taniec, życie to miłość.
Wielu ludzi pyta mnie o to samo, ale jak ty to robisz?, skąd czerpiesz tę radość?
A ja odpowiadam, że to proste, to umiłowanie życia, to właśnie ono sprawia, że dzisiaj na przykład buduję maszyny, a jutro kto wie, dlaczego by nie, oddam się pracy społecznej i będę ot, choćby sadzić znaczy marchew.
"""

def analyzeText(text):
    paragraphs = text.split('\n')
    sentences = [sentence for paragraph in paragraphs for sentence in paragraph.split('.')]
    words = text.split(" ")
    print(f"Liczba akapitów: {len(paragraphs)}")
    print(f"Liczba zdań: {len(sentences)}")
    print(f"Liczba znaków: {len(words)}")

    stopWords = {'a', 'w', 'z', 'i', 'o', 'the', 'or', 'to'}
    filteredWords = filter(lambda word: word not in stopWords, words)

    wordCount = Counter(filteredWords)
    mostCommon = wordCount.most_common(5)
    print(f"Najczęstsze słowa: {mostCommon}")

    reverseAWords = [word[::-1] if word.lower().startswith('a') else word for word in words]
    print(f"Odwrócone słowo na A: {' '.join(reverseAWords)}")

analyzeText(text)