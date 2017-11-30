from dsub.providers import google, local, stub
from dsub.lib import resources
from flask import current_app
from werkzeug.exceptions import BadRequest, Unauthorized, NotImplemented

from jobs.common import enum

ProviderType = enum(GOOGLE='google', LOCAL='local', STUB='stub')


def get_provider(provider_type, parent_id=None, auth_token=None):
    """Construct the dsub provider for the given parameters.

        Args:
            provider_type: A string indicating google, local, or stub provider
            parent_id: A string representing a Google Cloud Project ID
            auth_token: oauth2 token for authorizing Genomics API requests in
                dsub

        Returns:
            JobProvider: Instance of LocalJobProvider, GoogleJobProvider, or
                StubJobProvider.
    """
    if provider_type == ProviderType.GOOGLE:
        return _get_google_provider(parent_id, auth_token)
    elif parent_id or auth_token:
        raise BadRequest(
            'The Local provider does not support the `{}` field .'.format(
                'authToken' if auth_token else 'parentId'))
    elif provider_type == ProviderType.LOCAL:
        # TODO(https://github.com/googlegenomics/dsub/issues/93): Remove
        # resources parameter and import
        return local.LocalJobProvider(resources)
    elif provider_type == ProviderType.STUB:
        return stub.StubJobProvider()


def _get_google_provider(parent_id, auth_token):
    if not parent_id:
        raise BadRequest('Missing required field `parentId`.')
    if not auth_token:
        if _requires_auth():
            raise BadRequest('Missing required field `authToken`.')
        return google.GoogleJobProvider(False, False, parent_id)

    try:
        credentials = AccessTokenCredentials(auth_token, 'user-agent')
        return google.GoogleJobProvider(
            False, False, parent_id, credentials=credentials)
    except AccessTokenCredentialsError as e:
        raise Unauthorized('Invalid authentication token:{}.'.format(e))


def _requires_auth():
    return current_app.config['REQUIRES_AUTH']
