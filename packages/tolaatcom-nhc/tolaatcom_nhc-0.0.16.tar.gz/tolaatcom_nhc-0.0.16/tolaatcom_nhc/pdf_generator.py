import boto3
import tempfile
import logging


class PdfGenerator:

    logger = logging.getLogger('pdfgenerator')


    def build_document(self, caseid, decision_type, number):
        number = str(number).zfill(3)

        bucket = 'cloud-eu-central-1-q97dt1m5d4rndek'

        s3 = boto3.client('s3')

        path_pdf = f'documents_v2/decision_documents/{caseid}/{decision_type}/{number}.pdf'
        self.logger.info('Loading PDF from s3://%s/%s', bucket, path_pdf)
        r = s3.get_object(Bucket=bucket, Key=path_pdf)
        spooled_pdf = tempfile.SpooledTemporaryFile()
        spooled_pdf.write(r['Body'].read())
        spooled_pdf.seek(0)
        return spooled_pdf, r['LastModified']


if __name__=='__main__':
    pg = PdfGenerator()
    pg.build_document('32485892', 'decisions', 1)