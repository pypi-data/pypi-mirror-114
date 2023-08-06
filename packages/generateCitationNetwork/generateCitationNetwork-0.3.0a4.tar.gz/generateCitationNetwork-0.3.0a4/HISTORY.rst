.. :changelog:

History
-------

0.1.0 (2020-12-09)
++++++++++++++++++

* First release on PyPI.

0.2.0 (2021-02-19)
++++++++++++++++++

* Refactored to include references without DOI.
* New routine to determine publication year from different fields.
* Publications without year data are set to the source DOI year.

0.3.0 (2021-06-23)
++++++++++++++++++

* New generator class for querying app.dimension.ai `DimGenerateCitationNet`, enabling use outside of mpiwg VPN.
* Field of research categories in JSON output.
* Tests for `DimGenerateCitationNet` (`GenerateCitationNet` unable to be tested outside of mpiwg VPN).
