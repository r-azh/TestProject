README.mdChapter 5 - Classification - Detecting Poor Answers
===================================================

1. run so_xml_to_tsv from book with correct DATA_DIR to get filtered data in feltered.tsv
 resulted data file structures:
  > filtered.tsv contains data in following format:
    Id <TAB> ParentId <TAB> IsAccepted <TAB> TimeToAnswer <TAB> Score <TAB> Text
  
  > filtered-meta.json contains data in following format:
    {ParentId: [[Id, IsAccepted, TimeToAnswer, Score], ... ]
    
2. run chose_instances form book with correct DATA_DIR
 for speed up processing filtered data is split to following files:
  > chosen.tsv contains data in following format:
  Id <TAB> Text
  
  > chosen-meta.json contains data in following format:
   { Id: {"ParentId": -1, "IsAccepted": 0, "TimeToAnswer": 0, "Score": 245, 
   "NumTextTokens": 136, "NumCodeLines": 0, "LinkCount": 0, "MisSpelledFraction": 0.0, 
   "NumImages": 0, "idx": 0, "Answers": [2452, 31910], "HasAcceptedAnswer": true}
   
4. import nltk
5. nltk.download('punkt')