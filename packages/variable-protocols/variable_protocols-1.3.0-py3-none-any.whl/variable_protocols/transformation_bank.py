from collections import defaultdict
from typing import Dict, Set, List

from variable_protocols.protocols import Variable, struct_check, fmt
from variable_protocols.transformations import Transformation, Tr

LookUpTable = Dict[Variable, Set[Transformation]]
lookup_table_source: LookUpTable = defaultdict(set)
lookup_table_target: LookUpTable = defaultdict(set)


def register_(transformation: Transformation):
    lookup_table_source[transformation.source].add(transformation)
    lookup_table_target[transformation.source].add(transformation)


def look_up(source: Variable, target: Variable, max_depth: int = 16) -> List[Tr]:
    if struct_check(source, target):
        raise ValueError(f"Source and target are the same: {fmt(source)}")
    else:
        reachable_s_: Dict[Variable, List[Set[Tr]]] = {}
        reachable_t_: Dict[Variable, List[Set[Tr]]] = {}
        depth_ = 0
        while depth_ < max_depth:
            for i, r in reachable_s_.items():
                tr = lookup_table_source[i]
                reachable_s_[i] = r + [tr]
            common = set(reachable_s_).intersection(set(reachable_t_))
            if len(common) >= 1:
                tr_list: List[List[Set[Tr]]] = [reachable_s_[k] + reachable_t_[k]
                                                for k in common]
                break
        else:
            raise Exception("Max-depth is reached when looking up for transformations")

        if len(tr_list) == 0:
            raise Exception(f"No transformation are found from {source} to {target}")
        elif len(tr_list) == 1:
            tr_series = tr_list[0]
            if all(len(tr_set) == 1 for tr_set in tr_series):
                return [next(iter(trs)) for trs in tr_series]
            else:
                msg = ""
                for trs in tr_series:
                    nxt = next(iter(trs))
                    msg += f"Transformations that are found from {nxt.source} to {nxt.target}:\n"
                    msg += f"  {trs}"
                raise Exception(msg)
        else:
            raise Exception("Multiple transformations have been retrieved: \n"
                            + "".join(f"  {tr}\n" for tr in tr_list))
