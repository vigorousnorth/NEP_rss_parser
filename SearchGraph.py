
# class for storing data structure that defines the disambiguation search graph
class disambiguation_data:
    
    DATA = dict()
      
    def __init__(self, data_dict):
        
        def _checkIntegrity(data_struct):
            # check dictionary names
            d_names = list(data_struct.keys())
            d_names.sort()
            if d_names != ['children','relations','root']:
                raise KeyError("One or more keys is missing. 'root','children', and 'relations' must be present.")
            
            # check that root is contained in all children
            for c in data_struct['children']:
                if re.search(data_struct['root'], c) == None or len(c) < len(data_struct['root']):
                    raise ValueError("Warning! Children must contain root!")
        
        _checkIntegrity(data_dict)
        self.DATA = data_dict
        
    def get_data(self):
        return self.DATA
        
    def get_root(self):
        return self.DATA['root']
    
    def get_relations(self):
        return self.DATA['relations']
    
    def get_children(self):
        return self.DATA['children']


# class for nodes of search graph
class Vertex:
    
    def __init__(self, n, is_root):
        self.name = n
        self.neighbors = list()
        self.visited = False
        self.actual = 0
        self.matches = 0
        self.distance_from_root = int()
        self.is_root = is_root
    
    def add_neighbor(self, v):
        if v not in self.neighbors:
            self.neighbors.append(v)
            self.neighbors.sort()
            

class SearchGraph:
    
    # initialize global variables
    V = {}
    count_stage = False
    root_name = str()
    
    
    def __init__(self, disamb_data):
        
        ##### functions for initializing vertex and edge sets #################
        
        def _add_vertex(vertex):
            if isinstance(vertex, Vertex):     # check to make sure vertex object
                if vertex.name not in self.V:      # add vertex object if not in vertex name not in V
                    self.V[vertex.name] = vertex      # add vertex object to V
                    return True
                else:
                    return False
            else:
                return False
        
        def _add_edges(u, v):
            if u in self.V and v in self.V:          # check that vertex names are in V
                
                for vertex_name, vertex in self.V.items():  # iterate through vertex objects in V
                    if vertex_name == u:                    # if name matches u, add v to vertex object's neighbors
                        vertex.add_neighbor(v)
                    if vertex_name == v:                    # if name matches v, add u to vertex object's neighbors
                        vertex.add_neighbor(u)
                        
                return True
            else:
                return False
        
        #######################################################################
        
        # check input is of type disambiguation_data
        if isinstance(disamb_data, disambiguation_data) == False:
            raise ValueError("SearchGraph must be initialized with disambiguation_data object.")
        
        #### create nodes of search graph ####
        # add root node
        self.root_name = disamb_data.get_root()
        _add_vertex(Vertex(disamb_data.get_root(), True))
        # add child nodes
        for c in disamb_data.get_children():
            _add_vertex(Vertex(c, False))
        
        #### create edges of search graph ####
        for e in disamb_data.get_relations():
            _add_edges(e[0],e[1])
        
        

    ################################
    #### printing functions ########
    
    def get_node(self, v):
        return self.V[v]
    
    def print_matches(self):
        for v in self.V:
            node_v = self.V[v]
            print(node_v.name + ": " + str(node_v.matches))
            
    
    def print_actual(self):
        for v in self.V:
            node_v = self.V[v]
            print(node_v.name + ": " + str(node_v.actual))
    
    def print_data(self):
        for v in self.V:
            node_v = self.V[v]
            print(node_v.name + ". Total: " + str(node_v.matches) + ", Actual Matches: " + str(node_v.actual))
    
    def print_graph(self):
        for v in self.V:
            node_v = self.V[v]
            print("Node: " + v + ", Neighbors: " + str(node_v.neighbors))
            
    def get_root(self):
        for v in self.V:
            if self.V[v].is_root == True:
                return self.V[v].name
        

    def inneighbors(self, v):
        d = self.V[v].distance_from_root
        nbhd = [self.V[u] for u in self.V[v].neighbors]
        nbhd = list(filter(lambda n: n.distance_from_root < d, nbhd))
        nbhd = list(map(lambda n: n.name, nbhd))
        return nbhd
    
    def outneighbors(self, v):
        d = self.V[v].distance_from_root
        nbhd = [self.V[u] for u in self.V[v].neighbors]
        nbhd = list(filter(lambda n: n.distance_from_root > d, nbhd))
        nbhd = list(map(lambda n: n.name, nbhd))
        return nbhd
    
    
    ################### search functions ######################################
    
    def compute_actual(self):
        
        ########################### functions #################################
        # compute the sum of matches of out-neighbors
        # takes name of vertex v
        def _outneighbor_matches(v):
            
            # get out-neighbors of v
            d = self.V[v].distance_from_root
            nbhd = [self.V[u] for u in self.V[v].neighbors]
            nbhd = list(filter(lambda n: n.distance_from_root > d, nbhd))
            
            # total up matches of out-neighbors
            sums = []
            for n in nbhd:
                sums.append(n.matches)
            
            return sum(sums)
        #######################################################################
        
        
        # check that count_matches() has been run first and reset visit markers for new run
        if self.count_stage == False:
            raise ValueError("Must run count_matches() stage first!")
        else:
            for v in self.V:
                self.V[v].visited = False
                self.V[v].actual = 0
            
        root_node = self.V[self.root_name]
        
        # verify root node
        if root_node.distance_from_root > 0 or root_node.is_root == False:
            raise ValueError
        else:
            root_node.visited = True
            
        # initialize list
        actuals = list()
        queue = list()
        
        ### begin search run ###

        for v in root_node.neighbors:
            queue.append(v)
            self.V[v].actual = self.V[v].matches - _outneighbor_matches(v)
            actuals.append(self.V[v].actual)
            
        while len(queue) > 0:
            u = queue.pop(0)
            node_u = self.V[u]
            node_u.visited = True
            
            for v in node_u.neighbors:
                node_v = self.V[v]
                
                if node_v.visited == False:
                    queue.append(v)
                    node_v.visited = True
                    node_v.actual = node_v.matches - _outneighbor_matches(v)
                    actuals.append(node_v.actual)
        
        # compute actual matches of root node as number of matches - actual matches of children
        if sum(actuals) < root_node.matches:
            root_node.actual = root_node.matches - sum(actuals)
        
        # return actual matches
        actual_matches = dict()
        for v in self.V:
            if self.V[v].actual > 0:
                actual_matches[v] = self.V[v].actual
                
        return actual_matches
        
        
    
#    def find_matches(self):
#                
#        if self.count_stage == False:
#            raise ValueError("Must run count_matches() stage first!")
#        else:
#            for v in self.V:
#                self.V[v].visited = False
#        
#        def _active_outdegree(v):
#            d = self.V[v].distance_from_root
#            
#            nbhd = [self.V[u] for u in self.V[v].neighbors]
#            nbhd = list(filter(lambda n: n.distance_from_root > d, nbhd))
#            temp = list(filter(lambda x: x.matches > 0, nbhd))
#            
#            return len(temp)
#
#        
#        def _outneighbor_matches(v):
#            d = self.V[v].distance_from_root
#            nbhd = [self.V[u] for u in self.V[v].neighbors]
#            nbhd = list(filter(lambda n: n.distance_from_root > d, nbhd))
#            temp = list(filter(lambda x: x.matches > 0, nbhd))
#            
#            sums = []
#            for n in temp:
#                sums.append(n.matches)
#            
#            return sum(sums)
#            
#            
#            
#        
#        root_node = self.V[self.root_name]
#        # check that root node has distance 0
#        if root_node.distance_from_root > 0 or root_node.is_root == False:
#            raise ValueError
#            
#        queue = list()
#        name_list = list()
#        root_node.visited = True
#        
#        # check root node outdegree
#        if _outneighbor_matches(root_node.name) < root_node.matches:
#            name_list.append(root_node.name)
#            
#        
#        for v in root_node.neighbors:
#            queue.append(v)
#            if _outneighbor_matches(v) < self.V[v].matches:
#                name_list.append(v)
#            
#        while len(queue) > 0:
#            u = queue.pop(0)
#            node_u = self.V[u]
#            node_u.visited = True
#            
#            for v in node_u.neighbors:
#                node_v = self.V[v]
#                
#                if node_v.visited == False:
#                    queue.append(v)
#                    node_v.visited = True
#                    if _outneighbor_matches(v) < node_v.matches:
#                        name_list.append(v)
#        
#        return name_list


    # uses BFS to run through search graph and count number of matches in a given string
    
    def count_matches(self, string):
        
        ############################## functions ##############################
        
        # returns number of matches of expression in a string
        def _match(rex, string):
            temp = re.findall(rex, string)
            if temp != None:
                return len(temp)
            else:
                return 0
               
        #######################################################################
        
        ### initialize search ###
        # reset SearchGraph variables from any previous runs
        for v in self.V:
            self.V[v].visited = False
            self.V[v].matches = 0
            
        # initialize queue and root node
        root_node = self.V[self.root_name]
        root_node.distance_from_root = 0
        root_node.visited = True
        root_node.matches = _match(root_node.name, string)
        queue = list()
        
        
        # initialize BFS with root's neighbors
        for v in root_node.neighbors:
            queue.append(v)
            self.V[v].distance_from_root = 1
            self.V[v].matches = _match(v, string)
               
        ### continue BFS ###
        while len(queue) > 0:
            u = queue.pop(0)
            node_u = self.V[u]
            node_u.visited = True
            
            for v in node_u.neighbors:
                node_v = self.V[v]
                
                if node_v.visited == False:
                    queue.append(v)
                    node_v.visited = True
                    node_v.matches = _match(v, string)
                    node_v.distance_from_root = node_u.distance_from_root + 1
                    
#                    if node_v.distance_from_root > node_u.distance_from_root:
#                        node_v.distance_from_root = node_u.distance_from_root + 1
        
        self.count_stage = True
            
            
            
         