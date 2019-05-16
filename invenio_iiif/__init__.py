# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module to serve images complying with IIIF standard.

Invenio-IIIF integrates
`Invenio-Records-Files <https://invenio-records-files.rtfd.io>`_ with
`Flask-IIIF <https://flask-iiif.rtfd.io>`_ to provide an endpoint for serving
images complying with the `International Image Interoperability Framework
(IIIF) <https://iiif.io/>`_ API standards.

Invenio-IIIF registers the REST API endpoint provided by Flask-IIIF in the
Invenio instance through entry points. On each request, it delegates
authorization check to Invenio-Files-REST, load the file from the Invenio
bucket and serve it after Flask-IIIF manipulation.

Initialization
--------------
You can define the IIIF API prefix by setting the Invenio configuration
``IIIF_API_PREFIX``.

Usage
-----
*Prerequisites*: having an image or pdf stored as an Invenio File ObjectVersion
instance in a Bucket.

While Flask-IIIF requires in the path of the URL the UUID of the image to
retrieve, Invenio needs a bucket id, version id and a key to be able to
load the file via Invenio-Files-REST.
Invenio-IIIF provides an utility to map such URLs, e.g. ``/v2/<uuid>/<path``,
and convert the ``uuid`` to a concatenation of
``<bucket_id>:<version_id>:<key>``.

Given an image object:

.. code-block:: python

    from invenio_files_rest.models import ObjectVersion
    img_obj = ObjectResource.get_object(bucket='<bucket_id>', key='icon.png',
                                        version_id='<version_id>')

we can create the corresponding IIIF URL:

.. code-block:: python

    from invenio_iiif.utils import ui_iiif_image_url
    image_url = ui_iiif_image_url(
        obj=img_obj, version='v2', region='full', size='full', rotation=0,
        quality='default', image_format='png'
    )

The result will be
``/<prefix>/v2/<bucket_id>:<version_id>:icon.png/full/full/0/default.png``

If the file is a PDF and ImageMagick is installed in your system, then the
module can extract the first page of the PDF and create a ``png`` from it.

Authorization
~~~~~~~~~~~~~

Permissions to retrieve the requested images are delegated to
Invenio-Files-REST. At each request, authorization is checked to ensure the
user has sufficient privileges.

Preview
~~~~~~~

Invenio-IIIF provides an extension for
`Invenio-Previewer <https://invenio-previewer.rtfd.io>`_ to preview images.
The previewer is exposed in the entry points.

The template used to render the image can be configured with the configuration
``IIIF_PREVIEW_TEMPLATE``.

Thumbnails
~~~~~~~~~~

The module can precache thumbnails of requested images. It provides a celery
task that will fetch a given image and resize it to create a thumbnail. It is
then cached so it can be served efficiently.

.. code-block:: python

    from invenio_iiif.tasks import create_thumbnail
    create_thumbnail(image_key, '250')

"""

from __future__ import absolute_import, print_function

from .ext import InvenioIIIF, InvenioIIIFAPI
from .version import __version__

__all__ = ('__version__', 'InvenioIIIF')
