import pkg_resources
useragents = pkg_resources.resource_filename(__name__, 'useragents')
apikeys=  pkg_resources.resource_filename(__name__, 'api-key.yaml')
ipranges= pkg_resources.resource_filename(__name__, 'ip-ranges.json')
resolvers=  pkg_resources.resource_filename(__name__, 'resolvers.txt')