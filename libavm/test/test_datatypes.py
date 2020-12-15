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

import unittest

from libavm import *
from libavm import SPECS_1_1
from libavm.exceptions import AVMListLengthError, AVMItemNotInControlledVocabularyError
import datetime

class AVMMetaTestCase(unittest.TestCase):
    def setUp(self):
        #
        # Sample data
        #
        self.string_data = "Blah Blah Blah"
        self.unicode_data = u"Blah Blah Blah"
        self.url_data = "http://www.spacetelescope.org"
        self.email_data = "akapadia@eso.org"
        self.float_data = 10.0
        self.int_data = 10
        self.string_list_data = ["Blah 1", "Blah 2", "Blah 3", "Blah 4"]
        self.float_list_data = [1.0, 2.0, 3.0, 4.0]
        self.int_list_data = [1, 2, 3, 4]
        self.string_set_data = set(['Blah 1', 'Blah 2', 'Blah 3'])
        self.float_set_data = set([1.0, 2.0, 3.0])
        self.date_data = datetime.date.today()
        
        #
        # More specialize data
        #
        
        # String
        self.string_list_two = ['Blah 1', 'Blah 2']
        
        # Float
        self.float_list_two = [1.0, 2.0]
        self.float_list_four = [1.0, 2.0, 3.0, 4.0]
                
        # CV List
        self.string_list_color = ['Red', 'Green', 'Blue']
        self.string_list_band = ['Optical', 'Infrared', 'X-ray']
        
        
        
    def tearDown(self):
        pass
    

    #
    # Data type tests
    #
    def test_AVMString(self):    
        avm = AVMMeta()
        
        for key, value in list(SPECS_1_1.items()):
            if type(value) is AVMString:
                avm.__setitem__(key, self.string_data)
                self.assertEqual(avm.__getitem__(key), self.string_data, key)
                avm.__delitem__(key)
                self.assertEqual(avm.__getitem__(key), None, key)
                
                self.assertRaises( TypeError, avm.__setitem__, key, self.unicode_data )
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_data )
                self.assertRaises( TypeError, avm.__setitem__, key, self.string_list_data )
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_list_data )
                self.assertRaises( TypeError, avm.__setitem__, key, self.string_set_data )
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_set_data )
                self.assertRaises( TypeError, avm.__setitem__, key, self.date_data )
        
        del avm
    
    def test_AVMURL(self):
        avm = AVMMeta()
        
        for key, value in list(SPECS_1_1.items()):
            if type(value) is AVMURL:
                avm.__setitem__(key, self.url_data)
                self.assertEqual(avm.__getitem__(key), self.url_data, key)
                avm.__delitem__(key)
                self.assertEqual(avm.__getitem__(key), None, key)
                
                self.assertRaises( ValueError, avm.__setitem__, key, self.string_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.unicode_data)
                self.assertRaises( ValueError, avm.__setitem__, key, self.email_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.string_list_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_list_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.string_set_data )
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_set_data )
                self.assertRaises( TypeError, avm.__setitem__, key, self.date_data)
        
        del avm
    
    def test_AVMEmail(self):
        avm = AVMMeta()
        
        for key, value in list(SPECS_1_1.items()):
            if type(value) is AVMEmail:
                avm.__setitem__(key, self.email_data)
                self.assertEqual(avm.__getitem__(key), self.email_data, key)
                avm.__delitem__(key)
                self.assertEqual(avm.__getitem__(key), None, key)                
                
                self.assertRaises( ValueError, avm.__setitem__, key, self.string_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.unicode_data)
                self.assertRaises( ValueError, avm.__setitem__, key, self.url_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.string_list_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_list_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.string_set_data )
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_set_data )
                self.assertRaises( TypeError, avm.__setitem__, key, self.date_data)
        
        del avm
        
    def test_AVMLocalizedString(self):
        avm = AVMMeta()
        
        for key, value in list(SPECS_1_1.items()):
            if type(value) is AVMLocalizedString:
                avm.__setitem__(key, self.string_data)
                self.assertEqual(avm.__getitem__(key), self.string_data, key)
                avm.__delitem__(key)
                self.assertEqual(avm.__getitem__(key), None, key)    

                self.assertRaises( TypeError, avm.__setitem__, key, self.unicode_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.string_list_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_list_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.string_set_data )
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_set_data )
                self.assertRaises( TypeError, avm.__setitem__, key, self.date_data)

        del avm
        
    def test_AVMFloat(self):
        avm = AVMMeta()
        
        for key, value in list(SPECS_1_1.items()):
            if type(value) is AVMFloat:
                avm.__setitem__(key, self.float_data)
                self.assertEqual(avm.__getitem__(key), self.float_data, key)
                avm.__delitem__(key)
                self.assertEqual(avm.__getitem__(key), None, key)

                self.assertRaises( TypeError, avm.__setitem__, key, self.string_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.unicode_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.url_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.email_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.string_list_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_list_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.string_set_data )
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_set_data )
                self.assertRaises( TypeError, avm.__setitem__, key, self.date_data)
        
        del avm
                
    def test_AVMUnorderedStringList(self):
        avm = AVMMeta()
        
        for key, value in list(SPECS_1_1.items()):
            if type(value) is AVMUnorderedStringList:
                avm.__setitem__(key, self.string_set_data)
                self.assertEqual(avm.__getitem__(key), self.string_set_data, key)
                avm.__delitem__(key)
                self.assertEqual(avm.__getitem__(key), None, key)
                
                self.assertRaises( TypeError, avm.__setitem__, key, self.string_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.unicode_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.url_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.email_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.string_list_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_list_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_data )
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_set_data )
                self.assertRaises( TypeError, avm.__setitem__, key, self.date_data)
        
        del avm
        
    def test_AVMOrderedStringList(self):
        avm = AVMMeta()
        
        for key, value in list(SPECS_1_1.items()):
            if type(value) is AVMOrderedStringList:
                avm.__setitem__(key, self.string_list_data)
                self.assertEqual(avm.__getitem__(key), self.string_list_data, key)
                avm.__delitem__(key)
                self.assertEqual(avm.__getitem__(key), None, key)
                
                self.assertRaises( TypeError, avm.__setitem__, key, self.string_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.unicode_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.url_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.email_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_list_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_data )
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_set_data )
                self.assertRaises( TypeError, avm.__setitem__, key, self.string_set_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.date_data)
                
        del avm
        
    def test_AVMOrderedFloatList(self):
        """
        .todo:: need to improve
        """
        avm = AVMMeta()
        
        for key, value in list(SPECS_1_1.items()):
            if type(value) is AVMOrderedFloatList:
                #avm.__setitem__(key, self.float_list_data)
                #self.assertEqual(avm.__getitem__(key), self.float_list_data, key)
                #avm.__delitem__(key)
                #self.assertEqual(avm.__getitem__(key), None, key)

                #self.assertRaises( AVMListLengthError, avm.__setitem__, key, self.float_list_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.string_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.unicode_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.url_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.email_data)
                #self.assertRaises( TypeError, avm.__setitem__, key, self.string_list_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_data )
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_set_data )
                self.assertRaises( TypeError, avm.__setitem__, key, self.string_set_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.date_data)
        
        del avm
    
    def test_AVMDate(self):
        avm = AVMMeta()
        
        for key, value in list(SPECS_1_1.items()):
            if type(value) is AVMDate:
                avm.__setitem__(key, self.date_data)
                self.assertEqual(avm.__getitem__(key), self.date_data, key)
                avm.__delitem__(key)
                self.assertEqual(avm.__getitem__(key), None, key)
                
                self.assertRaises( TypeError, avm.__setitem__, key, self.string_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.unicode_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.url_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.email_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.string_list_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_list_data)
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_data )
                self.assertRaises( TypeError, avm.__setitem__, key, self.float_set_data )
                self.assertRaises( TypeError, avm.__setitem__, key, self.string_set_data)
        
        del avm            
    
    #
    # More specialized test
    #
    def test_AVMOrderedFloatList_strict(self):
            pass
    
    
    #
    # Creator Metadata Tests
    #
    def test_setitem_creator(self):
        field = 'Creator'
        
        avm = AVMMeta()
        data = 'Amit Kapadia'
        avm.__setitem__(field, data)
        self.assertEqual(avm.__getitem__(field), data, field)
        del avm
    
    def test_setitem_creatorurl(self):
        avm = AVMMeta()
        data = 'http://www.spacetelescope.org'
        avm.__setitem__('CreatorURL', data)
        self.assertEqual(avm.__getitem__('CreatorURL'), data, "CreatorURL")
        del avm
        
    def test_setitem_contactname(self):
        avm = AVMMeta()
        avm.__setitem__('Contact.Name', 'Amit Kapadia')
        self.assertEqual(avm.__getitem__('Contact.Name'), 'Amit Kapadia', "Contact.Name")
        del avm
        
    def test_setitem_contactemail(self):
        avm = AVMMeta()
        avm.__setitem__('Contact.Email', 'akapadia@eso.org')
        self.assertEqual(avm.__getitem__('Contact.Email'), 'akapadia@eso.org', "Contact.Email")
        del avm
        
    def test_setitem_contacttelephone(self):
        avm = AVMMeta()
        avm.__setitem__('Contact.Telephone', '14435196993')
        self.assertEqual(avm.__getitem__('Contact.Telephone'), '14435196993', "Contact.Telephone")
        del avm
        
    def test_setitem_contactaddress(self):
        avm = AVMMeta()
        avm.__setitem__('Contact.Address', 'Karl-Schwarzschild-Strasse 2')
        self.assertEqual(avm.__getitem__('Contact.Address'), 'Karl-Schwarzschild-Strasse 2', "Contact.Address")
        del avm
        
    def test_setitem_contactcity(self):
        avm = AVMMeta()
        avm.__setitem__('Contact.City', 'Garching')
        self.assertEqual(avm.__getitem__('Contact.City'), 'Garching', "Contact.City")
        del avm
        
    def test_setitem_contactstateprovince(self):
        avm = AVMMeta()
        avm.__setitem__('Contact.StateProvince', 'Bavaria')
        self.assertEqual(avm.__getitem__('Contact.StateProvince'), 'Bavaria', "Contact.StateProvince")
        del avm
        
    def test_setitem_contactpostalcode(self):
        avm = AVMMeta()
        avm.__setitem__('Contact.PostalCode', 'D-85748')
        self.assertEqual(avm.__getitem__('Contact.PostalCode'), 'D-85748', "Contact.PostalCode")
        del avm
        
    def test_setitem_contactcountry(self):
        avm = AVMMeta()
        avm.__setitem__('Contact.Country', 'Germany')
        self.assertEqual(avm.__getitem__('Contact.Country'), 'Germany', "Contact.Country")
        del avm
        
    def test_setitem_rights(self):
        avm = AVMMeta()
        avm.__setitem__('Rights', 'Public Domain')
        self.assertEqual(avm.__getitem__('Rights'), 'Public Domain', "Rights")
        del avm
        
    #
    # Content Metadata Tests
    #
    def test_setitem_title(self):
        avm = AVMMeta()
        avm.__setitem__('Title', 'Sample Title')
        self.assertEqual(avm.__getitem__('Title'), 'Sample Title', "Title")
        del avm
        
    def test_setitem_headline(self):
        avm = AVMMeta()
        avm.__setitem__('Headline', 'Sample Headline')
        self.assertEqual(avm.__getitem__('Headline'), 'Sample Headline', "Headline")
        del avm
        
    def test_setitem_description(self):
        avm = AVMMeta()
        avm.__setitem__('Description', 'Sample Description')
        self.assertEqual(avm.__getitem__('Description'), 'Sample Description', "Description")
        del avm
        
    def test_setitem_subjectcategory(self):
        avm = AVMMeta()
        avm.__setitem__('Subject.Category', set(['A.1.2.3', 'B.2.3.4']))
        self.assertEqual(avm.__getitem__('Subject.Category'), set(['A.1.2.3', 'B.2.3.4']), "Subject.Category")
        del avm
        
    def test_setitem_subjectname(self):
        avm = AVMMeta()
        avm.__setitem__('Subject.Name', set(['Sample Name 1', 'Sample Name 2']))
        self.assertEqual(avm.__getitem__('Subject.Name'), set(['Sample Name 1', 'Sample Name 2']), "Subject.Name")
        del avm
        
    def test_setitem_distance(self):        
        avm = AVMMeta()
        key = 'Distance'
        
        avm.__setitem__(key, self.float_list_two)
        self.assertEqual(avm.__getitem__(key), self.float_list_two, key)
            
        avm.__delitem__(key)
        self.assertEqual(avm.__getitem__(key), None, key)
        
        # Test with bad data
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.unicode_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.url_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.email_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_list_two)
        self.assertRaises( AVMListLengthError, avm.__setitem__, key, self.float_list_four)
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_set_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_set_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.date_data)
        
        del avm
        
        
    def test_setitem_distancenotes(self):
        avm = AVMMeta()
        avm.__setitem__('Distance.Notes', 'Sample distance notes')
        self.assertEqual(avm.__getitem__('Distance.Notes'), 'Sample distance notes', "Distance.Notes")
        del avm
        
    def test_setitem_referenceurl(self):
        avm = AVMMeta()
        avm.__setitem__('ReferenceURL', 'http://www.spacetelescope.org/images/html/heic0817a.html')
        self.assertEqual(avm.__getitem__('ReferenceURL'), 'http://www.spacetelescope.org/images/html/heic0817a.html', "ReferenceURL")
        del avm
        
    def test_setitem_credit(self):
        avm = AVMMeta()
        avm.__setitem__('Credit', 'NASA, ESA and Andy Fabian (University of Cambridge, UK)')
        self.assertEqual(avm.__getitem__('Credit'), 'NASA, ESA and Andy Fabian (University of Cambridge, UK)', "Credit")
        del avm
        
    def test_setitem_date(self):
        avm = AVMMeta()
        avm.__setitem__('Date', datetime.date(2009, 5, 27))
        self.assertEqual(avm.__getitem__('Date'), datetime.date(2009, 5, 27), "Date")
        del avm
        
    def test_setitem_id(self):
        avm = AVMMeta()
        avm.__setitem__('ID', 'heic0817a')
        self.assertEqual(avm.__getitem__('ID'), 'heic0817a', "ID")
        del avm
        
    def test_setitem_type(self):
        avm = AVMMeta()
        key = 'Type'
        
        for item in cv.TYPE_CHOICES:
            avm.__setitem__(key, item)
            self.assertEqual(avm.__getitem__(key), item, key)
            
            avm.__delitem__(key)
            self.assertEqual(avm.__getitem__(key), None, key)
        
        # Test with bad data
        self.assertRaises( AVMItemNotInControlledVocabularyError, avm.__setitem__, key, self.string_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.unicode_data)
        self.assertRaises( AVMItemNotInControlledVocabularyError, avm.__setitem__, key, self.url_data)
        self.assertRaises( AVMItemNotInControlledVocabularyError, avm.__setitem__, key, self.email_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_list_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_set_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_set_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.date_data)
        
        del avm
    
    def test_setitem_imageproductquality(self):
        avm = AVMMeta()
        key = 'Image.ProductQuality'
        
        for item in cv.IMAGE_PRODUCT_QUALITY_CHOICES:
            avm.__setitem__(key, item)
            self.assertEqual(avm.__getitem__(key), item, key)
            
            avm.__delitem__(key)
            self.assertEqual(avm.__getitem__(key), None, key)
        
        # Test with bad data
        self.assertRaises( AVMItemNotInControlledVocabularyError, avm.__setitem__, key, self.string_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.unicode_data)
        self.assertRaises( AVMItemNotInControlledVocabularyError, avm.__setitem__, key, self.url_data)
        self.assertRaises( AVMItemNotInControlledVocabularyError, avm.__setitem__, key, self.email_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_list_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_set_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_set_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.date_data)
        
        del avm

    #
    # Observation Metadata Tests
    #
    def test_setitem_facility(self):
        avm = AVMMeta()
        avm.__setitem__('Facility', ['Sample Facility 1', 'Sample Facility 2'])
        self.assertEqual(avm.__getitem__('Facility'), ['Sample Facility 1', 'Sample Facility 2'], "Facility")
        del avm

    def test_setitem_instrument(self):
        avm = AVMMeta()
        avm.__setitem__('Instrument', ['Sample Instrument 1', 'Sample Instrument 2'])
        self.assertEqual(avm.__getitem__('Instrument'), ['Sample Instrument 1', 'Sample Instrument 2'], "Instrument")
        del avm
        
    def test_setitem_spectralcolorassignment(self):
        
        avm = AVMMeta()
        key = 'Spectral.ColorAssignment'
        
        for item in cv.SPECTRAL_COLOR_ASSIGNMENT_CHOICES:
            avm.__setitem__(key, [item])
            self.assertEqual(avm.__getitem__(key), [item], key)
            
            avm.__delitem__(key)
            self.assertEqual(avm.__getitem__(key), None, key)
        
        # Test with bad data
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.unicode_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.url_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.email_data)
        self.assertRaises( AVMItemNotInControlledVocabularyError, avm.__setitem__, key, self.string_list_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_list_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_set_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_set_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.date_data)
        
        del avm
    
    def test_setitem_spectralband(self):
        avm = AVMMeta()
        key = 'Spectral.Band'
        
        for item in cv.SPECTRAL_BAND_CHOICES:
            avm.__setitem__(key, [item])
            self.assertEqual(avm.__getitem__(key), [item], key)
            
            avm.__delitem__(key)
            self.assertEqual(avm.__getitem__(key), None, key)
        
        # Test with bad data
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.unicode_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.url_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.email_data)
        self.assertRaises( AVMItemNotInControlledVocabularyError, avm.__setitem__, key, self.string_list_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_list_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_set_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_set_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.date_data)
        
        del avm

    def test_setitem_spectralbandpass(self):
        avm = AVMMeta()
        avm.__setitem__('Spectral.Bandpass', ['Sample Bandpass 1', 'Sample Bandpass 2'])
        self.assertEqual(avm.__getitem__('Spectral.Bandpass'), ['Sample Bandpass 1', 'Sample Bandpass 2'], "Spectral.Bandpass")
        del avm

    def test_setitem_spectralcentralwavelength(self):
        avm = AVMMeta()
        data = [1.0, 2.0]
        avm.__setitem__('Spectral.CentralWavelength', data)
        self.assertEqual(avm.__getitem__('Spectral.CentralWavelength'), data)
        del avm
        
    def test_setitem_spectralnotes(self):
        avm = AVMMeta()
        avm.__setitem__('Spectral.Notes', 'Sample spectral notes')
        self.assertEqual(avm.__getitem__('Spectral.Notes'), 'Sample spectral notes', "Spectral.Notes")
        del avm

    def test_setitem_temporalstarttime(self):
        avm = AVMMeta()
        avm.__setitem__('Temporal.StartTime', [0.0, 0.0])
        self.assertEqual(avm.__getitem__('Temporal.StartTime'), [0.0, 0.0], "Temporal.StartTime")
        del avm

    def test_setitem_temporalintegrationtime(self):
        avm = AVMMeta()
        avm.__setitem__('Temporal.IntegrationTime', [100.0, 200.0])
        self.assertEqual(avm.__getitem__('Temporal.IntegrationTime'), [100.0, 200.0], "Temporal.IntegrationTime")
        del avm
        
    def test_setitem_datasetid(self):
        avm = AVMMeta()
        avm.__setitem__('DatasetID', ['Data 1', 'Data 2'])
        self.assertEqual(avm.__getitem__('DatasetID'), ['Data 1', 'Data 2'], "DatasetID")
        del avm

    #
    # Coordinate Metadata Tests
    #
    def test_setitem_spatialcoordinateframe(self):
        avm = AVMMeta()
        key = 'Spatial.CoordinateFrame'
        
        for item in cv.SPATIAL_COORDINATE_FRAME_CHOICES:
            avm.__setitem__(key, item)
            self.assertEqual(avm.__getitem__(key), item, key)
            
            avm.__delitem__(key)
            self.assertEqual(avm.__getitem__(key), None, key)
        
        # Test with bad data
        self.assertRaises( AVMItemNotInControlledVocabularyError, avm.__setitem__, key, self.string_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.unicode_data)
        self.assertRaises( AVMItemNotInControlledVocabularyError, avm.__setitem__, key, self.url_data)
        self.assertRaises( AVMItemNotInControlledVocabularyError, avm.__setitem__, key, self.email_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_list_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_set_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_set_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.date_data)
        
        del avm
        
    def test_setitem_spatialequinox(self):
        avm = AVMMeta()
        key = 'Spatial.Equinox'
        
        for item in cv.SPATIAL_EQUINOX_CHOICES:
            avm.__setitem__(key, item)
            self.assertEqual(avm.__getitem__(key), item, key)
            
            avm.__delitem__(key)
            self.assertEqual(avm.__getitem__(key), None, key)
        
        # Test with bad data
        self.assertRaises( AVMItemNotInControlledVocabularyError, avm.__setitem__, key, self.string_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.unicode_data)
        self.assertRaises( AVMItemNotInControlledVocabularyError, avm.__setitem__, key, self.url_data)
        self.assertRaises( AVMItemNotInControlledVocabularyError, avm.__setitem__, key, self.email_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_list_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_set_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_set_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.date_data)
        
        del avm

    def test_setitem_spatialreferencevalue(self):
        avm = AVMMeta()
        key = 'Spatial.ReferenceValue'
        
        avm.__setitem__(key, self.float_list_two)
        self.assertEqual(avm.__getitem__(key), self.float_list_two, key)
            
        avm.__delitem__(key)
        self.assertEqual(avm.__getitem__(key), None, key)
        
        # Test with bad data
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.unicode_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.url_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.email_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_list_two)
        self.assertRaises( AVMListLengthError, avm.__setitem__, key, self.float_list_four)
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_set_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_set_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.date_data)
        
        del avm

    def test_setitem_spatialreferencedimension(self):
        avm = AVMMeta()
        key = 'Spatial.ReferenceDimension'
        
        avm.__setitem__(key, self.float_list_two)
        self.assertEqual(avm.__getitem__(key), self.float_list_two, key)
            
        avm.__delitem__(key)
        self.assertEqual(avm.__getitem__(key), None, key)
        
        # Test with bad data
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.unicode_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.url_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.email_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_list_two)
        self.assertRaises( AVMListLengthError, avm.__setitem__, key, self.float_list_four)
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_set_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_set_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.date_data)
        
        del avm

    def test_setitem_spatialreferencepixel(self):
        avm = AVMMeta()
        key = 'Spatial.ReferencePixel'
        
        avm.__setitem__(key, self.float_list_two)
        self.assertEqual(avm.__getitem__(key), self.float_list_two, key)
            
        avm.__delitem__(key)
        self.assertEqual(avm.__getitem__(key), None, key)
        
        # Test with bad data
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.unicode_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.url_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.email_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_list_two)
        self.assertRaises( AVMListLengthError, avm.__setitem__, key, self.float_list_four)
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_set_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_set_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.date_data)
        
        del avm

    def test_setitem_spatialscale(self):
        avm = AVMMeta()
        key = 'Spatial.Scale'
        
        avm.__setitem__(key, self.float_list_two)
        self.assertEqual(avm.__getitem__(key), self.float_list_two, key)
            
        avm.__delitem__(key)
        self.assertEqual(avm.__getitem__(key), None, key)
        
        # Test with bad data
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.unicode_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.url_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.email_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_list_two)
        self.assertRaises( AVMListLengthError, avm.__setitem__, key, self.float_list_four)
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_set_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_set_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.date_data)
        
        del avm

    def test_setitem_spatialrotation(self):
        avm = AVMMeta()
        data = 90.0
        avm.__setitem__('Spatial.Rotation', data)
        self.assertEqual(avm.__getitem__('Spatial.Rotation'), data, "Spatial.Rotation")
        del avm

    def test_setitem_spatialcoordsystemprojection(self):
        avm = AVMMeta()
        key = 'Spatial.CoordsystemProjection'
        
        for item in cv.SPATIAL_COORDSYSTEM_PROJECTION_CHOICES:
            avm.__setitem__(key, item)
            self.assertEqual(avm.__getitem__(key), item, key)
            
            avm.__delitem__(key)
            self.assertEqual(avm.__getitem__(key), None, key)
        
        # Test with bad data
        self.assertRaises( AVMItemNotInControlledVocabularyError, avm.__setitem__, key, self.string_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.unicode_data)
        self.assertRaises( AVMItemNotInControlledVocabularyError, avm.__setitem__, key, self.url_data)
        self.assertRaises( AVMItemNotInControlledVocabularyError, avm.__setitem__, key, self.email_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_list_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_set_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_set_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.date_data)
        
        del avm

    def test_setitem_spatialquality(self):
        avm = AVMMeta()
        key = 'Spatial.Quality'
        
        for item in cv.SPATIAL_QUALITY_CHOICES:
            avm.__setitem__(key, item)
            self.assertEqual(avm.__getitem__(key), item, key)
            
            avm.__delitem__(key)
            self.assertEqual(avm.__getitem__(key), None, key)
        
        # Test with bad data
        self.assertRaises( AVMItemNotInControlledVocabularyError, avm.__setitem__, key, self.string_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.unicode_data)
        self.assertRaises( AVMItemNotInControlledVocabularyError, avm.__setitem__, key, self.url_data)
        self.assertRaises( AVMItemNotInControlledVocabularyError, avm.__setitem__, key, self.email_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_list_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.float_set_data )
        self.assertRaises( TypeError, avm.__setitem__, key, self.string_set_data)
        self.assertRaises( TypeError, avm.__setitem__, key, self.date_data)
        
        del avm

    def test_setitem_spatialnotes(self):
        avm = AVMMeta()
        data = 'Sample spatial notes'
        avm.__setitem__('Spatial.Notes', data)
        self.assertEqual(avm.__getitem__('Spatial.Notes'), data, "Spatial.Notes")
        del avm

    def test_setitem_spatialfitsheader(self):
        avm = AVMMeta()
        data = 'Sample FITS Header'
        avm.__setitem__('Spatial.FITSheader', data)
        self.assertEqual(avm.__getitem__('Spatial.FITSheader'), data, "Spatial.FITSheader")
        del avm

    def test_setitem_spatialcdmatrix(self):
        avm = AVMMeta()
        data = [1.0, 2.0, 3.0, 4.0]
        avm.__setitem__('Spatial.CDMatrix', data)
        self.assertEqual(avm.__getitem__('Spatial.CDMatrix'), data, "Spatial.CDMatrix")
        del avm
        
    #
    # Publisher Metadata Tests
    #
    def test_setitem_publisher(self):
        avm = AVMMeta()
        data = 'European Southern Observaotry'
        avm.__setitem__('Publisher', data)
        self.assertEqual(avm.__getitem__('Publisher'), data, "Publisher")
        del avm

    def test_setitem_publisher_id(self):
        avm = AVMMeta()
        data = 'SamplePubID123'
        avm.__setitem__('PublisherID', data)
        self.assertEqual(avm.__getitem__('PublisherID'), data, "PublisherID")
        del avm
        
    def test_setitem_resourceid(self):
        avm = AVMMeta()
        data = 'SampleResourceID123'
        avm.__setitem__('ResourceID', data)
        self.assertEqual(avm.__getitem__('ResourceID'), data, "ResourceID")
        del avm
        
    def test_setitem_resourceurl(self):
        avm = AVMMeta()
        data = 'http://www.spacetelescope.org/images/screen/heic0817a.jpg'
        avm.__setitem__('ResourceURL', data)
        self.assertEqual(avm.__getitem__('ResourceURL'), data, "ResourceURL")
        del avm

    def test_setitem_relatedresources(self):
        avm = AVMMeta()
        data = set([
            'http://www.spacetelescope.org/images/screen/heic0817b.jpg',
            'http://www.spacetelescope.org/images/screen/heic0817c.jpg',
            'http://www.spacetelescope.org/images/screen/heic0817d.jpg',
            'http://www.spacetelescope.org/images/screen/heic0817e.jpg',
        ])
        avm.__setitem__('RelatedResources', data)
        self.assertEqual(avm.__getitem__('RelatedResources'), data, "RelatedResources")
        del avm

    def test_setitem_metadatadate(self):
        avm = AVMMeta()
        data = datetime.date.today()
        avm.__setitem__('MetadataDate', data)
        self.assertEqual(avm.__getitem__('MetadataDate'), data, "MetadataDate")
        del avm
        
    def test_setitem_metadataversion(self):
        avm = AVMMeta()
        data = 1.1
        avm.__setitem__('MetadataVersion', data)
        self.assertEqual(avm.__getitem__('MetadataVersion'), data, "MetadataVersion")
        del avm

if __name__ == '__main__':
    unittest.main()
    