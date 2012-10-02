"""
Test pm-delivery application
"""
import os
import ConfigParser
from cement.core import handler
from test_default import PmTest
from scilifelab.pm.core.deliver import *

filedir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

class PmProductionTest(PmTest):
    def setUp(self):
        if not os.path.exists(os.path.join(os.getenv("HOME"), "dbcon.ini")):
            self.url = None
            self.user = None
            self.pw = None
            self.examples = {}
        else:
            config = ConfigParser.ConfigParser()
            config.readfp(open(os.path.join(os.getenv("HOME"), "dbcon.ini")))
            self.url = config.get("couchdb", "url")
            self.user = config.get("couchdb", "username")
            self.pw = config.get("couchdb", "password")
            self.examples = {"sample":config.get("examples", "sample"),
                             "flowcell":config.get("examples", "flowcell"),
                             "project":config.get("examples", "project")}

        
    def test_1_sample_status(self):
        self.app = self.make_app(argv = ['report', 'sample_status', '--user', self.user, '--password', self.pw, '--url', self.url, self.examples["project"], self.examples["flowcell"], '--debug'],extensions=['scilifelab.pm.ext.ext_couchdb'])
        handler.register(DeliveryReportController)
        self._run_app()

    def test_1_project_status(self):
        self.app = self.make_app(argv = ['report', 'project_status', '--user', self.user, '--password', self.pw, '--url', self.url, self.examples["project"], self.examples["flowcell"], '--debug'],extensions=['scilifelab.pm.ext.ext_couchdb'])
        handler.register(DeliveryReportController)
        self._run_app()

