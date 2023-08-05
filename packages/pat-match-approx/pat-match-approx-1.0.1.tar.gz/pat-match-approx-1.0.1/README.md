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
pip install pat-match-approx
```
- Build locally:
    - Make sure you fulfil the requirements.
    - `pip install .`
    - That's it.
- Proceeding with any of the above methods will install the version `1.0.1`(current).
- Finally, both the above methods will install the following cmd tool: `gp9-mapper`.

## Usage:
`gp9-mapper`

```commandline
gp9-mapper [-h] [-p] [-d DISTANCE] [-o OUT_FILE_NAME] fasta_file [fastq_file]
```

```text
usage: gp9-mapper [-h] [-p] [-d DISTANCE] [-o OUT_FILE_NAME] fasta_file [fastq_file]

Matches a pattern using the naive suffix-tree implementation

positional arguments:
  fasta_file        fasta file
  fastq_file        fastq file

optional arguments:
  -h, --help        show this help message and exit
  -p                preprocess genome
  -d DISTANCE       distance
  -o OUT_FILE_NAME  output filename
```
-  preprocessing text-file in the current directory when ran with `-p` option. E.g.
   ```commandline 
   gp9-mapper -p fasta_input.fa 
   ```
   outputs
   ```text
    /path/to/current/dir/fasta_input_sa-lcp.txt
   ```

-  output sam-file(name based on the fasta input file) in the current director when ran without the `-p` option. E.g.
   ```commandline 
   gp9-mapper -d 1 -o /path/to/out.sam fasta_input.fa fastq_input.fq 
   ```
   outputs a file at
   ```text
    /path/to/out.sam
   ```
   <u>NOTE</u>: Before running this, the tool expects that you have a preprocessed text-file named based on the input fasta file.