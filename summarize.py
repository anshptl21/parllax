import spacy 
import pytextrank
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from transformers import pipeline
import streamlit as st



def createSum(example_text):

    nlp = spacy.load("en_core_web_lg")

    print("summarizing...")

    # python -m spacy download en_core_web_lg

    nlp.add_pipe("textrank")

    # example_text = "The Adventures of Roderick Random, Scottish author and poet Tobias Smollett’s debut picaresque novel, was published in 1748 and is loosely based on Smollett’s experiences in the British Navy. Set in the 1730s and 1740s, the narrative follows the life of the main protagonist and narrator, Roderick “Rory” Random, from childhood to adulthood as Roderick journeys through England, France, the Caribbean, Africa, and Latin America. The Adventures of Roderick Random’s synopsis details the book as “one of the first truly global novels [that] casts light on nearly every aspect of its time—imperialism, gender relations, slavery, urban life, colonial warfare, commerce, politics, the professions, high society, and the Hogarthian underworld.Roderick’s father is a Scottish gentleman, but his mother is a common woman. His father’s high-class family is ashamed of the son’s marriage to a woman from low society and subsequently shuns Roderick’s parents. Roderick’s mother dies soon after giving birth to him, which leaves his father overwhelmed by grief. Lost and with no family left to financially support him, Roderick’s father flees and abandons his only son."

    doc = nlp(example_text)

    st.write(doc)

example_text = user_input = st.text_area("label goes here", "enter summary...")

createSum(example_text)

#for sent in doc._.textrank.summary(limit_sentences=2):
   # print(sent)

#model_name = "google/pegasus-xsum"
#
#pegasus_t = PegasusTokenizer.from_pretrained(model_name)
#
#pegasus_m = PegasusForConditionalGeneration.from_pretrained(model_name)
#
#tokens = pegasus_t(example_text, truncation=True, padding = 'longest', return_tensors="pt")
#
##print(tokens)
#
#encoded_summary = pegasus_m.generate(**tokens)
#
#decode_summary = pegasus_t.decode(encoded_summary[0], skip_special_tokens = True)
#
##print(decode_summary)
#                                  
#            
#summarizer = pipeline("summarization", model =model_name, tokenizer = pegasus_t, framework = "pt")
#
#summary = summarizer(example_text, min_length = 30)
#
#print(summary[0]["summary_text"])
      