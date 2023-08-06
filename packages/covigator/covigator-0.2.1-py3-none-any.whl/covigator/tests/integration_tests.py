from unittest import TestCase

from covigator.accessor.ena_accessor import EnaAccessor
from covigator.model import Database
from covigator.tests import SARS_COV_2_TAXID, HOMO_SAPIENS_TAXID


class IntegrationTests(TestCase):

    def test_access(self):
        """
        If given enough time, this creates a database with all runs complying with the selection criteria from ENA
        """
        accessor = EnaAccessor(tax_id=SARS_COV_2_TAXID, host_tax_id=HOMO_SAPIENS_TAXID, database=Database())
        accessor.access()
