Using Python AVM Library
============================

This little tutorial will show you two different methods for how to read/write XMP/AVM documents from files as well as manipulate the astronomy visualization metadata once extracted from the file. 

The tutorial is meant to be understood without prior knowledge of XMP. However, readers who decides to use the library are strongly encouraged to gain basic knowledge and understanding of:

  * XMP Data Model
  * XMP Serialization

See the AVM documentation for a list of all AVM/XMP fields that this library can manipulate.  Documentation can be found in the links below:
 
 * http://www.virtualastronomy.org/avm_metadata.php#avmfinal


Method 1: Read AVM
------------------
One of the most basic uses of the library is::

	from libavm.utils import *

	avm = avm_from_file( "/path/to/some/file_with_xmp.ext" )

This will read the AVM embedded in the file and return it as a dictionary. The keys in the dictionary are AVM fields.

Method 2: Read/Write AVM
------------------------
Example 1 focused on just extracting the AVM from a file to determine the value of a field. If you, however, want to extract the AVM from a file, update it, *and* write it back again execute the following::

	from libavm.utils import *
	
	# Create a dictionary using AVM fields as the key, and the appropriate values
	avm_dict = {
		'Creator': 'Amit Kapadia',
		'CreatorURL': 'www.portaltotheuniverse.org',
		'Facility': ['Hubble Space Telescope', 'Spitzer Space Telescope', 'Chandra X-ray Observatory']
	}
	
	# Call this utility function, passing the AVM dictionary in the second argument
	avm_to_file("/path/to/some/file.ext", avm_dict)
	
	# To read this data back out from the file
	avm_data = avm_from_file("/path/to/some/file.ext") # returns a dictionary


Further Examples
-------------
Create an AVMMeta object, and inject AVM into the XMP packet::

	from libavm import *
	
	# Initialize the AVMMeta object
	avm = AVMMeta()
	
	# Adding, retriving, and deleting AVM is as simple as using a Python dictionary
	
	# Add a property
	avm['Facility'] = ['Hubble Space Telescope', 'Spitzer Space Telescope', 'Chandra X-ray Observatory']
	
	# Retrieve a property
	avm['Facility'] # Returns a list
	
	# Delete a property
	del avm['Facility']
	
	# Injecting AVM to file from AVMMeta()
	avm_to_file("/path/to/some/file.ext", avm.data) # avm.data is a dictionary
	
	