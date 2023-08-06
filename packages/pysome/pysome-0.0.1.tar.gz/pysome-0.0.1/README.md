### Work - in - progress
# PySome

`PySome` brings the `expect(...).to_be(...)` syntax to python for
easier and clearer testing of nested objects

### Example:
```python
from pysome import Some
from pysome.Some import SomeList, SomePartialDict
from pysome.expect import expect
# some large nested api response you want to test
api_response = {
    "menu": {
        "tags": [
            {"id": 1, "z-index": 12},
            {"id": 2, "name": "ax7"},
            {"id": 5, "name": "ax7", "z-index": 12},
            {"id": 2, "alias": "iivz"},
        ]
    }
}

# test only for needed stuff
expect(api_response).to_be({
    "menu": {
        "tags": SomeList(SomePartialDict({
            "id": Some(int)
        }))
    }
})
```
