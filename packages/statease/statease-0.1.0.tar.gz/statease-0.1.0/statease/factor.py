class Factor:
    """The Factor class holds information about an individual Factor in
    Stat-Ease 360. Instances of this class are typically created by
    :func:`statease.client.SEClient.get_factor`

    :ivar str name: the name of the factor
    :ivar str units: the units of the factor
    :ivar list values: the values of the factor, in run order
    """

    def __init__(self, client, name):
        self.client = client
        self.name = name

        result = self.client.send_payload({
            "method": "GET",
            "uri": "design/factor/" + self.name,
        })

        # overwrite the user entered name with the properly capitalized one
        self.name = result['payload'].get('name', self.name)
        self.units = result['payload'].get('units', '')
        self.values = result['payload'].get('values', [])

    def __str__(self):
        return 'name: "{}"\nunits: "{}"\nlength: {}'.format(self.name, self.units, len(self.values))

