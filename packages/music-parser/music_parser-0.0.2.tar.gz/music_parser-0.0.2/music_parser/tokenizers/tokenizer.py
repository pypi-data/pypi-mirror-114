from music_parser.columns import column
from tqdm import tqdm
"""Abstract class for all tokenizers as well as general functions"""


"""Tokenizers responsible for getting dataframe in final form. Each column will be tokens for ready for input"""
class Tokenizer:
    def __init__(self, fns, checks = []):
        self.fns = fns
        self.checks = checks
    
    def appendFn(self, fn):
        self.fns.append(fn)
    
    def check(self, columns):
        if(False in [ele in columns for ele in self.checks]):
            raise Exception(f"Dataframe must have the following columns: {self.checks}")


    def tokenize(self, df, fp = None):
        self.check(df.columns)

        print("tokenizing:")
        for fn in tqdm(self.fns):
            df = fn(df)
        if(fp != None):
            df.to_csv(fp)
        return df


def combineColumns(df, columnsToCombine, combinedColumnName, drop = False):
    df[combinedColumnName] = ["_".join([str(ele) for ele in row]) for row in zip(*[df[col].to_list() for col in columnsToCombine])]
    return df

        
def dropColumns(df, columnsToDrop):
    return df.drop(columnsToDrop, 1)


def dropColumnsExcept(df, columnsToNotDrop):
    return df.drop(df.columns.difference(columnsToNotDrop), 1)

