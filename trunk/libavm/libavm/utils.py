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

import libavm
try:
	import libxmp
	from libxmp import XMPError
except ImportError:
	pass

__all__ = ['avm_from_file', 'avm_to_file']

def avm_from_file(file_path):
	"""
	Function to retrieve the XMP packet from a file
	
	:param file_path: Path to file
	
	:return: A dictionary with AVM data
	"""
	xmpfile = libxmp.files.XMPFiles()
	
	try:
		xmpfile.open_file(file_path, open_option=libxmp.files.XMP_OPEN_READ)
		xmp = xmpfile.get_xmp()
		xmpfile.close_file()
	except libxmp.XMPError:
		return {}
	
	avm = libavm.AVMMeta(xmp=xmp)
	return avm.data

def avm_to_file(file_path, dict={}):
	"""
	Function to inject AVM into a file.  Preserves existing XMP in the file, while replacing
	fields passed through dict.
	
	If a field is an unordered list, then data is appended to existing values
	
	
	:param file_path: Path to file
	:param dict: A dictionary containing AVM metadata
	
	:return: Boolean
	
	.. todo:: Improve avm_to_file function
	"""
	xmpfile = libxmp.files.XMPFiles()
	
	try:
		xmpfile.open_file(file_path, open_forupdate=True)
	except libxmp.XMPError:
		return False

	xmp = xmpfile.get_xmp()
	if xmp:
		pass
	else:
		xmp = libxmp.XMPMeta()
	
	avm = libavm.AVMMeta(xmp=xmp, avm_dict=dict)
	
	if xmpfile.can_put_xmp(avm.xmp):
		xmpfile.put_xmp(avm.xmp)
		xmpfile.close_file()
		return True
	else:
		return False
	
	
	
	
	
	