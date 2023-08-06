import numpy as np
import logging
import os
from typing import Union

import yadg.core

def _list_validator(l: list) -> bool:
    if len(l) == 3:
        return _float_list(l)
    else:
        return _general_list(l)

def _float_list(l: list) -> bool:
    if (isinstance(l[0], float) and isinstance(l[1], float) and isinstance(l[2], str)): 
        return True
    else:
        return _general_list(l)

def _general_list(l: list) -> bool:
    for v in l:
        if isinstance(v, list):
            return _list_validator(v)
        elif isinstance(v, dict):
            return _dict_validator(v)
        else:
            assert isinstance(v, str) or isinstance(v, int), \
                "List elements have to be one of [str, int, dict, list], " \
                f"but entry id:{l.index(v)}:{type(v)} is neither: {l}"
    return True

def _dict_validator(d: dict) -> bool:
    for k, v in d.items():
        if isinstance(v, float):
            assert k == "uts", \
                f"Only 'uts':float can be a float entry, not '{k}'."
        elif isinstance(v, list):
            return _list_validator(v)
        elif isinstance(v, dict):
            return _dict_validator(v)
        else:
            assert isinstance(v, str) or isinstance(v, int), \
                "Dict elements have to be one of [str, int, dict, list], " \
                f"but '{k}':{type(v)} is neither: {v}"
    return True

def validator(item: Union[list, dict, str], spec: dict) -> True:
    """
    Worker validator function. 
    
    This function checks that ``item`` matches the specification supplied in 
    ``spec``. The ``spec`` :class:`(dict)` can have the following entries:

    - ``"type"`` :class:`(type)`\ , a required entry, defining the type of ``item``,
    - ``"all"`` :class:`(dict)` defining a set of required keywords and their
      respective ``spec``,
    - ``"any"`` :class:`(dict)` defining a set of optional keywords and their
      respective ``spec``,
    - ``"one"`` :class:`(dict)` defining a set of mutually exclusive keywords and
      their respective ``spec``,
    - ``"each"`` :class:`(dict)` providing the ``spec`` for any keywords not 
      listed in ``"all"``, ``"any"``, or ``"one"``,
    - ``"allow"`` :class:`(bool)` a switch whether to allow unspecified keys.

    To extend the existing `datagram` and `schema` specs, look into 
    :mod:`yadg.core.spec_datagram` and :mod:`yadg.core.spec_schema`, respectively.

    Parameters
    ----------
    item
        The ``item`` to be validated.
    
    spec
        The ``spec`` with which to validate the ``item``
    
    Returns
    -------
    True: bool
        If the ``item`` matches the ``spec``, returns `True`. Otherwise, an
        `AssertionError` is raised.

    """
    assert isinstance(item, spec["type"]), f"validator: item '{item}' does " \
                                           f"not match prescribed type in spec " \
                                           f"'{spec['type']}'."
    if len({"all", "one", "any", "each"}.intersection(spec)) > 0 and \
       spec["type"] in [list, dict]:
        for k, v in spec.get("all", {}).items():
            assert k in item, f"validator: required entry '{k}' was not " \
                              f"specified in item '{item}'."
        if "one" in spec:
            initem = set(spec["one"]).intersection(item)
            assert len(initem) == 1, f"validator: Exactly one of entries in " \
                            f"{spec['one']} has to be provided in item " \
                            f"{item}, but {len(initem)} were provided: {initem}."
        for k in item:
            s = False
            for d in ["all", "one", "any"]:
                if k in spec.get(d, []):
                    s = d
            assert s or spec.get("allow", False) or "each" in spec, \
                f"validator: Key '{k}' in item {item} is not understood."
            if s:
                assert validator(item[k], spec[s][k])
            elif "each" in spec:
                if spec["type"] == list:
                    assert validator(k, spec["each"])
                else:
                    assert validator(item[k], spec["each"])
    elif len({"all", "one", "any"}.intersection(spec)) > 0 and spec["type"] in [str]:
        if "all" in spec:
            assert len(spec["all"]) == 1 and item in spec["all"], \
                    f"validator: Item '{item}' is not in {spec['all']}."
        if "one" in spec:
            assert item in spec["one"], \
                    f"validator: Item '{item}' is not in {spec['one']}."
        if "any" in spec:
            assert item in spec["any"], \
                    f"validator: Item '{item}' is not in {spec['any']}."
    return True

def validate_schema(schema: Union[list, tuple], strictfiles: bool = True) -> True:
    """
    Schema validator. 
    
    Checks the overall `schema` format, checks every `step` of the `schema` for 
    required entries, and checks whether required parameters for each `parser` 
    are provided. The validator additionally fills in optional parameters, where
    necessary for a valid `schema`.

    The specification is:
    
    - The `schema` has to be a :class:`(dict)` with a top-level ``"metadata"``
      :class:`(dict)` and ``"steps"`` :class:`(list)` entries
    - The ``"metadata"`` entry has to specify the ``"provenance"`` of the `schema`,
      as well as the ``"schema_version"`` :class:`(str)`. Other entries may be
      specified.
    - Each element within the ``"steps"`` list is a `step`, of type :class:`(dict)`
    - Each `step` has to have the ``"parser"`` and ``"import"`` entries:
    
      - The ``"parser"`` is a :class:`(str)` entry that has to contain the name 
        of the requested parser module. This entry is processed in the 
        :func:`yadg.core.main._infer_datagram_handler` function in the core module.
      - The ``"import"`` is a :class:`(dict)` entry has to contain:
      
        - Exactly **one** entry out of ``"files"`` or ``"folders"``.
          This entry must be a :class:`(list)` even if only one element is provided. 
        - Any combination of ``"prefix"``, ``"suffix"``, ``"contains"`` entries.
          They must be of type :class:`(str)`. These entries specify the matching 
          of files within folders accordingly.
        
    - The only other allowed entries are:
    
      - ``"tag"`` :class:`(str)`: for defining a tag for each `step`; by default 
        assigned the numerical index of the `step` within the `schema`.
      - ``"export"`` :class:`(str)`: for exporting a single `step`; whether the 
        processed `step` should be exported as a ``json`` file. This file is kept 
        available for other `steps`, but will be removed at the end of `schema`
        processing.
      - ``"parameters"`` :class:`(dict)`: for specifying other parameters for 
        each of the parsers.
      
    - no other entries are permitted

    Parameters
    ----------
    schema
        The schema to be validated.
    
    strictfiles
        When `False`, any files specified using the ``"files"`` option will not 
        be checked for existence. Note that folders (specified via ``"folders"``) 
        are always checked.
    
    Returns
    -------
    True: bool
        When the `schema` is valid and passes all assertions, `True` is returned.
        Otherwise, an `AssertionError` is raised.
    """
    # schema has to meet the spec
    assert validator(schema, yadg.core.schema)
    for step in schema["steps"]:
        si = schema["steps"].index(step)
        # import files or folders must exist
        if "files" in step["import"] and strictfiles:
            for fn in step["import"]["files"]:
                assert os.path.exists(fn) and os.path.isfile(fn), \
                        f"schema_validator: File path {fn} provided in " \
                        f"step {si} is not a valid file."
        if "folders" in step["import"]:
            for fn in step["import"]["folders"]:
                assert os.path.exists(fn) and os.path.isdir(fn), \
                        f"schema_validator: Folder path {fn} provided in " \
                        f"step {si} is not a valid folder."
        # supply a default tag
        if "tag" not in step:
            logging.info(f"schema_validator: Tag not present in step {si}.")
            step["tag"] = f"{si:2d}"
    return True

def validate_datagram(datagram: dict) -> True:
    """
    Datagram validator.

    Checks the overall `datagram` format against the `datagram` spec, and ensures
    that each floating-point value is accompanied by standard deviation and unit.

    The current `datagram` specification is:

    -  The `datagram` must be a :class:`(dict)` with two entries:

       - ``"metadata"`` :class:`(dict)`: A top-level entry containing metadata. 
       - ``"data"`` :class:`(list[dict])`: List corresponding to a sequence of `steps`.
    
    - The ``"metadata"`` entry has to contain information about the ``"provenance"``
      of the `datagram`, the creation date using ISO8601 format in ``"date"`` 
      :class:`(str)` entry, a full copy of the input `schema` in the ``"input_schema"``
      entry, and version information in ``"datagram_version"`` :class:`(str)`.
    
    - Each element in the ``"data"`` corresponds to a single `step` from the `schema`.
    - Each `step` in ``"data"`` has to contain a ``"metadata"`` :class:`(dict)` entry,
      and a ``"timesteps"`` :class:`(list)`; an optional ``"common"`` :class:`(dict)` 
      data block can be provided.
    - Each timestep in the ``"timesteps"`` list has to specify a timestamp using the
      Unix Timestamp format in ``"uts"`` :class:`(float)` entry. Any other entries
      are allowed, including :class:`(str)`, :class:`(int)`, :class:`(list)`, or 
      :class:`(dict)`. 
    
    .. note:: 
        A floating-point entry has to be specified using a :class:`list(`\ ``value``\ 
        :class:`(float)`\ ``, error``\ :class:`(float)`\ ``, unit``\ :class:`(str))` format.

    Parameters
    ----------
    datagram
        The `datagram` to be validated.
    
    Returns
    -------
    True: bool
        If the `datagram` passes all assertions, returns `True`. Else,
        an AssertionError is raised.

    """
    # datagram has to meet the spec
    assert validator(datagram, yadg.core.datagram)
    # validate each step in the datagram
    for step in datagram["data"]:
        assert ("fn" in step["metadata"]) ^ all(["fn" in ts for ts in step["timesteps"]]), \
            "The 'fn':str entry has to be provided either in the 'metadata' entry " \
            "of each step, or in each element of 'timesteps."
        for ts in step["timesteps"]:
            assert _dict_validator(ts)
    return True