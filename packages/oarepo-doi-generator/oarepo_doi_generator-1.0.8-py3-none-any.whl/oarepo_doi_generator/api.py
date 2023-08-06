import datetime

from flask import current_app
from flask_login import current_user
from invenio_db import db
from invenio_pidstore.models import PersistentIdentifier, PIDStatus
from jsonref import requests

from .new_datasets_mapping import schema_mapping

def doi_already_registered(record):
    if "persistentIdentifiers" in record:
        for i in record['persistentIdentifiers']:
            if i['scheme'] == "doi" and i['status'] == "registered":
                return True
    return False

def doi_request(record, publisher):
    requested_date = datetime.datetime.today()
    if "oarepo:doirequest" not in record:
        record['oarepo:doirequest'] = {"publisher": publisher,
                                       "requestedBy": current_user.id,
                                       "requestedDate": requested_date.strftime('%Y-%m-%d')}

    record.commit()
    db.session.commit()
    return record


def doi_approved(record, pid_type):
    if "oarepo:doirequest" in record and not doi_already_registered(record):
        publisher = record["oarepo:doirequest"]["publisher"]
        data = schema_mapping(record, pid_type, publisher)
        doi_registration(data=data)
        doi = data['data']['attributes']['doi']
        if "persistentIdentifiers" not in record:
            record['persistentIdentifiers'] = [{
                "identifier": doi,
                "scheme": "DOI",
                "status": "registered"
            }]
        else:
            record['persistentIdentifiers'].append(
                {
                    "identifier": doi,
                    "scheme": "DOI",
                    "status": "registered"
                }
            )
        record.pop("oarepo:doirequest")
        PersistentIdentifier.create('DOI', doi, object_type='rec',
                                    object_uuid=record.id,
                                    status=PIDStatus.REGISTERED)

    return record


def doi_registration(data):
    username = current_app.config.get("DOI_DATACITE_USERNAME")
    password = current_app.config.get("DOI_DATACITE_PASSWORD")

    if current_app.config.get("DOI_TEST_MODE"):
        url = 'https://api.test.datacite.org/dois'
    else:
        url = 'https://api.datacite.org/dois'

    request = requests.post(url=url, json=data, headers={'Content-type': 'application/vnd.api+json'},
                            auth=(username, password))
    if request.status_code != 201:
        raise requests.ConnectionError("Expected status code 201, but got {}".format(request.status_code))
