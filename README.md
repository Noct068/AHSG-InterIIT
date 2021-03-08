# AHSG-InterIIT
Automated Headline and Sentiment Generator for Inter IIT tech meet 2021

### Important links:
1. [Google Doc file to keep track of our progress](https://docs.google.com/document/d/1SsXJjiLKxtuJC0whoP9daylfpWBGX4FuSvZZn7yImU0/edit?usp=sharing)
2. [Google Doc file for Queries answered by the Inter-IIT organizing team](https://docs.google.com/document/d/1y9IlOsstIJrhFlsqhyTyyVYj5g_jIM1e19fMjlYUGOg/edit)
3. [Problem statement](https://drive.google.com/file/d/1RrHu3dIRgOdg6_qNTVy5iwVkeFGCcz_H/view?usp=sharing)
4. [Data folder](https://drive.google.com/drive/folders/1XMxbp0zFawmSGy0P_NKRSo3R5rC1qK4c?usp=sharing)
5. [Orignal and cleaned data in .pkl form (Use pd.read_pickle)](https://drive.google.com/drive/folders/1HgsfTcG-0uuxb8HOujyL5CrMFIiFrBjf?usp=sharing)
6. [External and custom datasets](https://drive.google.com/drive/u/1/folders/1pB028xxJml-ivJoWWFweY_i96DLwVs8n)
### To-Do List

- [ ] Data Preprocessing
    - [ ] Remove redundant text
    - [ ] Convert Emojis to associated text
    - [ ] Transliteration of Hinglish to English
- [ ] Binary Classification for `mobile_tech`
    - [ ] Use of traditional classifiers using Bag-of-Words or Tf-Idf vectorizer
    - [ ] Benchmark Performance using BERT or variant  
    - [ ] Benchmark Performance using cross-lingual model like XLM Model
- [ ] Identifying `mobile brands` in text
    - [ ] Search for external datasets and pretrained models for this task
- [ ] Identify sentiment associated with recognized `mobile brands` from text
- [ ] Headline generation in english for articles with `mobile tech`



### Evaluation Criteria
- `0.4 x (F1 score of Mobile Tech Classification) + 0.2 x (Accuracy of Brand Identification) + 0.2 x ( F1 score Sentiment Analysis) + 0.2 x (Average Similarity Score)`
- Other metrics (mentioned in the case study) would aid the judges to understand the output better while the ones mentioned above would be used to compute the final score for submission. 
- In case of a tie, judges will look at the innovation in approaches, execution time, and scalability of the solution to decide the winner.
