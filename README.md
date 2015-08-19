# Python AVM Library

The Python AVM Library is a library for parsing, manipulating, and serializing Astronomy Visualization Metadata (AVM) in the XMP format. It is a light wrapper around the Python XMP Toolkit, simplifying the manipulation of AVM-specific fields.

Python AVM Library is being developed by:
* [ESA/Hubble - European Space Agency](http://www.spacetelescope.org/)
* [ESO - European Southern Observatory](http://www.eso.org/)

# What is AVM?

The astronomical education and public outreach (EPO) community plays a key role in conveying the results of scientific research to the general public. A key product of EPO development is a variety of non-scientific public image resources, both derived from scientific observations and created as artistic visualizations of scientific results. This refers to general image formats such as JPEG, TIFF, PNG, GIF, not scientific FITS datasets. Such resources are currently scattered across the internet in a variety of galleries and archives, but are not searchable in any coherent or unified way.

Just as Virtual Observatory (VO) standards open up all data archives to a common query engine, the EPO community will benefit greatly from a similar mechanism for image search and retrieval. Existing metadata standards for the Virtual Observatory are tailored to the management of research datasets and only cover EPO resources (like publication quality imagery) at the "collection" level and are thus insufficient for the needs of the EPO community.

The primary focus of the AVM is on print-ready and screen ready astronomical imagery, which has been rendered from telescopic observations (also known as "pretty pictures"). Such images can combine data acquired at different wavebands and from different observatories. While the primary intent is to cover data-derived astronomical images, there are broader uses as well. Specifically, the most general subset of this schema is also appropriate for describing artwork and illustrations of astronomical subject matter. This is covered in some detail in later sections.

The intended users of astronomical imagery cover a broad variety of fields: educators, students, journalists, enthusiasts, and scientists. The core set of required tags define the key elements needed in a practical database for identification of desired resources. For example, one might choose to search for images of the Crab Nebula that include both X-ray and visible light elements, or for any images within 2 degrees of a specified location on the sky that include at least some data from the Spitzer Space Telescope.

Future plans include "multimedia modules" and "planetarium modules" into the AVM standard.

# Further Information
[http://virtualastronomy.org/](http://virtualastronomy.org/)
