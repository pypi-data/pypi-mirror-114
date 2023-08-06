# FEATURES/IDEAS/MAYBE:
#   - .why() -> auto-assert with explanation? (maybe some other form of explanation)
#   - also useful as iterator and template for fast creation? -> need to give the wildcards a name?

class VSet:
    def __init__(self, template):
        self.template = template
        pass

    def __contains__(self, item):
        return self.template == item


