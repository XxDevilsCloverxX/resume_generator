import PyPDF2 as pypdf  #extract a resume from pdf
import pandas as pd #manage resume in a df
from tkinter.filedialog import askopenfilename

def clean_list(lis, terms=set(['', '', '+',' ',',', '.', '-'])):
    #return a list that does not contain 'terms'
    res = [x for x in lis if x not in terms]
    return res

filepath = askopenfilename(defaultextension=".pdf", filetypes=[('pdf file', '*.pdf')])
#Create a pdf object
with open(filepath, 'rb') as pdfFile:
    #create a reader
    pdf_reader= pypdf.PdfFileReader(pdfFile)
    #create a page object
    page = pdf_reader.getPage(0)
    #extract the text and split the words by newlines (possible headers)
    words = page.extract_text().lower().split("\n")
    words = clean_list(words)
    #words is likely still a large list of strings of multiple words
    cleaner_words = []
    for key in words:
        #split key
        mini=key.split()
        for minikey in mini:
            minikey = "".join(char for char in minikey if char.isalnum())
            cleaner_words.append(minikey)#feed the mini keys into the list

    unique_terms = set(cleaner_words)   #used for dataframe
    #create a dictionary object
    dataset = {"Keywords":[], "Frequency": []}
    #key-freq pairs need to be added to the dataset
    for item in unique_terms:
        if item not in ["the", "and", 'with', "but", "for", "that"] and len(item)>=3:
            dataset["Keywords"].append(item)
            dataset["Frequency"].append(cleaner_words.count(item))

    #generate a data frame from the dataset
    df = pd.DataFrame(data=dataset["Frequency"], index=dataset["Keywords"], columns=["Frequency"])

#close PDF
pdfFile.close()

#dataframe established - now organization
df = df.copy()
df = df.sort_values(by="Frequency",ascending=False)

#redefining some bins that users resumes may reflect
df2 = pd.read_csv("bins.csv")
resume_df = df2.copy().transpose()
resume_df["BinCount"] = 0
resume_df = resume_df[["BinCount"]]   #we only care about bin_counts, return a dataframe
df["included"] = pd.Series(dtype=object)

#perform a lookup for items in df2
for col in df2:
    series = set(df2[col].dropna())
    #perform a match between individual words and index
    for cell in series:
        if cell in df.index:
            #add the frequency to the sub_category
            resume_df.loc[col]+= df.loc[cell,"Frequency"]
            df.loc[cell, "included"] = True
        else:
            #final check:
            for ind in df.index:
                if cell in ind:
                    resume_df.loc[col]+= df.loc[ind,"Frequency"]
                    df.loc[ind, "included"] = True

#sum up total focus words
total = resume_df["BinCount"].sum()
resume_df = (resume_df / total)
resume_df.columns = ["Relative Frequency"] #rename column
resume_df = resume_df.sort_values(by="Relative Frequency",ascending=False)
included_strings = df.loc[df["included"] == True].index


"""
resume_df will be the primary dataframe that this program will return
to other programs. However, the other, original datas are available.
The transpose, however, gets us the relative frequency column needed in the tk app.
"""
