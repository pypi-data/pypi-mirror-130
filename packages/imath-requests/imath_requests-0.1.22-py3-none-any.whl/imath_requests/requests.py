"""
requests.py
====================================
Request handelling and data structures for interacting with iMath REST API
"""


class PartData:
    """
    Part data helper class.

    Includes addition functions creating json
    data from part data for easy use in REST API.

    Attributes
    ----------
    timestamp: str
        Timestamp e.g. 1516193959559
    part_id: str
        Unique part ID e.g. Part1234
    source: str
        Data source e.g. I3DR_DESKTOP_ABC123
    part_data: list
        Additional part data as a key value pair array

    """

    def __init__(
            self, timestamp: str, part_id: str,
            source: str, part_data: list):
        """
        Part data construction.

        Parameters
        ----------
        timestamp: str
            Timestamp e.g. 1516193959559
        part_id: str
            Unique part ID e.g. Part1234
        source: str
            Data source e.g. I3DR_DESKTOP_ABC123
        part_data: list
            Additional part data as a key value pair array

        """
        self.timestamp = timestamp
        self.part_id = part_id
        self.source = source
        self.part_data = part_data

    def get_json(self) -> dict:
        """
        Convert PartData into json string for use in REST API.

        Returns
        -------
        dict
            Json formatted string

        """
        return {
            "timestamp": self.timestamp,
            "part_id": self.part_id,
            "source": self.source,
            "part_data": self.part_data
        }


class ImageValue:
    """
    Image Value helper class.

    Includes addition functions creating json data
    from part data for easy use in REST API.
    # TODO impliment class for position
    # TODO impliment class for dimension

    Attributes
    ----------
    value: str
        Name of the image e.g. test001.png
    timestamp: str
        Timestamp e.g. 1516193959559
    position: str
        Position on the part where the image was taken
    dimension: str
        Dimension of the area of the part, which is on the image
    quality: str
        Quality

    """

    def __init__(
            self, value: str, timestamp: str,
            position: str, dimension: str, quality: str):
        """
        Image value construction.

        Parameters
        ----------
        value: str
            Name of the image e.g. test001.png
        timestamp: str
            Timestamp e.g. 1516193959559
        position: str
            Position on the part where the image was taken
        dimension: str
            Dimension of the area of the part, which is on the image
        quality : str
            Quality

        """
        self.value = value
        self.timestamp = timestamp
        self.position = position
        self.dimension = dimension
        self.quality = quality

    def get_json(self) -> dict:
        """
        Convert ImageValue into json string for use in REST API.

        Returns
        -------
        dict
            Json formatted string

        """
        return {
            "value": self.value,
            "timestamp": self.timestamp,
            "position": self.position,
            "dimension": self.dimension,
            "quality": self.quality
        }


class ImageMetaData:
    """
    Image meta data helper class.

    Includes addition functions creating json data
    from image meta data for easy use in REST API.

    Attributes
    ----------
    part_id: str
        Unique part ID e.g. Part1234
    value_id: str
        Unique identification of the capture device e.g. Camera1
    source: str
        Data source e.g. I3DR_DESKTOP_ABC123
    values: list
        List of ImageValues
    qualifying_metadata: list
        Qualifying metadata should be a key value pair array

    """

    def __init__(
            self, part_id: str, value_id: str,
            source: str, values: list, qualifying_metadata):
        """
        Image meta data construction.

        Parameters
        ----------
        part_id: str
            Unique part ID e.g. Part1234
        value_id: str
            Unique identification of the capture device e.g. Camera1
        source: str
            Data source e.g. I3DR_DESKTOP_ABC123
        values: list
            List of ImageValues
        qualifying_metadata: list
            Qualifying metadata should be a key value pair array

        """
        self.part_id = part_id
        self.value_id = value_id
        self.source = source
        self.values = values
        self.qualifying_metadata = qualifying_metadata

    def get_json(self) -> dict:
        """
        Convert ImageMetaData into json string for use in REST API.

        Returns
        -------
        dict
            Json formatted string

        """
        values_json_list = []
        for value in self.values:
            values_json_list.append(value.get_json())
        return {
            "part_id": self.part_id,
            "value_id": self.value_id,
            "source": self.source,
            "values": values_json_list,
            "qualifying_metadata": self.qualifying_metadata
        }


class ImageAnalysisFailure:
    """
    Image analysis failure helper class.

    Includes addition functions creating json data
    from part data for easy use in REST API.
    # TODO impliment class for position
    # TODO impliment class for dimension

    Attributes
    ----------
    id: str
        Unique failure id e.g. 124355435321576
    failure: str
        Failure type id e.g. 4711
    position: str
        Position on the part where the image was taken
    dimension: str
        Dimension of the area of the part, which is on the image
    qualifying_metadata: list
        Qualifying metadata should be a key value pair array

    """
    def __init__(
            self, id: str, failure: str,
            position: str, dimension: str, qualifying_metadata: list):
        """
        Image analysis failure construction.

        Parameters
        ----------
        id: str
            Unique failure id e.g. 124355435321576
        failure: str
            Failure type id e.g. 4711
        position: str
            Position on the part where the image was taken
        dimension: str
            Dimension of the area of the part, which is on the image
        qualifying_metadata: list
            Qualifying metadata should be a key value pair array

        """
        self.id = id
        self.failure = failure
        self.position = position
        self.dimension = dimension
        self.qualifying_metadata = qualifying_metadata

    def get_json(self) -> dict:
        """
        Convert ImageAnalysisFailure into json string for use in REST API.

        Returns
        -------
        dict
            Json formatted string

        """
        return {
            "id": self.id,
            "failure": self.failure,
            "position": self.position,
            "dimension": self.dimension,
            "qualifying_metadata": self.qualifying_metadata
        }

class ImageAnalysisData:
    """
    Image meta data helper class.

    Includes addition functions creating json data
    from image meta data for easy use in REST API.

    Attributes
    ----------
    part_id : str
        Unique part ID e.g. Part1234
    source : str
        Data source e.g. I3DR_DESKTOP_ABC123
    value: str
        List of ImageValues
    timestamp : str
        Timestamp e.g. 1516193959559
    failures: list
        list of ImageAnalysisFailure

    """

    def __init__(
            self, part_id: str, source: str,
            value: str, timestamp: str, failures: list):
        """
        Image Meta Data construction.

        Parameters
        ----------
        part_id : str
            Unique part ID e.g. Part1234
        source : str
            Data source e.g. I3DR_DESKTOP_ABC123
        value: str
            Name of the image (NOT ImageValue)
        timestamp : str
            Timestamp e.g. 1516193959559
        failures: list
            list of ImageAnalysisFailure

        """
        self.part_id = part_id
        self.source = source
        self.value = value 
        self.timestamp = timestamp
        self.failures = failures

    def get_json(self) -> dict:
        """
        Convert ImageAnalysisData into json string for use in REST API.

        Returns
        -------
        dict
            Json formatted string

        """
        failures_json_list = []
        for failure in self.failures:
            failures_json_list.append(failure.get_json())
        json = {
        	"part_id": self.part_id,
        	"source": self.source,
        	"value": self.value,
        	"timestamp": self.timestamp,
        	"failures": failures_json
        }


# TODO add REST API post functions
# # Create a new resource
# response = requests.post('https://httpbin.org/post', data = {'key':'value'})
# # Update an existing resource
# requests.put('https://httpbin.org/put', data = {'key':'value'})
