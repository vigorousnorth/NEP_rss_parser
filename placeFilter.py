
# the class placeFilter creates a filter for a set of search graphs and single-expression names
# constructs a SearchGraph for each disambiguation_data object. Strings that are to be filtered
# as passed through the SearchGraphs and are checked against the single-expression names and 
# all matches are returned in a list

class placeFilter:
    
    filters = list()
    
    def __init__(self, filter_list):
        
        for i, p in enumerate(filter_list):
            if isinstance(p, disambiguation_data) == True:
                filter_list[i] = SearchGraph((p))
            elif isinstance(p, str) == False:
                raise ValueError("Non-structed data must be string.")           

        self.filters = filter_list


    def checkFilters(self, string):
        matches = dict()
        for p in self.filters:
            if isinstance(p, SearchGraph):
                p.count_matches(string)
                matches.update(p.compute_actual())
            else:
                if re.search(p, string) != None:
                    temp = re.findall(p, string)
                    matches.update({p: len(temp)})
        
        return matches