class DataInsufficiencyException(Exception):
    """
    raised when data from previous step is insufficient and this cycle can not be proceeded anymore.
    """

    def __init__(self, data):
        super(DataInsufficiencyException, self).__init__(f'{type(data)} data was insufficient.')
