============
python-nimsp
============

A Python library for interacting with the `National Institute on Money in State Politics API <http://www.followthemoney.org/services/index.phtml>`_.

Released under a BSD-style license (see the LICENSE files for details).

python-nimsp is a project of Sunlight Labs (c) 2011.
Written by Michael Stephens <mstephens@sunlightfoundation.com>.

Source: http://github.com/sunlightlabs/python-nimsp

Installation
============

To install from PyPI run

   ``pip install nimsp``

or

   ``easy_install nimsp``

To install from a source package run

    ``python setup.py install``

Example Usage
=============

   >>> from nimsp import nimsp
   >>> nimsp.apikey = 'YOUR_API_KEY'
   >>> corte = nimsp.candidates.list(state='tx', year=2008, candidate_name='Corte Jr, Frank')
   >>> print "$%d" % corte.results[0].total_dollars
   $287372
   >>> print corte.results[0].candidate_status
   Won