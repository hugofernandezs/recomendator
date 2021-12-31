# Sistema de recomendación
## Funciones del programa principal

### Recoger y separar todos los documentos
Lo primero que habrá que hacer es ir leyendo el archivo y separando todos los documentos y eliminar el contenido que consideremos necesario.
```python
filename = ps.parse_args().file
file = open(filename, "r")
matrix: list[list[str]] = list[list[str]]()
line: str = file.readline()
while len(line) > 0:
    matrix.append(ev.remove_stopwords(re.sub(r'[^\w]', ' ', line).lower()))
    line = file.readline()
```

Así mismo podemos ver como se usa la función remove_stopwords para eliminar las palabras que no aportan información relevante y los signos de puntuación.

### Análisis de los documentos
El siguiente paso es analizar los documentos y calcular el tf, idf y tf+idf de cada térmno.
```python
tf: list[dict[str]] = list[dict[str]]()
idf: list[dict[str]] = list[dict[str]]()
w: list[dict[str]] = list[dict[str]]()
for document in matrix:
    document_tf: dict[str] = ev.term_frequency(document)
    document_idf: dict[str] = ev.inverse_document_frequency(document, matrix)
    document_w: dict[str] = ev.tf_idf(document, document_tf, document_idf)
    tf.append(document_tf)
    idf.append(document_idf)
    w.append(document_w)
cosine: list[list[int]] = ev.calculate_similarity(w)
````

### Muestreo de los resultados
Por último podemos mostrar los resultados mediante un simple bucle for que irá recorriendo e imprimiendo.
```python
print(f"    Content Based Recommendation - {filename}      ".center(120, "#"))
print("")
trm = "Term_freq"
doc = "Doc_freq"
res = "tf + idf"
for i in range(len(matrix)):
    print(f"    Article {i+1}    ".center(40, "-"))
    print("")
    print("{:>20}{:>10}{:>10}".format(trm, doc, res))
    for key, value in tf[i].items():
        print("{:<14}{}{:>10}{:>10}".format(key, "{:.2f}".format(value),
                                            "{:.2f}".format(idf[i][key]),
                                            "{:.2f}".format(w[i][key])))
    print("\n")
print("")
print(f"    Cosine relation    ".center(40, "-"))
print("")
for i in range(len(cosine)):
    for j in range(len(cosine[i])):
        if j != i:
            print(f"cos(A{i+1}, A{j+1}) = {cosine[i][j]}")
print("")
```

### IDF
Este proceso calcula la frecuencia inversa en la que aparece un término en todos los documentos.
```python
def inverse_document_frequency(document: list[str], matrix: list[list[str]]) -> dict[str]:
    idf: dict[str] = dict[str]()
    for term in document:
        if term not in idf:
            idf[term] = log(len(matrix) / document_frequency(term, matrix))
    return idf
```
Recibe como parámetor el documento y la matriz con todos los documentos y por cad término del documento lo anañiza con todos los demás a ver en cuentos ser repite.

### TF
Este calcula la frecuencia con la que se repite un término en un documento.
```python
def inverse_document_frequency(document: list[str], matrix: list[list[str]]) -> dict[str]:
    idf: dict[str] = dict[str]()
    for term in document:
        if term not in idf:
            idf[term] = log(len(matrix) / document_frequency(term, matrix))
    return idf
```
Este evalúa cada término del documento viendo cuántas veces se repite y lo divide entre el número total de palabras.

### DF
Calcula la cantidad de documentos en los que se encuentra un término.
```python
def document_frequency(term: str, matrix: list[list[str]]) -> int:
    count: int = 0
    for document in matrix:
        for word in document:
            if word == term:
                count += 1
    return count
```
Recibe como parámetro el término y todos los documentos y lo va buscando por todos ellos calculando cuántas veces lo encuentra.

### TF + IDF
Es la medida general sobre cada término en cada documento.
```Python
def tf_idf(document: list[str], tf: dict[str], idf: dict[str]) -> dict[str]:
    w: dict[str] = dict[str]()
    for term in document:
        if term not in w:
            w[term] = tf[term] * idf[term]
    return w
```
Básicamente, para cada término, multiplica su TF por su IDF.

### Preprocesamiento
Antes de evaluar losa documentos es importante eliminar todas las palabras y símbolos que no nos aporten información útil, así ahorraremos tiempo de cómputo.
También debemos cambiar las mayúsculas por minúsculas, pues para nosotros tienen el mismo significado las palabras independientemente de si están en mayúsculas o minúsculas.
```python
def remove_stopwords(line: str) -> list[str]:
    filtered_sentence: list[str] = list[str]()
    for term in word_tokenize(line):
        if term not in set(stopwords.words('english')):
            filtered_sentence.append(term)
    return filtered_sentence
```

### Cosine sim
Calcula la distancia coseno entre todos los tf + idf de cada término en cada documento y hace una valoración de la similitud entre cad documento.
Siendo este el valor que nos interesa para comparar varios documentos.
```python
def calculate_similarity(w: list[dict[str]]) -> list[list[int]]:
    result: list[list[int]] = list[list[int]]()
    for original_document in w:
        original: list[int] = list(original_document.values())
        values: list[int]() = list[int]()
        for compared_document in w:
            sim: int = 0
            compared: list[int] = list(compared_document.values())
            if len(original) > len(compared):
                for i in range(len(compared)):
                    sim += compared[i] * original[i]
            else:
                for i in range(len(original)):
                    sim += compared[i] * original[i]
            values.append(sim)
        result.append(values)
    return result
```

## Ejemplo de uso
Para usar el programa debemos invocarlo mediante python+y pasarle como argumento un archivo de texto que queramos analizar.
```bash
python main.py -f documento.txt
```

Nos devolverá por pantalla toda la infromación útil.
```bash
#################################    Content Based Recommendation - document.txt      ##################################

-----------    Article 1    ------------

           Term_freq  Doc_freq  tf + idf
aromas        0.05      1.39      0.07
include       0.05      1.39      0.07
tropical      0.05      1.39      0.07
fruit         0.05      1.39      0.07
broom         0.05      1.39      0.07
brimstone     0.05      1.39      0.07
dried         0.01      0.69      0.00
herb          0.05      1.39      0.07
palate        0.05      1.39      0.07
overly        0.05      1.39      0.07
expressive    0.05      1.39      0.07
offering      0.05      1.39      0.07
unripened     0.05      1.39      0.07
apple         0.05      0.69      0.03
citrus        0.05      1.39      0.07
sage          0.05      1.39      0.07
alongside     0.05      1.39      0.07
brisk         0.05      1.39      0.07
acidity       0.05      0.00      0.00


-----------    Article 2    ------------

           Term_freq  Doc_freq  tf + idf
ripe          0.05      1.39      0.07
fruity        0.05      1.39      0.07
wine          0.05      0.69      0.03
smooth        0.05      1.39      0.07
still         0.05      1.39      0.07
structured    0.05      1.39      0.07
firm          0.05      1.39      0.07
tannins       0.05      1.39      0.07
filled        0.05      1.39      0.07
juicy         0.05      1.39      0.07
red           0.05      1.39      0.07
berry         0.05      1.39      0.07
fruits        0.05      0.69      0.03
freshened     0.05      1.39      0.07
acidity       0.05      0.00      0.00
already       0.05      1.39      0.07
drinkable     0.05      1.39      0.07
although      0.05      1.39      0.07
certainly     0.05      1.39      0.07
better        0.05      1.39      0.07
2016          0.05      1.39      0.07


-----------    Article 3    ------------

           Term_freq  Doc_freq  tf + idf
tart          0.06      1.39      0.08
snappy        0.06      1.39      0.08
flavors       0.01      0.69      0.00
lime          0.06      1.39      0.08
flesh         0.06      1.39      0.08
rind          0.06      1.39      0.08
dominate      0.06      1.39      0.08
green         0.06      1.39      0.08
pineapple     0.06      1.39      0.08
pokes         0.06      1.39      0.08
crisp         0.06      0.69      0.04
acidity       0.06      0.00      0.00
underscoring  0.06      1.39      0.08
wine          0.06      0.69      0.04
stainless     0.06      1.39      0.08
steel         0.06      1.39      0.08
fermented     0.06      1.39      0.08


-----------    Article 4    ------------

cos(A2, A3) = 0.06369321260350053
cos(A2, A4) = 0.06863614484545734
cos(A3, A1) = 0.06862767124732827
cos(A3, A2) = 0.06369321260350053
cos(A3, A4) = 0.07209076562115463
cos(A4, A1) = 0.07058963512182806
cos(A4, A2) = 0.06863614484545734
cos(A4, A3) = 0.07209076562115463
```
