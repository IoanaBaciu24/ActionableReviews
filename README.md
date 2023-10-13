# Actionable Reviews

The aim of this project is to create a system that allows the user to get concrete and actionable insights from google play reviews of an app.

To get started, clone the project, create an environment and install the project:

```
cd ActionableReviews
python3 -m venv env
source env/bin/activate
pip install -e .
```

`Actionable Reviews` has 4 components. Each component normally uses as input the result of the previous component, however, the components can be used independently as well. 

## Scraper App

The purpose of the scraper app is to get reviews of a given app. The implementation currently supports Google Play reviews.

To run the scraper app you need to first edit the config file ```config/scrapper.json```:

```
{
    "app_name": <GOOGLE_PLAY_APP_ID>,
    "language": <LANGUAGE>,
    "country": <COUNTRY>,
    "count": <NUMBER_OF_REVIEWS_TO_SCRAPE>,

    "path_out": <OUTPUT_FILE_NAME>
}
```

An example of this, for Duolingo, is already in the repository.

After this is done, run ```main_dataset.py``` with the config file as an argument:

```
python3 main_dataset.py config/scrapper.json
```

The result of this module is a dataset that contains reviews for a given app, saved in ```<OUTPUT_FILE_NAME>```.

## Classifier App

The classifier app takes a dataset of reviews, and labes them in two categories: `actionable` and `non-actionable`. We consider a review to be actionable if, by reading it, one can take a concrete action to improve the product. For instance, _I hate this app_ is informative with respect to the feelings of the user, but it doesn't help the creator improve the product, so it is non-actionable. A review like _I hate that this app shows me 20 ads before I can use it_ can lead to an action (showing less ads), so it should be labeled as actionable. 

To run the classifier app, you should first edit the config file ```config/classification.json```

```
{
    "model":<OPENAI_LLM_MODEL_NAME>,
    "type":<TYPE_OF_MODEL>, # "chat", for the chat based classifier, "instruct" for models that are not compatible with Langchain's chat llms
    "dataset_path":<PATH_TO_DATASET>, # it can be the output file of the Scrapper App
    "output_path":<OUTPUT_PATH> # here you will save the labelled dataset
}
```

Then run:

```
python3 main_classify_dataset.py config/classification.json
```

## Clustering App

The clustering app takes only the actionable reviews, embeds them and them clusters them based on their semantic similarity. The purpose of this part of the project is to groupt the reviews that have similar content.

Start by editing ```config/clustering.json```: 

```

{
    "embed": <True/False>, # True if you didn't save the embeddings yet
    "source_path": <PATH>, #Classified reviews dataset, can be the output of the Classification App
    "embeddings_path": <OUTPUT_PATH>, # path to save the embeddings
    "embedding_model": <MODEL_NAME>, # name of model that is compatible to the Sentence Transformers module from Huggingface

    "elbow":<True/False>, # True if you want to first cluster multiple times, so that you can do the elbow method
    "min_clusters":<INT>,
    "max_clusters":<INT>,
    "do_plot":<BOOL>,

    "label_reviews": <True/False>, # True if you want to save the labels to a file
    "number_of_clusters": 40,
    "output_labels_path": <OUTPUT PATH>
}

```

Then run:

```
python3 main_clustering.py config/clustering.json
```