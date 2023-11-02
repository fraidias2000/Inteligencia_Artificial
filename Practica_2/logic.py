
"""
entail -- Propositional logic inference for Boolean variables.
http://barnesc.blogspot.com.es/2005/10/propositional-logic-in-python.html
Public domain, Connelly Barnes 2005-2006.
"""

import re
import copy

__all__ = ['AssumptionSet']
__version__ = '1.0.1'

class CompactSet(object):
    """
    Compact set of frozensets for truth tables.
    
    An arbitrary element e (a frozenset) is in self iff:
    
      e.intersection(self.subspace) in self.values
    
    Note that this always defines either an infinite or empty set.
    Also note that for every CompactSet, each set in self.subspace
    must be a subset of self.values.
    
      CompactSet(subspace, values) => instance
    
    The set containing every set is CompactSet([], [[]]).
    The empty set is CompactSet([], []).
    
    To convert a truth table to a CompactSet, we first construct
    a list by taking each line of the truth table which evaluates
    to "True" and adding a frozenset to the list representing the
    variables which are true on that line:
    
      >>> # Truth table for a => b:
      >>> # a      b      a => b
      >>> # False  False  True
      >>> # False  True   True
      >>> # True   False  False
      >>> # True   True   True
      >>> # List containing "true" variables for each "true"
      >>> # line on the truth table.
      >>> L = [[], ['b'], ['a', 'b']]
      >>> C = CompactSet(['a', 'b'], L)
    
    Now we construct a CompactSet with the subspace equal to the
    variables used in our truth table.
    
    The advantage in doing this is that we need not look at the "whole"
    truth table over all variables used in a problem -- instead, we can
    construct smaller truth tables, one for each assumption in the set
    of assumptions we have made.  Then to evaluate whether our set of
    assumptions is contradictory (always false) or satisfiable (true for
    some row in the truth table), we merge pairs of CompactSets by
    intersection (greedily, so as to to minimize the number of elements
    in result.values) and if we end up with an empty set we have
    contradiction, else we have satisfiability.
    """
    __slots__ = ['subspace', 'values']
    def __init__(self, subspace, values):
        """
        Initialize set from subspace and values.
        """
        self.subspace = set(subspace)
        self.values = set([frozenset(x) for x in values])
    
    def __contains__(self, e):
        return self.subspace.intersection(e) in self.values
    
    def __nonzero__(self):
        return len(self.values) != 0
    
    def __copy__(self):
        ans = CompactSet([], [])
        ans.subspace = set(self.subspace)
        ans.values = set(self.values)
        return ans
    
    def __eq__(self, other):
        if not isinstance(other, CompactSet):
            return NotImplemented
        return (self.subspace == other.subspace and
                self.values == other.values)
    
    def __ne__(self, other):
        return not (self == other)
    
    def __cmp__(self, other):
        raise ValueError('general comparisons not supported')
    
    def intersection(self, other):
        """
        Intersect two CompactSet objects.
        
        If self and other have equal subspaces, then this takes O(n+m)
        time and the result has size <= min(m, n).  If the subspaces are
        nonequal, this takes O(m*n) time and the result has size <= m*n.
        """
        ans = copy.copy(self)
        ans.intersection_update(other)
        return ans
    
        #    # Slower, readable version.
        #    ans = CompactSet(self.subspace.union(other.subspace), [])
        #    common = frozenset(self.subspace.intersection(other.subspace))
        #    for a in self.values:
        #      for b in other.values:
        #        if a.intersection(common) == b.intersection(common):
        #          ans.values.add(a.union(b))
        #    return ans
    
    def intersection_count(self, other):
        """
        Count the number of elements in self.intersection(other).values.
        """
        if not isinstance(other, CompactSet):
            raise TypeError('other is not CompactSet')
        if self.subspace == other.subspace:
            return len(self.values.intersection(other.values))
        common = frozenset(self.subspace.intersection(other.subspace))
        
        aorig = {}
        borig = {}
        for a in self.values:
            key = a.intersection(common)
            aorig.setdefault(key, 0)
            aorig[key] += 1
        
        for b in other.values:
            key = b.intersection(common)
            borig.setdefault(key, 0)
            borig[key] += 1
        
        count = 0
        for ab in set(aorig).intersection(borig):
            count += aorig[ab] * borig[ab]
        return count
    
    def intersection_update(self, other):
        """
        Intersect self in place with other.
        """
        if not isinstance(other, CompactSet):
            raise TypeError('other is not CompactSet')
        if self.subspace == other.subspace:
            self.values.intersection_update(other.values)
            return
        common = frozenset(self.subspace.intersection(other.subspace))
        self.subspace.update(other.subspace)
        
        aorig = {}
        borig = {}
        for a in self.values:
            aorig.setdefault(a.intersection(common), []).append(a)
        
        for b in other.values:
            borig.setdefault(b.intersection(common), []).append(b)
        
        self.values = set()
        
        for ab in set(aorig).intersection(borig):
            for afull in aorig[ab]:
                for bfull in borig[ab]:
                    self.values.add(afull.union(bfull))
    
    def __repr__(self):
        return 'CompactSet(' + str(self) + ')'
    
    def __str__(self):
        subspace = sorted(self.subspace)
        values = sorted([sorted(x) for x in self.values])
        return repr(subspace) + ', ' + repr(values)
    
    # __hash__() intentionally computed via id(self).


class AssumptionSet:
    """
    Set of assumptions over boolean variables.
    
    Assumptions can be added by assume() and checked by implies().
    
    Assumptions are Python expressions restricted to boolean variables
    and operators and, or, not, ==, !=, ^, => (implies), <= (reversed
    implies), <=> (if and only if).  Non-user defined constants are
    limited to True, False, and the integers (which cannot be assigned
    to variables, as all variables are boolean).
    
    To set a == True, use assume('a'), and to set a == False, use
    assume('not a').
    """
    keywords = set(['and', 'or', 'not', '==', '!=', '^', '=>', '<=',
                    '<=>', 'True', 'False'])
    
    def __init__(self, L=[]):
        self.assume_compact = []  # List of assumption CompactSet instances.
        if hasattr(L, 'capitalize'):
            raise ValueError('non-string iterable or sequence required')
        for x in L:
            self.assume(x)
    
    def is_varname(self, s):
        """
        True iff string s is a variable name.
        """
        if s in self.keywords:
            return False
        try:
            int(s)
            return False
        except:
            pass
        return True
    
    def expr_to_func(self, s):
        """
        Convert an expression to a tuple (var_list, func).
        
        Here var_list is a list of strings for variable IDs, and
        func(*args) when called on boolean values corresponding to these
        variables (in order) returns a boolean for the expression s.
        """
        if '\n' in s:
            raise ValueError('string must be expression')
        var_list = [x for x in set(re.findall(r'\w+', s)) if self.is_varname(x)]
        var_list.sort()
        s = s.replace('<=>', '==')
        # Swap <= and =>.
        s = s.replace('<=', '\xff')
        s = s.replace('=>', '<=')
        s = s.replace('\xff', '>=')
        expr = 'def f(' + ','.join(var_list) + '):\n  return ' + s
        d = {}
        exec expr in d, d
        return (var_list, d['f'])
    
    def expr_to_compact_set(self, s):
        """
        Convert expr to function, evaluate it and return a CompactSet.
        """
        (vars, f) = self.expr_to_func(s)
        ans = []
        for k in xrange(1<<len(vars)):
            args = [(k>>j)&1 for j in range(len(vars))]
            if f(*args):
                ans.append([vars[j] for j in range(len(vars)) if args[j]])
        return CompactSet(vars, ans)
    
    def assume(self, s):
        """
        Assume a given boolean string statement.
        """
        self.assume_compact.append(self.expr_to_compact_set(s))
    
    def __copy__(self):
        ans = AssumptionSet()
        ans.assume_compact = list(self.assume_compact)
        return ans
    
    def __deepcopy__(self, memo):
        return self.__copy__()
    
    def implies(self, s):
        """
        True iff self entails s (the assumptions in self imply s).
        """
        # Assume not s and look for a contradiction.
        return not intersect_compact_sequence(
               [self.expr_to_compact_set('not (' + s + ')')] +
                self.assume_compact)


def intersect_compact_sequence(L):
    """
    Return intersection of a sequence of CompactSet objects.
    
    Idea behind the algorithm:
    
      Intersect distinct items (a, b) of L where a = L[0], so that the
      number of elements in a.intersect(b).values is minimized.  In each
      intersection, remove b and replace L[0] with a.  If L is reduced
      to one element, then return this element.
    
      In practice, we terminate the minimization process early if
      the number of elements in a.intersect(b).values is <= 1, and we
      choose elements b of L in a certain order to attempt to make
      this "early exit" condition be true.
    
    Greedy algorithm INTERSECT-SEQUENCE:
    
      * Build undirected connectedness graph: two items in L are
        connected iff they share variables.  The set of "neighbors"
        of any given item a in L is the set of items in L adjacent
        to a.
      * Initialize set fringe = empty set.
      * Initialize set visited = empty set.
      * add_to_fringe(vars) takes a set of variables and adds all
        nodes which refer to these variables to fringe.
      * Set CompactSet ans = L[0].
      * Call add_to_fringe() with all variables used in ans.
      * Set last_visited = ans.
      * While fringe is nonempty:
          best = Null
          For each neighbor n of last_visited which is not in visited:
            If len(best.values) <= 1:
              Break
            If best is Null or ans.intersection(n).values < best.values:
              best = ans.intersection(n)
          For each element n of the fringe which is not visited:
            Same code as from previous for loop.
          Set ans = ans.intersection(best).
          If ans.values == 0:
            Return empty compact set.
          Add best to visited.
          Add all neighbors of best to fringe.
          Set last_visited = best.
      * Some elements of L will not have been intersected into ans
        in the above code.  Call INTERSECT-SEQUENCE() on these elements
        separately, then merge the result into ans with
        ans = ans.intersection(result).
    
    """
    intersect_compact_seq = intersect_compact_sequence
    Compact = CompactSet
    
    ans = L[0]              # Object at current state of intersection.
    connected_to = {}       # Maps var -> items with var in subspace.
    node_neighbor = {}      # Maps node -> neighbors of node.
    fringe = set()          # Candidates for expansion
    processed = set([ans])  # Set of items in L processed.
    
    # Build connected_to.
    for item in L[1:]:
        for var in item.subspace:
            connected_to.setdefault(var, set()).add(item)
    
    # Build node_neighbor.
    for item in L:
        for var in item.subspace:
            for connect in connected_to.get(var, []):
                if connect is not item:
                    node_neighbor.setdefault(item, set()).add(connect)
    
    # Add all clauses containing given variables to fringe.
    # Also fix up connected_to so we don't follow edges again.
    def add_to_fringe(var_set):
        for var in var_set:
            for item in connected_to.get(var, []):
                for var2 in item.subspace:
                    if var2 != var:
                        connected_to[var2].remove(item)
                        if len(connected_to[var2]) == 0:
                            del connected_to[var2]
                fringe.add(item)
            if var in connected_to:
                del connected_to[var]

    # Loop over all fringe, pop the best node to next expand, and
    # return item.  Also fix up node_neighbor so we don't follow edges
    # again.
    def pop_best_from_fringe():
        best_item = None
        best_value = ()
        
        dummy_fringe = node_neighbor.get(prev_node, [])
        
        done = False
        for cur_fringe in [dummy_fringe, fringe]:
            for item in cur_fringe:
                value = ans.intersection_count(item)
                if value < best_value:
                    best_item = item
                    best_value = value
                if value <= 1:
                    done = True
                    break
            if done:
                break
        fringe.remove(best_item)
        if best_item in node_neighbor:
            for my_neighbor in node_neighbor[best_item]:
                node_neighbor[my_neighbor].remove(best_item)
        return best_item
    
    # Greedily merge fringe with ans.
    add_to_fringe(ans.subspace)
    prev_node = ans
    while len(fringe) > 0:
        item = pop_best_from_fringe()
        processed.add(item)
        ans.intersection_update(item)
        prev_node = item
        if not ans:
            return Compact([], [])
        for var2 in item.subspace:
            if var2 in connected_to:
                add_to_fringe([var2])
    
    # Remaining items in L do not share variables with us.
    # Intersect them separately, then merge with us.
    remain = list(set(L) - processed)
    if len(remain) > 0:
        rest = intersect_compact_seq(remain)
        if not rest:
            return Compact([], [])
        ans.intersection_update(rest)
    
    return ans


class PropKB:
    
    def __init__(self):
        self.assumptions = AssumptionSet()
        
    def tell(self, sentence):
        self.assumptions.assume(sentence)
        
    def ask(self, query):
        return self.assumptions.implies(query)
        
        
