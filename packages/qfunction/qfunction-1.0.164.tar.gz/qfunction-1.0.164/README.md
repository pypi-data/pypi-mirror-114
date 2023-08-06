
<h1 align='center'>Qfunction</h1>
<p align='center'>
<img height='150px' width='200px' src='https://raw.githubusercontent.com/gpftc/qfunction/main/img/q_logo.png' style='height:200; witdh:200'>
 <br/>
<a href="https://github.com/perseu912"><img title="Autor" src="https://img.shields.io/badge/Autor-reinan_br-blue.svg?style=for-the-badge&logo=github"></a>
<br/>
<a href='http://dgp.cnpq.br/dgp/espelhogrupo/0180330616769073'><img src='https://shields.io/badge/cnpq-grupo_de_fisica_computacional_ifsertao--pe-blueviolet?logo=appveyor&style=for-the-badge'></a>
<br/>
<p align='center'>
<!-- github dados -->
<a href='https://python.org'><img src='https://img.shields.io/github/pipenv/locked/python-version/gpftc/covid_br'></a>
<a href='#'><img src='https://img.shields.io/github/languages/code-size/gpftc/qfunction'></a>
<a href='#'><img src='https://img.shields.io/github/commit-activity/w/gpftc/qfunction'></a>
<a href='#'><img src='https://img.shields.io/github/last-commit/gpftc/qfunction'></a>
<br/>
<!-- sites de pacotes -->
<a href='https://pypi.org/project/qfunction/'><img src='https://img.shields.io/pypi/v/qfunction'></a>
<a href='#'><img src='https://img.shields.io/pypi/wheel/qfunction'></a>
<a href='#'><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dd/covidbr"></a>
<a href='#'><img src='https://img.shields.io/pypi/implementation/covidbr'></a>
<br/>
<!-- outros premios e analises -->
<a href='#'><img alt="CodeFactor Grade" src="https://img.shields.io/codefactor/grade/github/gpftc/covid_br?logo=codefactor">
</a>
<!-- redes sociais -->
<br/>
<a href='https://instagram.com/gpftc_ifsertao/'><img src='https://shields.io/badge/insta-gpftc_ifsertao-violet?logo=instagram&style=flat'></a>
</p>
</p>
<p align='center'> <b>Library for researcher with statistics and mechanics equation non-extensive 📈📊📚</b></p>

#
This package is for development and works using the deformed non-extensive algebra, using for calculus, the simple algebra and the specials functions from quantum mechanics and theoretical physic, on the non-extensive mode.
<br/>
The all functions and equation on this work, is based in the articles and papers from  <a href='https://scholar.google.com.br/citations?user=wYFK45wAAAAJ&hl=pt-BR'>Dr. Bruno G. da Costa</a>, your friend, the <a href='https://scholar.google.com.br/citations?user=veVPJ4AAAAAJ&hl=pt-BR'>PhD Ignácio S. Gomes</a> and others peoples and articles about the non-extensive works.


## Installation:
this lib is found on the site of packages for python the <a href='https://pypi.org'>pypi</a> and on the site that is a repository for the codes with licenses from majority business of the word, the <a href='https://github.com'>github</a>.

##  Examples
<hr/>

### fundamentals
#### simple algebra

```py
from qfunction.fundamentals.canonic import prod
from qfunction.fundamentals import q_sum,q_mult,q_ln,q_sub

#the sum deformed on q=1
print(q_sum(4,2,1,q=1)) 
#output: 6

#the sum deformed on q=1.9
print(q_sum(4,2,1,q=1.9)) 
#output: -0.200000000000351

#the multiplication deformed on q=1
print(q_mult(1,2,q=1))
#output: 2

#the multiplication deformed on q=.8
print(q_mult(1,2,q=.8))
#output: 1.9999999999999998

#the natural logarithm on q=1
print(q_ln(3,q=1))
#output: 1.0984848484848484

#the natural logarithm deformed on q=.5
print(q_ln(3,q=.5))
#output: 1.4641016151377162

print(q_sub(4,3,q=.9))

```
### Quantum
#### creating a quantum circuit base

```py
from qfunction.quantum import QuantumCircuit as Qc

q = 1.
qc = Qc(4,q=q)
qc.Y(2)
qc.H(2,1)
qc.med(2)
#print(qc)
```
#### any equations
```py
from qfunction.quantum.equations import S,S_q
from qfunction.fundamentals import q_cos,q_sin
from numpy import array,linspace,pi

t = array([1,2,34,56,34,23])
p = t/t.sum()
#print(p)
#print(S(p))

t = linspace(-2,2,100)*2*pi

theta = t/2
gamma = t
q =1

## testing the entropy deformed  ##
print(S_q(theta,gamma,q))

q = .5
print(S_q(theta,gamma,q))

q = 1.5
print(S_q(theta,gamma,q))
```
### Algorithms
#### one simlpe example of code game on quantum circuit deformed
```py
from qfunction.quantum import QuantumCircuit as Qc
from qfunction.quantum.algorithms import ArenaGame

q = .9
qc = Qc(1,q=q)
game = ArenaGame(qc=qc)

game.up()
game.left()
game.left()
game.show()
```
<hr/>
<a href='https://colab.research.google.com/drive/1VjJoG36JH6A5h1VSgsIFYlHmnLMk4jpl#scrollTo=4eCILB58O2VG'><h3>Others Examples on colab.</h3></a>