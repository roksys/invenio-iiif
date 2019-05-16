# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Image cropping and previewer API.

Invenio-IIIF integrates
`Invenio-Records-Files <https://invenio-records-files.readthedocs.io>`_ with
`Flask-IIIF <https://flask-iiif.readthedocs.io/en/latest/>`_
to provide an endpoint for serving images
with the International Image Interoperability Framework (IIIF) API standards.
To be a bit more specific Invenio-IIIF is registering the provided endpoints
from Flask-IIIF and it is using the files permissions provided
by Invenio-Files-Rest.
On top of that it is providing additional functionalities based on the IIIF
standards. For more info check here (https://iiif.io/)

Initialization
--------------
When this package is installed with Flask-IIIF it will register the second's
blueprints under the configurable prefix in config['IIIF_API_PREFIX']

Usage
-----
*Prerequisites*: Having an image or pdf stored under an Invenio File Object
instance.

>>> from invenio_iiif.utils import ui_iiif_image_url

>>> from invenio_files_rest.models import ObjectVersion

obj = ObjectResource.get_object(bucket, key, version_id) or
 {'key': key, 'bucket': bucket,'version_id': version_id }

Get the corresponding url to access the processed image with.

.. code-block:: python

    image_url = ui_iiif_image_url(
        obj='previously referenced',version='v2', region='full', size='full',
        rotation=0, quality='default', image_format='png'
    )

Get the appropriate key to fetch the image with.

.. code-block:: python

    from invenio_iiif.utils import iiif_image_key
    image_key = iiif_image_key(obj)



Fetch the image or if it's a PDF it's first page as a png.

.. code-block:: python

    from invenio_iiif.handlers import image_opener
    image = image_opener(image_key)



Check if the image can be previewed
.. code-block:: python

    from invenio_iiif.previewer import can_preview, preview
    preview = can_preview(image)

Render a template with a preview of the image.
The template used is in config['IIIF_PREVIEW_TEMPLATE']
The preview image settings are in config['IIIF_PREVIEWER_PARAMS']
.. code-block:: python

    if preview:
       preview(image)

If there is any need to precache the processed images, there is an async
task provided that will fetch the images with the appropriate width
triggerring that way their caching

.. code-block:: python

    from invenio_iiif.tasks import create_thumbnail
    create_thumbnail(image_key, '250')

Security protection is implemented via the protect_api which is fetching the
image object from the invenio db having the permissions of the user checked
there against the image's.

"""

from __future__ import absolute_import, print_function

from .ext import InvenioIIIF, InvenioIIIFAPI
from .version import __version__

__all__ = ('__version__', 'InvenioIIIF')
