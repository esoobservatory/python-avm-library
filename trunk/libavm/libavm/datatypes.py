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
from dateutil import parser

from libxmp.core import _encode_as_utf8
from libavm.exceptions import *


__all__ = [
    'AVMString',
    'AVMStringCVCapitalize',
    'AVMStringCVUpper',
    'AVMURL',
    'AVMEmail',
    'AVMLocalizedString',
    'AVMFloat',
    'AVMUnorderedStringList',
    'AVMOrderedList',
    'AVMOrderedListCV',
    'AVMOrderedFloatList',
    'AVMDate',
    'AVMDateTimeList',
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
        Encoding of string into UTF-8 happens here.
        
        :return: String (UTF-8)
        """
        return _encode_as_utf8(value)
    
    def set_data(self, xmp_packet, value):
        """
        Injects data into an XMP packet.  Should be overridden if other
        requirements are necessary.
        
        :return: Boolean
        """
        if value is None:
            self.delete_data(xmp_packet)
            return True
        
        value = self.check_data(value)
        if xmp_packet.set_property(self.namespace, self.path, value):
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
    
    def to_string(self, xmp_packet):
        """
        Method to retrieve data from an XMP packet in a SQL-friendly string format.
        
        :return: String (UTF-8)
        """
        if self.get_data(xmp_packet):
            return self.get_data(xmp_packet)



class AVMString( AVMData ):
    """
    Data type for strings
    """
    def check_data(self, value):
        """
        Check that the data is a string or unicode, otherwise it raises a TypeError.
        
        :return: String (UTF-8)
        """
        if isinstance(value, str) or isinstance(value, unicode):
            return _encode_as_utf8(value)
        else:
            raise TypeError("Value is not a string or unicode.")


class AVMURL( AVMString ):
    """
    Data type for URLs.
    
    :return: String (UTF-8)
    """
    def check_data(self, value):
        """
        Checks the data is a string or unicode, and checks data
        against a regular expression for a URL.  If the user leaves
        off the protocol,then 'http://' is attached as a default.
        
        :return: String (UTF-8)
        """
        if not (isinstance(value, str) or isinstance(value, unicode)):
            raise TypeError("Value is not a string or unicode.")
        
        value =  _encode_as_utf8(value)
        
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
            raise ValueError("Enter a proper URL.")
        

class AVMEmail( AVMString ):
    """
    Data type for email addresses.
    
    :return: String (UTF-8)
    """       
    def check_data(self, value):
        """
        Checks data is a string or unicode, and checks against a regular expression
        for an email.  If value is not a string or unicode, a TypeError is raised.
        If the value is not a proper email, then a ValueError is raised.
        
        :return: String (UTF-8)
        """
        if not (isinstance(value, str) or isinstance(value, unicode)):
            raise TypeError("Value is not a string or unicode.") 
        
        value =  _encode_as_utf8(value)
        
        email_re = re.compile(
            r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
            r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
            r')@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE
        )
        
        if re.search(email_re, value):
            return value
        else:
            raise ValueError("Enter a proper email address.")



class AVMStringCV( AVMString ):
    """ """
    def __init__(self, ns, path, cv):
        self.controlled_vocabulary = cv
        super( AVMStringCV, self).__init__(ns, path) 
    
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
            return False
            
        
    def check_data(self, value):
        """
        Check that the data is a string or unicode, formats the data appropriately using format_data()
        and calls check_cv()
        
        :return: String (UTF-8)
        """
        
        if isinstance(value, str) or isinstance(value, unicode):
            value =  _encode_as_utf8(value)
            value = self.format_data(value)
            
            if self.check_cv(value):
                return value
            else:
                raise AVMItemNotInControlledVocabularyError("Item is not in the controlled vocabulary.")
        else:
            raise TypeError("Value is not a string or unicode.")    


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

class AVMLocalizedString( AVMString ):
    """
    Data type for localized strings.
    (i.e. fields contained in an alt tag, such as dc:description)
    """
    def __init__(self, ns, path, **kwargs):                
        if 'generic_lang' in kwargs:
            self.generic_lang = kwargs['generic_lang']
        else:
            self.generic_lang = 'x-default'
        
        if 'specific_lang' in kwargs:
            self.specific_lang = kwargs['specific_lang']
        else:
            self.specific_lang = 'x-default'
            
        super( AVMLocalizedString, self).__init__(ns, path)
    
    def set_data(self, xmp_packet, value):
        """
        After calling check_data(), injects the data into the XMP packet.
        
        :return: Boolean
        """
        if value is None:
            self.delete_data(xmp_packet)
            return True
        
        value = self.check_data(value)
        if xmp_packet.set_localized_text(self.namespace, self.path, self.generic_lang, self.specific_lang, value):
            return True
        else:
            return False
    
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
        Checks that data can be represented as a number.
        
        :return: String (UTF-8)
        """
        value = _encode_as_utf8(value)
        
        try:
            float(value)
        except:
            raise TypeError("Enter a value that can be represented as a number.")
        
        return value


class AVMDate( AVMData ):
    """
    Data type for Dates.
    """
    def check_data(self, value):
        """
        Checks for a Python date
        
        .. todo :: Implement a better way to determine class.
        """
        if value.__class__.__name__ == 'date':
            return value.isoformat()
        else:
            raise TypeError("Date needs to be a Python date object.")
        
    def get_data(self, xmp_packet):
        """
        .todo:: Something funny happens here...
        
        :return: Python date object
        """
        value =  xmp_packet.get_property(self.namespace, self.path)
        if value:
            try:
                time_value = time.strptime(value, "%Y-%m-%d")[0:3]
                date = datetime.date(time_value[0], time_value[1], time_value[2])
                return date
            except:
                return value

    def to_string(self, xmp_packet):
        """
        Method to retrieve data from an XMP packet in a SQL-friendly string format.
        
        :return: String (UTF-8)
        """
        if self.get_data(xmp_packet):
            data = self.get_data(xmp_packet)
            try:
                return data.isoformat()
            except:
                return data


class AVMUnorderedList( AVMData ):
    """
    Generic data type for lists (i.e xmp bag arrays)
    """
    def __init__(self, ns, path, **kwargs):
        # Optional keyword arguments
        if 'length' in kwargs:
            self.length = kwargs['length']
        else:
            self.length = False
            
        if 'strict_length' in kwargs:
            self.strict_length = kwargs['strict_length']
        else:
            self.strict_length = False
            
        super( AVMUnorderedList, self).__init__(ns, path)

    def check_length(self, values):
        """ 
        Checks the length of the Python List.
        
        :return: Boolean 
        """
        if self.strict_length:
            if len(values) is self.length:
                return True
            else:
                return False
        elif self.length:
            if len(values) <= self.length:
                return True
            else:
                return False
        else:
            return True

    def check_data(self, values):
        """
        Checks that the data type is a Python List.  Calls check_length() first.
        
        .. todo :: Redo this function.  Implement the dash functionality only for ordered lists.
        
        :return: List (UTF-8 elements)
        """
        # Check data type
        if not isinstance(values, list):
            raise TypeError("Data needs to be a Python List.")
        
        # Check length
        if not self.check_length(values):
            raise AVMListLengthError("Data is not the correct length.")
        
        # Convert to UTF-8
        checked_data = []
        length = 0
        
        for value in values:
            value = _encode_as_utf8(value)
            length += len(value)
            if value is "":
                value = "-"
            checked_data.append(value)
        
#        if length is 0:
#            raise AVMEmptyValueError("Make sure to enter data into the elements.") 
        return checked_data


    def set_data(self, xmp_packet, values):
        """
        After checking length and type, inject the data to the XMP packet.
        This function replaces the existing data; it is not meant to append values.
        
        :return: Boolean
        """
        if values is None:
            self.delete_data(xmp_packet)
            return True
        
        # Check data type and length
        values = self.check_data(values)
        
        # Delete the data for replacement
        self.delete_data(xmp_packet)
        
        arr_options = {
            'prop_value_is_array': True,
        }
        
        for value in values:
            if xmp_packet.append_array_item(self.namespace, self.path, value, arr_options):
                continue
            else:
                return False
            
        return True

    def get_data(self, xmp_packet):
        """
        Extract data from XMP packet
        
        :return: List (UTF-8 elements) or None if array does not have any elements
        """
        num_items = xmp_packet.count_array_items(self.namespace, self.path)
        
        if num_items is 0:
            return None
        
        num_items += 1
        
        items = []
        for i in range(1, num_items):
            item = _encode_as_utf8(xmp_packet.get_array_item(self.namespace, self.path, i).keys()[0])
            items.append(item)
            
        return items

    def to_string(self, xmp_packet):
        """
        Method to retrieve data from an XMP packet in a SQL-friendly string format.
        
        :return: String (UTF-8)
        """
        if self.get_data(xmp_packet):
            data = self.get_data(xmp_packet)
            try:
                return ';'.join(data)
            except:
                return data


class AVMUnorderedStringList( AVMUnorderedList ):
    """
    Data type for an unordered list of strings
    """
    def check_data(self, values):
        """
        Check that the passed data is a Python List, and checks that the elements
        are strings or unicode.
        
        :return: List of strings (UTF-8)
        """
        # Check that data is a list
        if not isinstance(values, list):
            raise TypeError("Data needs to be a Python List.")
        
        # Check length
        if not self.check_length(values):
            raise AVMListLengthError("Data is not the correct length.")
        
        checked_data = []
        # Check data type in list
        for value in values:
            if (isinstance(value, str) or isinstance(value, unicode)):
                value =  _encode_as_utf8(value)
                checked_data.append(value)
            else:
                raise TypeError("Elements of list need to be string or unicode.")
        
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
        if values is None:
            self.delete_data(xmp_packet)
            return True
        
        values = self.check_data(values)
        
        # Delete the data for replacement
        self.delete_data(xmp_packet)
        
        arr_options= {
            'prop_value_is_array': True,
            'prop_array_is_ordered': True
        }
        
        for value in values:
            if xmp_packet.append_array_item(self.namespace, self.path, value, arr_options):
                continue
            else:
                return False
        return True


class AVMOrderedListCV( AVMOrderedList, AVMStringCVCapitalize):
    """
    Data type for an ordered list constrained to a controlled vocabulary.
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
        
        :return: List of CV-Strings (UTF-8)
        """
        # Check that data is a list
        if not isinstance(values, list):
            raise TypeError("Data needs to be a Python List.")
        
        # Check length
        if not self.check_length(values):
            raise AVMListLengthError("List is not the correct length.")
        
        checked_data = []
        length = 0
        # Check data type in list
        for value in values:
            if (isinstance(value, str) or isinstance(value, unicode)):
                value =  _encode_as_utf8(value)
                value = self.format_data(value)
                
                if self.check_cv(value):
                    checked_data.append(value)
                else:
                    raise AVMItemNotInControlledVocabularyError("Item is not in the controlled vocabulary.")
            else:
                raise TypeError("Elements of list need to be string or unicode.")
        
        return checked_data
        

class AVMOrderedFloatList( AVMOrderedList ):
    """
    Data type for ordered lists of floats.
    """    
    def check_data(self, values):
        """
        Checks that the data is of the correct type, length and elements
        are strings able to be represented as floats.
        
        :return: List of strings (UTF-8)
        """
        # Check type for list
        if not isinstance(values, list):
            raise TypeError("Data needs to be a list.")
        
        # Check length
        if not self.check_length(values):
            raise AVMListLengthError("Data is not the correct length.")
        
        checked_data = []
        # Check data type in list
        for value in values:
            value = _encode_as_utf8(value)
            try:
                float(value)
                checked_data.append(value)
            except:
                raise TypeError("Enter a string that can be represented as a number.")
        return checked_data

        
class AVMDateTimeList( AVMOrderedList ):
    """ 
    Data type for lists composed of DateTime objects
    """
    def check_data(self, values):
        """
        Checks that the data passed is a Python List,
        and that the elements are Date or Datetime objects.
        
        :return: List of Datetime objects in ISO format (i.e. Strings encoded as UTF-8)
        """
        if not isinstance(values, list):
            raise TypeError("Data needs to be a list.")
        
        if not self.check_length(values):
            raise AVMListLengthError("Data is not the correct length.")
        
        checked_data = []
        # Check data type in list
        for value in values:
            if ( isinstance( value, datetime.date ) or isinstance( value, datetime.datetime ) ):
                value = _encode_as_utf8( value.isoformat() )
                checked_data.append( value )
            else:
                raise TypeError("Elements of the list need to be a Python Date or Datetime object.")                
        
        return checked_data
        
    def get_data(self, xmp_packet):
        """
        Extract data from XMP packet
        
        :return: List of Python Datetime elements or None if array does not have any elements
        """
        num_items = xmp_packet.count_array_items(self.namespace, self.path)
        
        if num_items is 0:
            return None
        
        num_items += 1
        
        items = []
        for i in range(1, num_items):
            item = parser.parse(xmp_packet.get_array_item(self.namespace, self.path, i).keys()[0])
            items.append(item)
            
        return items

    def to_string(self, xmp_packet):
        """
        Method to retrieve data from an XMP packet in a SQL-friendly string format.
        
        :return: String (UTF-8)
        """
        if self.get_data(xmp_packet):
            data = self.get_data(xmp_packet)
            try:
                tmp_data = []
                for item in data:
                    tmp_data.append(item.isoformat())
                return ';'.join(tmp_data)
            except:
                return data
