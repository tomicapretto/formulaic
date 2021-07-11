import wrapt


class ModelMatrix(wrapt.ObjectProxy):

    def __init__(self, data, spec=None):
        wrapt.ObjectProxy.__init__(self, data)
        self._self_model_spec = spec

    @property
    def model_spec(self):
        return self._self_model_spec

    def subset(self, tags=None, exact=True):
        tags = tags or set()
        cols = [
            name
            for term, factors, names in self.model_spec.structure
            if exact and set(term.tags) == set(tags) or not exact and set(tags).intersection(term.tags)
            for name in names
        ]
        return self[cols]

    def __repr__(self):
        return self.__wrapped__.__repr__()  # pragma: no cover
