import pandas as pd
from config import GRANULARITIES

ALL_COMMENTS_COLUMNS = [col for col in example_df.columns if "comment" in col.lower() and "each" not in col.lower() and type(example_df[col][0]) == str]

# verify that all granularities have the same comment columns
for granularity in GRANULARITIES:
    example_df = code_snippets[granularity][PROJECTS_NAMES[0]]
    all_comments_columns = [col for col in example_df.columns if "comment" in col.lower() and "each" not in col.lower() and type(example_df[col][0]) == str]
    assert all_comments_columns == ALL_COMMENTS_COLUMNS, f"Granularity {granularity} has different comment columns: {all_comments_columns} != {ALL_COMMENTS_COLUMNS}"

print("Verification complete: all the granularities have the same comments columns...")


def remove_comments_from_all_codes(df : pd.DataFrame) -> pd.DataFrame:



def remove_comments_from_code(code : str, comments_set : str) -> str:
    for comment in comments_set:
        if comment.strip() != "":
            code = code.replace(comment, "")
    
    return code