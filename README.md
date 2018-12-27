# sentences - find similar sentences

This is a homework project for Craig Douglas' [*Big Data and Mining*](http://mgnet.org/~douglas/Classes/bigdata/index.html) class, written in python. This is my second trial. My first trial is written in C and used a different definition of distance and is not *github*-ed.

## Problem Description

### Distance Function

A *change* to a sentence <img src="https://rawgit.com/xhu4/sentences/master/svgs/c745b9b57c145ec5577b82542b2df546.svg?invert_in_darkmode" align=middle width=10.537065pt height=14.10255pt/> can be:

* deleting a word from <img src="https://rawgit.com/xhu4/sentences/master/svgs/c745b9b57c145ec5577b82542b2df546.svg?invert_in_darkmode" align=middle width=10.537065pt height=14.10255pt/>;
* or adding a word to <img src="https://rawgit.com/xhu4/sentences/master/svgs/c745b9b57c145ec5577b82542b2df546.svg?invert_in_darkmode" align=middle width=10.537065pt height=14.10255pt/>.

A distance function <img src="https://rawgit.com/xhu4/sentences/master/svgs/9edebb8c5008b7dbd2689724ff970994.svg?invert_in_darkmode" align=middle width=37.648875pt height=24.56553pt/> of sentences is then defined as:

<p align="center"><img src="https://rawgit.com/xhu4/sentences/master/svgs/05b20461c52238f15ae91425337cf3d0.svg?invert_in_darkmode" align=middle width=444.6980208pt height=16.438356pt/></p>

The goal is to filter out a set of sentences in a text file, given <img src="https://rawgit.com/xhu4/sentences/master/svgs/63bb9849783d01d91403bc9a5fea12a2.svg?invert_in_darkmode" align=middle width=9.041505pt height=22.74591pt/>, such that:

* for any two distinct sentences <img src="https://rawgit.com/xhu4/sentences/master/svgs/d7093223b4d827e8c29d4ed84b7ae088.svg?invert_in_darkmode" align=middle width=27.95364pt height=22.74591pt/> in output file, <img src="https://rawgit.com/xhu4/sentences/master/svgs/96249f7c090ac68c03ddb83326555ddc.svg?invert_in_darkmode" align=middle width=80.12994pt height=24.56553pt/>,
* and for every sentence <img src="https://rawgit.com/xhu4/sentences/master/svgs/c745b9b57c145ec5577b82542b2df546.svg?invert_in_darkmode" align=middle width=10.537065pt height=14.10255pt/> in the input file, there is at least a sentence <img src="https://rawgit.com/xhu4/sentences/master/svgs/8217ed3c32a785f0b5aad4055f432ad8.svg?invert_in_darkmode" align=middle width=10.1277pt height=22.74591pt/> in 
  the output file such that <img src="https://rawgit.com/xhu4/sentences/master/svgs/2e282cf564be11414c36cc367cedcdec.svg?invert_in_darkmode" align=middle width=80.12994pt height=24.56553pt/>.

---

## Usage

This code is written in Python 2 but should be compatible with python3. 4 currently built-in 
modules are employed: `timeit`, `collections`, `itertools`, and `argparse`.

Run `python[3] sentences.py -h` to show usage information:

```sh
usage: sentences.py [-h] [-d [K]] [-o [filename]] [infile]

Solve Big Sentences Problem.

positional arguments:
  infile                input file

optional arguments:
  -h, --help            show this help message and exit
  -d [K], --dist [K]    Distance k, default: 0
  -o [filename], --outfile [filename]
                        Output filename. No output file will be generated if
                        not provided.
```

### Example

Solve distance 2 problem on *1M.txt*, and write the result to file *out.txt*:

```sh
python sentences.py 1M.txt -d2 -o out.txt
```

---

## Algorithm

For distance 0, `set` container is used to remove identical sentences. The code without I/O 
can be implemented in one line:

```python
distinct_sentences = set(input_sentences)
```

Since `set` is implemented using hash table, this algorithm has a linear complexity to the 
number of sentences.

The rest of this section talks about solving <img src="https://rawgit.com/xhu4/sentences/master/svgs/8733ac5ecc35ea70e3e236ade3c28a60.svg?invert_in_darkmode" align=middle width=39.101865pt height=22.74591pt/>.

### Basic Idea

We define some notations as follows:

* <img src="https://rawgit.com/xhu4/sentences/master/svgs/0794595b496cc9157977e2858fc49255.svg?invert_in_darkmode" align=middle width=28.48494pt height=24.56553pt/>: number of words of sentence <img src="https://rawgit.com/xhu4/sentences/master/svgs/c745b9b57c145ec5577b82542b2df546.svg?invert_in_darkmode" align=middle width=10.537065pt height=14.10255pt/>;
* <img src="https://rawgit.com/xhu4/sentences/master/svgs/50d755f7a5b0e4f0070fcddea3298af7.svg?invert_in_darkmode" align=middle width=40.410645pt height=19.10667pt/>: set of all strings that are sentence `\alpha` delete <img src="https://rawgit.com/xhu4/sentences/master/svgs/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode" align=middle width=9.83004pt height=14.10255pt/> words;
* <img src="https://rawgit.com/xhu4/sentences/master/svgs/808bfd7c24438423e9205226937534f7.svg?invert_in_darkmode" align=middle width=106.834035pt height=22.74591pt/>: <img src="https://rawgit.com/xhu4/sentences/master/svgs/e093d8f02802fb6e360298ca1eece6a2.svg?invert_in_darkmode" align=middle width=158.722245pt height=24.56553pt/>. Or, there exists a way 
  such that sentence <img src="https://rawgit.com/xhu4/sentences/master/svgs/c745b9b57c145ec5577b82542b2df546.svg?invert_in_darkmode" align=middle width=10.537065pt height=14.10255pt/> removing some <img src="https://rawgit.com/xhu4/sentences/master/svgs/0e51a2dede42189d77627c4d742822c3.svg?invert_in_darkmode" align=middle width=14.379255pt height=14.10255pt/> words is identical to sentence <img src="https://rawgit.com/xhu4/sentences/master/svgs/8217ed3c32a785f0b5aad4055f432ad8.svg?invert_in_darkmode" align=middle width=10.1277pt height=22.74591pt/> 
  removing <img src="https://rawgit.com/xhu4/sentences/master/svgs/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode" align=middle width=9.83004pt height=14.10255pt/> words;
  
Given two sentences <img src="https://rawgit.com/xhu4/sentences/master/svgs/c745b9b57c145ec5577b82542b2df546.svg?invert_in_darkmode" align=middle width=10.537065pt height=14.10255pt/> and <img src="https://rawgit.com/xhu4/sentences/master/svgs/651da20cd8f863cb3481bd6aa766d287.svg?invert_in_darkmode" align=middle width=29.224635pt height=22.74591pt/>, if

<p align="center"><img src="https://rawgit.com/xhu4/sentences/master/svgs/20805d87b4cf905539b8c19e3c48f5cc.svg?invert_in_darkmode" align=middle width=111.383085pt height=14.55729pt/></p>

then

<p align="center"><img src="https://rawgit.com/xhu4/sentences/master/svgs/7fa3351fd2f0111fc6ee9589ccdbb0aa.svg?invert_in_darkmode" align=middle width=275.59455pt height=16.376943pt/></p>

If <img src="https://rawgit.com/xhu4/sentences/master/svgs/9a1cadf7edaedea5b35c976a8ee22453.svg?invert_in_darkmode" align=middle width=137.970855pt height=24.56553pt/>, since <img src="https://rawgit.com/xhu4/sentences/master/svgs/c4526acbb1c9b612fdcc94cd36cc04e4.svg?invert_in_darkmode" align=middle width=142.72929pt height=24.56553pt/>, must have <img src="https://rawgit.com/xhu4/sentences/master/svgs/b0af4bfccba79e3d7b4867df584cb377.svg?invert_in_darkmode" align=middle width=75.558285pt height=22.74591pt/>. Thus

<p align="center"><img src="https://rawgit.com/xhu4/sentences/master/svgs/ed4d7b82a15341b5c68e8e2f84305946.svg?invert_in_darkmode" align=middle width=346.8267pt height=16.376943pt/></p>

Then <img src="https://rawgit.com/xhu4/sentences/master/svgs/3f49fc99e50a1ad77bd8c8dfed15f8aa.svg?invert_in_darkmode" align=middle width=80.12994pt height=24.56553pt/> if and only if

<p align="center"><img src="https://rawgit.com/xhu4/sentences/master/svgs/9bf91f4f2282c9d7c35b4e37fe669bf1.svg?invert_in_darkmode" align=middle width=260.4459pt height=16.376943pt/></p>
which is equivalent as
<p align="center"><img src="https://rawgit.com/xhu4/sentences/master/svgs/1c5be11a48f99064cfc1a5160e60235a.svg?invert_in_darkmode" align=middle width=285.58695pt height=39.30498pt/></p>

### Functions

For a set <img src="https://rawgit.com/xhu4/sentences/master/svgs/53d147e7f3fe6e47ee05b88b166bd3f6.svg?invert_in_darkmode" align=middle width=12.282765pt height=22.38192pt/> of <img src="https://rawgit.com/xhu4/sentences/master/svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.2397205pt height=14.10255pt/>-word sentences, and a set <img src="https://rawgit.com/xhu4/sentences/master/svgs/61e84f854bc6258d4108d08d4c4a0852.svg?invert_in_darkmode" align=middle width=13.243725pt height=22.38192pt/> of <img src="https://rawgit.com/xhu4/sentences/master/svgs/d5c18a8ca1894fd3a7d25f242cbe8890.svg?invert_in_darkmode" align=middle width=7.8985335pt height=14.10255pt/>-word sentences, say we want to 
remove all <img src="https://rawgit.com/xhu4/sentences/master/svgs/4055140544e47b792d3eb72348913116.svg?invert_in_darkmode" align=middle width=43.424865pt height=22.74591pt/>, where <img src="https://rawgit.com/xhu4/sentences/master/svgs/8fe2fac4eb2d77efffcdc6d534f15506.svg?invert_in_darkmode" align=middle width=80.12994pt height=24.56553pt/> for some <img src="https://rawgit.com/xhu4/sentences/master/svgs/140852cd080b024d735438df351bebc7.svg?invert_in_darkmode" align=middle width=42.870135pt height=22.38192pt/>. Without loss of 
generality, we assume <img src="https://rawgit.com/xhu4/sentences/master/svgs/e5c5062e7a758e33000e19fb59e03051.svg?invert_in_darkmode" align=middle width=38.00808pt height=20.83059pt/>. Two functions are written to solve two different cases: <img src="https://rawgit.com/xhu4/sentences/master/svgs/656e2f0f389dd67a66d1019404b187ca.svg?invert_in_darkmode" align=middle width=151.584675pt height=22.74591pt/>, which are `amam()` and `ambn()` respectively.

### Traps and Tricks

One can easily end up deleting more sentences than they should when <img src="https://rawgit.com/xhu4/sentences/master/svgs/f9bbd08bf846520586581437c960abac.svg?invert_in_darkmode" align=middle width=39.101865pt height=22.74591pt/>. For example, we 
decide to remove <img src="https://rawgit.com/xhu4/sentences/master/svgs/c745b9b57c145ec5577b82542b2df546.svg?invert_in_darkmode" align=middle width=10.537065pt height=14.10255pt/> because <img src="https://rawgit.com/xhu4/sentences/master/svgs/8fe2fac4eb2d77efffcdc6d534f15506.svg?invert_in_darkmode" align=middle width=80.12994pt height=24.56553pt/> for some <img src="https://rawgit.com/xhu4/sentences/master/svgs/8217ed3c32a785f0b5aad4055f432ad8.svg?invert_in_darkmode" align=middle width=10.1277pt height=22.74591pt/>, and then remove 
<img src="https://rawgit.com/xhu4/sentences/master/svgs/8217ed3c32a785f0b5aad4055f432ad8.svg?invert_in_darkmode" align=middle width=10.1277pt height=22.74591pt/> because <img src="https://rawgit.com/xhu4/sentences/master/svgs/45a5678c1336e3335f188fa0221c87c4.svg?invert_in_darkmode" align=middle width=78.984675pt height=24.56553pt/>, then there is a chance we cannot find any sentence in 
our result within distance <img src="https://rawgit.com/xhu4/sentences/master/svgs/63bb9849783d01d91403bc9a5fea12a2.svg?invert_in_darkmode" align=middle width=9.041505pt height=22.74591pt/> of <img src="https://rawgit.com/xhu4/sentences/master/svgs/c745b9b57c145ec5577b82542b2df546.svg?invert_in_darkmode" align=middle width=10.537065pt height=14.10255pt/>. To avoid such situation, we go through all 
sentences from the longest to the shortest, and always remove the shorter sentences when a 
pair of neighbors is found.

---

## Result & Performance

File metadata:

| Input file | # of lines | file size |
| :--------: | ---------- | --------- |
|  100.txt   | 100        | 12K       |
|   1K.txt   | 1,000      | 96K       |
|  10K.txt   | 10,000     | 884K      |
|  100K.txt  | 100,000    | 8.4M      |
|   1M.txt   | 1,000,000  | 85M       |
|   5M.txt   | 5,000,000  | 428M      |
|  25M.txt   | 25,000,000 | 2.1G      |

Performance (in second):

| Input file | Distance 0 | Distance 1 | Distance 2  |
| :--------: | ---------- | ---------- | ----------- |
|  100.txt   | 0.000120   | 0.002948   | 0.002877    |
|   1K.txt   | 0.000390   | 0.016582   | 0.131046    |
|  10K.txt   | 0.003342   | 0.148118   | 1.858770    |
|  100K.txt  | 0.040530   | 1.492312   | 21.979624   |
|   1M.txt   | 0.545091   | 16.050876  | 287.006949  |
|   5M.txt   | 2.829443   | 72.055627  | 1526.300508 |
|  25M.txt   | 18.832576  | 250.135241 | 5350.679652 |

Result (# of output sentences)

| Input file | Distance 0 | Distance 1 | Distance 2 |
| :--------: | ---------- | ---------- | ---------- |
|  100.txt   | 98         | 98         | 98         |
|   1K.txt   | 921        | 921        | 917        |
|  10K.txt   | 9179       | 9160       | 9075       |
|  100K.txt  | 84111      | 83646      | 80873      |
|   1M.txt   | 769170     | 760391     | 714946     |
|   5M.txt   | 3049422    | 2996383    | 2763966    |
|  25M.txt   | 8703720    | 8506155    | 7712287    |

---

## Reference

The **Big Sentences** problem is described in [Craig's webpage](http://mgnet.org/~douglas/Classes/common-problems/index.html#BigSentences), which also contains all sentence files used in the above section.

---

## Roadmap

- [ ] Add unit test
