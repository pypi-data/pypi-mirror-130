# This package constructs a suffix array using the naive implementation and provides with the functionality of searching Pattern using Improved Binary Search or Using BWT arrays.

## Folder structure
- `resources/` - contains our experiment results and test inputs
- `scripts` - contains python scripts(except the `setup.py` file which is in the root)
- The files under project root is required to properly package our script and build the command line tools
## Requirements:
- python version >= 3.9
- setuptools
- wheel
- pip >= 3.9

## Installation:
- Using Pip:
```commandline
pip install pat-match-bs-bwt
```
- Build locally:
    - Make sure you fulfil the requirements.
    - `pip install .`
    - That's it.
- Proceeding with any of the above methods will install the version `1.0.0`(current).
- Finally, both the above methods will install the following cmd tool: `search-bs` and `search-bw`.

## Usage:
- `search-bs`

```commandline
search-bs [-h] [-p] [-o OUT_FILE_NAME] fasta_file [fastq_file]
```

```text
usage: search-bs [-h] [-p] [-o OUT_FILE_NAME] fasta_file [fastq_file]

Matches a pattern using the improved binary search implementation

positional arguments:
  fasta_file        fasta file
  fastq_file        fastq file

optional arguments:
  -h, --help        show this help message and exit
  -p                preprocess genome
  -o OUT_FILE_NAME  output filename
```
-  preprocessing text-file in the current directory when ran with `-p` option. E.g.
   ```commandline 
   search-bs -p fasta_input.fa 
   ```
   outputs
   ```text
    /path/to/current/dir/fasta_input_processed.txt
   ```

-  output sam-file(name based on the fasta input file) in the current director when ran without the `-p` option. E.g.
   ```commandline 
   search-bs -o /path/to/out.sam fasta_input.fa fastq_input.fq 
   ```
   outputs a file at
   ```text
    /path/to/out.sam
   ```

- `search-bw`


```commandline
search-bw [-h] [-p] [-o OUT_FILE_NAME] fasta_file [fastq_file]
```

```text
usage: search-bw [-h] [-p] [-o OUT_FILE_NAME] fasta_file [fastq_file]

Matches a pattern using the BWT arrays implementation

positional arguments:
  fasta_file        fasta file
  fastq_file        fastq file

optional arguments:
  -h, --help        show this help message and exit
  -p                preprocess genome
  -o OUT_FILE_NAME  output filename
```
- preprocessing text-file in the current directory when ran with `-p` option. E.g.
   ```commandline 
   search-bw -p fasta_input.fa 
   ```
   outputs
   ```text
    /path/to/current/dir/fasta_input_processed.txt
   ```

- output sam-file(name based on the fasta input file) in the current director when ran without the `-p` option. E.g.
   ```commandline 
   search-bw -o /path/to/out.sam fasta_input.fa fastq_input.fq 
   ```
   outputs a file at
   ```text
    /path/to/out.sam
   ```
- <u>NOTE</u>: Before running this, the tool expects that you have a preprocessed text-file named based on the input fasta file.
