import os
import majka
from ufal.morphodita import Morpho, TaggedLemmas

from gensim.utils import deaccent
from gensim.parsing.preprocessing import (
    preprocess_string,
    strip_tags,
    strip_punctuation,
    strip_multiple_whitespaces,
    strip_numeric,
    remove_stopwords,
    strip_short
)

import multiprocessing as mp

from functools import partial
from pkg_resources import get_distribution
# from importlib.resources import path
from typing import Iterable, List, Union


_PREPROCESSING = [
    strip_tags,
    strip_punctuation,
    strip_multiple_whitespaces,
    strip_numeric,
    remove_stopwords,
    strip_short,
    deaccent,
    lambda x: x.lower(),
]

_STOPWORDS_FILE_NAME = "cs.stopwords"
_MAJKA_FILE_NAME = "majka.w-lt"
_MORPHODITA_FILE_NAME = "nlp_czech-morfflex-161115-no_dia.dict"


__module_name__ = 'vltava'

try:
    __version__ = get_distribution(__module_name__).version
except Exception:
    __version__ = 'unknown'


def _get_resource_path(file_name: str) -> str:
    """
    Returns a full path to a file in the `resources` directory.
    """

    this_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(this_dir, 'resources', file_name)


class _SerializableMajka(majka.Majka):
    """
    Wrapper around the `majka.Majka` class allowing serialization.
    """

    def __init__(self, db_file_path):

        self._db_file_path = db_file_path
        super().__init__(db_file_path)

    def __reduce__(self):

        return (majka.Majka, (self._db_file_path,))


class _MajkaAnalyzer:
    """
    Analyzer backend for finding word lemmas using MorphoDiTa database.

    Info: https://nlp.fi.muni.cz/ma/
    """

    def __init__(self):

        self._morph = _SerializableMajka(_get_resource_path(_MAJKA_FILE_NAME))

        self._morph.flags = majka.ADD_DIACRITICS
        self._morph.tags = False
        self._morph.first_only = True

    def get_lemma(self, raw_word: str) -> str:
        """
        Tries to find the lemma for the input `raw_word`.
        Returns the original word if no lemma is found.
        """

        lemma_list = self._morph.find(raw_word)

        if not lemma_list:
            return raw_word

        return lemma_list[0]['lemma']


class _MorphoditaAnalyzer:
    """
    Analyzer backend for finding word lemmas using Majka database.

    Info: http://ufal.mff.cuni.cz/morphodita
    """

    def __init__(self):

        self._morph = Morpho.load(_get_resource_path(_MORPHODITA_FILE_NAME))

    def get_lemma(self, raw_word: str) -> str:
        """
        Tries to find the lemma for the input `raw_word`.
        Returns the original word if no lemma is found.
        """

        lemmas = TaggedLemmas()
        result = self._morph.analyze(raw_word, self._morph.GUESSER, lemmas)

        if result == -1:
            return raw_word
        else:
            return lemmas[0].lemma


class DocumentProcessor:
    """
    Opinionated Czech language processing.

    The processor takes in raw documents and applies basic preprocessing
    (such as tags and accent striping) and lemmatization using either Majka
    or MorphoDiTa database.

    Example:
    ```
    from vltava import DocumentProcessor

    doc = "v televizi říkali, že zítra pršet nebude"
    document_processor = DocumentProcessor()
    result = document_processor.process(doc)
    # result is ['televize', 'rikat', 'zitra', 'prset', 'byt']
    ```

    `DocumentProcessor` supports multiprocessing when dealing with
    large collections of documents.

    Example:
    ```
    from vltava import DocumentProcessor

    docs = ["Ahoj, jak se máš?"] * 100

    result = DocumentProcessor().process_from_iterable(docs, n_jobs=2)
    ```
    """

    _supported_backends = {
        "majka": _MajkaAnalyzer,
        # "morphodita": _MorphoditaAnalyzer
    }

    def __init__(self, backend: str = "majka"):
        """
        Initializes `DocumentProcessor` with the selected `backend`.
        """

        try:
            self._analyzer = self._supported_backends[backend]()
        except KeyError:
            raise ValueError(
                "Supported values for `backend` are: "
                f"{list(self._supported_backends.keys())}."
            )

        with open(_get_resource_path(_STOPWORDS_FILE_NAME)) as f:
            self._stopwords = set(f.read().split('\n'))

    def process(
        self, doc: str, tokenize: bool = True
    ) -> Union[str, List[str]]:
        """
        Processes the input `doc` and returns it as a processed
        string or a list of processed tokens, if `tokenize` is `True`.
        """

        preprocessed_doc = preprocess_string(doc, filters=_PREPROCESSING)

        # lemmatization reintroduces accents
        processed_doc = [
            deaccent(self._analyzer.get_lemma(token))
            for token in preprocessed_doc if token not in self._stopwords
        ]

        return processed_doc if tokenize else ' '.join(processed_doc)

    def process_from_iterable(
        self, docs: Iterable[str], tokenize: bool = True, n_jobs: int = 1
    ) -> Union[Iterable[str], Iterable[List[str]]]:
        """
        Processes the input `docs` collection of documents. Result is either
        an iterable of processed strings or an iterable of lists of processed
        tokens (if `tokenize` is `True`).

        If `n_jobs` is greater than one, multiple worker are launched to
        process the documents.
        """

        if n_jobs > 1:

            worker = partial(self.process, tokenize=tokenize)

            with mp.Pool(n_jobs) as p:
                return p.map(worker, docs)

        def gen():
            for doc in docs:
                yield self.process(doc, tokenize=tokenize)

        return gen()
