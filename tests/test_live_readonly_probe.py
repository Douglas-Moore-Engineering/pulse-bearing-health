"""Ensure the operator's read-only verification cannot append workflow records."""
import base64
import io
import json
from pathlib import Path
import runpy
from urllib.error import HTTPError

import pytest


@pytest.mark.parametrize('review_status', [200, 403])
def test_probe_uses_only_get_and_never_prints_token(monkeypatch, capsys, review_status):
    claims = base64.urlsafe_b64encode(json.dumps({'roles': ['Pulse.Assess', 'Pulse.Review']}).encode()).decode().rstrip('=')
    token = 'synthetic.' + claims + '.never-log-this-signature'
    requests = []
    def urlopen(request, timeout):
        requests.append(request)
        assert request.get_method() == 'GET'
        assert request.data is None
        if request.full_url.startswith('http://169.254.169.254/'):
            body = {'access_token': token}
        elif not request.has_header('Authorization'):
            raise HTTPError(request.full_url, 401, 'Unauthorized', {}, None)
        elif request.full_url.endswith('/reviews'):
            if review_status != 200:
                raise HTTPError(request.full_url, review_status, 'Forbidden', {}, None)
            body = {'reviews': []}
        else:
            body = {'events': [{'event_id': 'synthetic-event'}]}
        response = io.BytesIO(json.dumps(body).encode())
        response.status = 200
        return response
    monkeypatch.setattr('urllib.request.urlopen', urlopen)
    probe = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'infra/single-node/verify-live-readonly.py'))
    probe['main']()
    output = capsys.readouterr().out
    report = json.loads(output)
    assert token not in output and 'never-log-this-signature' not in output
    assert report['mutations_performed'] is False
    assert report['closure_operation_verified'] is False
    assert report['review_checks'][0]['status'] == review_status
    assert len(requests) == 4
