# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
# Copyright (C) 2021 TU Wien.
#
# Invenio-RDM-Records is free software; you can redistribute it
# and/or modify it under the terms of the MIT License; see LICENSE file for
# more details.

"""Service level tests for Invenio RDM Records."""

from collections import namedtuple

import pytest
from flask_babelex import lazy_gettext as _
from invenio_pidstore.errors import PIDDoesNotExistError
from marshmallow import ValidationError

from invenio_rdm_records.proxies import current_rdm_records
from invenio_rdm_records.services.errors import EmbargoNotLiftedError

RunningApp = namedtuple("RunningApp", [
    "app", "location", "superuser_identity", "resource_type_v",
    "subject_v", "languages_v", "title_type_v"
])


@pytest.fixture
def running_app(
    app, location, superuser_identity, resource_type_v, subject_v, languages_v,
        title_type_v):
    """This fixture provides an app with the typically needed db data loaded.

    All of these fixtures are often needed together, so collecting them
    under a semantic umbrella makes sense.
    """
    return RunningApp(app, location, superuser_identity,
                      resource_type_v, subject_v, languages_v, title_type_v)


#
# PIDs
#
def test_resolve_pid(running_app, es_clear, minimal_record):
    """Test the reserve function with client logged in."""
    service = current_rdm_records.records_service
    superuser_identity = running_app.superuser_identity
    # create the draft
    draft = service.create(superuser_identity, minimal_record)
    # publish the record
    record = service.publish(draft.id, superuser_identity)
    doi = record.to_dict()["pids"]["doi"]["identifier"]

    # test resolution
    resolved_record = service.resolve_pid(
        id_=doi,
        identity=superuser_identity,
        pid_type="doi"
    )
    assert resolved_record.id == record.id
    assert resolved_record.to_dict()["pids"]["doi"]["identifier"] == doi


def test_resolve_non_existing_pid(running_app, es_clear, minimal_record):
    """Test the reserve function with client logged in."""
    service = current_rdm_records.records_service
    superuser_identity = running_app.superuser_identity
    # create the draft
    draft = service.create(superuser_identity, minimal_record)
    # publish the record
    service.publish(draft.id, superuser_identity)

    # test resolution
    fake_doi = "10.1234/client.12345-abdce"
    with pytest.raises(PIDDoesNotExistError):
        service.resolve_pid(
            id_=fake_doi,
            identity=superuser_identity,
            pid_type="doi"
        )


def test_pid_creation_default_required(running_app, es_clear, minimal_record):
    superuser_identity = running_app.superuser_identity
    service = current_rdm_records.records_service
    minimal_record["pids"] = {}
    # create the draft
    draft = service.create(superuser_identity, minimal_record)
    # publish the record
    record = service.publish(draft.id, superuser_identity)
    published_doi = record.to_dict()["pids"]["doi"]

    assert published_doi["identifier"]
    assert published_doi["provider"] == "datacite"  # default
    assert published_doi["client"] == "datacite"  # default


def test_pid_creation_invalid_format_value_managed(
    running_app, es_clear, minimal_record
):
    superuser_identity = running_app.superuser_identity
    service = current_rdm_records.records_service
    # set the pids field
    doi = {
        "identifier": "loremipsum",
        "provider": "datacite",
        "client": "datacite"
    }
    pids = {"doi": doi}
    minimal_record["pids"] = pids
    # create the draft
    # will pass creation since validation is just reported, not hard fail
    # but it will be removed (not saved)
    draft = service.create(superuser_identity, minimal_record)
    assert draft.to_dict()["pids"] == {}


def test_pid_creation_invalid_no_value_managed(
    running_app, es_clear, minimal_record
):
    # NOTE: This use case is tricky because it will spawn two exceptions
    # Because a value is missing and is also invalid. Should consider only
    # second case.
    # {
    #   'field': 'pids.doi.value.identifier',
    #   'messages': ['Missing data for required field.']
    # }
    # {
    #   'field': 'pids._schema',
    #   'messages': [l'Invalid value for scheme doi']
    # }
    superuser_identity = running_app.superuser_identity
    service = current_rdm_records.records_service
    # set the pids field
    # no value, to get a value from the system it should not send the pid_type
    doi = {
        "provider": "datacite",
        "client": "datacite"
    }
    pids = {"doi": doi}
    minimal_record["pids"] = pids
    # create the draft
    # will pass creation since validation is just reported, not hard fail
    # but it will be removed (not saved)
    draft = service.create(superuser_identity, minimal_record)
    assert draft.to_dict()["pids"] == {}


def test_pid_creation_invalid_scheme_managed(
    running_app, es_clear, minimal_record
):
    superuser_identity = running_app.superuser_identity
    service = current_rdm_records.records_service
    # set the pids field
    lorem = {
        "identifier": "10.1234/datacite.12345",
        "provider": "datacite",
        "client": "datacite"
    }
    pids = {"lorem": lorem}
    minimal_record["pids"] = pids
    # create the draft
    # check soft validation reported the error
    draft = service.create(superuser_identity, minimal_record)
    expected_errors = [
        {'field': 'pids', 'messages': [_('Invalid value for scheme lorem')]}
    ]
    assert draft.errors == expected_errors
    # NOTE: the invalid pid got removed, so if publish it will not be there
    assert draft.to_dict()["pids"] == {}


def test_pid_creation_valid_unmanaged(running_app, es_clear, minimal_record):
    superuser_identity = running_app.superuser_identity
    service = current_rdm_records.records_service
    # set the pids field
    doi = {
        "identifier": "10.1234/datacite.12345",
        "provider": "external",
    }
    pids = {"doi": doi}
    minimal_record["pids"] = pids
    # create the draft
    draft = service.create(superuser_identity, minimal_record)
    # publish the record
    record = service.publish(draft.id, superuser_identity)
    published_doi = record.to_dict()["pids"]["doi"]

    assert doi["identifier"] == published_doi["identifier"]
    assert doi["provider"] == published_doi["provider"]


def test_pid_creation_invalid_format_unmanaged(
    running_app, es_clear, minimal_record
):
    superuser_identity = running_app.superuser_identity
    service = current_rdm_records.records_service
    # set the pids field
    doi = {
        "identifier": "loremipsum",
        "provider": "external",
    }
    pids = {"doi": doi}
    minimal_record["pids"] = pids
    # create the draft
    # will pass creation since validation is just reported, not hard fail
    # but it will be removed (not saved)
    draft = service.create(superuser_identity, minimal_record)
    assert draft.to_dict()["pids"] == {}


def test_pid_creation_invalid_scheme_unmanaged(
    running_app, es_clear, minimal_record
):
    superuser_identity = running_app.superuser_identity
    service = current_rdm_records.records_service
    # set the pids field
    lorem = {
        "identifier": "10.1234/datacite.12345",
        "provider": "external",
    }
    pids = {"lorem": lorem}
    minimal_record["pids"] = pids
    # create the draft
    draft = service.create(superuser_identity, minimal_record)
    expected_errors = [
        {'field': 'pids', 'messages': [_('Invalid value for scheme lorem')]}
    ]
    assert draft.errors == expected_errors
    # NOTE: the invalid pid got removed, so if publish it will not be there
    assert draft.to_dict()["pids"] == {}


def _publish_record(identity, record):
    service = current_rdm_records.records_service
    record["pids"] = {}
    # create the draft
    draft = service.create(identity, record)
    # publish the record
    record = service.publish(draft.id, identity)
    published_doi = record.to_dict()["pids"]["doi"]

    return published_doi


def test_pid_creation_duplicated_unmanaged(
    running_app, es_clear, superuser_identity, minimal_record
):
    service = current_rdm_records.records_service
    published_doi = _publish_record(superuser_identity, minimal_record)

    # set the pids field
    doi = {
        "identifier": published_doi["identifier"],
        "provider": "external",
    }
    pids = {"doi": doi}
    minimal_record["pids"] = pids

    # create the draft with duplicated DOI
    with pytest.raises(ValidationError):
        service.create(superuser_identity, minimal_record)


def test_pid_update_duplicated_unmanaged(
    running_app, es_clear, superuser_identity, minimal_record
):
    service = current_rdm_records.records_service
    published_doi = _publish_record(superuser_identity, minimal_record)

    # create the draft
    draft = service.create(superuser_identity, minimal_record)
    # update draft with duplicated
    doi = {
        "identifier": published_doi["identifier"],
        "provider": "external",
    }
    pids = {"doi": doi}
    update_data = draft.to_dict()
    update_data["pids"] = pids
    with pytest.raises(ValidationError):
        service.update_draft(draft.id, superuser_identity, update_data)


def test_pid_create_duplicated_managed(
    running_app, es_clear, superuser_identity, minimal_record
):
    service = current_rdm_records.records_service
    published_doi = _publish_record(superuser_identity, minimal_record)

    # set the pids field
    doi = {
        "identifier": published_doi["identifier"],
        "provider": published_doi["provider"],
        "client": published_doi["client"],
    }
    pids = {"doi": doi}
    minimal_record["pids"] = pids

    # create the draft with duplicated DOI
    with pytest.raises(ValidationError):
        service.create(superuser_identity, minimal_record)


def test_pid_update_duplicated_managed(
    running_app, es_clear, superuser_identity, minimal_record
):
    service = current_rdm_records.records_service
    published_doi = _publish_record(superuser_identity, minimal_record)

    # create the draft
    draft = service.create(superuser_identity, minimal_record)
    # update draft with duplicated
    doi = {
        "identifier": published_doi["identifier"],
        "provider": published_doi["provider"],
        "client": published_doi["client"],
    }
    pids = {"doi": doi}
    update_data = draft.to_dict()
    update_data["pids"] = pids
    with pytest.raises(ValidationError):
        service.update_draft(draft.id, superuser_identity, update_data)


def test_minimal_draft_creation(running_app, es_clear, minimal_record):
    superuser_identity = running_app.superuser_identity
    service = current_rdm_records.records_service

    record_item = service.create(superuser_identity, minimal_record)
    record_dict = record_item.to_dict()

    assert record_dict["metadata"]["resource_type"] == {
        'id': 'image-photo',
        'title': {'en': 'Photo'}
    }


def test_draft_w_languages_creation(running_app, es_clear, minimal_record):
    superuser_identity = running_app.superuser_identity
    service = current_rdm_records.records_service
    minimal_record["metadata"]["languages"] = [{
        "id": "eng",
    }]

    record_item = service.create(superuser_identity, minimal_record)
    record_dict = record_item.to_dict()

    assert record_dict["metadata"]["languages"] == [{
        'id': 'eng',
        'title': {'en': 'English', 'da': 'Engelsk'}
    }]


#
# Embargo lift
#
def test_embargo_lift_without_draft(embargoed_record, running_app, es_clear):
    record = embargoed_record
    service = current_rdm_records.records_service

    service.lift_embargo(
        _id=record['id'],
        identity=running_app.superuser_identity
    )

    record_lifted = service.record_cls.pid.resolve(record['id'])
    assert record_lifted.access.embargo.active is False
    assert record_lifted.access.protection.files == 'public'
    assert record_lifted.access.protection.record == 'public'
    assert record_lifted.access.status.value == 'metadata-only'


def test_embargo_lift_with_draft(
        embargoed_record, es_clear, superuser_identity):
    record = embargoed_record
    service = current_rdm_records.records_service

    # Edit a draft
    ongoing_draft = service.edit(
        id_=record['id'], identity=superuser_identity)

    service.lift_embargo(_id=record['id'], identity=superuser_identity)
    record_lifted = service.record_cls.pid.resolve(record['id'])
    draft_lifted = service.draft_cls.pid.resolve(ongoing_draft['id'])

    assert record_lifted.access.embargo.active is False
    assert record_lifted.access.protection.files == 'public'
    assert record_lifted.access.protection.record == 'public'

    assert draft_lifted.access.embargo.active is False
    assert draft_lifted.access.protection.files == 'public'
    assert draft_lifted.access.protection.record == 'public'


def test_embargo_lift_with_updated_draft(
        embargoed_record, superuser_identity, es_clear):
    record = embargoed_record
    service = current_rdm_records.records_service

    # This draft simulates an existing one while lifting the record
    draft = service.edit(id_=record['id'], identity=superuser_identity).data

    # Change record's title and access field to be restricted
    draft["metadata"]["title"] = 'Record modified by the user'
    draft["access"]["status"] = 'restricted'
    draft["access"]["embargo"] = dict(
        active=False, until=None, reason=None
    )
    # Update the ongoing draft with the new data simulating the user's input
    ongoing_draft = service.update_draft(
        id_=draft['id'], identity=superuser_identity, data=draft)

    service.lift_embargo(_id=record['id'], identity=superuser_identity)
    record_lifted = service.record_cls.pid.resolve(record['id'])
    draft_lifted = service.draft_cls.pid.resolve(ongoing_draft['id'])

    assert record_lifted.access.embargo.active is False
    assert record_lifted.access.protection.files == 'public'
    assert record_lifted.access.protection.record == 'public'

    assert draft_lifted.access.embargo.active is False
    assert draft_lifted.access.protection.files == 'restricted'
    assert draft_lifted.access.protection.record == 'public'


def test_embargo_lift_with_error(running_app, es_clear, minimal_record):
    superuser_identity = running_app.superuser_identity
    service = current_rdm_records.records_service
    # Add embargo to record
    minimal_record["access"]["files"] = 'restricted'
    minimal_record["access"]["status"] = 'embargoed'
    minimal_record["access"]["embargo"] = dict(
        active=True, until='3220-06-01', reason=None
    )
    draft = service.create(superuser_identity, minimal_record)
    record = service.publish(id_=draft.id, identity=superuser_identity)

    # Record should not be lifted since it didn't expire (until 3220)
    with pytest.raises(EmbargoNotLiftedError):
        service.lift_embargo(_id=record['id'], identity=superuser_identity)
