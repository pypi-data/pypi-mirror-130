# utility functions that aren't really class-specific
import os
from typing import Union

def make_dir(destdir: str, logger: Union[logging.Logger, None]):
    """
    Attempt to create a directory if it doesn't already exist
    Raise an error if the creation fails
    """
    if os.path.exists(destdir):
        return True
    else:
        try:
            os.makedirs(self.topdir)
            return True
        except (IOError, OSError) as E:
            logger.exception(f"Unable to create output dir {E.filename} - {E.strerror}")
            raise






