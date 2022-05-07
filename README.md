<!-- vim:set et sw=4 ts=4 tw=72: -->
# Math Expert
*Let me do your work*

## Preview

https://user-images.githubusercontent.com/63563250/167239624-4faf126e-fd08-49f9-87df-b7820664ca6c.mp4

## Introduction

**Math Expert** is our ([@salastro](https://github.com/salastro), [@younis-tarek](https://github.com/younis-tarek),
[@marawn-mogeb](https://github.com/marawan-mogeb)) math high school
graduation project. The project tackles the problem of generating
beautiful, quick, and useful mathematics. While most software can either
only generate beautiful formatted PDF (i.e. [LaTeX](https://www.latex-project.org/))
or sufficiently solve mathematical problems (e.g. [Wolfram|Alpha](https://wolframalpha.com/)).
There may be, however, alternatives to these tools, yet they can not
fully grasp the potential of either of them or are slow and hard-to-use.
Therefore, this project tries to do what other failed in.

## Inner Workings

Our approach was to create an easy to use graphical user interface (GUI)
that uses different components to reach our goal. LaTeX is the main PDF
generation backend due to its indubitable abilities and speed; it is the
universal standard for mathematical notation. However, it is reasonably
hard to use making it difficult to use in a short-term practical
context. This makes the done application even more useful. It was mainly
interacted with through [PyLaTeX](https://jeltef.github.io/PyLaTeX/); it
provides a usable set of commands that make use of LaTeX's capabilities.

Although both [SymPy](https://www.sympy.org/) and [NumPy](https://numpy.org/)
were used, the focus was on SymPy due to the symbolic focus of the
project. The latter is powerful in mathematical evaluations, which
— although supported — is not the focus of this project.

## Usage

Although the interface is obvious, some clarifications may need to be
made.
* First text input is the file name without extension
* Second text input is the document title
* Third text input is the author(s) title
* Fourth (and last) text input is the mathematical expression to be
  operated on
    * Euler's number should be written as `exp(x)` instead of `e^(x)`
    * `log` is the natural logarithm.
    * Multiplication should be written in the form `2*x`
* After defining all the previous inputs, click *Generate PDF*
* Choose the type of operation you want to perform, then click *Generate
  PDF* again

## Dependences
### Building
* [Python](https://www.python.org/) 3.10:
    * [PyLaTeX](https://jeltef.github.io/PyLaTeX/) 1.4
    * [SymPy](https://www.sympy.org/) 1.10
    * [NumPy](https://numpy.org/) 1.22
    * [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) 5.15
### Running
[LaTeX](https://www.latex-project.org/) (see https://github.com/salastro/math-expert/issues/9)

## Philosophy

It follows the *just works* philosophy and focuses on getting stuff
done. The code base is so bad that we could be paid not to work on it.
There is no clear structure followed. Sometimes you fill find patterns
that is clear crystal, yet they are avoided to make a worse codebase. We
do not believe in: OO, Functional, Array, Prototype, Procedural,
Declarative, or any other programming paradigm known to human kind. Only
aliens will understand the paradigms of this code.

## COCOMO estimations
***Using [scc](https://github.com/boyter/scc)***
```
───────────────────────────────────────────────────────────────────────────────
Language                 Files     Lines   Blanks  Comments     Code Complexity
───────────────────────────────────────────────────────────────────────────────
Python                       3       396       30        16      350         14
───────────────────────────────────────────────────────────────────────────────
Total                        3       396       30        16      350         14
───────────────────────────────────────────────────────────────────────────────
Estimated Cost to Develop (organic) $8,971
Estimated Schedule Effort (organic) 2.293525 months
Estimated People Required (organic) 0.347520
───────────────────────────────────────────────────────────────────────────────
Processed 16605 bytes, 0.017 megabytes (SI)
───────────────────────────────────────────────────────────────────────────────

```
