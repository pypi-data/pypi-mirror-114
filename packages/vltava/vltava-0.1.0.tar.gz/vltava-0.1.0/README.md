# Vltava

[1]: https://nlp.fi.muni.cz/czech-morphology-analyser/
[2]: https://ufal.mff.cuni.cz/morphodita
[3]: https://github.com/petrpulc/python-majka
[4]: https://pypi.org/project/ufal.morphodita/

Opinionated Czech language processing.

The processor takes in raw documents and applies basic preprocessing
(such as tags and accent striping) and lemmatization using either [Majka][1]
or [MorphoDiTa][2].

```python
from vltava import DocumentProcessor

doc = "v televizi říkali, že zítra pršet nebude"
document_processor = DocumentProcessor()
result = document_processor.process(doc)
# result is ['televize', 'rikat', 'zitra', 'prset', 'byt']
```

`DocumentProcessor` supports multiprocessing when dealing with
large collections of documents.

```python
from vltava import DocumentProcessor

docs = ["Ahoj, jak se máš?"] * 100

result = DocumentProcessor().process_from_iterable(docs, n_jobs=2)
```

## Backend

The package is using two different backends for finding Czech lemmas:
[Majka][1], [MorphoDiTa][2]. Check out the links for more information.
The required binary files are contained directly in the package.

- [Majka Python API][3]
- [MorphoDiTa Python API][4]

## Public API

### `vltava.DocumentProcessor`

```python
vltava.DocumentProcessor(backend: str = "majka")
```

Initializes `DocumentProcessor` with the selected `backend`.

__Methods:__

```python
DocumentProcessor.process(
    self, doc: str, tokenize: bool = True
) -> Union[str, List[str]]
```

Processes the input `doc` and returns it as a processed
string or a list of processed tokens, if `tokenize` is `True`.

```python
DocumentProcessor.process_from_iterable(
    self, docs: Iterable[str], tokenize: bool = True, n_jobs: int = 1
) -> Union[Iterable[str], Iterable[List[str]]]:
```

Processes the input `docs` collection of documents. Result is either
an iterable of processed strings or an iterable of lists of processed
tokens (if `tokenize` is `True`).

If `n_jobs` is greater than one, multiple worker are launched to
process the documents.

## Installation

```bash
pip install vltava
```
