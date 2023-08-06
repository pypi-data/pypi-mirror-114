# Package `dipwmsearch`

## Description
Dedicated package to `dipwmsearch` through a text. Provides different approaches to seek for motifs (diPWM) through a text (for example a sequence) :
- sliding window (`search_semi_naive`)
- enumeration of valids words and AhoCorasick search of that set of words through the text (`search_aho`)
- super alphabet search (`search_super`)

## Install
### Local installation using git

- clone the git repository
```bash
git clone git@gite.lirmm.fr:rivals/dipwmsearch.git
```
- go to the root of the folder
```bash
cd dipwmsearch
```

- use the `Makefile` to install
```bash
make install
```

### Installation using pip

```bash
pip install dipwmsearch
```


## Getting started

- To import the package
```python
import dipwmsearch as ds
```

- To parse a diPWM file and create an object diPWM
```python
diP = ds.create_diPwm(diPwm_path_file)
```

- To use the enumeration and Aho-Corasick search
```python
for start_position, word, score in ds.search_aho_ratio(diP, text, ratio):
	   print(f'{start_position}\t{word}\t{score}')
```

## Documentation
More info in the [documentation](https://rivals.lirmm.net/dipwmsearch/)

## License
License type: CeCILL-B
[More info](https://cecill.info/licences/Licence_CeCILL-B_V1-en.html)

## Authors

- Marie Mille (main contributor)
- Bastien Cazaux
- Julie Ripoll
- Eric Rivals

## Dependencies
### Basics to install
- `pyahocorasick`

### For tests
- `pytest`
- `pandas`
