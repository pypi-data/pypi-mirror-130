=====================
Base Rest External ID
=====================

This addon provides a mixin to be used to provide an external ID field on all the models managed via REST API.
This way we'll be able to reference this models on other systems without having to use the internal ID used on odoo.


Usage
=====
Once using a model on rest api we'll make it inherit from our mixin.

For example while using res.parter

.. code-block:: python

    class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "external.id.mixin"]


Changelog
=========


12.0.1.0.0
~~~~~~~~~~

First official version.

Bug Tracker
===========

Bugs are tracked on `GitLab Issues <https://gitlab.com/coopdevs/odoo-addons/-/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Based on the initial work of Robin Keunen <robin@coopiteasy.be> for easy_my_coop_api module.
Trying to decople this functionallity from easy_my_coop vertical-cooperative infraestructure.

Authors
~~~~~~~

* Coop It Easy
* Coodpevs Treball SCCL

Contributors
~~~~~~~~~~~~

* Robin Keunen <robin@coopiteasy.be>
* Dani Quilez <dani.quilez@coopdevs.org>

Maintainers
~~~~~~~~~~~

This module is maintained by Coopdevs Treball SCCL.
