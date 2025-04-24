from copy import deepcopy

from tabulate import tabulate

from utils.example import Example

class Preprocessor:
  
    def __init__(self, data: list):
        self.data = data

    def _get_context(self, row):
        pre_table_context = '\n'.join(row['pre_text'])
        post_table_context = '\n'.join(row['post_text'])
        return pre_table_context, post_table_context
    
    def _make_example(self, row):
        pre_table_context, post_table_context = self._get_context(row)
        return Example(
            question=row['qa']['question'],
            answer=row['qa']['exe_ans'],
            pre_table_context=pre_table_context,
            post_table_context=post_table_context,
            table=self._list_table_to_text_table(row.get("table")),
        )
    
    def _get_examples(self, row: dict):
        if row.get('qa'):
            return [self._make_example(row)]

        flattened = []
        for k, v in row.items():
            if k.startswith('qa_'):
                copied_row = deepcopy(row)
                copied_row['qa'] = v
                flattened.append(self._make_example(copied_row))
        return flattened
    

    def _list_table_to_text_table(self, table):
        # Transpose column-major to row-major
        row_major = list(map(list, zip(*table)))

        # First row after transpose becomes the header
        headers = row_major[0]
        data = row_major[1:]

        # Pretty print
        return tabulate(data, headers=headers, tablefmt='grid')

    def preprocess(self):
        examples = []
        for row in self.data:
            examples.extend(self._get_examples(row))
        return examples



