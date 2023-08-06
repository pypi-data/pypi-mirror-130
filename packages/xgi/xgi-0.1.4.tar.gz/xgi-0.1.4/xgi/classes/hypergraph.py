"""Base class for undirected hypergraphs.

The Hypergraph class allows any hashable object as a node
and can associate key/value attribute pairs with each undirected edge and node.

Multiedges and self-loops are allowed.
"""
from copy import deepcopy

from xgi.classes.reportviews import (
    NodeView,
    EdgeView,
    DegreeView,
    EdgeSizeView,
)
from xgi.exception import XGIError
import xgi.convert as convert
import numpy as np
from xgi.utils import XGICounter
import xgi

__all__ = ["Hypergraph"]


class Hypergraph:
    """A class to represent undirected hypergraphs."""

    node_dict_factory = dict
    node_attr_dict_factory = dict
    hyperedge_dict_factory = dict
    hyperedge_attr_dict_factory = dict
    hypergraph_attr_dict_factory = dict

    def __init__(self, incoming_hypergraph_data=None, **attr):
        """Initialize a hypergraph with hypergraph data and arbitrary hypergraph attributes.

        Parameters
        ----------
        incoming_hypergraph_data : input hypergraph data (optional, default: None)
            Data to initialize the hypergraph. If None (default), an empty
            hypergraph is created.
            The data can be in the following formats:
            * hyperedge list
            * hyperedge dictionary
            * 2-column Pandas dataframe (bipartite edges)
            * Scipy/Numpy incidence matrix
            * Hypergraph object.

        attr : keyword arguments, optional (default=no attributes)
            Attributes to add to the hypergraph as key=value pairs.

        See Also
        --------
        convert_to_hypergraph
        """
        self._edge_uid = XGICounter()

        self.hypergraph_attr_dict_factory = self.hypergraph_attr_dict_factory
        self.node_dict_factory = self.node_dict_factory
        self.node_attr_dict_factory = self.node_attr_dict_factory
        self.hyperedge_attr_dict_factory = self.hyperedge_attr_dict_factory

        self._hypergraph = (
            self.hypergraph_attr_dict_factory()
        )  # dictionary for graph attributes
        self._node = self.node_dict_factory()  # empty node attribute dict
        self._node_attr = self.node_attr_dict_factory()
        self._edge = self.hyperedge_dict_factory()
        self._edge_attr = self.hyperedge_attr_dict_factory()  # empty adjacency dict
        # attempt to load graph with data
        if incoming_hypergraph_data is not None:
            convert.convert_to_hypergraph(incoming_hypergraph_data, create_using=self)
        # load hypergraph attributes (must be after convert)
        self._hypergraph.update(attr)

    @property
    def name(self):
        """Get the string identifier of the hypergraph.

        This hypergraph attribute appears in the attribute dict H._hypergraph
        keyed by the string `"name"`. as well as an attribute (technically
        a property) `H.name`. This is entirely user controlled.

        Returns
        -------
        string
            The name of the hypergraph
        """
        return self._hypergraph.get("name", "")

    @name.setter
    def name(self, s):
        """Set the name of the hypergraph

        Parameters
        ----------
        s : string
            The desired name of the hypergraph.
        """
        self._hypergraph["name"] = s

    def __str__(self):
        """Returns a short summary of the hypergraph.

        Returns
        -------
        string
            Hypergraph information

        Examples
        --------
        >>> import xgi
        >>> H = xgi.Hypergraph(name="foo")
        >>> str(H)
        "Hypergraph named 'foo' with 0 nodes and 0 edges"

        """
        return "".join(
            [
                type(self).__name__,
                f" named {self.name!r}",
                f" with {self.number_of_nodes()} nodes and {self.number_of_edges()} hyperedges",
            ]
        )

    def __iter__(self):
        """Iterate over the nodes. Use: 'for n in H'.

        Returns
        -------
        iterator
            An iterator over all nodes in the hypergraph.
        """
        return iter(self._node)

    def __contains__(self, n):
        """Returns True if n is a node, False otherwise. Use: 'n in H'.

        Parameters
        ----------
        n : hashable
            node ID

        Returns
        -------
        bool
            Whether the node exists in the hypergraph.
        """
        try:
            return n in self._node
        except TypeError:
            return False

    def __len__(self):
        """Returns the number of nodes in the hypergraph. Use: 'len(H)'.

        Returns
        -------
        int
            The number of nodes in the hypergraph.

        See Also
        --------
        number_of_nodes: identical method
        order: identical method
        """
        return len(self._node)

    def __getitem__(self, n):
        """Returns a list of neighboring edge IDs of node n.  Use: 'H[n]'.

        Returns
        -------
        list
           A list of the edges of which the specified node is a part.

        Notes
        -----
        H[n] is the same as H.nodes[n]
        """
        return self._node[n]

    @property
    def shape(self):
        """Return the number of nodes and edges as a tuple.

        Returns
        -------
        tuple
           A tuple of the number of nodes and edges respectively.

        Examples
        --------
        >>> import xgi
        >>> hyperedge_list = [[1, 2], [2, 3, 4]]
        >>> H = xgi.Hypergraph(hyperedge_list)
        >>> H.shape
        (4, 2)
        """
        return len(self._node), len(self._edge)

    def neighbors(self, n):
        """Find the neighbors of a specified node.

        Parameters
        ----------
        n : node
            Node to find neighbors of.

        Returns
        -------
        set
            A set of the neighboring nodes

        Examples
        --------
        >>> import xgi
        >>> hyperedge_list = [[1, 2], [2, 3, 4]]
        >>> H = xgi.Hypergraph(hyperedge_list)
        >>> H.neighbors(1)
        {2}
        >>> H.neighbors(2)
        {1, 3, 4}
        """
        if n in self._node:
            return {i for e in self._node[n] for i in self._edge[e]}.difference({n})
        else:
            raise XGIError("Invalid node ID.")

    def add_node(self, node_for_adding, **attr):
        """Add a single node `node_for_adding` and update node attributes.

        Parameters
        ----------
        node_for_adding : node
            A node can be any hashable Python object except None.
        attr : keyword arguments, optional
            Set or change node attributes using key=value.

        See Also
        --------
        add_nodes_from
        """
        if node_for_adding not in self._node:
            if node_for_adding is None:
                raise ValueError("None cannot be a node")
            self._node[node_for_adding] = list()
            self._node_attr[node_for_adding] = self.node_attr_dict_factory()
        else:  # update attr even if node already exists
            self._node_attr[node_for_adding].update(attr)

    def add_nodes_from(self, nodes_for_adding, **attr):
        """Add multiple nodes.

        Parameters
        ----------
        nodes_for_adding : iterable container
            A container of nodes (list, dict, set, etc.).
            OR
            A container of (node, attribute dict) tuples.
            Node attributes are updated using the attribute dict.
        attr : keyword arguments, optional (default= no attributes)
            Update attributes for all nodes in nodes.
            Node attributes specified in nodes as a tuple take
            precedence over attributes specified via keyword arguments.

        See Also
        --------
        add_node
        """
        for n in nodes_for_adding:
            try:
                newnode = n not in self._node
                newdict = attr
            except TypeError:
                n, ndict = n
                newnode = n not in self._node
                newdict = attr.copy()
                newdict.update(ndict)
            if newnode:
                if n is None:
                    raise ValueError("None cannot be a node")
                self._node[n] = list()
                self._node_attr[n] = self.node_attr_dict_factory()
            self._node_attr[n].update(newdict)

    def remove_node(self, n):
        """Remove node n.

        Removes the node n and all adjacent hyperedges.
        Attempting to remove a non-existent node will raise an exception.

        Parameters
        ----------
        n : node
           A node in the hypergraph

        Raises
        ------
        XGIError
           If n is not in the hypergraph.

        See Also
        --------
        remove_nodes_from
        """
        try:
            edge_neighbors = self.nodes[n]  # list handles self-loops (allows mutation)
            del self._node[n]
            del self._node_attr[n]
        except KeyError as e:  # XGIError if n not in self
            raise XGIError(f"The node {n} is not in the graph.") from e
        for edge in edge_neighbors:
            self._edge[edge].remove(n)
            if len(self._edge[edge]) == 0:
                del self._edge[edge]
                del self._edge_attr[edge]

    def remove_nodes_from(self, nodes):
        """Remove multiple nodes.

        Parameters
        ----------
        nodes : iterable container
            A container of nodes (list, dict, set, etc.).  If a node
            in the container is not in the graph it is silently
            ignored.

        See Also
        --------
        remove_node
        """
        for n in nodes:
            try:
                edge_neighbors = self.nodes[
                    n
                ]  # list handles self-loops (allows mutation)
                del self._node[n]
                del self._node_attr[n]
                for edge in edge_neighbors:
                    self._edge[edge].remove(n)  # remove all edges n-u in graph
                    # delete empty edges
                    if len(self._edge[edge]) == 0:
                        del self._edge[edge]
                        del self._edge_attr[edge]
            except KeyError as e:
                pass

    @property
    def nodes(self):
        """A NodeView of the Hypergraph as H.nodes or H.nodes().

        Can be used as `H.nodes` for data lookup and for set-like operations.
        Can also be used as `H.nodes(data='color', default=None)` to return a
        NodeDataView which reports specific node data but no set operations.
        It presents a dict-like interface as well with `H.nodes.items()`
        iterating over `(node, edge_ids)` 2-tuples. In addition,
        a view `H.nodes.data('foo')` provides a dict-like interface to the
        `foo` attribute of each node. `H.nodes.data('foo', default=1)`
        provides a default for nodes that do not have attribute `foo`.

        Returns
        -------
        NodeView
            Allows set-like operations over the nodes as well as node
            attribute dict lookup and calling to get a NodeDataView.
            A NodeDataView iterates over `(n, data)` and has no set operations.
            A NodeView iterates over `n` and includes set operations.

            When called, if data is False, an iterator over nodes.
            Otherwise an iterator of 2-tuples (node, attribute value)
            where the attribute is specified in `data`.
            If data is True then the attribute becomes the
            entire data dictionary.

        Notes
        -----
        If your node data is not needed, it is simpler and equivalent
        to use the expression ``for n in H``, or ``list(H)``.
        """
        nodes = NodeView(self)
        # Lazy View creation: overload the (class) property on the instance
        # Then future H.nodes use the existing View
        # setattr doesn't work because attribute already exists
        self.__dict__["nodes"] = nodes
        return nodes

    def number_of_nodes(self):
        """Returns the number of nodes in the hypergraph.

        Returns
        -------
        int
            The number of nodes in the hypergraph.

        See Also
        --------
        order: identical method
        __len__: identical method

        Examples
        --------
        >>> import xgi
        >>> hyperedge_list = [[1, 2], [2, 3, 4]]
        >>> H = xgi.Hypergraph(hyperedge_list)
        >>> H.number_of_nodes()
        4
        """
        return len(self._node)

    def order(self):
        """Returns the number of nodes in the hypergraph.

        Returns
        -------
        int
            The number of nodes in the hypergraph.

        See Also
        --------
        number_of_nodes: identical method
        __len__: identical method

        Examples
        --------
        >>> import xgi
        >>> hyperedge_list = [[1, 2], [2, 3, 4]]
        >>> H = xgi.Hypergraph(hyperedge_list)
        >>> H.order()
        4
        """
        return len(self._node)

    def has_node(self, n):
        """Returns True if the hypergraph contains the node n.

        Identical to `n in H`

        Parameters
        ----------
        n : node

        Returns
        -------
        bool
            Whether the node exists in the hypergraph

        Examples
        --------
        >>> import xgi
        >>> hyperedge_list = [[1, 2], [2, 3, 4]]
        >>> H = xgi.Hypergraph(hyperedge_list)
        >>> H.has_node(1)
        True
        >>> H.has_node(0)
        False
        """
        try:
            return n in self._node
        except TypeError:
            return False

    def has_edge(self, edge):
        """Specifies whether an edge appears in the hypergraph as a different ID.

        Parameters
        ----------
        H : Hypergraph object
            The hypergraph of interest
        edge : list or set
            A container of hashables that specifies an edge

        Returns
        -------
        bool
           Whether or not the set appears as an edge in the hypergraph.

        Examples
        --------
        >>> import xgi
        >>> hyperedge_list = [[1, 2], [2, 3, 4]]
        >>> H = xgi.Hypergraph(hyperedge_list)
        >>> H.has_edge([1, 2])
        True
        >>> H.has_edge({1, 3})
        False
        """
        return set(edge) in [set(self.edges(e)) for e in self.edges]

    def add_edge(self, edge, **attr):
        """Add an edge to the hypergraph. The universal ID
        is automatically assigned to the edge.

        Edge attributes can be specified with keywords or by directly
        accessing the edge's attribute dictionary. See examples below.

        Parameters
        ----------
        edge : an container or iterable of hashables
            A list of node ids
        attr : keyword arguments, optional
            Edge data (or labels or objects) can be assigned using
            keyword arguments.

        See Also
        --------
        add_edges_from : add a collection of edges

        Notes
        -----
        Currently cannot add empty edges.
        """
        if edge:
            uid = self._edge_uid()
        else:
            raise XGIError("Cannot add an empty edge.")
        for node in edge:
            if node not in self._node:
                if node is None:
                    raise ValueError("None cannot be a node")
                self._node[node] = list()
                self._node_attr[node] = self.node_attr_dict_factory()
            self._node[node].append(uid)

        try:
            self._edge[uid] = list(edge)
            self._edge_attr[uid] = self.hyperedge_attr_dict_factory()
        except:
            raise XGIError("The edge cannot be cast to a list.")

        self._edge_attr[uid].update(attr)

    def add_edges_from(self, ebunch_to_add, **attr):
        """Add all the edges in ebunch_to_add.

        Parameters
        ----------
        ebunch_to_add : container of edges
            Each edge given in the container will be added to the
            graph. Each edge must be given as as a container of nodes
            or a container with the last entry as a dictionary.
        attr : keyword arguments, optional
            Edge data (or labels or objects) can be assigned using
            keyword arguments.

        See Also
        --------
        add_edge : add a single edge
        add_weighted_edges_from : convenient way to add weighted edges

        Notes
        -----
        Adding the same edge twice will create a multi-edge. Currently
        cannot add empty edges; the method skips over them.
        """
        for e in ebunch_to_add:

            try:
                if isinstance(e[-1], dict):
                    dd = e[-1]
                    e = e[:-1]
                else:
                    dd = {}
            except:
                pass

            if e:
                uid = self._edge_uid()

                for n in e:
                    if n not in self._node:
                        if n is None:
                            raise ValueError("None cannot be a node")
                        self._node[n] = list()
                        self._node_attr[n] = self.node_attr_dict_factory()
                    self._node[n].append(uid)

                try:
                    self._edge[uid] = list(e)
                    self._edge_attr[uid] = self.hyperedge_attr_dict_factory()
                except:
                    raise XGIError("The edge cannot be cast to a list.")

                self._edge_attr[uid].update(attr)
                self._edge_attr[uid].update(dd)

    def add_weighted_edges_from(self, ebunch_to_add, weight="weight", **attr):
        """Add weighted edges in `ebunch_to_add` with specified weight attr

        Parameters
        ----------
        ebunch_to_add : container of edges
            Each edge given in the list or container will be added
            to the graph. The edges must be given as containers.
        weight : string, optional (default= 'weight')
            The attribute name for the edge weights to be added.
        attr : keyword arguments, optional (default= no attributes)
            Edge attributes to add/update for all edges.

        See Also
        --------
        add_edge : add a single edge
        add_edges_from : add multiple edges

        Notes
        -----
        Adding the same edge twice creates a multiedge.
        """
        try:
            self.add_edges_from(
                ((edge[:-1], {weight: edge[-1]}) for edge in ebunch_to_add), **attr
            )
        except:
            XGIError("Empty or invalid edges specified.")

    def add_node_to_edge(self, edge, node):
        """Add a node to an edge.

        If the node or edge IDs do not exist, this method creates them.

        Parameters
        ----------
        edge : hashable
            edge ID
        node : hashable
            node ID
        """
        if edge not in self._edge:
            self._edge[edge] = [node]
            self._edge_attr[edge] = self.hyperedge_attr_dict_factory()
        else:
            self._edge[edge].append(node)

        if node not in self._node:
            self._node[node] = [edge]
            self._node_attr[node] = self.node_attr_dict_factory()
        else:
            self._node[node].append(edge)

    def remove_edge(self, id):
        """Remove an edge with a given id.

        Parameters
        ----------
        id : Hashable
            edge ID to remove

        Raises
        ------
        XGIError
            If no edge has that ID.

        See Also
        --------
        remove_edges_from : remove a collection of edges
        """
        try:
            for node in self.edges[id]:
                self._node[node].remove(id)
            del self._edge[id]
            del self._edge_attr[id]
        except KeyError as e:
            raise XGIError(f"Edge {id} is not in the graph") from e

    def remove_edges_from(self, ebunch):
        """Remove all edges specified in ebunch.

        Parameters
        ----------
        ebunch: list or container of hashables
            Each edge id given in the list or container will be removed
            from the hypergraph.

        See Also
        --------
        remove_edge : remove a single edge

        Notes
        -----
        Will fail silently if an edge in ebunch is not in the hypergraph.
        """
        for id in ebunch:
            try:
                for node in self.edges[id]:
                    self._node[node].remove(id)
                del self._edge[id]
                del self._edge_attr[id]
            except:
                pass

    def remove_node_from_edge(self, edge, node):
        """Remove a node from a given edge

        Parameters
        ----------
        edge : hashable
            The edge ID
        node : hashable
            The node ID

        Raises
        ------
        XGIError
            Raises an error if the user tries to delete nonexistent nodes or edges.

        Notes
        -----
        Removes empty edges as a result of removing nodes.
        """
        try:
            self._edge[edge].remove(node)
            self._node[node].remove(edge)
            if len(self._edge[edge]) == 0:
                del self._edge[edge]
                del self._edge_attr[edge]
        except KeyError as e:
            raise XGIError(f"Edge or node is not in the hypergraph") from e

    def update(self, edges=None, nodes=None):
        """Update the graph using nodes/edges/graphs as input.

        Like dict.update, this method takes two inputs:
        edges and nodes.It can take either edges or nodes.
        To specify only nodes the keyword `nodes` must be used.

        The collections of edges and nodes are treated similarly to
        the add_edges_from/add_nodes_from methods.

        Parameters
        ----------
        edges : collection of edges, or None
            The first parameter is a collection of edges and added to the hypergraph.
            If the first argument is None, no edges are added.
        nodes : collection of nodes, or None
            The second parameter is treated as a collection of nodes
            to be added to the hypergraph unless it is None.
            If `edges is None` and `nodes is None` an exception is raised.

        See Also
        --------
        add_edges_from: add multiple edges to a hypergraph
        add_nodes_from: add multiple nodes to a hypergraph
        """

        if edges is None and nodes is None:
            raise XGIError("update needs nodes or edges input")

        self.add_nodes_from(nodes)
        self.add_edges_from(edges)

    def has_edge_id(self, id):
        """Returns True if the edge id is in the hypergraph.

        This is the same as `v in H.edges` without KeyError exceptions.

        Parameters
        ----------
        id : hashable
            Edge id

        Returns
        -------
        bool
            True if edge is in the hypergraph, False otherwise.
        """
        try:
            return id in self._edge
        except KeyError:
            return False

    @property
    def edges(self):
        """An EdgeView of the Hyperraph as H.edges or H.edges().

        edges(self, nbunch=None, data=False, default=None)

        The EdgeView provides set-like operations on the edge IDs
        as well as edge attribute lookup. When called, it also provides
        an EdgeDataView object which allows control of access to edge
        attributes (but does not provide set-like operations).

        Parameters
        ----------
        e : hashable or None (default = None)
            The edge ID to access

        Returns
        -------
        edges : EdgeView
            A view of edges in the hypergraph.

        Notes
        -----
        Nodes in nbunch that are not in the hypergraph will be (quietly) ignored.
        """
        return EdgeView(self)

    def get_edge_data(self, id, default=None):
        """Returns the attribute dictionary associated with edge id.

        This is identical to `H._edge_attr[id]` except the default is returned
        instead of an exception if the edge doesn't exist.

        Parameters
        ----------
        id : hashable
            edge ID
        default:  any Python object (default=None)
            Value to return if the edge ID is not found.

        Returns
        -------
        edge_dict : dictionary
            The edge attribute dictionary.
        """
        try:
            return self.edges.data(id, default=default)
        except KeyError:
            return default

    @property
    def degree(self):
        """A NodeDegreeView for the Hypergraph as H.degree or H.degree().

        The degree is the number of edges adjacent to the node.
        The weighted node degree is the sum of the edge weights for
        edges incident to that node.

        This object provides an iterator for (node, degree) as well as
        lookup for the degree for a single node.

        Parameters
        ----------
        nbunch : single node, container, or all nodes (default= all nodes)
            The view will only report edges incident to these nodes.

        weight : string or None, optional (default=None)
           The name of an edge attribute that holds the numerical value used
           as a weight.  If None, then each edge has weight 1.
           The degree is the sum of the edge weights adjacent to the node.

        Returns
        -------
        If a single node is requested
        float or int
            Degree of the node

        OR if multiple nodes are requested
        DegreeView object
            The degrees of the hypergraph capable of iterating (node, degree) pairs
        """
        return DegreeView(self)

    @property
    def edge_size(self):
        """A EdgeSizeView for the Hypergraph as H.edge_size or H.edge_size().

        The edge degree is the number of nodes in that edge, or the edge size.
        The weighted edge degree is the sum of the node weights for
        nodes in that edge.

        This object provides an iterator for (edge, degree) as well as
        lookup for the degree for a single edge.

        Parameters
        ----------
        nbunch : single edge, container, or all edges (default= all edges)
            The view will only report sizes of these edges.

        weight : string or None, optional (default=None)
           The name of an node attribute that holds the numerical value used
           as a weight.  If None, then each node has weight 1.
           The size is the sum of the node weights adjacent to the edge.

        Returns
        -------
        If a single edge is requested
        int
            size of the edge.

        OR if multiple edges are requested
        EdgeSizeView object
            The sizes of the hypergraph edges capable of iterating (edge, size) pairs
        """
        return EdgeSizeView(self)

    def clear(self):
        """Remove all nodes and edges from the graph.

        This also removes the name, and all graph, node, and edge attributes.
        """
        self._node.clear()
        self._node_attr.clear()
        self._edge.clear()
        self._edge_attr.clear()
        self._hypergraph.clear()

    def clear_edges(self):
        """Remove all edges from the graph without altering nodes."""
        for node in self.nodes:
            self._node[node] = {}
        self._edge.clear()
        self._edge_attr.clear()

    def copy(self, as_view=False):
        """Returns a copy of the hypergraph.

        The copy method by default returns a deep copy of the hypergraph
        and attributes. Use the "as_view" flag to for a frozen copy of
        the hypergraph with references to the original

        If `as_view` is True then a view is returned instead of a copy.

        Parameters
        ----------
        as_view : bool, optional (default=False)
            If True, the returned hypergraph view provides a read-only view
            of the original hypergraph without actually copying any data.

        Returns
        -------
        H : Hypergraph
            A copy of the hypergraph.

        Notes
        -----
        All copies reproduce the hypergraph structure, but data attributes
        may be handled in different ways. There are two options that this
        method provides.

        Deepcopy -- A "deepcopy" copies the graph structure as well as
        all data attributes and any objects they might contain.
        The entire hypergraph object is new so that changes in the copy
        do not affect the original object. (see Python's copy.deepcopy)

        View -- Inspired by dict-views, graph-views act like read-only
        versions of the original graph, providing a copy of the original
        structure without requiring any memory for copying the information.

        See the Python copy module for more information on shallow
        and deep copies, https://docs.python.org/3/library/copy.html.
        """
        if as_view is True:
            return xgi.hypergraphviews.generic_hypergraph_view(self)
        H = self.__class__()
        H._hypergraph = deepcopy(self._hypergraph)
        H._node = deepcopy(self._node)
        H._node_attr = deepcopy(self._node_attr)
        H._edge = deepcopy(self._edge)
        H._edge_attr = deepcopy(self._edge_attr)
        return H

    def dual(self):
        """Returns the dual of the hypergraph (nodes become edges and
        edges become nodes).

        Returns
        -------
        Hypergraph object
            The dual of the hypergraph.

        Notes
        -----
        This method simply switches the nodes (with their attributes)
        with the edges (with their attributes) with a deep copy.

        """
        dual = self.__class__()
        dual._hypergraph = deepcopy(self._hypergraph)
        dual._node = deepcopy(self._edge)
        dual._node_attr = deepcopy(self._edge_attr)
        dual._edge = deepcopy(self._node)
        dual._edge_attr = deepcopy(self._node_attr)
        return dual

    def subhypergraph(self, nodes):
        """Returns a SubHypergraph view of the subhypergraph induced on `nodes`.

        The induced subhypergraph of the hypergraph contains the nodes in `nodes`
        and the edges that only contain those nodes.

        Parameters
        ----------
        nodes : list, iterable
            A container of nodes which will be iterated through once.

        Returns
        -------
        H : SubHypergraph View
            A subhypergraph view of the hypergraph. The hypergraph structure
            cannot be changed but node/edge attributes can and are shared with the
            original hypergraph.

        Notes
        -----
        The hypergraph, edge and node attributes are shared with the original
        hypergraph. Changes to the hypergraph structure is ruled out by the view,
        but changes to attributes are reflected in the original hypergraph.

        For an inplace reduction of a hypergraph to a subhypergraph you can remove nodes:
        H.remove_nodes_from([n for n in H if n not in set(nodes)])
        """
        induced_nodes = self.nbunch_iter(nodes)
        subhypergraph = xgi.hypergraphviews.subhypergraph_view
        return subhypergraph(self, induced_nodes, None)

    def edge_subhypergraph(self, edges):
        """Returns a SubHypergraph view of the subhypergraph with only the edges specified.

        The list of nodes is not affected, potentially leading to a disconnected hypergraph.

        Parameters
        ----------
        edges : list, iterable
            A container of edge ids which will be iterated through once.

        Returns
        -------
        H : SubHypergraph View
            A subhypergraph view of the hypergraph. The hypergraph structure
            cannot be changed but node/edge attributes can and are shared with the
            original hypergraph.

        Notes
        -----
        The hypergraph, edge and node attributes are shared with the original
        hypergraph. Changes to the hypergraph structure is ruled out by the view,
        but changes to attributes are reflected in the original hypergraph.

        For an inplace reduction of a hypergraph to a subhypergraph you can remove nodes:
        H.remove_edges_from([n for n in H if n not in set(nodes)])
        """
        subhypergraph = xgi.hypergraphviews.subhypergraph_view
        return subhypergraph(self, None, edges)

    def arbitrary_subhypergraph(self, nodes, edges):
        """Returns a SubHypergraph view of the subhypergraph with specified
        nodes and edges.

        This subhypergraph contains the list of nodes induced by the edges
        as well as additional nodes specified.

        Parameters
        ----------
        nodes : list, iterable
            A container of nodes which will be iterated through once.

        edges : list, iterable
            A container of edge ids which will be iterated through once.

        Returns
        -------
        H : SubHypergraph View
            A subhypergraph view of the hypergraph. The hypergraph structure
            cannot be changed but node/edge attributes can and are shared with the
            original hypergraph.

        Notes
        -----
        The hypergraph, edge and node attributes are shared with the original
        hypergraph. Changes to the hypergraph structure is ruled out by the view,
        but changes to attributes are reflected in the original hypergraph.
        """
        subhypergraph = xgi.hypergraphviews.subhypergraph_view
        return subhypergraph(self, nodes, edges)

    def number_of_edges(self):
        """Returns the number of edges in the hypergraph.

        Returns
        -------
        int
            The number of edges in the hypergraph.

        See Also
        --------
        number_of_nodes : returns the number of nodes in the hypergraph

        Examples
        --------
        >>> import xgi
        >>> hyperedge_list = [[1, 2], [2, 3, 4]]
        >>> H = xgi.Hypergraph(hyperedge_list)
        >>> H.number_of_edges()
        2
        """
        return len(self._edge)

    def nbunch_iter(self, nbunch=None):
        """Returns an iterator over nodes contained in nbunch that are
        also in the hypergraph.

        The nodes in nbunch are checked for membership in the hypergraph
        and if not are silently ignored.

        Parameters
        ----------
        nbunch : single node, container, or all nodes (default= all nodes)
            The view will only report edges incident to these nodes.

        Returns
        -------
        niter : iterator
            An iterator over nodes in nbunch that are also in the hypergraph.
            If nbunch is None, iterate over all nodes in the hypergraph.

        Raises
        ------
        XGIError
            If nbunch is not a node or sequence of nodes.
            If a node in nbunch is not hashable.

        See Also
        --------
        Hypergraph.__iter__

        Notes
        -----
        When nbunch is an iterator, the returned iterator yields values
        directly from nbunch, becoming exhausted when nbunch is exhausted.

        To test whether nbunch is a single node, one can use
        "if nbunch in self:", even after processing with this routine.

        If nbunch is not a node or a (possibly empty) sequence/iterator
        or None, a :exc:`XGIError` is raised.  Also, if any object in
        nbunch is not hashable, a :exc:`XGIError` is raised.
        """
        if nbunch is None:  # include all nodes via iterator
            bunch = iter(self._node)
        elif nbunch in self:  # if nbunch is a single node
            bunch = iter([nbunch])
        else:  # if nbunch is a sequence of nodes

            def bunch_iter(nlist, nodes):
                try:
                    for n in nlist:
                        if n in nodes:
                            yield n
                except TypeError as e:
                    exc, message = e, e.args[0]
                    # capture error for non-sequence/iterator nbunch.
                    if "iter" in message:
                        exc = XGIError("nbunch is not a node or a sequence of nodes.")
                    # capture error for unhashable node.
                    if "hashable" in message:
                        exc = XGIError(
                            f"Node {n} in sequence nbunch is not a valid node."
                        )
                    raise exc

            bunch = bunch_iter(nbunch, self._node)
        return bunch
