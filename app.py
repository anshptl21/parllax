import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import streamlit as st
import streamlit.components.v1 as components
#import requests
#import time
#import webbrowser
#import lxml.html
import os
#from react import jsx
#import pandas as pd
#import pandas_profiling
#from streamlit_pandas_profiling import st_profile_report
#from annotated_text import annotated_text, annotation
#from annotated_text import annotated_text
from pymed import PubMed
from pprint import pprint
from Bio import Entrez
Entrez.email = "sejaldua@gmail.com"
handle = Entrez.einfo() # or esearch, efetch, ...
record = Entrez.read(handle)
handle.close()


#importing css
def local_css(file_name, url):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)
        st.markdown(f'<link href= "{url}" rel="stylesheet">', unsafe_allow_html = True)
    return None
local_css("app.css", "https://fonts.googleapis.com/icon?family=Material+Icons")
#query_search function with filter
def querySearch(keywords):
    #taking in search term and getting results
      refined_search = keywords.lower()
      article_info = []
      pubmed = PubMed(tool="MyTool", email="sejaldua@gmail.com")
      results = pubmed.query(refined_search , max_results=num_of_results)
      result_list = list(results)
      pprint(result_list[0].toDict())
    # if results are none - return try again
      if len(result_list) == 0:
        zero_results = st.write("No results. Try another search term.")
        return zero_results
    #otherwise give resutls
      else:
        result_list_results = len(result_list)
        count = 0
    #for loop for formatting articles
        search_term_results = st.info(f'Number of Results: {result_list_results}')
        for t, article in enumerate(result_list):
          article_info.insert(t, article.toDict())
          dicts = article_info[t]
          doi = dicts.get("doi")
          authors = dicts.get("authors")
    #formatting authors
          for i in range(len(authors)):
            if "lastname" in authors[i]:
                auth_lastname = authors[i].get("lastname")
            if "firstname" in authors[i]:
                auth_firstname = authors[i].get("firstname")
            if "affiliation" in authors[i]:
                auth_affiliation = authors[i].get("affiliation")
            authors[i] = f'{auth_lastname} {auth_firstname} | {auth_affiliation}'
    #formatting id/doi
          id = dicts.get("pubmed_id")
              
          if doi != None:
            if "\n" in doi:
                doi_index = doi.index("\n")
                dicts.update({"doi" : article.doi[0:doi_index]})
          if id != None:
            if "\n" in id:
                id_index = id.index("\n")
                dicts.update({"pubmed_id" : article.pubmed_id[0:id_index]})
          elif id == None:
              dicts.update({"pubmed_id" : "None"})
              
          # SEJAL to ANSH: uncomment the code below find similar articles

          dicts["link"] = "https://pubmed.ncbi.nlm.nih.gov/" + dicts.get("pubmed_id")
    #if filter is applied - do this: will only occur is options aren't none
          format = st.header(t+1, f'{t+1}'), st.header(f'[{dicts.get("title")}]({dicts.get("link")})'), "\n", st.write(f'Publication Date: {dicts.get("publication_date")}\n'), "\n", st.write(f'PubMed Id: {dicts.get("pubmed_id")}\n'), "\n", st.write(f'Journal: {dicts.get("journal")}'), "/n", st.write(f'Authors: {dicts.get("authors")}\n'), "\n", st.write(f'Keywords: {dicts.get("keywords")}\n'), "\n", st.write(f'Abstract: {dicts.get("abstract")}\n')
          st.write(id, dicts.get('title'))
          handle = Entrez.elink(dbfrom="pubmed", id=id, linkname="pubmed_pubmed")
          record = Entrez.read(handle)
          handle.close()
          st.write(record[0]["LinkSetDb"][0]["LinkName"])
          # pubmed_pubmed
          linked = [link["Id"] for link in record[0]["LinkSetDb"][0]["Link"]][:5]
          st.write(linked)
          

#creating search bar
st.sidebar.markdown(
"""  <i class = "material-icons">search</i> """, unsafe_allow_html = True )
search_query = st.sidebar.empty()
input = search_query.text_input("Search", value = "Nanotechnology", key = "search_bar")
num_of_results = st.sidebar.slider("Number of Results", 1, 100, 1)

#creating and storing filter option
st.sidebar.markdown(
""" <div id = "filter">Filters</div> """, unsafe_allow_html = True)

#st.session - intilziaing and storing filter options
if "key_word_options" not in st.session_state:
    st.session_state["key_word_options"] = None
if "apply_filter_state" not in st.session_state:
    st.session_state["apply_filter_state"] = False

# choose options and apply filters button
options = st.sidebar.multiselect(
    'Elements',
    ['ID', 'Abstract', 'Title', 'Link', "Publication Date", 'Authors', 'Journal',])
apply_filter = st.sidebar.button("Apply Filters")

#if filter button was pressed or true + if options isn't equal to none
if apply_filter or st.session_state["apply_filter_state"]:
    if options != []:
        remove_filter = st.sidebar.button("Remove Fiters")
        message = "Filters On"
        st.session_state["apply_filter_state"] = True
        st.session_state["key_word_options"] = options
        if remove_filter:
            st.session_state["apply_filter_state"] = False
            st.session_state["apply_filter_state"] = False
            message = "Filters Off - Remove Any Keywords to Search"
        st.sidebar.write(message)

    else:
        st.sidebar.write("Please choose a keyword first")


# try:
search_term = input
results = str(querySearch(search_term))
# except Exception as e:
# st.info("Too Many Requests For Server. Please Wait")
# else:
#     st.write(results)

#back to top link
st.markdown("<a id = 'back_to_top_btn' href='#1'>Back To Top</a>", unsafe_allow_html = True)





#df = pd.read_csv("https://storage.googleapis.com/tf-datasets/titanic/train.csv")#
#pr = df.profile_report()

#st_profile_report(pr)

#for i in diseases:
#  querySearch(i)
#for j in treatments:
#  querySearch(j)
