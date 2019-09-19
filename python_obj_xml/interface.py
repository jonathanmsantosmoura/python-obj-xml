import abc


class XmlInterfaceMain(abc.ABC):

    @abc.abstractmethod
    def tag_main(self) -> str:
        pass

    @abc.abstractmethod
    def element_xmls(self) -> list:
        pass

    @abc.abstractmethod
    def attr_xmls_tag_main(self) -> list:
        pass

    @abc.abstractmethod
    def attr_xmls(self) -> list:
        pass


class XmlInterface(abc.ABC):

    @abc.abstractmethod
    def element_xmls(self) -> list:
        pass

    @abc.abstractmethod
    def attr_xmls(self) -> list:
        pass