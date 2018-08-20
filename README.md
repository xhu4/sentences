# Sentences - find similar sentences

## Problem Description

### Distance Function

A *change* to a sentence $\alpha$ can be:

* deleting a word from $\alpha$;
* or adding a word to $\alpha$.

A distance function $d(\cdot,\cdot)$ of sentences is then defined as:

$$ d(\alpha,\beta)\coloneqq\text{minimum number of changes applied to $\alpha$ to get $\beta$}. $$

The goal is to filter out a set of sentences in a text file, given $k$, such that:

* for any two distinct sentences $\alpha, \beta$ in output file, $d(\alpha,\beta)>k$,
* and for every sentence $\alpha$ in the input file, there is at least a sentence $\beta$ in the output file such that $d(\alpha,\beta)\le k$.

---

## Usage

This code is written in Python 2 but should be compatible with python3. 4 currently built-in modules are employed: `timeit`, `collections`, `itertools`, and `argparse`.

Run `python[3] Sentences.py -h` to show usage information:

```sh
usage: Sentences.py [-h] [-d [K]] [-o [filename]] [infile]

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
python Sentences.py 1M.txt -d2 -o out.txt
```

---

## Algorithm

For distance 0, `set` container is used to remove identical sentences. The code without I/O can be implemented in one line:

```python
distinct_sentences = set(input_sentences)
```

Since `set` is implemented using hash table, this algorithm has a linear complexity to the number of sentences.

The rest of this section talks about solving $k>1$.

### Basic Idea

We define some notations as follows:

* $l(\alpha)$: number of words of sentence $\alpha$;
* $\alpha - n$: set of all strings that are sentence `\alpha` delete $n$ words;
* $\alpha -m = \beta - n$: $(\alpha-m) \cap (\beta-n) \ne \emptyset$. Or, there exists a way such that sentence $\alpha$ removing some $m$ words is identical to sentence $\beta$ removing $n$ words;
  
Given two sentences $\alpha$ and $beta$, if

$$ \alpha-m = \beta-n, $$

then

$$ d(\alpha, \beta) = m+n-2p, \text{ for some } p \in \mathbb{N}.$$

If $l(\alpha)-l(\beta)=h\ge0$, since $l(\alpha)-m = l(\beta)-n$, must have $m-n=h$. Thus

$$ d(A,B) = h+2n+2p = h+2t, \text{ for some } t\in\mathbb{N}. $$

Then $d(\alpha, \beta) \le k$ if and only if

$$ \alpha - (t+h) = \beta - t, \text{ and } 2t+h\le k, $$
which is equivalent as
$$ \alpha - (t+h) = \beta - t,\; t=\operatorname{floor}\left(\frac{k-h}2\right). $$

### Functions

For a set $A$ of $p$-word sentences, and a set $B$ of $q$-word sentences, say we want to remove all $\beta\in B$, where $d(\alpha, \beta)\le k$ for some $\alpha\in A$. Without loss of generality, we assume $p\ge q$. Three functions are written to solve three different cases: $p = q,\; p-q=k,\;0<p-q<k$, which are `amam()`, `ambn()`, and `amb()` respectively.

---

## Result & Performance

Performance table (in second):

| Input file | Distance 0 | Distance 1 | Distance 2  |
| :--------: | ---------- | ---------- | ----------- |
| 100.txt    | 0.000120   | 0.002948   | 0.002877    |
| 1K.txt     | 0.000390   | 0.016582   | 0.131046    |
| 10K.txt    | 0.003342   | 0.148118   | 1.858770    |
| 100K.txt   | 0.040530   | 1.492312   | 21.979624   |
| 1M.txt     | 0.545091   | 16.050876  | 287.006949  |
| 5M.txt     | 2.829443   | 72.055627  | 1526.300508 |
| 25M.txt    | 18.832576  | 250.135241 | 5350.679652 |

Result (# of output sentences)

| Input file | Distance 0 | Distance 1 | Distance 2 |
| :--------: | ---------- | ---------- | ---------- |
| 100.txt    | 98         | 98         | 98         |
| 1K.txt     | 921        | 921        | 917        |
| 10K.txt    | 9179       | 9160       | 9075       |
| 100K.txt   | 84111      | 83646      | 80873      |
| 1M.txt     | 769170     | 760391     | 714946     |
| 5M.txt     | 3049422    | 2996383    | 2763966    |
| 25M.txt    | 8703720    | 8506155    | 7712287    |