


data_struct = {'root':'Portland', 
               'children': ['South Portland', 'West Portland', 'Portland Heights', 'South Portland Heights', 'South Portland Heights Park', 'West Portland Heights', 'South Portland Heights Grove'],
               'relations': [('Portland', 'South Portland'),
                         ('Portland', 'West Portland'),
                         ('Portland','Portland Heights'),
                         ('West Portland', 'West Portland Heights'),
                         ('Portland Heights','West Portland Heights'),
                         ('Portland Heights','South Portland Heights'),
                         ('South Portland','South Portland Heights'),
                         ('South Portland Heights','South Portland Heights Park'),
                         ('South Portland Heights', 'South Portland Heights Grove')]}



data_struct1 = {'root':'Crown Heights',
               'children' : ['Crown Heights Plaza'],
               'relations': [('Crown Heights', 'Crown Heights Plaza')]}
        



singleton = 'New Haven'

places = [data_struct, data_struct1, singleton]



class placeFilter:
    
    filters = []
    
    def __init__(self, filter_list):
        
        for i, p in enumerate(filter_list):
            if isinstance(p, dict) == True:
                filter_list[i] = SearchGraph(disambiguation_data(p))
            else isinstance(p, str) == False:
                raise ValueError("Non-structed data must be string.")           

        self.filters = filter_list


    def checkFilters(self, string):
        matches = []
        for p in self.filters:
            if isinstance(p, SearchGraph):
                p.count_matches(string)
                matches.extend(p.find_matches())
            else:
                if re.search(p, string) != None:
                    matches.append(p)
        
        return matches
        
        


temp = []

for p in places:
    if isinstance(p, SearchGraph):
        p.count_matches(string)
        temp.extend(p.find_matches())
    else:
        if re.search(p, string) != None:
            temp.append(p)



data = disambiguation_data(data_struct)

G = SearchGraph(data)
G.count_matches(string)

G.compute_actual()
G.print_data()

G.outneighbor_path('Portland')

G.find_matches()
G.outneighbor_matches('Portland')

V = [data_struct['root']]
V.extend(data_struct['children'])

E = data_struct['edges']



string = 'Welcome to West Portland Heights! A suburb of South Portland, which is next to South Portland Heights but not to be confused with South Portland Heights Grove, which are all part of Portland.'


    
    
G.bfs('Portland', string)
G.reset_visits()

temp = G.name_bfs('Portland')
print(temp)



