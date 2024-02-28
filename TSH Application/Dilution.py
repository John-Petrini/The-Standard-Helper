class Dilution:
    def __init__(self, pipet, flask):
        self.pipet = pipet
        self.flask = flask
        self.dilution_factor = (pipet.volume / flask.volume)
        # TODO: placeholder
        self.error = pipet.error + flask.error

    @staticmethod
    def from_glassware_array(pipets, flasks):
        dilutions = []
        for pipet in pipets:
            for flask in flasks:
                if flask.volume > pipet.volume:
                    dilutions.append(Dilution(pipet, flask))
        return dilutions