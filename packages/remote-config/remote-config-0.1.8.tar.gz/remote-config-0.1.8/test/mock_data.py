def cluster_list(self, path):
    return [u'general/clusters/cluster-google-merchant']

def cluster_data(self, key):
    return {u'ids': [123, 456]}

def feature_list(self, path):
    return [u'general/feature-toggle/google-merchant']

def feature_data(self, key):
    return {
        u'default': False,
        u'clusters': [u'general/clusters/cluster-google-merchant'],
        u'enable': True}

def global_list(self, path):
    return [
        u'general/globals/object-global',
        u'general/globals/string-global',
        u'general/globals/number-global',
        u'general/globals/boolean-global',
    ]

def global_data(self, key):
    data = {
        'general/globals/object-global': {'some': 'random', 'test': 'values'},
        'general/globals/string-global': 'some random string',
        'general/globals/number-global': 1234,
        'general/globals/boolean-global': True,
    }
    return data[key]

def invalid_feature_data(self, key):
    return {
        u'clusters': [u'general/clusters/cluster-google-merchant'],
        u'enable': True}

def invalid_cluster_data(self, key):
    return {u'ids': ["123", 456]}

def invalid_global_data(self, key):
    return None

def cache_init_data(self, key):
    if 'cluster' in key :
        return cluster_data(self, key)
    else:
        return feature_data(self, key)

def cache_init_list(self, path):
    if path == self.toggle_path:
        return feature_list(self, path)
    else:
        return cluster_list(self, path)

def cache_update_cluster_data(self, key):
    if 'cluster' in key :
        return {u'ids': [124]}
    else:
        return feature_data(self, key)

def cache_update_feature_cluster_data(self, key):
    if 'cluster' in key :
        return {u'ids': [124]}
    else:
       return {u'default': False, u'clusters': [u'general/clusters/cluster-google-merchant'], u'enable': False}