import os, en_core_web_sm

class SentenceParser(object):
    def __init__(self, directoryname):
        self.directoryname = directoryname
        self.nlp = en_core_web_sm.load()

    def __iter__(self):
        for filename in os.listdir(self.directoryname):
            content = ""
            with open(os.path.join(self.directoryname, filename)) as fdoc:
                content = fdoc.read()

            for doc in nlp.pipe(content, batch_size=10000, n_threads=3):
                for sentence in doc.sents:
                    yield [token.lower_ for token in sentence
                           if not token.is_punct and not token.is_space and not token.is_stop]