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
authorization check to
`Invenio-Files-REST <https://invenio-files-rest.rtfd.io>`_, load the file from
the Invenio bucket and serve it after Flask-IIIF manipulation.

Initialization
--------------

First create a Flask application (Flask-CLI is not needed for Flask
version 1.0+):

>>> from flask import Flask
>>> app = Flask('myapp')
>>> app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

Configuration
~~~~~~~~~~~~~

Then, You can define the IIIF API prefix by setting the Invenio configuration
``IIIF_UI_URL``.

>>> app.config.update(IIIF_UI_URL='/iiif-demo')

Usage
-----

To demonstrate how Invenio-IIIF works, we need to have a pdf or image file
uploaded to Invenio instance. To achieve that we need to initialize all
dependent Invenio extensions:

>>> from invenio_db import InvenioDB, db
>>> from invenio_files_rest import InvenioFilesREST
>>> ext_db = InvenioDB(app)
>>> ext_files_rest = InvenioFilesREST(app)
>>> app.app_context().push()
>>> db.create_all()

Creating a location
~~~~~~~~~~~~~~~~~~~

Before uploading a file we need to create a location:

>>> import tempfile
>>> from invenio_files_rest.models import Bucket
>>> tmpdir = tempfile.mkdtemp()
>>> from invenio_files_rest.models import Location
>>> loc = Location(name='local', uri=tmpdir, default=True)
>>> db.session.add(loc)
>>> db.session.commit()

Creating a bucket with a previously created location:

>>> b1 = Bucket.create(loc)

Adding files to the bucket:

>>> import os
>>> from invenio_files_rest.models import ObjectVersion
>>> demo_files_path = 'examples/demo_files'
>>> demo_files = (
...     'img.jpg',
...     'img.png')
>>> for f in demo_files:
...     with open(os.path.join(demo_files_path, f), 'rb') as fp:
...         img = ObjectVersion.create(b1, f, sream=fp)
>>> db.session.commit()

Serving a file
~~~~~~~~~~~~~~

While Flask-IIIF requires in the path of the URL the UUID of the image to
retrieve, Invenio needs a bucket id, version id and a key to be able to
load the file via `Invenio-Files-REST <https://invenio-files-rest.rtfd.io>`_.
Invenio-IIIF provides an utility to map such URLs, e.g. ``/v2/<uuid>/<path>``,
and convert the ``uuid`` to a concatenation of
``<bucket_id>:<version_id>:<key>``.

Given a previously created image object:

>>> img_obj = ObjectVersion.get_versions(bucket=b1,
...                                      key=demo_files[1]).first()

we can create the corresponding IIIF URL:

>>> from invenio_iiif.utils import ui_iiif_image_url
>>> image_url = ui_iiif_image_url(
...       obj=img_obj, version='v2', region='full', size='full', rotation=0,
...       quality='default', image_format='png')

The result will be
``/iiif-demov2/<bucket_id>:<version_id>:image.png/full/full/0/default.png``

If the file is a PDF and ImageMagick is installed in your system, then the
module can extract the first page of the PDF and create a ``png`` from it.

Authorization
~~~~~~~~~~~~~

Permissions to retrieve the requested images are delegated to
`Invenio-Files-REST <https://invenio-files-rest.rtfd.io>`_.
At each request, authorization is checked to ensure the
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
