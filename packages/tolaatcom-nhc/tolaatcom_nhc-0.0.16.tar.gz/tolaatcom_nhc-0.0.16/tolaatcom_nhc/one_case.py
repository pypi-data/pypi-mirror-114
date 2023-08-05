import time
import threading
import json

from tolaatcom_nhc import boto3factory
from tolaatcom_nhc import nethamishpat


class OneCase:

    def __init__(self, master_table=None):
        self.master = master_table or 'master_table'
        self.bucket = 'cloud-eu-central-1-q97dt1m5d4rndek'
        self.prefix = 'documents_v2/decision_documents'
        self.local = threading.local()


    def map_to_dynamo(self, m):
        d = {}
        for k, v in m.items():
            if v:
                d[k] = {'S': str(v)}
        return {'M': d}

    def list_to_dynamo(self, l):
        dl = []
        for s in l:
            del s['__type']
            dl.append(self.map_to_dynamo(s))

        return {'L': dl}


    def upload_decisions(self, caseid, type, decisions):
        s3 = boto3factory.client('s3')
        for index, decision in enumerate(decisions):
            i = str(index).zfill(3)

            if 'images' in decision:
                key = f'{self.prefix}/{caseid}/{type}/{i}.json'
                j = json.dumps(decision['images'])
                s3.put_object(Bucket=self.bucket, Key=key, ContentType='application/json', Body=j)
                del decision['images']

            if 'pdf' in decision:
                key = f'{self.prefix}/{caseid}/{type}/{i}.pdf'
                s3.put_object(Bucket=self.bucket, Key=key, ContentType='application/pdf', Body=decision['pdf'])
                del decision['pdf']

    def get_nhc(self):
        if not hasattr(self.local, 'nhc'):
            nhc = nethamishpat.NethamishpatApiClient()
            setattr(self.local, 'nhc', nhc)

        return getattr(self.local, 'nhc')

    def init_permissions(self, key):
        dynamo = boto3factory.client('dynamodb')
        dynamo.update_item(TableName=self.master, Key=key, UpdateExpression='SET #p = if_not_exists(#p, :empty)',
                           ExpressionAttributeNames={'#p': 'permissions'},
                           ExpressionAttributeValues={':empty': {'M': {}}})

    def set_permissions(self, key, permission_name, reason):
        dynamo = boto3factory.client('dynamodb')

        self.init_permissions(key)

        value = {'M': {'ts': {'N': str(int(time.time()))}, 'reason': {'S': reason}}}

        dynamo.update_item(TableName=self.master, Key=key,
                                UpdateExpression='SET #ps.#p=:v',
                                ExpressionAttributeNames={'#ps': 'permissions', '#p': permission_name},
                                ExpressionAttributeValues={':v': value})
        return

    def mark_unavailable(self, case):
        case_id = case['CaseDisplayIdentifier']
        keys = [{'case_id': {'S': f'{t}:{case_id}'}} for t in ('n', 't')]
        dynamo = boto3factory.client('dynamodb')

        r= dynamo.batch_get_item(RequestItems={self.master: {'Keys': keys}})
        for item in r['Responses'][self.master]:
            title = item['title']['S']
            if title.strip() == case['Title'].strip():
                key = {'case_id': item['case_id']}

                self.set_permissions(key, 'deleted', 'missing_in_api')
        return



    def handle(self, by_date):
        n = by_date['CaseDisplayIdentifier']

        nhc = self.get_nhc()

        r = nhc.parse_everything(by_date)

        if r is None:
            #self.mark_unavailable(by_date)
            return "deleted"

        if r['type'] == 'court':
            t = 'n'
        elif r['type'] == 'transport':
            t = 't'
        elif r['type'] == 'old':
            t = 'o'
            case_id = by_date['CaseDisplayIdentifier']
            court = by_date['CourtName']
            case_type = by_date['CaseTypeShortName']
            n = f'{case_type} {case_id} {court}'

        else:
            raise Exception()

        case_id = r['case']['CaseID']

        for what in 'decisions', 'verdicts':
            self.upload_decisions(case_id, what, r[what])

        sittings = self.list_to_dynamo(r['sittings'])
        decisions = self.list_to_dynamo(r['decisions'])
        verdicts = self.list_to_dynamo(r['verdicts'])

        if 'case' in r:
            case = self.map_to_dynamo(r['case'])
        else:
            case = {'M': {}}

        by_date = self.map_to_dynamo(by_date)

        ts = {'S': str(int(time.time()))}

        m = {'ts': ts,
             'case': case,
             'type': {'S': r['type']},
             'sittings': sittings,
             'decisions': decisions,
             'verdicts': verdicts}

        object = {'M': m}
        k = f'{t}:{n}'
        key = {'case_id': {'S': k}}
        dynamo = boto3factory.client('dynamodb')
        dynamo.update_item(
            TableName=self.master,
            Key=key,
            UpdateExpression='Set #api=:api, #by_date=:by_date',
            ExpressionAttributeNames={'#api': 'api', '#by_date': 'by_date'},
            ExpressionAttributeValues={':api': object, ':by_date': by_date}
        )


if __name__=='__main__':
    title = """ת"פ 46542-04-16 : מדינת ישראל נ' וולפינגר"""
    o=OneCase()
    o.handle({'Title': title, 'CaseDisplayIdentifier': '46542-04-16'})
