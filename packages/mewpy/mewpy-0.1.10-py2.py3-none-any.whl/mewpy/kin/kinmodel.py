


class KineticReaction(object):

    def __init__(self, r_id, substrates: list = [],
                 products: list = [], parameters: dict = {}, modifiers: list = []):
        """[summary]

        Args:
            r_id (str): Reaction identifier
            parameters (dict, optional): local parameters. Defaults to dict().
            substrates (list, optional): substrates. Defaults to [].
            products (list, optional): products. Defaults to [].
        """
        self.substrates = substrates
        self.products = products
        self.parameters = parameters
        self.modifiers = modifiers
        self.parameter_distributions = {}
        

