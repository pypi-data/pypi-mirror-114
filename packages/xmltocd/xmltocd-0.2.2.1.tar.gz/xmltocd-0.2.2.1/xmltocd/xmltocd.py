from collections import OrderedDict
from typing import Any, Dict, List, OrderedDict as Type_OrderedDict
from functools import reduce
from copy import deepcopy as _deepcopy

try:
    import xmltodict
except:
    raise ImportError('Unable to import xmltodict, please `pip install xmltodict==0.12.0`.')
else:
    if xmltodict.__version__ != '0.12.0':
        raise ImportError("xmltodict's version must be `0.12.0`.")

''' 2021-07-23 ~ '''
__author__ = 'jiyang'
__version__ = '0.0.1'
__license__ = 'MIT'

ATTR_PREFIX = '@'
CDATA_KEY = '#text'
REAL_CDATA_KEY = 'text_'

class DocTypeError(Exception): ...
class KeywordAttrsError(Exception): ...
class MoreNodesFound(Exception): ...
class NotNodeFound(Exception): ...
class TextNotFound(Exception): ...
class UpdateError(Exception): ...
class AddNodeError(Exception): ...

class TextType:
    STR = 0
    INT = 1
    FLOAT = 2
    DECIMAL = 3


class ChainDict(OrderedDict):

    def __init__(self):
        super(ChainDict, self).__init__()

    def __getattr__(self, name):
        if not name.startswith('_'):
            return self[name]
        return super(ChainDict, self).__getattr__(name)

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            self[name] = value
        else:
            super(ChainDict, self).__setattr__(name, value)


class ChainXML:

    xml = None

    def __init__(self
                 , doc: Type_OrderedDict
                 , attr_prefix: str = ATTR_PREFIX # default attribute prefix
                 , cdata_key: str = CDATA_KEY # default original text-flag
                 , real_cdata_key = REAL_CDATA_KEY # obj's default text-flag
                 ) -> None:

        if not isinstance(doc, OrderedDict) or 1 != len(doc):
            raise DocTypeError('`doc` type error.')

        self.doc = doc
        self.attr_prefix = attr_prefix
        self.cdata_key = cdata_key
        self.real_cdata_key = real_cdata_key

        '''self._attr_searcher:

            {
                'name=ok': {
                    'count': 0,
                    'nodes': [
                        id(node),
                        ...
                    ]
                }
            }
        '''
        self._attr_searcher = {}

        '''self._reverse_attr_name
            {
                ("name", "#name"): [
                    id(node),
                    ...
                ],
                ...
            }
        '''
        self._reverse_attr_name = {}

        '''self._reverse_text_node
            [
                id(node),
                ...
            ]
        '''
        self._reverse_text_node = []

        '''self._id_nodes
            {
                id(node): node, # node: ChainDict
                ...
            }
        '''
        self._id_nodes = {}

        '''self._id_tags
            {
                id(node): Tag, # Tag: str
                ...
            }
        '''
        self._id_tags = {}

        '''self._tag_ids
            {
                Tag: [
                    id(node),
                    ...
                ], # Tag: str
                ...
            }
        '''
        self._tag_ids = {}

        '''self._text_ids
            {
                Text: [
                    id(node),
                    ...
                ], # Text: str
                ...
            }
        '''
        self._text_ids = {}
        
        '''self._contrast_ids
            {
                id(sub_node): id(parent_node),
                ...
            }
        '''
        self._contrast_ids = {}

        self.xml = self._build_chain_by_recursion(self.doc)

    
    def _build_chain_by_BFS(self, doc_obj: Type_OrderedDict) -> ChainDict:
        '''generate chained struct by BFS. (future)
        '''

    def _build_chain_by_DFS(self, doc_obj: Type_OrderedDict) -> ChainDict:
        '''generate chained struct by DFS. (future)
        '''

    def registry_ids(self, sub_node: Any, node: ChainDict) -> None:
        self._contrast_ids[id(sub_node)] = id(node)

    def _build_chain_by_recursion(self, doc_obj: Any) -> ChainDict:
        '''generate chained struct by recursion.
        '''
        if not isinstance(doc_obj, dict): # dict used to filter original data, not ChainDict.
            if isinstance(doc_obj, (list, tuple, )): # safely change to BFS. (future)
                temp_list = []
                for line in doc_obj:
                    each = self._build_chain_by_recursion(line)
                    if not isinstance(each, str):
                        self.registry_ids(each, temp_list)
                        temp_list.append(each)

                        # record node-text and it's id(node).
                        if isinstance(each, ChainDict) and self.real_cdata_key in each:
                            if each[self.real_cdata_key] in self._text_ids:
                                self._text_ids[each[self.real_cdata_key]].append(id(each))
                            else:
                                self._text_ids[each[self.real_cdata_key]] = [id(each), ]
                    else:
                        temp_node = ChainDict()
                        temp_node[self.real_cdata_key] = each
                        temp_list.append(temp_node)

                        self._reverse_text_node.append(id(temp_node))
                        self._id_nodes[id(temp_node)] = temp_node
                        self.registry_ids(temp_node, temp_list)

                        # record node-text and it's id(node).
                        if each in self._text_ids:
                            self._text_ids[each].append(id(temp_node))
                        else:
                            self._text_ids[each] = [id(temp_node), ]
                return temp_list
            if doc_obj is None:
                t_node = ChainDict()
                self._id_nodes[id(t_node)] = t_node # record {id(node): node}
                return t_node # None is not allowed, must be an ChainDict object, 
            return doc_obj

        temp_xml = ChainDict()
        self._id_nodes[id(temp_xml)] = temp_xml # record {id(node): node}
        
        for k, v in doc_obj.items():
            _attr_name_new_old = None
            _text_ = False # flag, node has text content
            if self.attr_prefix == k[0]: # attribute
                _attr_name_new_old = (k[1:], k)
                k = k[1:]
            if self.cdata_key == k: # text
                k = self.real_cdata_key
                _text_ = True
            
            temp_node_content = self._build_chain_by_recursion(v)

            if not (_attr_name_new_old is not None or _text_) and isinstance(temp_node_content, str):
                temp_node = ChainDict()
                temp_node[self.real_cdata_key] = temp_node_content
                temp_xml[k] = temp_node

                self._reverse_text_node.append(id(temp_node))
                self._id_nodes[id(temp_node)] = temp_node
                self._id_tags[id(temp_node)] = k
                if k in self._tag_ids:
                    self._tag_ids[k].append(id(temp_xml[k]))
                else:
                    self._tag_ids[k] = [id(temp_xml[k]), ]
                self.registry_ids(temp_node, temp_xml)

                # record node-text and it's id(node).
                if temp_node_content in self._text_ids:
                    self._text_ids[temp_node_content].append(id(temp_node))
                else:
                    self._text_ids[temp_node_content] = [id(temp_node), ]
            else:
                temp_xml[k] = temp_node_content

            if _attr_name_new_old is not None: # record attribute.
                if _attr_name_new_old not in self._reverse_attr_name:
                    self._reverse_attr_name[_attr_name_new_old] = [id(temp_xml), ] # deal with attr specially(due to save).
                else:
                    self._reverse_attr_name[_attr_name_new_old].append(id(temp_xml))

                search_key = f'{k}={temp_xml[k]}'
                if search_key in self._attr_searcher:
                    self._attr_searcher[search_key]['nodes'].append(id(temp_xml))
                    self._attr_searcher[search_key]['count'] += 1
                else:
                    self._attr_searcher[search_key] = {
                        'count': 1,
                        'nodes': [id(temp_xml), ]
                    }

            if _text_: # record text node.
                self._reverse_text_node.append(id(temp_xml))
                continue

            if not isinstance(temp_xml[k], str): # record ChainDict or list.
                # ChainDict or list（problem: if node is `list` type, it's id(temp_xml[k]) is different from self._attr_searcher.）
                self._id_nodes[id(temp_xml[k])] = temp_xml[k] # record {id(node): node}
                self.registry_ids(temp_xml[k], temp_xml) # due to fast index（contain all）

                # if isinstance(temp_xml[k], ChainDict):
                #     self._id_tags[id(temp_xml[k])] = k # record tag, to execute delete operate. [only one]
                self._id_tags[id(temp_xml[k])] = k
                if k in self._tag_ids:
                    self._tag_ids[k].append(id(temp_xml[k]))
                else:
                    self._tag_ids[k] = [id(temp_xml[k]), ]

                # record node-text and it's id(node).
                if isinstance(temp_xml[k], ChainDict) and self.real_cdata_key in temp_xml[k]:
                    if temp_xml[k][self.real_cdata_key] in self._text_ids:
                        self._text_ids[temp_xml[k][self.real_cdata_key]].append(id(temp_xml[k]))
                    else:
                        self._text_ids[temp_xml[k][self.real_cdata_key]] = [id(temp_xml[k]), ]
            # else:
            #     # record node-text and it's id(node).
            #     if temp_xml[k] in self._text_ids:
            #         self._text_ids[temp_xml[k]].append(id(temp_xml))
            #     else:
            #         self._text_ids[temp_xml[k]] = [id(temp_xml), ]
                    
        return temp_xml

class ChainManager:

    def __init__(self, xml_data: str, *args, **kwargs) -> None:

        self.attr_prefix = kwargs['attr_prefix'] if 'attr_prefix' in kwargs else ATTR_PREFIX
        self.cdata_key = kwargs['cdata_key'] if 'cdata_key' in kwargs else CDATA_KEY
        self.real_cdata_key = kwargs['real_cdata_key'] if 'real_cdata_key' in kwargs else REAL_CDATA_KEY
        
        self.chainXML = ChainXML(
            xmltodict.parse(xml_data, attr_prefix=self.attr_prefix, cdata_key=self.cdata_key)
            , attr_prefix = self.attr_prefix
            , cdata_key = self.cdata_key
            , real_cdata_key = self.real_cdata_key
        )
        self.xml = self.chainXML.xml

        # belong to attribute, used to search quickly.
        self._attr_searcher = self.chainXML._attr_searcher
        self._searcher_keys = list(self._attr_searcher.keys())

        # add operations must update `_reverse_attr_name` and `_reverse_text_node`
        self._reverse_attr_name = self.chainXML._reverse_attr_name
        self._reverse_text_node = self.chainXML._reverse_text_node

        self._id_nodes = self.chainXML._id_nodes
        self._id_tags = self.chainXML._id_tags
        self._tag_ids = self.chainXML._tag_ids
        self._text_ids = self.chainXML._text_ids
        self._contrast_ids = self.chainXML._contrast_ids

    def __intersection(self, obj1, obj2):
        result = []
        for _1 in obj1:
            for _2 in obj2:
                if _1 == _2:
                    result.append(_1)
                    break
        return result

    def __find_intersection(self, datas: List[List[int]]) -> List[int]:
        
        return list(reduce(self.__intersection, datas))
    
    def find_node_by_attrs(self, *args, **kwargs) -> ChainDict:

        if len(kwargs) < 1:
            raise KeywordAttrsError('Keyword parameters must be passed in.')

        conditions = set([f'{k}={v}' for k, v in kwargs.items()])
        match_cons = []
        for sk in self._searcher_keys:
            if sk in conditions:
                match_cons.append(sk)

        len_match_cons = len(match_cons)
        if 0 == len_match_cons:
            raise NotNodeFound('Not found.')
        elif 1 == len_match_cons:
            obj = self._attr_searcher[match_cons[0]]
            if obj['count'] > 1:
                raise MoreNodesFound('Match to more than one result.')
            else:
                return self._id_nodes[obj['nodes'][0]]
        else:
            objs = self.__find_intersection([self._attr_searcher[t]['nodes'] for t in match_cons])
            if 0 == len(objs):
                raise NotNodeFound('Not found.')
            elif 1 == len(objs):
                return self._id_nodes[objs[0]]
            else:
                raise MoreNodesFound('Match to more than one result.')

    def find_nodes_by_attrs(self, *args, **kwargs) -> List[ChainDict]:

        if len(kwargs) < 1:
            raise KeywordAttrsError('Keyword parameters must be passed in.')

        conditions = set([f'{k}={v}' for k, v in kwargs.items()])
        match_cons = []
        for sk in self._searcher_keys:
            if sk in conditions:
                match_cons.append(sk)

        len_match_cons = len(match_cons)
        if 0 == len_match_cons:
            raise NotNodeFound('Not found.')
        elif 1 == len_match_cons:
            obj = self._attr_searcher[match_cons[0]]
            if obj['count'] > 1:
                return [self._id_nodes[_t] for _t in obj['nodes']]
            else:
                return self._id_nodes[obj['nodes'][0]]
        else:
            objs = self.__find_intersection([self._attr_searcher[t]['nodes'] for t in match_cons])
            if 0 == len(objs):
                raise NotNodeFound('Not found.')
            elif 1 == len(objs):
                return self._id_nodes[objs[0]]
            else:
                return [self._id_nodes[_t] for _t in objs]

    def find_nodes_by_indexs(self, indexs: List[int], *args, **kwargs) -> List[ChainDict]:
        nodes = self.find_nodes_by_attrs(*args, **kwargs)
        len_nodes = len(nodes)
        return_nodes = []
        for index in indexs:
            if 0 <= index < len_nodes:
                return_nodes.append(nodes[index])
        return return_nodes

    def find_text(self, node) -> str:
        
        if self.real_cdata_key in node:
            return node[self.real_cdata_key]
        elif isinstance(node, str):
            return node
        else:
            raise TextNotFound('Text not found.')

    def find_nodes_by_tag(self, tag: str) -> List[ChainDict]:
        return [self._id_nodes[_id] for _id in self._tag_ids[tag]]
    
    def find_nodes_by_tag_and_attrs(self, tag: str, *args, **kwargs) -> List[ChainDict]:

        if tag not in self._tag_ids:
            raise NotNodeFound('Not found.')

        conditions = set([f'{k}={v}' for k, v in kwargs.items()])
        match_cons = []
        for sk in self._searcher_keys:
            if sk in conditions:
                match_cons.append(sk)

        len_match_cons = len(match_cons)
        if 0 == len_match_cons:
            raise NotNodeFound('Not found.')
        else:
            tag_ids = []
            for _i in self._tag_ids[tag]: # if node type is list, must dig up all sub_node_ids.
                if isinstance(self._id_nodes[_i], list):
                    for k, v in self._contrast_ids.items():
                        if v == _i:
                            tag_ids.append(k) # get subnode id.
                else:
                    tag_ids.append(_i)

            tag_ids = list(set(tag_ids)) # id maybe repeat. be faster.

            objs = self.__find_intersection([self._attr_searcher[t]['nodes'] for t in match_cons] + [tag_ids])
            if 0 == len(objs):
                raise NotNodeFound('Not found.')
            elif 1 == len(objs):
                return self._id_nodes[objs[0]]
            else:
                return [self._id_nodes[_t] for _t in objs]


    def find_text_by_attrs(self, *args, text_type: int=TextType.STR, **kwargs) -> str:
        node = self.find_node_by_attrs(*args, **kwargs)
        text = self.find_text(node)
        if TextType.STR == text_type:
            return str(text)
        elif TextType.FLOAT == text_type:
            return float(text)
        elif TextType.INT == text_type:
            return int(text)
        else:
            return text

    def find_nodes(self
            , attr_limits: Dict[str, str] = None
            , text_limits: List[str] = None
            , tag: str = None
            , *args
            , **kwargs
        ):
        ...

    def registry_ids(self, sub_node: Any, node: ChainDict):
        self._contrast_ids[id(sub_node)] = id(node)
        
    def insert(self, obj, tag, attrs={}, text=''):
        if isinstance(obj, ChainDict):
            new_node = ChainDict()
            self.add_attrs(new_node, **attrs)
            self.update_text(new_node, text, first=True)
            insert_node = ChainDict()
            insert_node[tag] = new_node
            obj.update(insert_node)

            self._id_nodes[id(new_node)] = new_node
            self._id_nodes[id(insert_node)] = insert_node

            self._id_tags[id(insert_node)] = tag
            if tag in self._tag_ids:
                self._tag_ids[tag].append(id(insert_node))
            else:
                self._tag_ids[tag] = [id(insert_node), ]

            self.registry_ids(insert_node, obj)
            self.registry_ids(new_node, insert_node)
        else:
            raise AddNodeError('Add node error, obj must be `ChainDict` type.')

    # def _unbound_attrname(self, node: ChainDict):
    #     self._reverse_attr_name.values()

    # def _unbound_searcher(self, node: ChainDict):
    #     self._attr_searcher = self.chainXML._attr_searcher
    #     self._searcher_keys = list(self._attr_searcher.keys())

    def _unbound_text(self, node: ChainDict):

        while id(node) in self._reverse_text_node:
            self._reverse_text_node.remove(id(node))

    def _ids_find_parent(self, sub_id: int) -> int:

        if sub_id in self._contrast_ids:
            return self._contrast_ids[sub_id]
        else:
            if sub_id in self._contrast_ids.values():
                return sub_id
            else:
                raise IndexError('`sub_id` is not exists.')

    def pop_node_by_attrs(self, *args, **kwargs):
        obj = self.find_node_by_attrs(*args, **kwargs)
        return self.popitem(obj)

    def pop_nodes_by_attrs(self, *args, **kwargs) -> List[ChainDict]:
        objs = self.find_nodes_by_attrs(*args, **kwargs)
        del_nodes = []
        for obj in objs:
            del_nodes.append(self.popitem(obj))
        return del_nodes

    def popitem(self, obj: ChainDict) -> ChainDict:

        parent_id = self._ids_find_parent(id(obj))
        parent_obj = self._id_nodes[parent_id]

        if isinstance(parent_obj, ChainDict):
            # self._unbound_attrname(obj) # so hard.
            # self._unbound_searcher(obj)

            this_tag = self._id_tags[id(obj)] # key faster.
            self._unbound_text(obj)
            return parent_obj.pop(this_tag)

        elif isinstance(parent_obj, list):
            self._unbound_text(obj)
            bak = _deepcopy(obj)
            parent_obj.remove(obj)
            return bak
            
        else:
            raise AddNodeError("Add node error, obj must be `ChainDict` type, and obj's parent node-type must be `ChainDict` or `list`.")

    def register_attr(self, node, attr_name, value):
        temp_key = (attr_name, f'{self.attr_prefix}{attr_name}')
        if temp_key in self._reverse_attr_name:
            if id(node) not in self._reverse_attr_name[temp_key]:
                self._reverse_attr_name[temp_key].append(id(node))
        else:
            self._reverse_attr_name[temp_key] = [id(node), ]

        # update self._attr_searcher
        key = f'{attr_name}={value}'
        if key in self._attr_searcher:
            self._attr_searcher[key].append(id(node))
        else:
            self._attr_searcher[key] = [id(node), ]
        self._searcher_keys = list(self._attr_searcher.keys()) # synchronize

    def _register_text(self, node):
        self._reverse_text_node.append(id(node))

    def add_attrs(self, node, *args, **kwargs):
        for attr_name, value in args+tuple(kwargs.items()):
            if attr_name not in node:
                node[attr_name] = value
                self.register_attr(node, attr_name, value)

    def update_attr(self, obj: ChainDict, attr_name: str, new_value: Any):
        if obj is None:
            obj = ChainDict()
        if attr_name in obj:
            obj[attr_name] = new_value
        else:
            raise UpdateError('Unable to update this node, check whether the attribute exists.')

    def batch_update_attrs(self, obj, *args, **kwargs):
        if len(args) < 1 and len(kwargs) < 1:
            raise KeywordAttrsError('Parameters or keyword parameters must be passed in.')
        for attr_name, value in args+tuple(kwargs.items()):
            self.update_attr(obj, attr_name, value)
        
    def update_text(self, obj: ChainDict, new_text: Any, first=False):
        if obj is not None and self.real_cdata_key in obj:
            obj[self.real_cdata_key] = new_text
        else:
            if obj is None:
                raise UpdateError('Unable to update this node, None is found.')
            if first:
                obj[self.real_cdata_key] = new_text
                self._register_text(obj)
            else:
                raise UpdateError('Unable to update this node, check whether text exists.')

    def __revert_data(self, forward=True):
        for no, objs in self._reverse_attr_name.items():
            new_name, old_name = no
            for obj in objs:
                obj = self._id_nodes[obj]
                if forward:
                    obj[new_name] = obj[old_name]
                    del obj[old_name]
                else:
                    obj[old_name] = obj[new_name]
                    del obj[new_name]

        for node in self._reverse_text_node:
            node = self._id_nodes[node]
            if forward:
                node[self.real_cdata_key] = node[self.cdata_key]
                del node[self.cdata_key]
            else:
                node[self.cdata_key] = node[self.real_cdata_key]
                del node[self.real_cdata_key]

    def save(self, path: str = 'output.xml') -> None:
        self.__revert_data(forward=False)
        with open(path, 'w', encoding='utf-8') as fp:
            xmltodict.unparse(self.xml, fp)
        self.__revert_data()

def parse_string(
        xml_data: str
        , attr_prefix: str = ATTR_PREFIX
        , cdata_key: str = CDATA_KEY
        , real_cdata_key: str = REAL_CDATA_KEY
    ):
    return ChainManager(
        xml_data
        , attr_prefix = attr_prefix
        , cdata_key = cdata_key
        , real_cdata_key = real_cdata_key
    )

def parse(
        path: str
        , attr_prefix: str = ATTR_PREFIX
        , cdata_key: str = CDATA_KEY
        , real_cdata_key: str = REAL_CDATA_KEY
        , encoding: str = 'utf-8'
    ):
    with open(path, 'r', encoding=encoding) as fp:
        xml_data = fp.read()

    return parse_string(
        xml_data
        , attr_prefix = attr_prefix
        , cdata_key = cdata_key
        , real_cdata_key = real_cdata_key
    )

if __name__ == '__main__':
    ...
