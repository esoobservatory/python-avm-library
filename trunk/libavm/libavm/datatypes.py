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
Definition of various AVM specific data types
"""
import libxmp
import re
import time
import datetime

from libavm.exceptions import AVMListLengthError, AVMItemNotInControlledVocabularyError


__all__ = [
    'AVMString',
    'AVMStringCVCapitalize',
    'AVMStringCVUpper',
    'AVMURL',
    'AVMEmail',
    'AVMLocalizedString',
    'AVMFloat',
    'AVMUnorderedStringList',
    'AVMOrderedStringList',
    'AVMOrderedStringListCV',
    'AVMOrderedFloatList',
    'AVMDate',
]


class AVMData( object ):
    """
    Abstract AVM data class.  All other data classes inherit from AVMData.
    """
    def __init__(self, ns, path):
        """ """
        self.namespace = ns
        self.path = path
        
    def check_data(self, value):
        """
        All other data classes should define check_data() based on the type of data.
        
        :return: Object
        """
        return value
    
    def set_data(self, xmp_packet, value):
        """
        Injects data into an XMP packet.  Should be overridden if other
        requirements are necessary.
        
        :return: Boolean
        """
        value = self.check_data(value)
        if xmp_packet.set_property(self.namespace, self.path, str(value)):
            return True
        else:
            return False
    
    def get_data(self, xmp_packet):
        """
        Retrieves data from an XMP packet.  Should be overridden when appropriate.
        
        :return: Object.  Depending on the data type, different objects will be returned.  If the data does not exist
        in the xmp packet, then the None object is returned
        """
        if xmp_packet.get_property(self.namespace, self.path):
            return xmp_packet.get_property(self.namespace, self.path)
    
    def delete_data(self, xmp_packet):
        """
        Deletes data from an XMP packet.  Should be overridden when appropriate.
        """
        xmp_packet.delete_property(self.namespace, self.path)



class AVMString( AVMData ):
    """
    Data type for strings
    """
    def check_data(self, value):
        """
        Check that the data is a string, otherwise it raises a TypeError
        
        :return: String
        """
        if isinstance(value, str):
            return value
        else:
            raise TypeError, "Value is not a string"
    
    def set_data(self, xmp_packet, value):
        """
        Injects data into the XMP packet after imposing the appropriate check_data function 
        
        :return: Boolean
        """        
        value = self.check_data(value)
        if xmp_packet.set_property(self.namespace, self.path, value):
            return True

class AVMStringCV( AVMString ):
    """ """
    def __init__(self, ns, path, cv):
        self.namespace = ns
        self.path = path
        self.controlled_vocabulary = cv 
    
    def format_data(self, value):
        """
        :return: String
        """
        return value
    
    def check_cv(self, value):
        """
        If a controlled vocabulary is specified, this function checks the input value against the allowed values.
        AVMItemNotInControlledVocabularyError is raised if not in the controlled vocabulary
        
        :return: Boolean 
        """
        if value in self.controlled_vocabulary:
            return True
        else:
            raise AVMItemNotInControlledVocabularyError
        
    def check_data(self, value):
        """
        Check that the data is a string, formats the data appropriately using format_data()
        and calls check_cv()
        
        :return: String
        """
        
        if isinstance(value, str):
            value = self.format_data(value)
            
            if self.check_cv(value):
                return value
        else:
            raise TypeError, "Value is not a string"    

class AVMStringCVCapitalize( AVMStringCV ):
    def format_data(self, value):
        """
        Formats the data to be a capitalized string
        
        :return: String
        """
        return value.capitalize()

class AVMStringCVUpper( AVMStringCV ):
    def format_data(self, value):
        """
        Formats the data to be an upper case string
        
        :return: String:
        """
        return value.upper()

class AVMURL( AVMString ):
    """
    Data type for URLs
    """
    def check_data(self, value):
        """
        Checks data against a regular expression for a URL.  If the user leaves off 
        the protocol, then 'http://' is attached
        
        :return: String
        """
        
        if not isinstance(value, str):
            raise TypeError, "Value is not a string"
        
        if value and '://' not in value:
            value = 'http://%s' % value
        
        url_re = re.compile(
            r'^https?://' # http:// or https://
            r'(?:(?:[A-Z0-9-]+\.)+[A-Z]{2,6}|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|/\S+)$', re.IGNORECASE)
        
        if re.search(url_re, value):
            return value
        else:
            raise ValueError, "Enter a proper URL"

    def set_data(self, xmp_packet, value):
        """ 
        Calls check_data() then injects the data into the XMP packet.
        
        :return: Boolean
        """
        value = self.check_data(value)
        if xmp_packet.set_property(self.namespace, self.path, value):
            return True               



class AVMEmail( AVMString ):
    """
    Data type for email addresses
    
    :return: String
    """       
    def check_data(self, value):
        """
        Checks data against a regular expression for an email.  If value is not a string,
        a TypeError is raised.  If the value is not a proper email, then a ValueError is raised.
        
        :return: String
        """
        if not isinstance(value, str):
            raise TypeError, "Value is not a string" 
        
        email_re = re.compile(
            r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
            r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
            r')@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE
        )
        
        if re.search(email_re, value):
            return value
        else:
            raise ValueError, "Enter a proper email address"



class AVMLocalizedString( AVMString ):
    """
    Data type for localized strings.
    (i.e. fields contained in an alt tag, such as dc:description)
    """
    def __init__(self, ns, path, **kwargs):
        self.namespace = ns
        self.path = path
                
        if 'generic_lang' in kwargs:
            self.generic_lang = kwargs['generic_lang']
        else:
            self.generic_lang = 'x-default'
        
        if 'specific_lang' in kwargs:
            self.specific_lang = kwargs['specific_lang']
        else:
            self.specific_lang = 'x-default'
    
    def set_data(self, xmp_packet, value):
        """
        After calling check_data(), injects the data into the XMP packet.
        
        :return: Boolean
        """
        value = self.check_data(value)
        if xmp_packet.set_localized_text(self.namespace, self.path, self.generic_lang, self.specific_lang, value):
            return True
    
    def get_data(self, xmp_packet):
        """
        Retrieves localized data from an XMP packet.
        
        :return: String
        """
        return xmp_packet.get_localized_text(self.namespace, self.path, self.generic_lang, self.specific_lang)



class AVMFloat( AVMData ):
    """ 
    Data type for float fields
    """
    def check_data(self, value):
        """
        Checks that data is a float.  If an integer is passed, it is 
        typecasted to a float
        
        :return: Float
        """
        if isinstance(value, int):
            return float(value)
        if isinstance(value, float):
            return value
        else:
            raise TypeError, "Value is not a float"
    
    def get_data(self, xmp_packet):
        """
        Retrieves data from an XMP packet.  The value returned is a string, so
        typecasting is used to convert to float.
        
        :return: Float
        
        .. todo:: Return a float type without typecasting 
        """
        if xmp_packet.get_property(self.namespace, self.path):
            return float(xmp_packet.get_property(self.namespace, self.path))


class AVMUnorderedList( AVMData ):
    """
    Generic data type for unordered lists (i.e xmp bag arrays)
    """
    def __init__(self, ns, path, **kwargs):
        self.namespace = ns
        self.path = path
        
        # Optional keyword arguments
        if 'length' in kwargs:
            self.length = kwargs['length']
        else:
            self.length = False
            
        if 'strict_length' in kwargs:
            self.strict_length = kwargs['strict_length']
        else:
            self.strict_length = False
    
    def check_data(self, values):
        """
        For the unordered list, the Set data type is employed to remove arbitrary duplication of data.
        The function check_length() is called before checking the type of data.
        
        :return: Set
        """
        # Check length
        if self.check_length(values):
            pass
        
        if isinstance(values, set):
            return values
        else:
            raise TypeError, "Data needs to be a Python List"
        
    def check_length(self, values):
        """ 
        Checks the length of the data type.
        
        :return: Boolean 
        """
        if self.strict_length:
            if len(values) is self.length:
                return True
            else:
                raise AVMListLengthError, "Data is not of the correct length"
        elif self.length:
            if len(values) <= self.length:
                return True
            else:
                raise AVMListLengthError, "Data exceeds the maximum allowed length"
        else:
            return True

    def set_data(self, xmp_packet, values):
        """
        After checking length and type, inject the data to the XMP packet.
        
        :return: Boolean
        """
        values = self.check_data(values)
        
        # Delete previous data if strict length is required
        if self.strict_length:
            self.delete_data(xmp_packet)
        
        arr_options = {
            'prop_value_is_array': True,
        }
        
        for value in values:
            if xmp_packet.append_array_item(self.namespace, self.path, str(value), arr_options):
                pass
            else:
                return False
            
        return True

    def get_data(self, xmp_packet):
        """
        Extract data from XMP packet
        
        :return: Set if array items exist
        """
        num_items = xmp_packet.count_array_items(self.namespace, self.path)
        
        if num_items is 0:
            return None
        
        num_items += 1
        
        items = set()
        for i in range(1, num_items):
            item = str(xmp_packet.get_array_item(self.namespace, self.path, i).keys()[0])
            items.add(item)
            
        return items


class AVMUnorderedStringList( AVMUnorderedList, AVMString ):
    """
    Data type for an unordered set of strings
    """
    def check_data(self, values):
        """
        Check that the passed data is of type Set, and checks that the data
        inside of the set are strings.
        
        :return: Set
        """
        # Check that data is a list
        if not isinstance(values, set):
            raise TypeError, "Data needs to be a Python Set"
        
        # Check length
        if self.check_length(values):
            pass
        
        checked_data = set()
        # Check data type in list
        for value in values:
            if isinstance(value, str):
                checked_data.add(value)
            else:
                raise TypeError, "Data needs to be of type string"
        
        return checked_data


class AVMOrderedList( AVMUnorderedList ):
    """
    Data type for ordered lists (i.e. seq arrays)
    """    
    def set_data(self, xmp_packet, values):
        """ 
        Checks the data before injecting to the XMP packets.
        
        :return: Boolean
        """
        values = self.check_data(values)
        
        # Delete previous data if strict length is required
        if self.strict_length:
            self.delete_data(xmp_packet)
        
        arr_options= {
            'prop_value_is_array': True,
            'prop_array_is_ordered': True
        }
        
        for value in values:
            if xmp_packet.append_array_item(self.namespace, self.path, str(value), arr_options):
                pass
            else:
                return False
        
        return True


class AVMOrderedStringList( AVMOrderedList, AVMString ):
    """
    Data type for an ordered list comprising of strings 
    """
    def check_data(self, values):
        """
        Checks that data is a list, and checks that the elements are strings.
        
        :return: List
        """
        # Check that data is a list
        if not isinstance(values, list):
            raise TypeError, "Data needs to be a Python List"
        
        # Check length
        if self.check_length(values):
            pass
        
        checked_data = []
        
        # Check data type in list
        for value in values:
            if isinstance(value, str):
                checked_data.append(value)
            else:
                raise TypeError, "Data needs to be of type string"
        
        return checked_data
    
    def get_data(self, xmp_packet):
        """
        Extracts data from the XMP packet.
        
        :return: Set
        """
        num_items = xmp_packet.count_array_items(self.namespace, self.path)
        
        if num_items is 0:
            return None
        
        num_items += 1
        
        items = []
        for i in range(1, num_items):
            item = str(xmp_packet.get_array_item(self.namespace, self.path, i).keys()[0])
            items.append(item)
            
        return items

class AVMOrderedStringListCV( AVMOrderedStringList, AVMStringCVCapitalize):
    """
    Data type for an ordered string list constrained to a controlled vocabulary.
    """
    def __init__(self, ns, path, cv, **kwargs):
        self.namespace = ns
        self.path = path
        self.controlled_vocabulary = cv
        
        # Optional keyword arguments
        if 'length' in kwargs:
            self.length = kwargs['length']
        else:
            self.length = False
            
        if 'strict_length' in kwargs:
            self.strict_length = kwargs['strict_length']
        else:
            self.strict_length = False
            
    def check_data(self, values):
        """
        Checks that the data is a list, elements are strings, and strings are in the specified controlled vocabulary.
        
        :return: List
        """
        # Check that data is a list
        if not isinstance(values, list):
            raise TypeError, "Data needs to be a Python List"
        
        # Check length
        if self.check_length(values):
            pass
        
        checked_data = []
        
        # Check data type in list
        for value in values:
            if isinstance(value, str):
                value = self.format_data(value)
                
                if self.check_cv(value):
                    checked_data.append(value)
                else:
                    raise AVMItemNotInControlledVocabularyError
            else:
                raise TypeError, "Data needs to be of type string"
        
        return checked_data
        

class AVMOrderedFloatList( AVMOrderedList ):
    """
    Data type for an ordered list of floats.
    """    
    def check_data(self, values):
        """
        Checks that the data is of the correct type, length and elements
        are floats.  If integers are passed, then they become typecasted
        to floats.
        
        :return: Float
        """
        # Check type for list
        if not isinstance(values, list):
            raise TypeError, "Data needs to be a list"
        
        # Check length
        if self.check_length(values):
            pass
        
        checked_data = []
        # Check data type in list
        for value in values:
            if isinstance(value, int):
                value = float(value)
            if isinstance(value, float):
                checked_data.append(value)
            else:
                raise TypeError, "Data needs to be of type float"
        
        return checked_data

    
    def get_data(self, xmp_packet):
        """
        Retrieves data from XMP packet
        
        :return: List of floats
        """
        num_items = xmp_packet.count_array_items(self.namespace, self.path)
        
        if num_items is 0:
            return None
        
        items = []
        for i in range(1, num_items+1):
            try:
                item = float(xmp_packet.get_array_item(self.namespace, self.path, i).keys()[0])
            except:
                item = xmp_packet.get_array_item(self.namespace, self.path, i).keys()[0]
            items.append(item)
            
        return items


class AVMDate( AVMData ):
    """
    Data type for Dates
    
    :return: An AVM validated Python date.
    """
    def check_data(self, value):
        """
        Checks for a Python date
        """
        if isinstance(value, datetime.date):
            return value
        else:
            raise TypeError, "Date needs to be a Python date object"
        
    def get_data(self, xmp_packet):
        """
        Returns a Python date object
        """
        value =  xmp_packet.get_property(self.namespace, self.path)
        if value:
            time_value = time.strptime(value, "%Y-%m-%d")[0:3]
            date = datetime.date(time_value[0], time_value[1], time_value[2])
            return date
