import copy

class ViewCollection:
    def __init__(self):
        self.raw_def_map = dict()
        self.bases_map = dict()

    def clone(self):
        other = ViewCollection()
        other.raw_def_map = copy.deepcopy(self.raw_def_map)
        other.bases_map = copy.deepcopy(self.bases_map)
        return other

    def list(self):
        return sorted(self.raw_def_map.keys())

    def raw_def(self, v):
        return self.raw_def_map.get(v, None)

    def find_dependents(self, v, recurse=False):
        assert v in self.raw_def_map
        dependents = set(u for u, bases in self.bases_map.items() if v in bases)
        if not recurse:
            return dependents
        more = dependents
        while len(more) > 0:
            new_more = set()
            for u in more:
                new_more |= (self.find_dependents(u) - dependents)
            more = new_more
            dependents |= more
        return dependents

    def topo(self, dst=None, seen=None):
        """List views in topological order (where dependent views come later).
        If dst is specified, list only those views that it depends on
        indirectly or directly, plus itself.  Assume that the
        dependency graph is acyclic (and will not verify that).

        This implementation is not particularly efficient, but it
        suffices for the size of the dependency graph we face.
        """
        assert dst is None or dst in self.raw_def_map
        if seen is None:
            seen = set()
        elif dst in seen:
            return list()
        # handle the case of dst=None by treating it as a dummy node
        # that depends on everything else.
        seen |= {dst}
        ancestors = [dst]
        for parent in (sorted(self.bases_map[dst]) if dst is not None else self.list()):
            for a in self.topo(parent, seen):
                assert a not in ancestors
                ancestors.insert(-1, a)
        if ancestors[-1] is None:
            return ancestors[0:-1]
        else:
            return ancestors

    def register(self, v, raw_def, bases):
        assert isinstance(bases, set)
        self.raw_def_map[v] = raw_def
        self.bases_map[v] = bases

    def clear(self, v=None):
        if v is None:
            self.raw_def_map = dict()
            self.bases_map = dict()
        else:
            for u in list(self.find_dependents(v, recurse=True)) + [v]:
                del self.bases_map[u]
                del self.raw_def_map[u]

if __name__ == '__main__':
    views = ViewCollection()
    views.register(1, None, {2, 3})
    views.register(2, None, {4})
    views.register(3, None, {4, 8})
    views.register(4, None, {5})
    views.register(5, None, {6, 7})
    views.register(6, None, set())
    views.register(7, None, {8})
    views.register(8, None, {6})
    print(views.topo(1))
    print(views.topo())
