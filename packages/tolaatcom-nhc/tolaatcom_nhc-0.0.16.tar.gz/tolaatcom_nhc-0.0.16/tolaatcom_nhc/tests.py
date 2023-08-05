import unittest
from tolaatcom_nhc import nethamishpat
from tolaatcom_nhc import pdf_generator
from tolaatcom_nhc import one_case
import logging

logging.basicConfig(level=logging.DEBUG)
logging.root.setLevel(level=logging.WARN)
logging.getLogger('pdfgenerator').setLevel(level=logging.DEBUG)


class SimpleTestCase(unittest.TestCase):

    def setUp(self):
        logging.info('set up')

    def test_metadata(self):
        api = nethamishpat.NethamishpatApiClient()
        r = api.parse_everything({'CaseType': 'n', 'CaseDisplayIdentifier': '52512-02-18'})
        self.assertEqual(r['case']['CourtName'].strip(), 'מחוזי מרכז')
        self.assertEqual(r['case']['CaseID'], 75263135)
        self.assertEqual(2, len(r['sittings']))
        self.assertEqual(5, len(r['decisions']))
        self.assertEqual(0, len(r['verdicts']))

    def test_metadata2(self):
        api = nethamishpat.NethamishpatApiClient()
        r = api.parse_everything({'CaseType': 'n', 'CaseDisplayIdentifier': '52512-02-18'})
        from os.path import expanduser
        with open(expanduser('~/a.pdf'), 'wb') as f:
            f.write(r['decisions'][4]['pdf'].read())
        print('done')

    def test_does_not_exist(self):
        api = nethamishpat.NethamishpatApiClient()
        r = api.parse_everything({'CaseType': 'n', 'CaseDisplayIdentifier': '26078-04-17'})
        self.assertIsNone(r)


    def test_pdf_getn(self):
        pdfg = pdf_generator.PdfGenerator()
        d, last_m = pdfg.build_document('77636097', 'decisions', 4)
        from os.path import expanduser, join
        out = join(expanduser('~'), 'temp.pdf')
        open(out, 'wb').write(d.read())
        print(out)

    def test_scrap(self):
        oc = one_case.OneCase()
        p = {'CaseDisplayIdentifier': '27040-08-20', 'CaseType': 'n'}
        oc.handle(p)

