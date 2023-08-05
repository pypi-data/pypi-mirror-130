# TextPreprocessing

This is the beta release of TextPreprocessing library. This library currenly capable of cleansing your text data for modal training.

TextPreprocessing library can do the below actions:

    * Expand general abbreviations
    * Clear email ids in the text data
    * Clear web URLs
    * Clear html tags present in the text dataset
    * Clear ordianl, cardinal numbers, date, person name, etc.
    * Clear gibberish charsets
    * Removes english stop words
    * Lemetize the text
    * Correct spelling errors.

We are enhancing this package on a regular basis and adding more flexible components to it in the upcoming releases. Please do update this package on frequently.

### How to install this package?

```
pip install TextPreprocessing

```
- Post installing the package, please install spacy en_core_web_md library.

```
python spacy download en_core_web_md
```

### How to use the package?

```
>>> from TextPreprocessing.preprocess import preprocess
>>> obj = preprocess()
>>> obj.__version__
'3.0.0'
>>> entities_ignore_list = ["PERSON", "ORDINAL", "CARDINAL", "DATE", "TIME", "PRODUCT"]
>>> obj.load_language_model("en_core_web_md") // Add any spacy language model
>>> obj.set_entity_ignore_list(entities_ignore_list) // Add the list of entities needs to excluded from your dataset.
>>> texts = ["""Good morning Natalia A, here are the detailed items listed below:  Loan ID: PNIO-UIZD Store Invoice: NOT SENT (ONLY Affirm Transaction ID) Transaction ID: 0011473451  Please let me know of any other info needed to assist you in regards to this unfulfilled purchase.  Sincerely,  William Langford  Again, here is the credentials required to process my request, reference #: 210916-000538""", """Adam,  Sorry, I was out of town with limited network access but getting back to you now.  I donâ€™t think I made myself clear enough before, I have had MyC loud Version 5 installed for over a year on the PR4100 but, there was a new version 5 update automatically installed on October 30, 2021 with version 5.18.117 and since that update, we have not been able to access the PR4100 locally through the network.  We can however access the PR4100 using the mycloud.com web access.  The PR4100 is connected to the internet with the Google Nest router and we are able to access the dashboard pages with no issues.  Please find the attached error we get after accessing the PR4100 a second time after reboot and any time thereafter.  Thank you in advance.  Brent D. Beck"""]
>>> obj.reset_start()
>>> results = list(map(lambda x: obj.cleanup(x, len(texts)), texts))
1/2
2/2

>>> print(results)
```

**Output**

```
['good morning detailed item list loan i d no did store voice send affirm transaction i d transaction i d 0011473451 let know into need assist regard unfulfilled purchase sincerely credentials require process request reference 210916 0538', 'sorry town limit network access get donaTMt think clear my loud version instal year new version update automatically instal version 18 117 update able access locally network access cloud com web access connect internet goose nest outer able access dashboard page issue find attach error access time report time thank advance']

```
