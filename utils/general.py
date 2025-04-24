from tabulate import tabulate

from utils.example import Example

def list_table_to_text_table(table):
    # Transpose column-major to row-major
    row_major = list(map(list, zip(*table)))

    # First row after transpose becomes the header
    headers = row_major[0]
    data = row_major[1:]

    # Pretty print
    return tabulate(data, headers=headers, tablefmt='grid')

def get_context(row):
  pre_table_context = '\n'.join(row['pre_text'])
  post_table_context = '\n'.join(row['post_text'])
  context = pre_table_context + '\n' + post_table_context

def print_example(example: Example):
  print(f"""
  Example datapoint:
  Question: {example.question}
  Answer: {example.answer}
  Predicted answer: {example.predicted_answer if example.predicted_answer else 'Not yet predicted'}
  Table: {example.table}
  """)