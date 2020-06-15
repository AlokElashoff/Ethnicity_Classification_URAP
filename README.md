# Ethnicity_Classification_URAP

(https://arxiv.org/pdf/1708.07903v1.pdf)
This paper guided this approach to predicting ethnicity based on a resume. The goal is to use the principle of homiphily (people associate with others of similar ethnicity)
to predict ethnicity.

# Code Breakdown
1. dataProcessing.py - Given a directory of json resumes, creates two dictionaries containing the information we need.
  name_to_related - goes from names to urls of related people on linkedin
  
  url_to_name - goes from urls to names
  
2. randomDataSample.py - Given the outputs from dataProcessing.py, creates a random sample of people and their connections
  from a seed number. It only takes people who have connections (~1/20). Essentially is a depth 2 search and will create pairs
  of people.
3. adjacenyList.py - Creates an adjaceny list from a randomDataSample.
4. sampledGraph.py - Given an adjaceny list, creates a graph and labels all people via:
  US Census
  Character Set
  Homiphily

# Further Steps
1. Rerun the process on the newer version of the data. See if there is a higher rate of connections.
2. Train a more traditional classifier based on the resumes, by hand selecting features that do not relate to employment.
