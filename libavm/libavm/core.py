# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, European Space Agency & European Southern Observatory (ESA/ESO)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#      * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
# 
#      * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
# 
#      * Neither the name of the European Space Agency, European Southern 
#        Observatory nor the names of its contributors may be used to endorse or 
#        promote products derived from this software without specific prior 
#        written permission.
# 
# THIS SOFTWARE IS PROVIDED BY ESA/ESO ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL ESA/ESO BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE

"""
A module for parsing, manipulating, and serializing AVM data in the XMP format.
"""

try:
	import libxmp
except ImportError:
	pass

from libavm.specs import *
import datetime


__all__ = ['AVMMeta']


class AVMMeta(object):
	"""
	AVMMeta is a class offering direct access and validation of AVM metadata.  An AVM dictionary
	or XMPMeta object may be passed to the constructor.  Priority will be given to the AVM dictionary.
	
	:param avm_dict:	Python dictionary containing AVM
	:param xmp: 	XMPMeta object
	:param version:	AVM version, default to the current (1.1)
	"""
	def __init__(self, avm_dict=None, xmp=None, version="1.1"):
		# Dictionary storage for AVM, synchronizes with the XMP packet
		self.data = {}
		# Create an XMPMeta object
		self.xmp = libxmp.XMPMeta()
				
		# Check the version type
		if version == "1.1":
			self.specs = SPECS_1_1
		
		# Register all avm schema
		for SCHEMA, PREFIX in AVM_SCHEMAS.items():
			self.xmp.register_namespace(SCHEMA, PREFIX)
			
		# Impose the current date as the metadata date
		self['MetadataDate'] = datetime.date.today()
		
		# Pass an XMPMeta object
		if xmp:
			# Parse for AVM
			self.xmp = xmp
			# Synchronize XMP data with dictionary
			for key, value in self.specs.items():
				avmdt = self.specs[key]
				self.data[key] = avmdt.get_data(self.xmp)
				
		# Pass an AVM dictionary
		if avm_dict:
			for key, item in avm_dict.items():
				try:
					self[key] = item
				except:
					# Suppress error for items not in specs dictionary
					continue 
	
	def __setitem__(self, key, value):
		
		if key in self.specs:
			avmdt = self.specs[key]
			if avmdt.set_data(self.xmp, value):
				self.data[key] = avmdt.get_data(self.xmp)
		else:
			raise KeyError, "The key '%s' is not an AVM field" % key
	
	def __getitem__(self, key):
		
		if key in self.specs:
			avmdt = self.specs[key]
			return avmdt.get_data(self.xmp)
		else:
			raise KeyError, "The key '%s' is not an AVM field" % key
	
	def __delitem__(self, key):
		
		if key in self.specs:
			avmdt = self.specs[key]
			avmdt.delete_data(self.xmp)


