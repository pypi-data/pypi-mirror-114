from unittest import TestCase

from toil.job import Job

from covigator.model import Database
from covigator.processor.processor import Processor
from covigator.processor.ena_processor_toil import EnaProcessor as EnaProcessorToil
from dask.distributed import Client


class EnaProcessorTests(TestCase):

    def test_process_dask(self):

        client = Client(n_workers=2, threads_per_worker=2)
        processor = Processor(database=Database(), dask_client=client)
        processor.process()

    def test_process_toil(self):

        processor = EnaProcessorToil()
        # TODO: make this location configurable in some temp folder
        options = Job.Runner.getDefaultOptions("./toilWorkflowRun")
        options.logLevel = "INFO"
        options.clean = "always"
        # NOTE: use this option for slurm
        # options.batchSystem = "slurm"
        # NOTE: further slurm config through env variables such as export TOIL_SLURM_ARGS="-t 1:00:00 -q fatq"
        processor.process(options)
