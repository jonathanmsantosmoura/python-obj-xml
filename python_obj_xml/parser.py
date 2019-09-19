import abc
from enum import Enum
from typing import List
from python_obj_xml.interface import XmlInterfaceMain, XmlInterface


class ParserObjXml:

    @classmethod
    def _get_tag(self, name: str, xml_alias):
        for obj in xml_alias:
            if name in obj:
                return obj[name]

        return None

    @classmethod
    def _get_list_object_tag(self, name, element_xmls):
        for obj in element_xmls:
            if name in obj and 'list_object_tag' in obj:
                return obj['list_object_tag']

        return None

    @classmethod
    def _isobject(self, obj) -> bool:
        if not isinstance(obj, (str, int, float, bool, list, dict, Enum)):
            return True

        return False

    @classmethod
    def _isprimitive(self, obj) -> bool:
        if isinstance(obj, (str, int, float, bool)):
            return True

        return False

    @classmethod
    def _islist(self, obj) -> bool:
        if type(obj) is list:
            return True

        return False

    @classmethod
    def _isenum(self, obj) -> bool:
        if isinstance(obj, Enum):
            return True

        return False

    @classmethod
    def _mount_tag(self, tag: str, value) -> str:
        return '<'+tag+'>'+str(value)+'<'+tag+'/>'

    @classmethod
    def _mount_tag_with_attrs(self, tag: str, value, attrs: list) -> str:
        attrs_str = None

        if attrs and len(attrs) > 0:
            attrs_str = ''
            for attr in attrs:
                for at in attr:
                    attrs_str += ' {0}="{1}"'.format(at, attr[at])

        tag_resp = None

        if attrs_str:
            tag_resp = '<'+tag+attrs_str+'>'+str(value)+'<'+tag+'/>'
        else:
            tag_resp = '<'+tag+'>'+str(value)+'<'+tag+'/>'

        return tag_resp

    @classmethod
    def _list_attr_xmls_by_obj_attr(self, name: str, obj) -> list:

        attr_xmls = obj.attr_xmls()

        if attr_xmls and len(attr_xmls) > 0:

            attr_xmls_process = []

            for attr_xml in attr_xmls:
                if name in attr_xml:
                    for attr in attr_xml[name]:
                        for at in attr:
                            if '@' in attr[at]:
                                try:
                                    attr_xmls_process.append(
                                        {at: getattr(obj, attr[at][1:])})
                                except AttributeError:
                                    attr_xmls_process.append({at: attr[at]})
                            else:
                                attr_xmls_process.append({at: attr[at]})

                    return attr_xmls_process
        return None

    @classmethod
    def _check_not_empty_obj(self, value) -> bool:
        return not value is None

    @classmethod
    def _check_not_empty_value(self, value) -> bool:
        return not value is None and str(value).strip() != ''

    def TAG_EMPTY_LIST_OBJECT_TAG():
        return '@@tag_empty_list_object_tag'

    @classmethod
    def parser(self, obj):
        if self._check_not_empty_obj(obj):
            element_xmls = obj.element_xmls()

            xml = ''
            xml_list_object_tag = ''

            for attr_name in obj.__dict__:
                attr_value = getattr(obj, attr_name)
                attr_xmls = self._list_attr_xmls_by_obj_attr(
                    attr_name, obj)

                tag = self.__get_tag(attr_name, element_xmls)
                tag_value = ''

                xml_list_object_tag = ''

                if tag and self._check_not_empty_value(attr_value):
                    if self._isprimitive(attr_value):
                        tag_value = attr_value

                        xml += self._mount_tag_with_attrs(tag,
                                                          tag_value, attr_xmls)
                    elif self._isenum(attr_value):
                        tag_value = attr_value.value

                        if tag_value:
                            xml += self._mount_tag_with_attrs(tag,
                                                              tag_value, attr_xmls)
                    elif self._isobject(attr_value):
                        tag_value = parser(attr_value)

                        if tag_value:
                            xml += self._mount_tag_with_attrs(tag,
                                                              tag_value, attr_xmls)
                    elif islist(attr_value):
                        list_object_tag = self._get_list_object_tag(
                            attr_name, element_xmls)
                        for value_obj in attr_value:
                            xml_list_object_tag += mount_tag_with_attrs(list_object_tag,
                                                                        parser(value_obj), attr_xmls)

                        if tag == __TAG_EMPTY_LIST_OBJECT_TAG():
                            xml += xml_list_object_tag
                        else:
                            xml += self._mount_tag_with_attrs(tag,
                                                              xml_list_object_tag, attr_xmls)

            if issubclass(obj.__class__, XmlInterfaceMain):
                tag_main = obj.tag_main()

                xml = self._mount_tag_with_attrs(
                    tag_main, xml, obj.attr_xmls_tag_main())

            return xml

        return None