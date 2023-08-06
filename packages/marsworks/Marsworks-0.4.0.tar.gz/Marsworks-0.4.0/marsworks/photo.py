import inspect
from datetime import date, datetime
from typing import Optional

from rfc3986 import ParseResult, urlparse

__all__ = ("Photo",)


class Photo:
    """
    A class representing a `Photo`.

    Attributes:
        photo_id (int): ID of the photo.
        sol (int): Sol when the photo was taken.
        img_src (str): Image url.
    """

    __slots__ = ("_data", "photo_id", "sol", "_camera", "img_src", "_rover")

    def __init__(self, data: dict):
        self._data: dict = data
        self._camera: dict = data.get("camera", {})
        self._rover: dict = data.get("rover", {})
        self.photo_id: Optional[int] = data.get("id")
        self.sol: Optional[int] = data.get("sol")
        self.img_src: Optional[str] = data.get("img_src")

    def __len__(self) -> int:
        """
        Returns:
            length of internal dict of attributes. (Result of `len(obj)`)
        """
        return len(self._data)

    def __str__(self) -> Optional[str]:
        """
        Returns:
            url of image. (Result of `str(obj)`)
        """
        return self.img_src

    def __eq__(self, value) -> bool:
        """
        Checks if two objects are same using `photo_id`.

        Returns:
            Result of `obj == obj`.
        """
        return isinstance(value, self.__class__) and value.photo_id == self.photo_id

    def __hash__(self) -> int:
        """
        Returns:
            hash of the class. (Result of `hash(obj)`)
        """
        return hash(self.__class__)

    def __repr__(self) -> str:
        """
        Returns:
            Representation of Photo. (Result of `repr(obj)`)
        """
        attrs = [
            attr
            for attr in inspect.getmembers(self)
            if not inspect.ismethod(attr[1])
            if not attr[0].startswith("_")
        ]
        fmt = ", ".join(f"{attr}={value}" for attr, value in attrs)[:-2]
        return f"{__class__.__name__}({fmt})"

    @property
    def camera_id(self) -> Optional[int]:
        """
        ID of camera with which photo was taken.

        Returns:
            The id as an integer.
        """
        return self._camera.get("id")

    @property
    def camera_name(self) -> Optional[str]:
        """
        Name of camera with which photo was taken.

        Returns:
            The name as a string.
        """
        return self._camera.get("name")

    @property
    def camera_rover_id(self) -> Optional[int]:
        """
        Rover id on which this camera is present.

        Returns:
            The rover id as an integer.
        """
        return self._camera.get("rover_id")

    @property
    def camera_full_name(self) -> Optional[str]:
        """
        Full-Name of camera with which photo was taken.

        Returns:
            The full-name as a string.
        """
        return self._camera.get("full_name")

    @property
    def rover_id(self) -> Optional[int]:
        """
        Similar to `camera_rover_id`.

        Returns:
            The rover id as an integer.
        """
        return self._rover.get("id")

    @property
    def rover_name(self) -> Optional[str]:
        """
        Name of rover which took the photo.

        Returns:
            The name as a string.
        """
        return self._rover.get("name")

    @property
    def rover_landing_date(self) -> Optional[date]:
        """
        The Rover's landing date on Mars.

        Returns:
            A [datetime.date](https://docs.python.org/3/library/datetime.html?highlight=datetime%20date#datetime.date) object.
        """  # noqa: E501
        return datetime.date(datetime.strptime(self._rover["landing_date"], "%Y-%m-%d"))

    @property
    def rover_launch_date(self) -> Optional[date]:
        """
        The Rover's launch date from Earth.

        Returns:
            A [datetime.date](https://docs.python.org/3/library/datetime.html?highlight=datetime%20date#datetime.date) object.
        """  # noqa: E501
        return datetime.date(datetime.strptime(self._rover["launch_date"], "%Y-%m-%d"))

    @property
    def rover_status(self) -> Optional[str]:
        """
        The Rover's mission status.

        Returns:
            The rover's mission status as string.
        """
        return self._rover.get("status")

    def parse_img_src(self) -> ParseResult:
        """
        Parses the image URL.

        Returns:
            A [ParseResult](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.ParseResult)-like object.

        *Introduced in [v0.3.0](../changelog.md#v030).*
        """  # noqa: E501

        return urlparse(self.img_src)
