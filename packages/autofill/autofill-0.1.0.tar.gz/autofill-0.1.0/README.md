# Autofill

Autofill is a Python library for dealing with auto-completion of words.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install autofill.

```bash
pip install autofill
```

## Usage

```python
from autofill import autofill

# register list of 'words' into autofill system
words = ["mobile", "mouse", "moneypot", "monitor", "mousepad"]
autofill.register_words(words)

# prefix search
autofill.search('mou') # returns ['mouse', 'mousepad']

# Find top k words from previous search matches
autofill.find_top_k_matches(k=4) # returns [('mouse', 1), ('mousepad', 1), ('mobile', 0), ('moneypot', 0)]
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## License
[MIT](https://choosealicense.com/licenses/mit/)