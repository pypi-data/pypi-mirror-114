class Response:
    """The Response class holds information about an individual Response in
    Stat-Ease 360. Instances of this class are typically created by
    :func:`statease.client.SEClient.get_response`.

    :ivar str name: the name of the response
    :ivar str units: the units of the response
    :ivar list values: the values of the response, in run order
    """

    def __init__(self, client, name):
        self.client = client
        self.name = name

        result = self.client.send_payload({
            "method": "GET",
            "uri": "design/response/" + self.name,
        })

        self.name = result['payload'].get('name', self.name)
        self.units = result['payload'].get('units', '')
        self.values = result['payload'].get('values', [])

    def __str__(self):
        return 'name: "{}"\nunits: "{}"\nlength: {}'.format(self.name, self.units, len(self.values))

    def post(self, endpoint, payload):
        return self.client.send_payload({
            "method": "POST",
            "uri": "design/response/{}/{}".format(self.name, endpoint),
            **payload,
        })

    def simulate(self, equation, std_dev=1, variance_ratio=1):
        """Simulates data for a response.

        :param str equation: An equation that is recognized by the Stat-Ease
                             360 simulator. Search the help for
                             "Equation Entry" for more information on the
                             equation format.
        :param float std_dev: This adds some normal error to each simulated
                              value.
        :param float variance_ratio: If there are groups in the design,
                                     inter-group variability will be simulated
                                     using a combination of this parameter
                                     and the std_dev parameter.

        :Example:
            >>> response.simulate('a+b+sin(a)', std_dev=2)
        """

        self.post("simulate", {
            "equation": equation,
            "std_dev": std_dev,
            "variance_ratio": variance_ratio,
        })
