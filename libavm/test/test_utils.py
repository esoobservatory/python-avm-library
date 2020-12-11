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

from __future__ import print_function
import unittest

import sys
import os
import os.path

sys.path.append(os.path.pardir)

from libavm.utils import avm_from_file, avm_to_file
import datetime

from samples import samplefiles, open_flags, sampledir, make_temp_samples, remove_temp_samples

class AVMUtilsTestCase(unittest.TestCase):
    """ Class to test utility functions """
    def setUp(self):
        # Create working temp sample copy
        make_temp_samples()
        
        # AVM dictionary
        self.avm_dict = {
            # Creator Metadata
            'Creator' : 'Sample Creator',
            'CreatorURL': 'http://www.spacetelescope.org',
            'Contact.Name': ['Sample Name 1', 'Sample Name 2', 'Sample Name 3'],
            'Contact.Email': 'akapadia@eso.org',
            'Contact.Telephone': '+49 89 320 06 761',
            'Contact.Address': 'Karl-Schwarschild-Strasse 2',
            'Contact.City': 'Garching bei München',
            'Contact.StateProvince': 'Baveria',
            'Contact.PostalCode': 'D-85748',
            'Contact.Country': 'Germany',
            'Rights': 'Public Domain',
            
            # Content Metadata
            'Title': 'Lorem ipsum',
            'Headline': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam vel sapien a urna volutpat accumsan.',
            'Description': 'Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Praesent fringilla varius lacus id pellentesque. Ut nec volutpat odio. Etiam purus ligula, aliquam quis interdum sit amet, eleifend eget magna. Maecenas mattis libero vel risus commodo laoreet. Fusce sit amet magna tincidunt massa imperdiet euismod id vel urna. Donec a enim est. Pellentesque condimentum, erat sit amet vehicula posuere, augue diam placerat nisi, in posuere orci mauris ac sem. Etiam enim ante, molestie faucibus mattis eu, viverra id turpis. Integer vitae leo arcu, sit amet imperdiet enim. Quisque pulvinar, risus at pharetra viverra, dolor mi mollis justo, id sodales sapien sem vel est. Ut ut quam at felis vestibulum faucibus. Pellentesque nibh leo, auctor at malesuada quis, faucibus sollicitudin metus. Mauris eget arcu sem, at tempor tellus. Integer eu mi sem, vitae pharetra augue. Mauris malesuada aliquam libero vitae elementum.',
            'Subject.Category': set(['A.1.2.3', 'B.4.5.6', 'C.7.8.9']),
            'Subject.Name': set(['Nullam vel sapien', 'Mauris malesuada']),
            'Distance': [3000.0],
            'Distance.Notes': 'Vestibulum vitae lectus sed tortor dapibus ultricies in vel lorem. In auctor facilisis fringilla. Praesent consectetur luctus est nec ullamcorper. Curabitur et augue id odio viverra egestas ac et diam.',
            'ReferenceURL': 'http://www.spacetelescope.org/images/html/heic0817a.html',
            'Credit': 'Morbi scelerisque faucibus sem',
            'Date': datetime.date.today(),
            'ID': 'heic123456',
            'Type': 'Observation',
            'Image.ProductQuality': 'Good',
            
            # Observation Metadata
            'Facility': ['Hubble Space Telescope', 'Spitzer Space Telescope', 'Chandra X-ray Observatory'],
            'Instrument': ['ACS', 'IRAC', 'ACIS'],
            'Spectral.ColorAssignment': ['Red', 'Green', 'Blue'],
            'Spectral.Band': ['Optical', 'Infrared', 'X-ray'],
            'Spectral.Bandpass': ['optical', 'near-infrared', 'x-ray'],
            'Spectral.CentralWavelength': [1.0, 2.0, 3.0],
            'Spectral.Notes': 'In tincidunt laoreet diam, pharetra convallis sapien rutrum at. Aenean elementum enim non velit imperdiet rhoncus.',
            'Temporal.StartTime': [1.0, 1.0, 1.0],
            'Temporal.IntegrationTime': [300.0, 300.0, 300.0],
            'DatasetID': ['HST123', 'SSC123', 'CFA123'],
            
            # Coordinate Metadata
            'Spatial.CoordinateFrame': 'ICRS',
            'Spatial.Equinox': 'J2000',
            'Spatial.ReferenceValue': [123.0, 456.0],
            'Spatial.ReferenceDimension':[3000.0, 3000.0],
            'Spatial.ReferencePixel': [1500.0, 1500.0],
            'Spatial.Scale': [0.001, 0.001],
            'Spatial.Rotation': 90.0,
            'Spatial.CoordsystemProjection': 'TAN',
            'Spatial.Quality': 'Full',
            'Spatial.Notes': 'Morbi sit amet gravida metus. Sed vitae velit ante, eget aliquam purus. Donec commodo est et libero facilisis ut dictum enim pellentesque.',
            'Spatial.FITSheader':'Sample FITS Header',
            'Spatial.CDMatrix': [1.0, 0.0, -1.0, 0.0],
            
            # Publisher Metadata
            'Publisher': 'Hubble European Information Centre', 
            'PublisherID': '123456',
            'ResourceID': '78910',
            'ResourceURL': 'http://www.spacetelescope.org/images/html/heic0817a.html',
            'RelatedResources':  set(['one', 'two' , 'three']),
            'MetadataDate': datetime.date.today(),
            'MetadataVersion': 1.1,
        }
        
    def tearDown(self):
        remove_temp_samples()
        
    def test_avm_to_file(self):
        for f in samplefiles.iteritems():
            print(f[0])
            avm_to_file(f[0], self.avm_dict, replace=True)
            retrieved_avm = avm_from_file(f[0])
            self.assertEqual(retrieved_avm, self.avm_dict, f[0])
            """
            missing = []
            for key, value in self.avm_dict.iteritems():
                if key in retrieved_avm.keys():
                    if value != retrieved_avm[key]:
                        missing.append(key)
                        print self.avm_dict[key]
                        print retrieved_avm[key]
                        print '\n'
            
            print missing
            """

if __name__ == '__main__':
    unittest.main()