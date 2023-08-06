from abc import ABC


class Report(ABC):
    """
    All `report` routines of `common.measures.measures.Measure` must return an instance of this class
    """

    def _repr_html_(self):
        """
        To render in jupyter notebooks
        """
        raise NotImplementedError
