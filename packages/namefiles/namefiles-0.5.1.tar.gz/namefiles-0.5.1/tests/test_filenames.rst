>>> from namefiles import disassemble_filename
>>> from doctestprinter import print_pandas
>>> from pandas import DataFrame
>>> test_filenames = [
...     "A",
...     "A#1",
...     "A#12",
...     "A#123",
...     "A#1234",
...     "A#1#SOURCE78",
...     "A#12#SOURCE7",
...     "A#123#SOURCE",
...     "A#1234#SOURC",
...     "A.txt",
...     "A#1.txt",
...     "A#12.txt",
...     "A#123.txt",
...     "A#1234.txt",
...     "A#1#SOURCE78.txt",
...     "A#12#SOURCE7.txt",
...     "A#123#SOURCE.txt",
...     "A#1234#SOURC.txt",
... ]
>>> sample_parts = [disassemble_filename(test_name) for test_name in test_filenames]
>>> sample_frame = DataFrame(sample_parts)
>>> column_order = [
...     "identifier", "sub_id", "source_id", "vargroup", "context", "extension"
... ]
>>> print_pandas(sample_frame[column_order])
    identifier  sub_id  source_id  vargroup  context  extension
 0           A
 1           A       1
 2           A      12
 3           A     123
 4           A    1234
 5           A       1   SOURCE78
 6           A      12    SOURCE7
 7           A     123     SOURCE
 8           A    1234      SOURC
 9           A                                             .txt
10           A       1                                     .txt
11           A      12                                     .txt
12           A     123                                     .txt
13           A    1234                                     .txt
14           A       1   SOURCE78                          .txt
15           A      12    SOURCE7                          .txt
16           A     123     SOURCE                          .txt
17           A    1234      SOURC                          .txt
