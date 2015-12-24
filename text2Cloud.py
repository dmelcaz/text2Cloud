#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import operator

def cleanText(text):

    # Salvamos los guiones
    text = text.replace('-\n', '')

    # Quito signos de puntuacion
    text = re.sub('[.,:!@#$%^&*()/_|•><\-¡¿?]', '', text)

    # Fuera números
    text = re.sub('[0-9]', '', text)

    # Devuelvo una lista de palabras
    text = re.sub('\n', ' ', text)

    # Filtro las palabras por número de letras
    text = ' '.join([w for w in text.split() if len(w)>3])

    return text.lower()

def applySubs(text, filename):
    # Cargo la lista de reemplazos
    replaceList = open(filename, 'r')

    # Efectuo los reemplazos
    for line in replaceList:
        replace = line.split()
        text = re.sub(replace[0] + ' ', replace[1], text)

    return text


if __name__ == '__main__':
    
    # Número de palabras en el Cloud
    wordNum = 100

    for arg in sys.argv:
        inputFile = arg

    # Lectura del texto extraido del pdf
    textFile = open(inputFile, 'r')
    text = textFile.read()

    # Limpieza del texto y aplicación de sustituciones
    text = cleanText(text)
    text = applySubs(text, 'replaceWords.txt')

    # Separo el texto en palabras
    words = text.split()

    # Diccionario donde la palabra actua como clave y las repeticiones como valor
    wordcount = {}

    # Lista de stop words
    stopWordList = open('stopWords.txt', 'r')
    stopWords = [str(line).rstrip() for line in stopWordList]

    # Bucle para contar el número de repeticiones de cada palabra
    for word in words:
        if word not in stopWords:
            if word not in wordcount:
                wordcount[word] = 0
            wordcount[word] += 1


    # Ordenos el vector con los resultados
    wordsSorted = sorted(wordcount.items(), key=operator.itemgetter(1))
    wordsSorted.reverse()


    # Resultados normalizados max:100 min:10
    maxval = wordsSorted[0][1]
    minval = wordsSorted[wordNum-1][1]
    rangeval = maxval-minval
    

    # String con el array
    result = '['
    for i in range(0,wordNum-2):
        result += '["%s",%d],' % (wordsSorted[i][0], (wordsSorted[i][1]-minval)*90/rangeval+10)
    result += '["%s",%d]]' % (wordsSorted[wordNum-1][0], (wordsSorted[wordNum-1][1]-minval)*90/rangeval+10)


    cloudFile = open('cloudTemplate.html', 'r')
    cloud = cloudFile.read()
    cloud = re.sub('resultArray', result, cloud)
    cloudFile.close

    outFile = open('index.html', 'w')
    outFile.write(cloud)
    outFile.close
