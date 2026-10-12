"""Read-only reference identity checks. Run on the VM; never print tokens."""
import base64
from datetime import datetime, timezone
import json
import urllib.error
import urllib.parse
import urllib.request


def main():
    query = urllib.parse.urlencode({'api-version': '2018-02-01',
        'resource': 'api://a7064e03-b8e9-46d7-bb0d-52f030b2a39a',
        'client_id': 'e168e6af-1310-4cbf-9677-54e5ff3f294b'})
    request = urllib.request.Request('http://169.254.169.254/metadata/identity/oauth2/token?' + query,
                                     headers={'Metadata': 'true'})
    with urllib.request.urlopen(request, timeout=20) as response:
        token = json.load(response)['access_token']
    claims = json.loads(base64.urlsafe_b64decode(token.split('.')[1] + '=='))
    def get(path, authenticated=True):
        headers = {'Authorization': 'Bearer ' + token} if authenticated else {}
        try:
            with urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:18080' + path,
                                        headers=headers, method='GET'), timeout=15) as response:
                return response.status, json.load(response)
        except urllib.error.HTTPError as error:
            return error.code, None
    status, inbox = get('/v1/reference/alerts')
    anonymous, _ = get('/v1/reference/alerts', False)
    report = {'observed_at': datetime.now(timezone.utc).isoformat(),
        'roles': claims.get('roles', []), 'inbox_status': status,
        'anonymous_status': anonymous, 'mutations_performed': False,
        'closure_role_observed': 'Pulse.Close' in claims.get('roles', []),
        'closure_operation_verified': False, 'review_checks': []}
    if status == 200:
        for event in inbox['events'][:100]:
            review_status, history = get('/v1/reference/alerts/' + urllib.parse.quote(event['event_id'], safe='') + '/reviews')
            report['review_checks'].append({'status': review_status,
                'count': len(history['reviews']) if review_status == 200 else None})
    print(json.dumps(report, indent=2))
    if status != 200 or anonymous != 401:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
