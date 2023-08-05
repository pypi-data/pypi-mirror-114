import typing
import onetrick

def map_entry(entry, mcept):
    if isinstance(entry, type):
        if issubclass(entry, Exception):
            exception_type:type[Exception] = entry
            mcept.catch.add(exception_type)
    elif isinstance(entry, slice):
        rng:slice = entry

        if isinstance(rng.start, type) and issubclass(rng.start, Exception):
            mcept.catch.add(rng.start)
            mcept.defaults[rng.start] = rng.stop

@onetrick
class MapExcept:
    def __init__(self, *__iterables:typing.Iterable):
        self.catch = set()
        self.defaults = dict()

        self.iterables = __iterables

    def __getitem__(self, __key):
        cloned:'MapExcept' = type(self)(*self.iterables)

        try:
            for entry in __key:
                map_entry(entry, cloned)
        except TypeError:
            map_entry(__key, cloned)

        return cloned
    
    def __call__(self, __func):
        tupled_exception_types = tuple(self.catch)
        cached_supertypes = dict() # etype : supertype

        for args in zip(*self.iterables):
            value:object

            try:
                value = __func(*args)
            except tupled_exception_types as e:
                supertype = etype = type(e)

                if etype in cached_supertypes:
                    supertype = cached_supertypes[etype]
                else:
                    for caught_type in tupled_exception_types:
                        if issubclass(supertype, caught_type):
                            supertype = caught_type
                    
                    cached_supertypes[etype] = supertype
                
                if supertype in self.defaults:
                    value = self.defaults[supertype]
                else:
                    continue
            
            yield value
