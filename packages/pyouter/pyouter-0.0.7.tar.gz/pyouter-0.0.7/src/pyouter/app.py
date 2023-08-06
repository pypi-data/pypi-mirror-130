
from pyouter.default import create_parser
from pyouter.errors import NotInit
from pyouter.router import Router


class App(object):
    def __init__(self, config=None, parser=None):
        opt_parser = create_parser("tasks router runner") if parser is None else parser
        self.options = opt_parser.parse_args()
        self.config = {} if config is None else config
        self.router: Router

    def use(self, router: Router):
        self.router = router
        self.router.context(self.config, self.options)
        return self

    def run(self):
        if self.router is None:
            raise NotInit("self.router in App")

        if self.options.tasks:
            for task in self.router.tasks():
                print(task)
        else:
            self.router.dispatch(self.options.actions)
        return self
