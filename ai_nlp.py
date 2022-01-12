from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from enum import Enum


class SummaryModel:

    def __init__(self, model_type: str, **kwargs):
        # I used this construction method to make it easier to add new models and model types in the future.
        if model_type in Models.__members__.keys():
            self.model = Models[model_type].value(**kwargs)
        else:
            raise Exception(f"Model {model_type} not abailable.\nAvailable models are: {Models.__members__.keys()}")

    def get_summary(self, text):
        return self.model.get_summary(text)


class SummaryModelTest(SummaryModel):
    def __init__(self):
        pass

    def get_summary(self, text):
        summary = f"Test summary of string {text}"
        return summary


class SummaryModelTransformer(SummaryModel):
    def __init__(self, hf_model_name: str = "sshleifer/distilbart-cnn-12-6"):
        self.tokenizer = AutoTokenizer.from_pretrained(hf_model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(hf_model_name)

    def get_summary(self, text):
        assert type(text) == str, f"Input text must be a string but found {type(text)}"
        inputs = self.tokenizer.encode(text, return_tensors="pt", max_length=512)
        outputs = self.model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4,
                                      early_stopping=True)
        summary = self.tokenizer.batch_decode(outputs)[0]
        return summary[7:-4]  # remove useless characters given as output by the tokenizer


class Models(Enum):
    TRANSFORMERS = SummaryModelTransformer
    # NLTK = SummaryModelTest
    TEST = SummaryModelTest


if __name__ == '__main__':
    # simple AI model test
    text = "this is a test text from which we want to extract a good summary!"
    summary_model = SummaryModel('TRANSFORMERS', hf_model_name="sshleifer/distilbart-cnn-12-6")
    # summary_model = SummaryModel('nothing')
    summary = summary_model.get_summary(text)
    print(summary)
