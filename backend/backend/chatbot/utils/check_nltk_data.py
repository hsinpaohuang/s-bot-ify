import nltk

def check_nltk_data():
    """
    Checks if the required NLTK datasets are present on the system.
    If not, ask the user for permission to download.
    """

    data = {
        'averaged_perceptron_tagger': 'taggers/averaged_perceptron_tagger/averaged_perceptron_tagger.pickle', # for `pos_tag_sents`
        'universal_tagset': 'taggers/universal_tagset/en-ptb.map', # for pos_tag_sents (tagset='universal')
        'wordnet': 'corpora/wordnet.zip/wordnet/', # for WordNetLemmatizer
    }
    missing_data = list[str]()

    for name, location in data.items():
        try:
            nltk.data.find(location)
        except LookupError:
            missing_data.append(name)

    if len(missing_data) > 0:
        print('Downloading datasets...')
        nltk.download(missing_data, quiet=True)
        # for some reasons, nltk.data.find cannot locate omw-1.4, so skipping its check and just download it here
        # omw-1.4 will not be required in future versions, see: https://github.com/nltk/nltk/issues/3024
        nltk.download('omw-1.4', quiet=True)
        print('Download complete.\n')
