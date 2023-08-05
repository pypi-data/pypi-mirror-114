from genologics.lims import Lims
from genologics.entities import Process, Sample


def test_A(server_test1):
    # GIVEN: A lims with a sample with the udf 'customer': 'cust002'

    # WHEN creating a genologics Sample entity of that sample
    lims = Lims("http://127.0.0.1:8000", 'dummy', 'dummy')
    s = Sample(lims, id='ACC2351A1')

    # THEN the sample instance should have the udf
    assert s.udf['customer'] == 'cust002'



def test_B(server_test1):
    # GIVEN: A lims with a process with the udf 'Instrument Used': 'Cava'

    # WHEN creating a genologics Process entity of that process
    lims = Lims("http://127.0.0.1:8000", 'dummy', 'dummy')
    p = Process(lims, id='24-168017')

    # THEN the process instance should have the udf
    assert p.udf['Instrument Used'] == 'Cava'


def test_C(server_test1):
    # GIVEN: A lims with a process with:
    #   process type: 'CG002 - qPCR QC (Library Validation) (Dev)'
    #   input artifact: '2-1155237'
    #   Udf 'Instrument Used': 'Cava'

    # WHEN creating a genologics Lims object and filtering on the fields.
    lims = Lims("http://127.0.0.1:8000", 'dummy', 'dummy')
    processes = lims.get_processes(type=['CG002 - qPCR QC (Library Validation) (Dev)'], inputartifactlimsid=['2-1155237'], udf={'Instrument Used': 'Cava'})

    # Then the process should be found
    assert processes == [Process(lims, id='24-168017')]


def test_D(server_test1):
    # GIVEN: A lims with a sample with:
    #   name: 'maya'
    #   Udf "Source": "blood", "Reads missing (M)": 0

    # WHEN creating a genologics Lims object and filtering on the fields.
    lims = Lims("http://127.0.0.1:8000", 'dummy', 'dummy')
    samples = lims.get_samples(udf={"Source": "blood", "Reads missing (M)": 0}, name='maya')

    # Then the sample should be found
    assert samples == [Sample(lims, id='ACC2351A2')]
