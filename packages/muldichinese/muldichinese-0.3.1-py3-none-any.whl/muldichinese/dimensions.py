#!/usr/bin/python3
# coding=UTF-8 #note capitalisation

#dependencies
import os
import csv
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np


class MulDiChinese:

    def __init__(self, file_path):
        if not os.path.exists(file_path):
            raise ValueError(
                f"MulDi Chinese did not find the files at: {file_path}")
        self.file_path = file_path
        self.feature_file = self.file_path+'linguistic_features.csv'

    def print_filepath(self):
        print(self.file_path)

    #create dataframe from standardised feature frequencies
    def dimensions(self): 
        stats=pd.read_csv(self.feature_file, header=0, index_col=0, quoting=csv.QUOTE_NONE)
        stdsc = StandardScaler()
        stats_std = stdsc.fit_transform(stats)
        df = pd.DataFrame(data=np.array(stats_std), index=stats.index, columns=stats.columns)
        text_list=list(df.index.values)

        dimension1_scores=[(df.loc[text, 'question']+df.loc[text, 'particle']+df.loc[text, 'exclamation']+df.loc[text, 'SPP']+df.loc[text, 'interrogative']+df.loc[text, 'PUBV']+df.loc[text, 'mono_negation']+df.loc[text, 'Chinese_person']+df.loc[text, 'honourifics']+df.loc[text, 'FPP']+df.loc[text, 'INPR']+df.loc[text, 'emotion']-df.loc[text, 'AWL']) for text in text_list]
        dimension1_scores=[round(x, 3) for x in dimension1_scores]

        dimension2_scores=[(df.loc[text, 'descriptive']+df.loc[text, 'imperfect']+df.loc[text, 'adverbial_marker_di']+df.loc[text, 'simile']+df.loc[text, 'PEAS']+df.loc[text, 'onomatopoeia']+df.loc[text, 'TPP']+df.loc[text, 'classifier']+df.loc[text, 'mono_verbs']+df.loc[text, 'SMP']+df.loc[text, 'complement_marker_de']) for text in text_list]
        dimension2_scores=[round(x, 3) for x in dimension2_scores]

        dimension3_scores=[(df.loc[text, 'BE']+df.loc[text, 'COND']+df.loc[text, 'modify_adv']+df.loc[text, 'AMP']+df.loc[text, 'EX']+df.loc[text, 'HDG']+df.loc[text, 'DWNT']+df.loc[text, 'RB']+df.loc[text, 'di_negation']+df.loc[text, 'HSK_3']+df.loc[text, 'DEMP']+df.loc[text, 'PRIV']+df.loc[text, 'HSK_1']+df.loc[text, 'other_personal']-df.loc[text, 'noun']) for text in text_list]
        dimension3_scores=[round(x, 3) for x in dimension3_scores]

        dimension4_scores=[(df.loc[text, 'ACL']+df.loc[text, 'ASL']+df.loc[text, 'ASL_std']+df.loc[text, 'PHC']+df.loc[text, 'BPIN']-df.loc[text, 'unique']-df.loc[text, 'intransitive']-df.loc[text, 'di_verbs']) for text in text_list]
        dimension4_scores=[round(x, 3) for x in dimension4_scores]

        dimension5_scores=[(df.loc[text, 'classical_gram']+df.loc[text, 'classical_syntax']-df.loc[text, 'aux_adj']-df.loc[text, 'lexical_density']-df.loc[text, 'NOMZ']-df.loc[text, 'disyllabic_words']) for text in text_list]
        dimension5_scores=[round(x, 3) for x in dimension5_scores]

        #create dataframe for dimension scores
        d = {'text': text_list, 'dimension1':dimension1_scores, 'dimension2':dimension2_scores,    'dimension3':dimension3_scores, 'dimension4':dimension4_scores,    'dimension5':dimension5_scores}
        dimension_scores = pd.DataFrame(data=d)

        #write dimension scores
        dimension_scores.to_csv(self.file_path + 'dimension_scores.csv', index=False)

        print("Completed. Dimension scores written.")