def read_network(network):
    ''' interpret network  information'''
    for net_i in network:
        if not 'buildings' in net_i:
            net_i['buildings'] = None
        net_i['location'] = {}
        net_i['location']['latitude'] = net_i['latitude']
        net_i['location']['longitude'] = net_i['longitude']
        net_i['location']['time_zone'] = net_i['time_zone']
        if 'connections' in net_i:
            data = net_i['connections']
            test_con = True
            headers = list(data.keys())
            j = 1
            con = []
            limit = []
            eff = []
            while test_con:
                n = 'Connexn' + str(j) + ':node_name'
                if n in headers:
                    l = 'Connexn' + str(j) + ':line_limit'
                    e = 'Connexn' + str(j) + ':line_efficiency'
                    con.append(data[n])
                    limit.append(data[l])
                    eff.append(data[e])
                    del data[n]
                    del data[l]
                    del data[e]
                    j += 1
                else:
                    test_con = False
            if len(con) > 0:
                data['connections'] = {'node_name': con, 'line_limit': limit, 'line_efficiency': eff}
        else:
            net_i['connections'] ={}
            net_i['connections']['node_name'] = None
            net_i['connections']['line_limit'] = None
            net_i['connections']['line_efficiency'] = None