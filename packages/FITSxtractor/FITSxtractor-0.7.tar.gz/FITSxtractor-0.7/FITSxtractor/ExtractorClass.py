#!/usr/bin/env python3
"""
This class will be used as a operating class for the XML metadata from FITS output files.

Because of the modularity as well as the sheer size of the whole project, I have decided to separate
the really extensive function and include every part into a class that can be expanded on.


@Author: ovanov
@date:   28.07.21
"""

from FITSClass import FITS_obj as fits
import xml.etree.cElementTree as ET


class Extraction:


    def __init__(self, file_path: str) -> None:

        self.fits_obj = fits() # initialise the object as a class attribute, in order to modify it calling the expandable methods
        self.root = ET.parse(file_path).getroot()
        self.ns = {'fits':'http://hul.harvard.edu/ois/xml/ns/fits/fits_output'} #ns to get faster to the ordered and labeled information in the FITS output 


    def extract_identification(self) -> None:
        """
        This function takes the initialized self.root object and works throught the sorted XML structure to 
        extract all needed identification information. The loop loops at least once, but sometimes FITS delivers
        multiple results. The for loop keeps track of that. Currently it tracks:
        - identification
            -- identity
                --- externalIdentifier
            -- mimetype
            -- format
        """
        
        for element in self.root.findall(f'fits:identification', self.ns):
            id = element.get('status')
            if id != None:
                self.fits_obj.status = id

            #extract "identity" info
            id_base = element.find('fits:identity',self.ns)
            id_format = id_base.get('format')
            mimetype = id_base.get('mimetype')

            # change the default values of the fits_obj
            self.fits_obj.identity_format.append(id_format)
            self.fits_obj.mimetype.append(mimetype)
            
            for e in element.findall('fits:identity', self.ns):
                ext = e.find('fits:externalIdentifier', self.ns)
                if ext != None: # if ext == None, the appended object is empty and therefore not represented in the DataFrame later
                    self.fits_obj.puid.append(ext.text)
            
        return self

    
    def extract_fileinfo(self) -> None:
        """
        This function takes the initialized self.root object and works throught the sorted XML structure to 
        extract all needed fileinfo information. The loop loops at least once, but sometimes FITS delivers
        multiple results. The for loop keeps track of that. Currently it tracks: 
        - fileinfo
            -- filepath
            -- md5checksum
            -- size
        """

        for element in self.root.findall(f'fits:fileinfo', self.ns):
            self.fits_obj.filepath = element.find(f'fits:filepath',self.ns).text
            self.fits_obj.size = element.find(f'fits:size',self.ns).text
            self.fits_obj.md5checksum = element.find(f'fits:md5checksum',self.ns).text
        
        return self


    def extract_filestatus(self) -> None:
        """
        This function takes the initialized self.root object and works throught the sorted XML structure to 
        extract all needed filestatus information. The loop loops at least once, but sometimes FITS delivers
        multiple results. The for loop keeps track of that. Currently it holds track of:
        - filestatus
            -- well-formed
            -- well-formed status
        """

        for element in self.root.findall(f'fits:filestatus', self.ns):
            info = element.find(f'fits:well-formed',self.ns)
            if info != None:
                self.fits_obj.well_formed = info.text
                self.fits_obj.well_formed_stat = info.get('status')

        return self