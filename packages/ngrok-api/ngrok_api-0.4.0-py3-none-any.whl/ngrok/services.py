from __future__ import annotations
from collections.abc import Iterator
from typing import Any, Mapping, Sequence

from .http_client import HTTPClient
from .datatypes import *


class AbuseReportsClient(object):
    """Abuse Reports allow you to submit take-down requests for URLs hosted by
    ngrok that violate ngrok's terms of service."""

    def __init__(self, client):
        self._client = client

    def create(
        self,
        urls: Sequence[str],
        metadata: str = "",
    ) -> AbuseReport:
        """Creates a new abuse report which will be reviewed by our system and abuse response team. This API is only available to authorized accounts. Contact abuse@ngrok.com to request access

        :param urls: a list of URLs containing suspected abusive content
        :param metadata: arbitrary user-defined data about this abuse report. Optional, max 4096 bytes.

        https://ngrok.com/docs/api#api-abuse-reports-create
        """
        path = "/abuse_reports"
        result = self._client.http_client.post(
            path,
            dict(
                urls=urls,
                metadata=metadata,
            ),
        )
        return AbuseReport(self._client, result)

    def get(
        self,
        id: str,
    ) -> AbuseReport:
        """Get the detailed status of abuse report by ID.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-abuse-reports-get
        """
        path = "/abuse_reports/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return AbuseReport(self._client, result)


class AgentIngressesClient(object):
    def __init__(self, client):
        self._client = client

    def create(
        self,
        domain: str,
        description: str = "",
        metadata: str = "",
    ) -> AgentIngress:
        """Create a new Agent Ingress. The ngrok agent can be configured to connect to ngrok via the new set of addresses on the returned Agent Ingress.

        :param description: human-readable description of the use of this Agent Ingress. optional, max 255 bytes.
        :param metadata: arbitrary user-defined machine-readable data of this Agent Ingress. optional, max 4096 bytes
        :param domain: the domain that you own to be used as the base domain name to generate regional agent ingress domains.

        https://ngrok.com/docs/api#api-agent-ingresses-create
        """
        path = "/agent_ingresses"
        result = self._client.http_client.post(
            path,
            dict(
                description=description,
                metadata=metadata,
                domain=domain,
            ),
        )
        return AgentIngress(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """Delete an Agent Ingress by ID

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-agent-ingresses-delete
        """
        path = "/agent_ingresses/{id}"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())

    def get(
        self,
        id: str,
    ) -> AgentIngress:
        """Get the details of an Agent Ingress by ID.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-agent-ingresses-get
        """
        path = "/agent_ingresses/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return AgentIngress(self._client, result)

    def list(
        self,
        before_id: str = None,
        limit: str = None,
    ) -> AgentIngressList:
        """List all Agent Ingresses owned by this account

        :param before_id:
        :param limit:

        https://ngrok.com/docs/api#api-agent-ingresses-list
        """
        path = "/agent_ingresses"
        result = self._client.http_client.get(
            path,
            dict(
                before_id=before_id,
                limit=limit,
            ),
        )
        return AgentIngressList(self._client, result)

    def update(
        self,
        id: str,
        description: str = None,
        metadata: str = None,
    ) -> AgentIngress:
        """Update attributes of an Agent Ingress by ID.

        :param id:
        :param description: human-readable description of the use of this Agent Ingress. optional, max 255 bytes.
        :param metadata: arbitrary user-defined machine-readable data of this Agent Ingress. optional, max 4096 bytes

        https://ngrok.com/docs/api#api-agent-ingresses-update
        """
        path = "/agent_ingresses/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.patch(
            path,
            dict(
                description=description,
                metadata=metadata,
            ),
        )
        return AgentIngress(self._client, result)


class APIKeysClient(object):
    """API Keys are used to authenticate to the `ngrok
    API` <https://ngrok.com/docs/api#authentication>`_. You may use the API itself
    to provision and manage API Keys but you'll need to provision your first API
    key from the `API Keys page` <https://dashboard.ngrok.com/api/keys>`_ on your
    ngrok.com dashboard."""

    def __init__(self, client):
        self._client = client

    def create(
        self,
        description: str = "",
        metadata: str = "",
    ) -> APIKey:
        """Create a new API key. The generated API key can be used to authenticate to the ngrok API.

        :param description: human-readable description of what uses the API key to authenticate. optional, max 255 bytes.
        :param metadata: arbitrary user-defined data of this API key. optional, max 4096 bytes

        https://ngrok.com/docs/api#api-api-keys-create
        """
        path = "/api_keys"
        result = self._client.http_client.post(
            path,
            dict(
                description=description,
                metadata=metadata,
            ),
        )
        return APIKey(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """Delete an API key by ID

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-api-keys-delete
        """
        path = "/api_keys/{id}"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())

    def get(
        self,
        id: str,
    ) -> APIKey:
        """Get the details of an API key by ID.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-api-keys-get
        """
        path = "/api_keys/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return APIKey(self._client, result)

    def list(
        self,
        before_id: str = None,
        limit: str = None,
    ) -> APIKeyList:
        """List all API keys owned by this account

        :param before_id:
        :param limit:

        https://ngrok.com/docs/api#api-api-keys-list
        """
        path = "/api_keys"
        result = self._client.http_client.get(
            path,
            dict(
                before_id=before_id,
                limit=limit,
            ),
        )
        return APIKeyList(self._client, result)

    def update(
        self,
        id: str,
        description: str = None,
        metadata: str = None,
    ) -> APIKey:
        """Update attributes of an API key by ID.

        :param id:
        :param description: human-readable description of what uses the API key to authenticate. optional, max 255 bytes.
        :param metadata: arbitrary user-defined data of this API key. optional, max 4096 bytes

        https://ngrok.com/docs/api#api-api-keys-update
        """
        path = "/api_keys/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.patch(
            path,
            dict(
                description=description,
                metadata=metadata,
            ),
        )
        return APIKey(self._client, result)


class CertificateAuthoritiesClient(object):
    """Certificate Authorities are x509 certificates that are used to sign other
    x509 certificates. Attach a Certificate Authority to the Mutual TLS module
    to verify that the TLS certificate presented by a client has been signed by
    this CA. Certificate Authorities  are used only for mTLS validation only and
    thus a private key is not included in the resource."""

    def __init__(self, client):
        self._client = client

    def create(
        self,
        ca_pem: str,
        description: str = "",
        metadata: str = "",
    ) -> CertificateAuthority:
        """Upload a new Certificate Authority

        :param description: human-readable description of this Certificate Authority. optional, max 255 bytes.
        :param metadata: arbitrary user-defined machine-readable data of this Certificate Authority. optional, max 4096 bytes.
        :param ca_pem: raw PEM of the Certificate Authority

        https://ngrok.com/docs/api#api-certificate-authorities-create
        """
        path = "/certificate_authorities"
        result = self._client.http_client.post(
            path,
            dict(
                description=description,
                metadata=metadata,
                ca_pem=ca_pem,
            ),
        )
        return CertificateAuthority(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """Delete a Certificate Authority

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-certificate-authorities-delete
        """
        path = "/certificate_authorities/{id}"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())

    def get(
        self,
        id: str,
    ) -> CertificateAuthority:
        """Get detailed information about a certficate authority

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-certificate-authorities-get
        """
        path = "/certificate_authorities/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return CertificateAuthority(self._client, result)

    def list(
        self,
        before_id: str = None,
        limit: str = None,
    ) -> CertificateAuthorityList:
        """List all Certificate Authority on this account

        :param before_id:
        :param limit:

        https://ngrok.com/docs/api#api-certificate-authorities-list
        """
        path = "/certificate_authorities"
        result = self._client.http_client.get(
            path,
            dict(
                before_id=before_id,
                limit=limit,
            ),
        )
        return CertificateAuthorityList(self._client, result)

    def update(
        self,
        id: str,
        description: str = None,
        metadata: str = None,
    ) -> CertificateAuthority:
        """Update attributes of a Certificate Authority by ID

        :param id:
        :param description: human-readable description of this Certificate Authority. optional, max 255 bytes.
        :param metadata: arbitrary user-defined machine-readable data of this Certificate Authority. optional, max 4096 bytes.

        https://ngrok.com/docs/api#api-certificate-authorities-update
        """
        path = "/certificate_authorities/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.patch(
            path,
            dict(
                description=description,
                metadata=metadata,
            ),
        )
        return CertificateAuthority(self._client, result)


class CredentialsClient(object):
    """Tunnel Credentials are ngrok agent authtokens. They authorize the ngrok
    agent to connect the ngrok service as your account. They are installed with
    the ``ngrok authtoken`` command or by specifying it in the ``ngrok.yml``
    configuration file with the ``authtoken`` property."""

    def __init__(self, client):
        self._client = client

    def create(
        self,
        description: str = "",
        metadata: str = "",
        acl: Sequence[str] = [],
    ) -> Credential:
        """Create a new tunnel authtoken credential. This authtoken credential can be used to start a new tunnel session. The response to this API call is the only time the generated token is available. If you need it for future use, you must save it securely yourself.

        :param description: human-readable description of who or what will use the credential to authenticate. Optional, max 255 bytes.
        :param metadata: arbitrary user-defined machine-readable data of this credential. Optional, max 4096 bytes.
        :param acl: optional list of ACL rules. If unspecified, the credential will have no restrictions. The only allowed ACL rule at this time is the ``bind`` rule. The ``bind`` rule allows the caller to restrict what domains and addresses the token is allowed to bind. For example, to allow the token to open a tunnel on example.ngrok.io your ACL would include the rule ``bind:example.ngrok.io``. Bind rules may specify a leading wildcard to match multiple domains with a common suffix. For example, you may specify a rule of ``bind:*.example.com`` which will allow ``x.example.com``, ``y.example.com``, ``*.example.com``, etc. A rule of ``'*'`` is equivalent to no acl at all and will explicitly permit all actions.

        https://ngrok.com/docs/api#api-credentials-create
        """
        path = "/credentials"
        result = self._client.http_client.post(
            path,
            dict(
                description=description,
                metadata=metadata,
                acl=acl,
            ),
        )
        return Credential(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """Delete a tunnel authtoken credential by ID

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-credentials-delete
        """
        path = "/credentials/{id}"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())

    def get(
        self,
        id: str,
    ) -> Credential:
        """Get detailed information about a tunnel authtoken credential

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-credentials-get
        """
        path = "/credentials/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return Credential(self._client, result)

    def list(
        self,
        before_id: str = None,
        limit: str = None,
    ) -> CredentialList:
        """List all tunnel authtoken credentials on this account

        :param before_id:
        :param limit:

        https://ngrok.com/docs/api#api-credentials-list
        """
        path = "/credentials"
        result = self._client.http_client.get(
            path,
            dict(
                before_id=before_id,
                limit=limit,
            ),
        )
        return CredentialList(self._client, result)

    def update(
        self,
        id: str,
        description: str = None,
        metadata: str = None,
        acl: Sequence[str] = None,
    ) -> Credential:
        """Update attributes of an tunnel authtoken credential by ID

        :param id:
        :param description: human-readable description of who or what will use the credential to authenticate. Optional, max 255 bytes.
        :param metadata: arbitrary user-defined machine-readable data of this credential. Optional, max 4096 bytes.
        :param acl: optional list of ACL rules. If unspecified, the credential will have no restrictions. The only allowed ACL rule at this time is the ``bind`` rule. The ``bind`` rule allows the caller to restrict what domains and addresses the token is allowed to bind. For example, to allow the token to open a tunnel on example.ngrok.io your ACL would include the rule ``bind:example.ngrok.io``. Bind rules may specify a leading wildcard to match multiple domains with a common suffix. For example, you may specify a rule of ``bind:*.example.com`` which will allow ``x.example.com``, ``y.example.com``, ``*.example.com``, etc. A rule of ``'*'`` is equivalent to no acl at all and will explicitly permit all actions.

        https://ngrok.com/docs/api#api-credentials-update
        """
        path = "/credentials/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.patch(
            path,
            dict(
                description=description,
                metadata=metadata,
                acl=acl,
            ),
        )
        return Credential(self._client, result)


class EndpointConfigurationsClient(object):
    """Endpoint Configurations are a reusable group of modules that encapsulate how
    traffic to a domain or address is handled. Endpoint configurations are only
    applied to Domains and TCP Addresses they have been attached to."""

    def __init__(self, client):
        self._client = client

    def create(
        self,
        type: str = "",
        description: str = "",
        metadata: str = "",
        circuit_breaker: EndpointCircuitBreaker = None,
        compression: EndpointCompression = None,
        request_headers: EndpointRequestHeaders = None,
        response_headers: EndpointResponseHeaders = None,
        ip_policy: EndpointIPPolicyMutate = None,
        mutual_tls: EndpointMutualTLSMutate = None,
        tls_termination: EndpointTLSTermination = None,
        webhook_validation: EndpointWebhookValidation = None,
        oauth: EndpointOAuth = None,
        logging: EndpointLoggingMutate = None,
        saml: EndpointSAMLMutate = None,
        oidc: EndpointOIDC = None,
    ) -> EndpointConfiguration:
        """Create a new endpoint configuration

        :param type: they type of traffic this endpoint configuration can be applied to. one of: ``http``, ``https``, ``tcp``
        :param description: human-readable description of what this endpoint configuration will be do when applied or what traffic it will be applied to. Optional, max 255 bytes
        :param metadata: arbitrary user-defined machine-readable data of this endpoint configuration. Optional, max 4096 bytes.
        :param circuit_breaker: circuit breaker module configuration or ``null``
        :param compression: compression module configuration or ``null``
        :param request_headers: request headers module configuration or ``null``
        :param response_headers: response headers module configuration or ``null``
        :param ip_policy: ip policy module configuration or ``null``
        :param mutual_tls: mutual TLS module configuration or ``null``
        :param tls_termination: TLS termination module configuration or ``null``
        :param webhook_validation: webhook validation module configuration or ``null``
        :param oauth: oauth module configuration or ``null``
        :param logging: logging module configuration or ``null``
        :param saml: saml module configuration or ``null``
        :param oidc: oidc module configuration or ``null``

        https://ngrok.com/docs/api#api-endpoint-configurations-create
        """
        path = "/endpoint_configurations"
        result = self._client.http_client.post(
            path,
            dict(
                type=type,
                description=description,
                metadata=metadata,
                circuit_breaker=circuit_breaker,
                compression=compression,
                request_headers=request_headers,
                response_headers=response_headers,
                ip_policy=ip_policy,
                mutual_tls=mutual_tls,
                tls_termination=tls_termination,
                webhook_validation=webhook_validation,
                oauth=oauth,
                logging=logging,
                saml=saml,
                oidc=oidc,
            ),
        )
        return EndpointConfiguration(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """Delete an endpoint configuration. This operation will fail if the endpoint configuration is still referenced by any reserved domain or reserved address.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-configurations-delete
        """
        path = "/endpoint_configurations/{id}"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())

    def get(
        self,
        id: str,
    ) -> EndpointConfiguration:
        """Returns detailed information about an endpoint configuration

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-configurations-get
        """
        path = "/endpoint_configurations/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return EndpointConfiguration(self._client, result)

    def list(
        self,
        before_id: str = None,
        limit: str = None,
    ) -> EndpointConfigurationList:
        """Returns a list of all endpoint configurations on this account

        :param before_id:
        :param limit:

        https://ngrok.com/docs/api#api-endpoint-configurations-list
        """
        path = "/endpoint_configurations"
        result = self._client.http_client.get(
            path,
            dict(
                before_id=before_id,
                limit=limit,
            ),
        )
        return EndpointConfigurationList(self._client, result)

    def update(
        self,
        id: str,
        description: str = None,
        metadata: str = None,
        circuit_breaker: EndpointCircuitBreaker = None,
        compression: EndpointCompression = None,
        request_headers: EndpointRequestHeaders = None,
        response_headers: EndpointResponseHeaders = None,
        ip_policy: EndpointIPPolicyMutate = None,
        mutual_tls: EndpointMutualTLSMutate = None,
        tls_termination: EndpointTLSTermination = None,
        webhook_validation: EndpointWebhookValidation = None,
        oauth: EndpointOAuth = None,
        logging: EndpointLoggingMutate = None,
        saml: EndpointSAMLMutate = None,
        oidc: EndpointOIDC = None,
    ) -> EndpointConfiguration:
        """Updates an endpoint configuration. If a module is not specified in the update, it will not be modified. However, each module configuration that is specified will completely replace the existing value. There is no way to delete an existing module via this API, instead use the delete module API.

        :param id: unique identifier of this endpoint configuration
        :param description: human-readable description of what this endpoint configuration will be do when applied or what traffic it will be applied to. Optional, max 255 bytes
        :param metadata: arbitrary user-defined machine-readable data of this endpoint configuration. Optional, max 4096 bytes.
        :param circuit_breaker: circuit breaker module configuration or ``null``
        :param compression: compression module configuration or ``null``
        :param request_headers: request headers module configuration or ``null``
        :param response_headers: response headers module configuration or ``null``
        :param ip_policy: ip policy module configuration or ``null``
        :param mutual_tls: mutual TLS module configuration or ``null``
        :param tls_termination: TLS termination module configuration or ``null``
        :param webhook_validation: webhook validation module configuration or ``null``
        :param oauth: oauth module configuration or ``null``
        :param logging: logging module configuration or ``null``
        :param saml: saml module configuration or ``null``
        :param oidc: oidc module configuration or ``null``

        https://ngrok.com/docs/api#api-endpoint-configurations-update
        """
        path = "/endpoint_configurations/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.patch(
            path,
            dict(
                description=description,
                metadata=metadata,
                circuit_breaker=circuit_breaker,
                compression=compression,
                request_headers=request_headers,
                response_headers=response_headers,
                ip_policy=ip_policy,
                mutual_tls=mutual_tls,
                tls_termination=tls_termination,
                webhook_validation=webhook_validation,
                oauth=oauth,
                logging=logging,
                saml=saml,
                oidc=oidc,
            ),
        )
        return EndpointConfiguration(self._client, result)


class EventStreamsClient(object):
    def __init__(self, client):
        self._client = client

    def create(
        self,
        metadata: str = "",
        description: str = "",
        fields: Sequence[str] = [],
        event_type: str = "",
        destination_ids: Sequence[str] = [],
        sampling_rate: float = 0,
    ) -> EventStream:
        """Create a new Event Stream. It will not apply to anything until you associate it with one or more Endpoint Configs.

        :param metadata: Arbitrary user-defined machine-readable data of this Event Stream. Optional, max 4096 bytes.
        :param description: Human-readable description of the Event Stream. Optional, max 255 bytes.
        :param fields: A list of protocol-specific fields you want to collect on each event.
        :param event_type: The protocol that determines which events will be collected. Supported values are ``tcp_connection_closed`` and ``http_request_complete``.
        :param destination_ids: A list of Event Destination IDs which should be used for this Event Stream. Event Streams are required to have at least one Event Destination.
        :param sampling_rate: The percentage of all events you would like to capture. Valid values range from 0.01, representing 1% of all events to 1.00, representing 100% of all events.

        https://ngrok.com/docs/api#api-event-streams-create
        """
        path = "/event_streams"
        result = self._client.http_client.post(
            path,
            dict(
                metadata=metadata,
                description=description,
                fields=fields,
                event_type=event_type,
                destination_ids=destination_ids,
                sampling_rate=sampling_rate,
            ),
        )
        return EventStream(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """Delete an Event Stream. Associated Event Destinations will be preserved.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-event-streams-delete
        """
        path = "/event_streams/{id}"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())

    def get(
        self,
        id: str,
    ) -> EventStream:
        """Get detailed information about an Event Stream by ID.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-event-streams-get
        """
        path = "/event_streams/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return EventStream(self._client, result)

    def list(
        self,
        before_id: str = None,
        limit: str = None,
    ) -> EventStreamList:
        """List all Event Streams available on this account.

        :param before_id:
        :param limit:

        https://ngrok.com/docs/api#api-event-streams-list
        """
        path = "/event_streams"
        result = self._client.http_client.get(
            path,
            dict(
                before_id=before_id,
                limit=limit,
            ),
        )
        return EventStreamList(self._client, result)

    def update(
        self,
        id: str,
        metadata: str = None,
        description: str = None,
        fields: Sequence[str] = None,
        destination_ids: Sequence[str] = None,
        sampling_rate: float = None,
    ) -> EventStream:
        """Update attributes of an Event Stream by ID.

        :param id: Unique identifier for this Event Stream.
        :param metadata: Arbitrary user-defined machine-readable data of this Event Stream. Optional, max 4096 bytes.
        :param description: Human-readable description of the Event Stream. Optional, max 255 bytes.
        :param fields: A list of protocol-specific fields you want to collect on each event.
        :param destination_ids: A list of Event Destination IDs which should be used for this Event Stream. Event Streams are required to have at least one Event Destination.
        :param sampling_rate: The percentage of all events you would like to capture. Valid values range from 0.01, representing 1% of all events to 1.00, representing 100% of all events.

        https://ngrok.com/docs/api#api-event-streams-update
        """
        path = "/event_streams/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.patch(
            path,
            dict(
                metadata=metadata,
                description=description,
                fields=fields,
                destination_ids=destination_ids,
                sampling_rate=sampling_rate,
            ),
        )
        return EventStream(self._client, result)


class EventDestinationsClient(object):
    def __init__(self, client):
        self._client = client

    def create(
        self,
        metadata: str = "",
        description: str = "",
        format: str = "",
        target: EventTarget = None,
    ) -> EventDestination:
        """Create a new Event Destination. It will not apply to anything until it is associated with an Event Stream, and that Event Stream is associated with an Endpoint Config.

        :param metadata: Arbitrary user-defined machine-readable data of this Event Destination. Optional, max 4096 bytes.
        :param description: Human-readable description of the Event Destination. Optional, max 255 bytes.
        :param format: The output format you would like to serialize events into when sending to their target. Currently the only accepted value is ``JSON``.
        :param target: An object that encapsulates where and how to send your events. An event destination must contain exactly one of the following objects, leaving the rest null: ``kinesis``, ``firehose``, ``cloudwatch_logs``, or ``s3``.

        https://ngrok.com/docs/api#api-event-destinations-create
        """
        path = "/event_destinations"
        result = self._client.http_client.post(
            path,
            dict(
                metadata=metadata,
                description=description,
                format=format,
                target=target,
            ),
        )
        return EventDestination(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """Delete an Event Destination. If the Event Destination is still referenced by an Event Stream, this will throw an error until that Event Stream has removed that reference.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-event-destinations-delete
        """
        path = "/event_destinations/{id}"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())

    def get(
        self,
        id: str,
    ) -> EventDestination:
        """Get detailed information about an Event Destination by ID.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-event-destinations-get
        """
        path = "/event_destinations/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return EventDestination(self._client, result)

    def list(
        self,
        before_id: str = None,
        limit: str = None,
    ) -> EventDestinationList:
        """List all Event Destinations on this account.

        :param before_id:
        :param limit:

        https://ngrok.com/docs/api#api-event-destinations-list
        """
        path = "/event_destinations"
        result = self._client.http_client.get(
            path,
            dict(
                before_id=before_id,
                limit=limit,
            ),
        )
        return EventDestinationList(self._client, result)

    def update(
        self,
        id: str,
        metadata: str = None,
        description: str = None,
        format: str = None,
        target: EventTarget = None,
    ) -> EventDestination:
        """Update attributes of an Event Destination.

        :param id: Unique identifier for this Event Destination.
        :param metadata: Arbitrary user-defined machine-readable data of this Event Destination. Optional, max 4096 bytes.
        :param description: Human-readable description of the Event Destination. Optional, max 255 bytes.
        :param format: The output format you would like to serialize events into when sending to their target. Currently the only accepted value is ``JSON``.
        :param target: An object that encapsulates where and how to send your events. An event destination must contain exactly one of the following objects, leaving the rest null: ``kinesis``, ``firehose``, ``cloudwatch_logs``, or ``s3``.

        https://ngrok.com/docs/api#api-event-destinations-update
        """
        path = "/event_destinations/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.patch(
            path,
            dict(
                metadata=metadata,
                description=description,
                format=format,
                target=target,
            ),
        )
        return EventDestination(self._client, result)


class EventSubscriptionsClient(object):
    def __init__(self, client):
        self._client = client

    def create(
        self,
        metadata: str = "",
        description: str = "",
        sources: Sequence[EventSourceReplace] = [],
        destination_ids: Sequence[str] = [],
    ) -> EventSubscription:
        """Create an Event Subscription.

        :param metadata: Arbitrary customer supplied information intended to be machine readable. Optional, max 4096 chars.
        :param description: Arbitrary customer supplied information intended to be human readable. Optional, max 255 chars.
        :param sources: Sources containing the types for which this event subscription will trigger
        :param destination_ids: A list of Event Destination IDs which should be used for this Event Stream. Event Streams are required to have at least one Event Destination.

        https://ngrok.com/docs/api#api-event-subscriptions-create
        """
        path = "/event_subscriptions"
        result = self._client.http_client.post(
            path,
            dict(
                metadata=metadata,
                description=description,
                sources=sources,
                destination_ids=destination_ids,
            ),
        )
        return EventSubscription(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """Delete an Event Subscription.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-event-subscriptions-delete
        """
        path = "/event_subscriptions/{id}"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())

    def get(
        self,
        id: str,
    ) -> EventSubscription:
        """Get an Event Subscription by ID.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-event-subscriptions-get
        """
        path = "/event_subscriptions/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return EventSubscription(self._client, result)

    def list(
        self,
        before_id: str = None,
        limit: str = None,
    ) -> EventSubscriptionList:
        """List this Account's Event Subscriptions.

        :param before_id:
        :param limit:

        https://ngrok.com/docs/api#api-event-subscriptions-list
        """
        path = "/event_subscriptions"
        result = self._client.http_client.get(
            path,
            dict(
                before_id=before_id,
                limit=limit,
            ),
        )
        return EventSubscriptionList(self._client, result)

    def update(
        self,
        id: str,
        metadata: str = None,
        description: str = None,
        sources: Sequence[EventSourceReplace] = None,
        destination_ids: Sequence[str] = None,
    ) -> EventSubscription:
        """Update an Event Subscription.

        :param id: Unique identifier for this Event Subscription.
        :param metadata: Arbitrary customer supplied information intended to be machine readable. Optional, max 4096 chars.
        :param description: Arbitrary customer supplied information intended to be human readable. Optional, max 255 chars.
        :param sources: Sources containing the types for which this event subscription will trigger
        :param destination_ids: A list of Event Destination IDs which should be used for this Event Stream. Event Streams are required to have at least one Event Destination.

        https://ngrok.com/docs/api#api-event-subscriptions-update
        """
        path = "/event_subscriptions/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.patch(
            path,
            dict(
                metadata=metadata,
                description=description,
                sources=sources,
                destination_ids=destination_ids,
            ),
        )
        return EventSubscription(self._client, result)


class EventSourcesClient(object):
    def __init__(self, client):
        self._client = client

    def create(
        self,
        subscription_id: str,
        type: str = "",
    ) -> EventSource:
        """Add an additional type for which this event subscription will trigger

        :param subscription_id: The unique identifier for the Event Subscription that this Event Source is attached to.
        :param type: Type of event for which an event subscription will trigger

        https://ngrok.com/docs/api#api-event-sources-create
        """
        path = "/event_subscriptions/{subscription_id}/sources"
        path = path.format(
            subscription_id=subscription_id,
        )
        result = self._client.http_client.post(
            path,
            dict(
                type=type,
            ),
        )
        return EventSource(self._client, result)

    def delete(
        self,
        subscription_id: str,
        type: str,
    ):
        """Remove a type for which this event subscription will trigger

        :param subscription_id: The unique identifier for the Event Subscription that this Event Source is attached to.
        :param type: Type of event for which an event subscription will trigger

        https://ngrok.com/docs/api#api-event-sources-delete
        """
        path = "/event_subscriptions/{subscription_id}/sources/{type}"
        path = path.format(
            subscription_id=subscription_id,
            type=type,
        )
        self._client.http_client.delete(path, dict())

    def get(
        self,
        subscription_id: str,
        type: str,
    ) -> EventSource:
        """Get the details for a given type that triggers for the given event subscription

        :param subscription_id: The unique identifier for the Event Subscription that this Event Source is attached to.
        :param type: Type of event for which an event subscription will trigger

        https://ngrok.com/docs/api#api-event-sources-get
        """
        path = "/event_subscriptions/{subscription_id}/sources/{type}"
        path = path.format(
            subscription_id=subscription_id,
            type=type,
        )
        result = self._client.http_client.get(path, dict())
        return EventSource(self._client, result)

    def list(
        self,
        subscription_id: str,
    ) -> EventSourceList:
        """List the types for which this event subscription will trigger

        :param subscription_id: The unique identifier for the Event Subscription that this Event Source is attached to.

        https://ngrok.com/docs/api#api-event-sources-list
        """
        path = "/event_subscriptions/{subscription_id}/sources"
        path = path.format(
            subscription_id=subscription_id,
        )
        result = self._client.http_client.get(path, dict())
        return EventSourceList(self._client, result)

    def update(
        self,
        subscription_id: str,
        type: str,
    ) -> EventSource:
        """Update the type for which this event subscription will trigger

        :param subscription_id: The unique identifier for the Event Subscription that this Event Source is attached to.
        :param type: Type of event for which an event subscription will trigger

        https://ngrok.com/docs/api#api-event-sources-update
        """
        path = "/event_subscriptions/{subscription_id}/sources/{type}"
        path = path.format(
            subscription_id=subscription_id,
            type=type,
        )
        result = self._client.http_client.patch(path, dict())
        return EventSource(self._client, result)


class IPPoliciesClient(object):
    """IP Policies are reusable groups of CIDR ranges with an ``allow`` or ``deny``
    action. They can be attached to endpoints via the Endpoint Configuration IP
    Policy module. They can also be used with IP Restrictions to control source
    IP ranges that can start tunnel sessions and connect to the API and dashboard."""

    def __init__(self, client):
        self._client = client

    def create(
        self,
        action: str,
        description: str = "",
        metadata: str = "",
    ) -> IPPolicy:
        """Create a new IP policy. It will not apply to any traffic until you associate to a traffic source via an endpoint configuration or IP restriction.

        :param description: human-readable description of the source IPs of this IP policy. optional, max 255 bytes.
        :param metadata: arbitrary user-defined machine-readable data of this IP policy. optional, max 4096 bytes.
        :param action: the IP policy action. Supported values are ``allow`` or ``deny``

        https://ngrok.com/docs/api#api-ip-policies-create
        """
        path = "/ip_policies"
        result = self._client.http_client.post(
            path,
            dict(
                description=description,
                metadata=metadata,
                action=action,
            ),
        )
        return IPPolicy(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """Delete an IP policy. If the IP policy is referenced by another object for the purposes of traffic restriction it will be treated as if the IP policy remains but has zero rules.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-ip-policies-delete
        """
        path = "/ip_policies/{id}"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())

    def get(
        self,
        id: str,
    ) -> IPPolicy:
        """Get detailed information about an IP policy by ID.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-ip-policies-get
        """
        path = "/ip_policies/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return IPPolicy(self._client, result)

    def list(
        self,
        before_id: str = None,
        limit: str = None,
    ) -> IPPolicyList:
        """List all IP policies on this account

        :param before_id:
        :param limit:

        https://ngrok.com/docs/api#api-ip-policies-list
        """
        path = "/ip_policies"
        result = self._client.http_client.get(
            path,
            dict(
                before_id=before_id,
                limit=limit,
            ),
        )
        return IPPolicyList(self._client, result)

    def update(
        self,
        id: str,
        description: str = None,
        metadata: str = None,
    ) -> IPPolicy:
        """Update attributes of an IP policy by ID

        :param id:
        :param description: human-readable description of the source IPs of this IP policy. optional, max 255 bytes.
        :param metadata: arbitrary user-defined machine-readable data of this IP policy. optional, max 4096 bytes.

        https://ngrok.com/docs/api#api-ip-policies-update
        """
        path = "/ip_policies/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.patch(
            path,
            dict(
                description=description,
                metadata=metadata,
            ),
        )
        return IPPolicy(self._client, result)


class IPPolicyRulesClient(object):
    """IP Policy Rules are the IPv4 or IPv6 CIDRs entries that
    make up an IP Policy."""

    def __init__(self, client):
        self._client = client

    def create(
        self,
        cidr: str,
        ip_policy_id: str,
        description: str = "",
        metadata: str = "",
    ) -> IPPolicyRule:
        """Create a new IP policy rule attached to an IP Policy.

        :param description: human-readable description of the source IPs of this IP rule. optional, max 255 bytes.
        :param metadata: arbitrary user-defined machine-readable data of this IP policy rule. optional, max 4096 bytes.
        :param cidr: an IP or IP range specified in CIDR notation. IPv4 and IPv6 are both supported.
        :param ip_policy_id: ID of the IP policy this IP policy rule will be attached to

        https://ngrok.com/docs/api#api-ip-policy-rules-create
        """
        path = "/ip_policy_rules"
        result = self._client.http_client.post(
            path,
            dict(
                description=description,
                metadata=metadata,
                cidr=cidr,
                ip_policy_id=ip_policy_id,
            ),
        )
        return IPPolicyRule(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """Delete an IP policy rule.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-ip-policy-rules-delete
        """
        path = "/ip_policy_rules/{id}"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())

    def get(
        self,
        id: str,
    ) -> IPPolicyRule:
        """Get detailed information about an IP policy rule by ID.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-ip-policy-rules-get
        """
        path = "/ip_policy_rules/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return IPPolicyRule(self._client, result)

    def list(
        self,
        before_id: str = None,
        limit: str = None,
    ) -> IPPolicyRuleList:
        """List all IP policy rules on this account

        :param before_id:
        :param limit:

        https://ngrok.com/docs/api#api-ip-policy-rules-list
        """
        path = "/ip_policy_rules"
        result = self._client.http_client.get(
            path,
            dict(
                before_id=before_id,
                limit=limit,
            ),
        )
        return IPPolicyRuleList(self._client, result)

    def update(
        self,
        id: str,
        description: str = None,
        metadata: str = None,
        cidr: str = None,
    ) -> IPPolicyRule:
        """Update attributes of an IP policy rule by ID

        :param id:
        :param description: human-readable description of the source IPs of this IP rule. optional, max 255 bytes.
        :param metadata: arbitrary user-defined machine-readable data of this IP policy rule. optional, max 4096 bytes.
        :param cidr: an IP or IP range specified in CIDR notation. IPv4 and IPv6 are both supported.

        https://ngrok.com/docs/api#api-ip-policy-rules-update
        """
        path = "/ip_policy_rules/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.patch(
            path,
            dict(
                description=description,
                metadata=metadata,
                cidr=cidr,
            ),
        )
        return IPPolicyRule(self._client, result)


class IPRestrictionsClient(object):
    """An IP restriction is a restriction placed on the CIDRs that are allowed to
    initiate traffic to a specific aspect of your ngrok account. An IP
    restriction has a type which defines the ingress it applies to. IP
    restrictions can be used to enforce the source IPs that can make API
    requests, log in to the dashboard, start ngrok agents, and connect to your
    public-facing endpoints."""

    def __init__(self, client):
        self._client = client

    def create(
        self,
        type: str,
        ip_policy_ids: Sequence[str],
        description: str = "",
        metadata: str = "",
        enforced: bool = False,
    ) -> IPRestriction:
        """Create a new IP restriction

        :param description: human-readable description of this IP restriction. optional, max 255 bytes.
        :param metadata: arbitrary user-defined machine-readable data of this IP restriction. optional, max 4096 bytes.
        :param enforced: true if the IP restriction will be enforced. if false, only warnings will be issued
        :param type: the type of IP restriction. this defines what traffic will be restricted with the attached policies. four values are currently supported: ``dashboard``, ``api``, ``agent``, and ``endpoints``
        :param ip_policy_ids: the set of IP policy identifiers that are used to enforce the restriction

        https://ngrok.com/docs/api#api-ip-restrictions-create
        """
        path = "/ip_restrictions"
        result = self._client.http_client.post(
            path,
            dict(
                description=description,
                metadata=metadata,
                enforced=enforced,
                type=type,
                ip_policy_ids=ip_policy_ids,
            ),
        )
        return IPRestriction(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """Delete an IP restriction

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-ip-restrictions-delete
        """
        path = "/ip_restrictions/{id}"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())

    def get(
        self,
        id: str,
    ) -> IPRestriction:
        """Get detailed information about an IP restriction

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-ip-restrictions-get
        """
        path = "/ip_restrictions/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return IPRestriction(self._client, result)

    def list(
        self,
        before_id: str = None,
        limit: str = None,
    ) -> IPRestrictionList:
        """List all IP restrictions on this account

        :param before_id:
        :param limit:

        https://ngrok.com/docs/api#api-ip-restrictions-list
        """
        path = "/ip_restrictions"
        result = self._client.http_client.get(
            path,
            dict(
                before_id=before_id,
                limit=limit,
            ),
        )
        return IPRestrictionList(self._client, result)

    def update(
        self,
        id: str,
        description: str = None,
        metadata: str = None,
        enforced: bool = None,
        ip_policy_ids: Sequence[str] = [],
    ) -> IPRestriction:
        """Update attributes of an IP restriction by ID

        :param id:
        :param description: human-readable description of this IP restriction. optional, max 255 bytes.
        :param metadata: arbitrary user-defined machine-readable data of this IP restriction. optional, max 4096 bytes.
        :param enforced: true if the IP restriction will be enforced. if false, only warnings will be issued
        :param ip_policy_ids: the set of IP policy identifiers that are used to enforce the restriction

        https://ngrok.com/docs/api#api-ip-restrictions-update
        """
        path = "/ip_restrictions/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.patch(
            path,
            dict(
                description=description,
                metadata=metadata,
                enforced=enforced,
                ip_policy_ids=ip_policy_ids,
            ),
        )
        return IPRestriction(self._client, result)


class EndpointLoggingModuleClient(object):
    def __init__(self, client):
        self._client = client

    def replace(
        self,
        id: str,
        module: EndpointLoggingMutate = None,
    ) -> EndpointLogging:
        """

        :param id:
        :param module:

        https://ngrok.com/docs/api#api-endpoint-logging-module-replace
        """
        path = "/endpoint_configurations/{id}/logging"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.put(
            path,
            dict(
                module=module,
            ),
        )
        return EndpointLogging(self._client, result)

    def get(
        self,
        id: str,
    ) -> EndpointLogging:
        """

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-logging-module-get
        """
        path = "/endpoint_configurations/{id}/logging"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return EndpointLogging(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-logging-module-delete
        """
        path = "/endpoint_configurations/{id}/logging"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())


class EndpointCircuitBreakerModuleClient(object):
    def __init__(self, client):
        self._client = client

    def replace(
        self,
        id: str,
        module: EndpointCircuitBreaker = None,
    ) -> EndpointCircuitBreaker:
        """

        :param id:
        :param module:

        https://ngrok.com/docs/api#api-endpoint-circuit-breaker-module-replace
        """
        path = "/endpoint_configurations/{id}/circuit_breaker"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.put(
            path,
            dict(
                module=module,
            ),
        )
        return EndpointCircuitBreaker(self._client, result)

    def get(
        self,
        id: str,
    ) -> EndpointCircuitBreaker:
        """

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-circuit-breaker-module-get
        """
        path = "/endpoint_configurations/{id}/circuit_breaker"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return EndpointCircuitBreaker(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-circuit-breaker-module-delete
        """
        path = "/endpoint_configurations/{id}/circuit_breaker"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())


class EndpointCompressionModuleClient(object):
    def __init__(self, client):
        self._client = client

    def replace(
        self,
        id: str,
        module: EndpointCompression = None,
    ) -> EndpointCompression:
        """

        :param id:
        :param module:

        https://ngrok.com/docs/api#api-endpoint-compression-module-replace
        """
        path = "/endpoint_configurations/{id}/compression"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.put(
            path,
            dict(
                module=module,
            ),
        )
        return EndpointCompression(self._client, result)

    def get(
        self,
        id: str,
    ) -> EndpointCompression:
        """

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-compression-module-get
        """
        path = "/endpoint_configurations/{id}/compression"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return EndpointCompression(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-compression-module-delete
        """
        path = "/endpoint_configurations/{id}/compression"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())


class EndpointTLSTerminationModuleClient(object):
    def __init__(self, client):
        self._client = client

    def replace(
        self,
        id: str,
        module: EndpointTLSTermination = None,
    ) -> EndpointTLSTermination:
        """

        :param id:
        :param module:

        https://ngrok.com/docs/api#api-endpoint-tls-termination-module-replace
        """
        path = "/endpoint_configurations/{id}/tls_termination"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.put(
            path,
            dict(
                module=module,
            ),
        )
        return EndpointTLSTermination(self._client, result)

    def get(
        self,
        id: str,
    ) -> EndpointTLSTermination:
        """

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-tls-termination-module-get
        """
        path = "/endpoint_configurations/{id}/tls_termination"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return EndpointTLSTermination(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-tls-termination-module-delete
        """
        path = "/endpoint_configurations/{id}/tls_termination"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())


class EndpointIPPolicyModuleClient(object):
    def __init__(self, client):
        self._client = client

    def replace(
        self,
        id: str,
        module: EndpointIPPolicyMutate = None,
    ) -> EndpointIPPolicy:
        """

        :param id:
        :param module:

        https://ngrok.com/docs/api#api-endpoint-ip-policy-module-replace
        """
        path = "/endpoint_configurations/{id}/ip_policy"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.put(
            path,
            dict(
                module=module,
            ),
        )
        return EndpointIPPolicy(self._client, result)

    def get(
        self,
        id: str,
    ) -> EndpointIPPolicy:
        """

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-ip-policy-module-get
        """
        path = "/endpoint_configurations/{id}/ip_policy"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return EndpointIPPolicy(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-ip-policy-module-delete
        """
        path = "/endpoint_configurations/{id}/ip_policy"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())


class EndpointMutualTLSModuleClient(object):
    def __init__(self, client):
        self._client = client

    def replace(
        self,
        id: str,
        module: EndpointMutualTLSMutate = None,
    ) -> EndpointMutualTLS:
        """

        :param id:
        :param module:

        https://ngrok.com/docs/api#api-endpoint-mutual-tls-module-replace
        """
        path = "/endpoint_configurations/{id}/mutual_tls"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.put(
            path,
            dict(
                module=module,
            ),
        )
        return EndpointMutualTLS(self._client, result)

    def get(
        self,
        id: str,
    ) -> EndpointMutualTLS:
        """

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-mutual-tls-module-get
        """
        path = "/endpoint_configurations/{id}/mutual_tls"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return EndpointMutualTLS(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-mutual-tls-module-delete
        """
        path = "/endpoint_configurations/{id}/mutual_tls"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())


class EndpointRequestHeadersModuleClient(object):
    def __init__(self, client):
        self._client = client

    def replace(
        self,
        id: str,
        module: EndpointRequestHeaders = None,
    ) -> EndpointRequestHeaders:
        """

        :param id:
        :param module:

        https://ngrok.com/docs/api#api-endpoint-request-headers-module-replace
        """
        path = "/endpoint_configurations/{id}/request_headers"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.put(
            path,
            dict(
                module=module,
            ),
        )
        return EndpointRequestHeaders(self._client, result)

    def get(
        self,
        id: str,
    ) -> EndpointRequestHeaders:
        """

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-request-headers-module-get
        """
        path = "/endpoint_configurations/{id}/request_headers"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return EndpointRequestHeaders(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-request-headers-module-delete
        """
        path = "/endpoint_configurations/{id}/request_headers"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())


class EndpointResponseHeadersModuleClient(object):
    def __init__(self, client):
        self._client = client

    def replace(
        self,
        id: str,
        module: EndpointResponseHeaders = None,
    ) -> EndpointResponseHeaders:
        """

        :param id:
        :param module:

        https://ngrok.com/docs/api#api-endpoint-response-headers-module-replace
        """
        path = "/endpoint_configurations/{id}/response_headers"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.put(
            path,
            dict(
                module=module,
            ),
        )
        return EndpointResponseHeaders(self._client, result)

    def get(
        self,
        id: str,
    ) -> EndpointResponseHeaders:
        """

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-response-headers-module-get
        """
        path = "/endpoint_configurations/{id}/response_headers"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return EndpointResponseHeaders(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-response-headers-module-delete
        """
        path = "/endpoint_configurations/{id}/response_headers"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())


class EndpointOAuthModuleClient(object):
    def __init__(self, client):
        self._client = client

    def replace(
        self,
        id: str,
        module: EndpointOAuth = None,
    ) -> EndpointOAuth:
        """

        :param id:
        :param module:

        https://ngrok.com/docs/api#api-endpoint-o-auth-module-replace
        """
        path = "/endpoint_configurations/{id}/oauth"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.put(
            path,
            dict(
                module=module,
            ),
        )
        return EndpointOAuth(self._client, result)

    def get(
        self,
        id: str,
    ) -> EndpointOAuth:
        """

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-o-auth-module-get
        """
        path = "/endpoint_configurations/{id}/oauth"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return EndpointOAuth(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-o-auth-module-delete
        """
        path = "/endpoint_configurations/{id}/oauth"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())


class EndpointWebhookValidationModuleClient(object):
    def __init__(self, client):
        self._client = client

    def replace(
        self,
        id: str,
        module: EndpointWebhookValidation = None,
    ) -> EndpointWebhookValidation:
        """

        :param id:
        :param module:

        https://ngrok.com/docs/api#api-endpoint-webhook-validation-module-replace
        """
        path = "/endpoint_configurations/{id}/webhook_validation"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.put(
            path,
            dict(
                module=module,
            ),
        )
        return EndpointWebhookValidation(self._client, result)

    def get(
        self,
        id: str,
    ) -> EndpointWebhookValidation:
        """

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-webhook-validation-module-get
        """
        path = "/endpoint_configurations/{id}/webhook_validation"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return EndpointWebhookValidation(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-webhook-validation-module-delete
        """
        path = "/endpoint_configurations/{id}/webhook_validation"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())


class EndpointSAMLModuleClient(object):
    def __init__(self, client):
        self._client = client

    def replace(
        self,
        id: str,
        module: EndpointSAMLMutate = None,
    ) -> EndpointSAML:
        """

        :param id:
        :param module:

        https://ngrok.com/docs/api#api-endpoint-saml-module-replace
        """
        path = "/endpoint_configurations/{id}/saml"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.put(
            path,
            dict(
                module=module,
            ),
        )
        return EndpointSAML(self._client, result)

    def get(
        self,
        id: str,
    ) -> EndpointSAML:
        """

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-saml-module-get
        """
        path = "/endpoint_configurations/{id}/saml"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return EndpointSAML(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-saml-module-delete
        """
        path = "/endpoint_configurations/{id}/saml"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())


class EndpointOIDCModuleClient(object):
    def __init__(self, client):
        self._client = client

    def replace(
        self,
        id: str,
        module: EndpointOIDC = None,
    ) -> EndpointOIDC:
        """

        :param id:
        :param module:

        https://ngrok.com/docs/api#api-endpoint-oidc-module-replace
        """
        path = "/endpoint_configurations/{id}/oidc"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.put(
            path,
            dict(
                module=module,
            ),
        )
        return EndpointOIDC(self._client, result)

    def get(
        self,
        id: str,
    ) -> EndpointOIDC:
        """

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-oidc-module-get
        """
        path = "/endpoint_configurations/{id}/oidc"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return EndpointOIDC(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-endpoint-oidc-module-delete
        """
        path = "/endpoint_configurations/{id}/oidc"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())


class ReservedAddrsClient(object):
    """Reserved Addresses are TCP addresses that can be used to listen for traffic.
    TCP address hostnames and ports are assigned by ngrok, they cannot be
    chosen."""

    def __init__(self, client):
        self._client = client

    def create(
        self,
        description: str = "",
        metadata: str = "",
        region: str = "",
        endpoint_configuration_id: str = None,
    ) -> ReservedAddr:
        """Create a new reserved address.

        :param description: human-readable description of what this reserved address will be used for
        :param metadata: arbitrary user-defined machine-readable data of this reserved address. Optional, max 4096 bytes.
        :param region: reserve the address in this geographic ngrok datacenter. Optional, default is us. (au, eu, ap, us, jp, in, sa)
        :param endpoint_configuration_id: ID of an endpoint configuration of type tcp that will be used to handle inbound traffic to this address

        https://ngrok.com/docs/api#api-reserved-addrs-create
        """
        path = "/reserved_addrs"
        result = self._client.http_client.post(
            path,
            dict(
                description=description,
                metadata=metadata,
                region=region,
                endpoint_configuration_id=endpoint_configuration_id,
            ),
        )
        return ReservedAddr(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """Delete a reserved address.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-reserved-addrs-delete
        """
        path = "/reserved_addrs/{id}"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())

    def get(
        self,
        id: str,
    ) -> ReservedAddr:
        """Get the details of a reserved address.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-reserved-addrs-get
        """
        path = "/reserved_addrs/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return ReservedAddr(self._client, result)

    def list(
        self,
        before_id: str = None,
        limit: str = None,
    ) -> ReservedAddrList:
        """List all reserved addresses on this account.

        :param before_id:
        :param limit:

        https://ngrok.com/docs/api#api-reserved-addrs-list
        """
        path = "/reserved_addrs"
        result = self._client.http_client.get(
            path,
            dict(
                before_id=before_id,
                limit=limit,
            ),
        )
        return ReservedAddrList(self._client, result)

    def update(
        self,
        id: str,
        description: str = None,
        metadata: str = None,
        endpoint_configuration_id: str = None,
    ) -> ReservedAddr:
        """Update the attributes of a reserved address.

        :param id:
        :param description: human-readable description of what this reserved address will be used for
        :param metadata: arbitrary user-defined machine-readable data of this reserved address. Optional, max 4096 bytes.
        :param endpoint_configuration_id: ID of an endpoint configuration of type tcp that will be used to handle inbound traffic to this address

        https://ngrok.com/docs/api#api-reserved-addrs-update
        """
        path = "/reserved_addrs/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.patch(
            path,
            dict(
                description=description,
                metadata=metadata,
                endpoint_configuration_id=endpoint_configuration_id,
            ),
        )
        return ReservedAddr(self._client, result)

    def delete_endpoint_config(
        self,
        id: str,
    ):
        """Detach the endpoint configuration attached to a reserved address.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-reserved-addrs-delete-endpoint-config
        """
        path = "/reserved_addrs/{id}/endpoint_configuration"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())


class ReservedDomainsClient(object):
    """Reserved Domains are hostnames that you can listen for traffic on. Domains
    can be used to listen for http, https or tls traffic. You may use a domain
    that you own by creating a CNAME record specified in the returned resource.
    This CNAME record points traffic for that domain to ngrok's edge servers."""

    def __init__(self, client):
        self._client = client

    def create(
        self,
        name: str,
        region: str = "",
        description: str = "",
        metadata: str = "",
        http_endpoint_configuration_id: str = None,
        https_endpoint_configuration_id: str = None,
        certificate_id: str = None,
        certificate_management_policy: ReservedDomainCertPolicy = None,
    ) -> ReservedDomain:
        """Create a new reserved domain.

        :param name: the domain name to reserve. It may be a full domain name like app.example.com. If the name does not contain a '.' it will reserve that subdomain on ngrok.io.
        :param region: reserve the domain in this geographic ngrok datacenter. Optional, default is us. (au, eu, ap, us, jp, in, sa)
        :param description: human-readable description of what this reserved domain will be used for
        :param metadata: arbitrary user-defined machine-readable data of this reserved domain. Optional, max 4096 bytes.
        :param http_endpoint_configuration_id: ID of an endpoint configuration of type http that will be used to handle inbound http traffic to this domain
        :param https_endpoint_configuration_id: ID of an endpoint configuration of type https that will be used to handle inbound https traffic to this domain
        :param certificate_id: ID of a user-uploaded TLS certificate to use for connections to targeting this domain. Optional, mutually exclusive with ``certificate_management_policy``.
        :param certificate_management_policy: configuration for automatic management of TLS certificates for this domain, or null if automatic management is disabled. Optional, mutually exclusive with ``certificate_id``.

        https://ngrok.com/docs/api#api-reserved-domains-create
        """
        path = "/reserved_domains"
        result = self._client.http_client.post(
            path,
            dict(
                name=name,
                region=region,
                description=description,
                metadata=metadata,
                http_endpoint_configuration_id=http_endpoint_configuration_id,
                https_endpoint_configuration_id=https_endpoint_configuration_id,
                certificate_id=certificate_id,
                certificate_management_policy=certificate_management_policy,
            ),
        )
        return ReservedDomain(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """Delete a reserved domain.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-reserved-domains-delete
        """
        path = "/reserved_domains/{id}"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())

    def get(
        self,
        id: str,
    ) -> ReservedDomain:
        """Get the details of a reserved domain.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-reserved-domains-get
        """
        path = "/reserved_domains/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return ReservedDomain(self._client, result)

    def list(
        self,
        before_id: str = None,
        limit: str = None,
    ) -> ReservedDomainList:
        """List all reserved domains on this account.

        :param before_id:
        :param limit:

        https://ngrok.com/docs/api#api-reserved-domains-list
        """
        path = "/reserved_domains"
        result = self._client.http_client.get(
            path,
            dict(
                before_id=before_id,
                limit=limit,
            ),
        )
        return ReservedDomainList(self._client, result)

    def update(
        self,
        id: str,
        description: str = None,
        metadata: str = None,
        http_endpoint_configuration_id: str = None,
        https_endpoint_configuration_id: str = None,
        certificate_id: str = None,
        certificate_management_policy: ReservedDomainCertPolicy = None,
    ) -> ReservedDomain:
        """Update the attributes of a reserved domain.

        :param id:
        :param description: human-readable description of what this reserved domain will be used for
        :param metadata: arbitrary user-defined machine-readable data of this reserved domain. Optional, max 4096 bytes.
        :param http_endpoint_configuration_id: ID of an endpoint configuration of type http that will be used to handle inbound http traffic to this domain
        :param https_endpoint_configuration_id: ID of an endpoint configuration of type https that will be used to handle inbound https traffic to this domain
        :param certificate_id: ID of a user-uploaded TLS certificate to use for connections to targeting this domain. Optional, mutually exclusive with ``certificate_management_policy``.
        :param certificate_management_policy: configuration for automatic management of TLS certificates for this domain, or null if automatic management is disabled. Optional, mutually exclusive with ``certificate_id``.

        https://ngrok.com/docs/api#api-reserved-domains-update
        """
        path = "/reserved_domains/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.patch(
            path,
            dict(
                description=description,
                metadata=metadata,
                http_endpoint_configuration_id=http_endpoint_configuration_id,
                https_endpoint_configuration_id=https_endpoint_configuration_id,
                certificate_id=certificate_id,
                certificate_management_policy=certificate_management_policy,
            ),
        )
        return ReservedDomain(self._client, result)

    def delete_certificate_management_policy(
        self,
        id: str,
    ):
        """Detach the certificate management policy attached to a reserved domain.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-reserved-domains-delete-certificate-management-policy
        """
        path = "/reserved_domains/{id}/certificate_management_policy"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())

    def delete_certificate(
        self,
        id: str,
    ):
        """Detach the certificate attached to a reserved domain.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-reserved-domains-delete-certificate
        """
        path = "/reserved_domains/{id}/certificate"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())

    def delete_http_endpoint_config(
        self,
        id: str,
    ):
        """Detach the http endpoint configuration attached to a reserved domain.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-reserved-domains-delete-http-endpoint-config
        """
        path = "/reserved_domains/{id}/http_endpoint_configuration"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())

    def delete_https_endpoint_config(
        self,
        id: str,
    ):
        """Detach the https endpoint configuration attached to a reserved domain.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-reserved-domains-delete-https-endpoint-config
        """
        path = "/reserved_domains/{id}/https_endpoint_configuration"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())


class SSHCertificateAuthoritiesClient(object):
    """An SSH Certificate Authority is a pair of an SSH Certificate and its private
    key that can be used to sign other SSH host and user certificates."""

    def __init__(self, client):
        self._client = client

    def create(
        self,
        description: str = "",
        metadata: str = "",
        private_key_type: str = "",
        elliptic_curve: str = "",
        key_size: int = 0,
    ) -> SSHCertificateAuthority:
        """Create a new SSH Certificate Authority

        :param description: human-readable description of this SSH Certificate Authority. optional, max 255 bytes.
        :param metadata: arbitrary user-defined machine-readable data of this SSH Certificate Authority. optional, max 4096 bytes.
        :param private_key_type: the type of private key to generate. one of ``rsa``, ``ecdsa``, ``ed25519``
        :param elliptic_curve: the type of elliptic curve to use when creating an ECDSA key
        :param key_size: the key size to use when creating an RSA key. one of ``2048`` or ``4096``

        https://ngrok.com/docs/api#api-ssh-certificate-authorities-create
        """
        path = "/ssh_certificate_authorities"
        result = self._client.http_client.post(
            path,
            dict(
                description=description,
                metadata=metadata,
                private_key_type=private_key_type,
                elliptic_curve=elliptic_curve,
                key_size=key_size,
            ),
        )
        return SSHCertificateAuthority(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """Delete an SSH Certificate Authority

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-ssh-certificate-authorities-delete
        """
        path = "/ssh_certificate_authorities/{id}"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())

    def get(
        self,
        id: str,
    ) -> SSHCertificateAuthority:
        """Get detailed information about an SSH Certficate Authority

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-ssh-certificate-authorities-get
        """
        path = "/ssh_certificate_authorities/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return SSHCertificateAuthority(self._client, result)

    def list(
        self,
        before_id: str = None,
        limit: str = None,
    ) -> SSHCertificateAuthorityList:
        """List all SSH Certificate Authorities on this account

        :param before_id:
        :param limit:

        https://ngrok.com/docs/api#api-ssh-certificate-authorities-list
        """
        path = "/ssh_certificate_authorities"
        result = self._client.http_client.get(
            path,
            dict(
                before_id=before_id,
                limit=limit,
            ),
        )
        return SSHCertificateAuthorityList(self._client, result)

    def update(
        self,
        id: str,
        description: str = None,
        metadata: str = None,
    ) -> SSHCertificateAuthority:
        """Update an SSH Certificate Authority

        :param id:
        :param description: human-readable description of this SSH Certificate Authority. optional, max 255 bytes.
        :param metadata: arbitrary user-defined machine-readable data of this SSH Certificate Authority. optional, max 4096 bytes.

        https://ngrok.com/docs/api#api-ssh-certificate-authorities-update
        """
        path = "/ssh_certificate_authorities/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.patch(
            path,
            dict(
                description=description,
                metadata=metadata,
            ),
        )
        return SSHCertificateAuthority(self._client, result)


class SSHCredentialsClient(object):
    """SSH Credentials are SSH public keys that can be used to start SSH tunnels
    via the ngrok SSH tunnel gateway."""

    def __init__(self, client):
        self._client = client

    def create(
        self,
        public_key: str,
        description: str = "",
        metadata: str = "",
        acl: Sequence[str] = [],
    ) -> SSHCredential:
        """Create a new ssh_credential from an uploaded public SSH key. This ssh credential can be used to start new tunnels via ngrok's SSH gateway.

        :param description: human-readable description of who or what will use the ssh credential to authenticate. Optional, max 255 bytes.
        :param metadata: arbitrary user-defined machine-readable data of this ssh credential. Optional, max 4096 bytes.
        :param acl: optional list of ACL rules. If unspecified, the credential will have no restrictions. The only allowed ACL rule at this time is the ``bind`` rule. The ``bind`` rule allows the caller to restrict what domains and addresses the token is allowed to bind. For example, to allow the token to open a tunnel on example.ngrok.io your ACL would include the rule ``bind:example.ngrok.io``. Bind rules may specify a leading wildcard to match multiple domains with a common suffix. For example, you may specify a rule of ``bind:*.example.com`` which will allow ``x.example.com``, ``y.example.com``, ``*.example.com``, etc. A rule of ``'*'`` is equivalent to no acl at all and will explicitly permit all actions.
        :param public_key: the PEM-encoded public key of the SSH keypair that will be used to authenticate

        https://ngrok.com/docs/api#api-ssh-credentials-create
        """
        path = "/ssh_credentials"
        result = self._client.http_client.post(
            path,
            dict(
                description=description,
                metadata=metadata,
                acl=acl,
                public_key=public_key,
            ),
        )
        return SSHCredential(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """Delete an ssh_credential by ID

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-ssh-credentials-delete
        """
        path = "/ssh_credentials/{id}"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())

    def get(
        self,
        id: str,
    ) -> SSHCredential:
        """Get detailed information about an ssh_credential

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-ssh-credentials-get
        """
        path = "/ssh_credentials/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return SSHCredential(self._client, result)

    def list(
        self,
        before_id: str = None,
        limit: str = None,
    ) -> SSHCredentialList:
        """List all ssh credentials on this account

        :param before_id:
        :param limit:

        https://ngrok.com/docs/api#api-ssh-credentials-list
        """
        path = "/ssh_credentials"
        result = self._client.http_client.get(
            path,
            dict(
                before_id=before_id,
                limit=limit,
            ),
        )
        return SSHCredentialList(self._client, result)

    def update(
        self,
        id: str,
        description: str = None,
        metadata: str = None,
        acl: Sequence[str] = None,
    ) -> SSHCredential:
        """Update attributes of an ssh_credential by ID

        :param id:
        :param description: human-readable description of who or what will use the ssh credential to authenticate. Optional, max 255 bytes.
        :param metadata: arbitrary user-defined machine-readable data of this ssh credential. Optional, max 4096 bytes.
        :param acl: optional list of ACL rules. If unspecified, the credential will have no restrictions. The only allowed ACL rule at this time is the ``bind`` rule. The ``bind`` rule allows the caller to restrict what domains and addresses the token is allowed to bind. For example, to allow the token to open a tunnel on example.ngrok.io your ACL would include the rule ``bind:example.ngrok.io``. Bind rules may specify a leading wildcard to match multiple domains with a common suffix. For example, you may specify a rule of ``bind:*.example.com`` which will allow ``x.example.com``, ``y.example.com``, ``*.example.com``, etc. A rule of ``'*'`` is equivalent to no acl at all and will explicitly permit all actions.

        https://ngrok.com/docs/api#api-ssh-credentials-update
        """
        path = "/ssh_credentials/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.patch(
            path,
            dict(
                description=description,
                metadata=metadata,
                acl=acl,
            ),
        )
        return SSHCredential(self._client, result)


class SSHHostCertificatesClient(object):
    """SSH Host Certificates along with the corresponding private key allows an SSH
    server to assert its authenticity to connecting SSH clients who trust the
    SSH Certificate Authority that was used to sign the certificate."""

    def __init__(self, client):
        self._client = client

    def create(
        self,
        ssh_certificate_authority_id: str,
        public_key: str,
        principals: Sequence[str] = [],
        valid_after: str = "",
        valid_until: str = "",
        description: str = "",
        metadata: str = "",
    ) -> SSHHostCertificate:
        """Create a new SSH Host Certificate

        :param ssh_certificate_authority_id: the ssh certificate authority that is used to sign this ssh host certificate
        :param public_key: a public key in OpenSSH Authorized Keys format that this certificate signs
        :param principals: the list of principals included in the ssh host certificate. This is the list of hostnames and/or IP addresses that are authorized to serve SSH traffic with this certificate. Dangerously, if no principals are specified, this certificate is considered valid for all hosts.
        :param valid_after: The time when the host certificate becomes valid, in RFC 3339 format. Defaults to the current time if unspecified.
        :param valid_until: The time when this host certificate becomes invalid, in RFC 3339 format. If unspecified, a default value of one year in the future will be used. The OpenSSH certificates RFC calls this ``valid_before``.
        :param description: human-readable description of this SSH Host Certificate. optional, max 255 bytes.
        :param metadata: arbitrary user-defined machine-readable data of this SSH Host Certificate. optional, max 4096 bytes.

        https://ngrok.com/docs/api#api-ssh-host-certificates-create
        """
        path = "/ssh_host_certificates"
        result = self._client.http_client.post(
            path,
            dict(
                ssh_certificate_authority_id=ssh_certificate_authority_id,
                public_key=public_key,
                principals=principals,
                valid_after=valid_after,
                valid_until=valid_until,
                description=description,
                metadata=metadata,
            ),
        )
        return SSHHostCertificate(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """Delete an SSH Host Certificate

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-ssh-host-certificates-delete
        """
        path = "/ssh_host_certificates/{id}"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())

    def get(
        self,
        id: str,
    ) -> SSHHostCertificate:
        """Get detailed information about an SSH Host Certficate

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-ssh-host-certificates-get
        """
        path = "/ssh_host_certificates/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return SSHHostCertificate(self._client, result)

    def list(
        self,
        before_id: str = None,
        limit: str = None,
    ) -> SSHHostCertificateList:
        """List all SSH Host Certificates issued on this account

        :param before_id:
        :param limit:

        https://ngrok.com/docs/api#api-ssh-host-certificates-list
        """
        path = "/ssh_host_certificates"
        result = self._client.http_client.get(
            path,
            dict(
                before_id=before_id,
                limit=limit,
            ),
        )
        return SSHHostCertificateList(self._client, result)

    def update(
        self,
        id: str,
        description: str = None,
        metadata: str = None,
    ) -> SSHHostCertificate:
        """Update an SSH Host Certificate

        :param id:
        :param description: human-readable description of this SSH Host Certificate. optional, max 255 bytes.
        :param metadata: arbitrary user-defined machine-readable data of this SSH Host Certificate. optional, max 4096 bytes.

        https://ngrok.com/docs/api#api-ssh-host-certificates-update
        """
        path = "/ssh_host_certificates/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.patch(
            path,
            dict(
                description=description,
                metadata=metadata,
            ),
        )
        return SSHHostCertificate(self._client, result)


class SSHUserCertificatesClient(object):
    """SSH User Certificates are presented by SSH clients when connecting to an SSH
    server to authenticate their connection. The SSH server must trust the SSH
    Certificate Authority used to sign the certificate."""

    def __init__(self, client):
        self._client = client

    def create(
        self,
        ssh_certificate_authority_id: str,
        public_key: str,
        principals: Sequence[str] = [],
        critical_options: Mapping[str, str] = {},
        extensions: Mapping[str, str] = {},
        valid_after: str = "",
        valid_until: str = "",
        description: str = "",
        metadata: str = "",
    ) -> SSHUserCertificate:
        """Create a new SSH User Certificate

        :param ssh_certificate_authority_id: the ssh certificate authority that is used to sign this ssh user certificate
        :param public_key: a public key in OpenSSH Authorized Keys format that this certificate signs
        :param principals: the list of principals included in the ssh user certificate. This is the list of usernames that the certificate holder may sign in as on a machine authorizinig the signing certificate authority. Dangerously, if no principals are specified, this certificate may be used to log in as any user.
        :param critical_options: A map of critical options included in the certificate. Only two critical options are currently defined by OpenSSH: ``force-command`` and ``source-address``. See `the OpenSSH certificate protocol spec` <https://github.com/openssh/openssh-portable/blob/master/PROTOCOL.certkeys>`_ for additional details.
        :param extensions: A map of extensions included in the certificate. Extensions are additional metadata that can be interpreted by the SSH server for any purpose. These can be used to permit or deny the ability to open a terminal, do port forwarding, x11 forwarding, and more. If unspecified, the certificate will include limited permissions with the following extension map: ``{"permit-pty": "", "permit-user-rc": ""}`` OpenSSH understands a number of predefined extensions. See `the OpenSSH certificate protocol spec` <https://github.com/openssh/openssh-portable/blob/master/PROTOCOL.certkeys>`_ for additional details.
        :param valid_after: The time when the user certificate becomes valid, in RFC 3339 format. Defaults to the current time if unspecified.
        :param valid_until: The time when this host certificate becomes invalid, in RFC 3339 format. If unspecified, a default value of 24 hours will be used. The OpenSSH certificates RFC calls this ``valid_before``.
        :param description: human-readable description of this SSH User Certificate. optional, max 255 bytes.
        :param metadata: arbitrary user-defined machine-readable data of this SSH User Certificate. optional, max 4096 bytes.

        https://ngrok.com/docs/api#api-ssh-user-certificates-create
        """
        path = "/ssh_user_certificates"
        result = self._client.http_client.post(
            path,
            dict(
                ssh_certificate_authority_id=ssh_certificate_authority_id,
                public_key=public_key,
                principals=principals,
                critical_options=critical_options,
                extensions=extensions,
                valid_after=valid_after,
                valid_until=valid_until,
                description=description,
                metadata=metadata,
            ),
        )
        return SSHUserCertificate(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """Delete an SSH User Certificate

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-ssh-user-certificates-delete
        """
        path = "/ssh_user_certificates/{id}"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())

    def get(
        self,
        id: str,
    ) -> SSHUserCertificate:
        """Get detailed information about an SSH User Certficate

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-ssh-user-certificates-get
        """
        path = "/ssh_user_certificates/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return SSHUserCertificate(self._client, result)

    def list(
        self,
        before_id: str = None,
        limit: str = None,
    ) -> SSHUserCertificateList:
        """List all SSH User Certificates issued on this account

        :param before_id:
        :param limit:

        https://ngrok.com/docs/api#api-ssh-user-certificates-list
        """
        path = "/ssh_user_certificates"
        result = self._client.http_client.get(
            path,
            dict(
                before_id=before_id,
                limit=limit,
            ),
        )
        return SSHUserCertificateList(self._client, result)

    def update(
        self,
        id: str,
        description: str = None,
        metadata: str = None,
    ) -> SSHUserCertificate:
        """Update an SSH User Certificate

        :param id:
        :param description: human-readable description of this SSH User Certificate. optional, max 255 bytes.
        :param metadata: arbitrary user-defined machine-readable data of this SSH User Certificate. optional, max 4096 bytes.

        https://ngrok.com/docs/api#api-ssh-user-certificates-update
        """
        path = "/ssh_user_certificates/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.patch(
            path,
            dict(
                description=description,
                metadata=metadata,
            ),
        )
        return SSHUserCertificate(self._client, result)


class TLSCertificatesClient(object):
    """TLS Certificates are pairs of x509 certificates and their matching private
    key that can be used to terminate TLS traffic. TLS certificates are unused
    until they are attached to a Domain. TLS Certificates may also be
    provisioned by ngrok automatically for domains on which you have enabled
    automated certificate provisioning."""

    def __init__(self, client):
        self._client = client

    def create(
        self,
        certificate_pem: str,
        private_key_pem: str,
        description: str = "",
        metadata: str = "",
    ) -> TLSCertificate:
        """Upload a new TLS certificate

        :param description: human-readable description of this TLS certificate. optional, max 255 bytes.
        :param metadata: arbitrary user-defined machine-readable data of this TLS certificate. optional, max 4096 bytes.
        :param certificate_pem: chain of PEM-encoded certificates, leaf first. See `Certificate Bundles` <https://ngrok.com/docs/api#tls-certificates-pem>`_.
        :param private_key_pem: private key for the TLS certificate, PEM-encoded. See `Private Keys` <https://ngrok.com/docs/ngrok-link#tls-certificates-key>`_.

        https://ngrok.com/docs/api#api-tls-certificates-create
        """
        path = "/tls_certificates"
        result = self._client.http_client.post(
            path,
            dict(
                description=description,
                metadata=metadata,
                certificate_pem=certificate_pem,
                private_key_pem=private_key_pem,
            ),
        )
        return TLSCertificate(self._client, result)

    def delete(
        self,
        id: str,
    ):
        """Delete a TLS certificate

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-tls-certificates-delete
        """
        path = "/tls_certificates/{id}"
        path = path.format(
            id=id,
        )
        self._client.http_client.delete(path, dict())

    def get(
        self,
        id: str,
    ) -> TLSCertificate:
        """Get detailed information about a TLS certificate

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-tls-certificates-get
        """
        path = "/tls_certificates/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return TLSCertificate(self._client, result)

    def list(
        self,
        before_id: str = None,
        limit: str = None,
    ) -> TLSCertificateList:
        """List all TLS certificates on this account

        :param before_id:
        :param limit:

        https://ngrok.com/docs/api#api-tls-certificates-list
        """
        path = "/tls_certificates"
        result = self._client.http_client.get(
            path,
            dict(
                before_id=before_id,
                limit=limit,
            ),
        )
        return TLSCertificateList(self._client, result)

    def update(
        self,
        id: str,
        description: str = None,
        metadata: str = None,
    ) -> TLSCertificate:
        """Update attributes of a TLS Certificate by ID

        :param id:
        :param description: human-readable description of this TLS certificate. optional, max 255 bytes.
        :param metadata: arbitrary user-defined machine-readable data of this TLS certificate. optional, max 4096 bytes.

        https://ngrok.com/docs/api#api-tls-certificates-update
        """
        path = "/tls_certificates/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.patch(
            path,
            dict(
                description=description,
                metadata=metadata,
            ),
        )
        return TLSCertificate(self._client, result)


class TunnelSessionsClient(object):
    """Tunnel Sessions represent instances of ngrok agents or SSH reverse tunnel
    sessions that are running and connected to the ngrok service. Each tunnel
    session can include one or more Tunnels."""

    def __init__(self, client):
        self._client = client

    def list(
        self,
        before_id: str = None,
        limit: str = None,
    ) -> TunnelSessionList:
        """List all online tunnel sessions running on this account.

        :param before_id:
        :param limit:

        https://ngrok.com/docs/api#api-tunnel-sessions-list
        """
        path = "/tunnel_sessions"
        result = self._client.http_client.get(
            path,
            dict(
                before_id=before_id,
                limit=limit,
            ),
        )
        return TunnelSessionList(self._client, result)

    def get(
        self,
        id: str,
    ) -> TunnelSession:
        """Get the detailed status of a tunnel session by ID

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-tunnel-sessions-get
        """
        path = "/tunnel_sessions/{id}"
        path = path.format(
            id=id,
        )
        result = self._client.http_client.get(path, dict())
        return TunnelSession(self._client, result)

    def restart(
        self,
        id: str,
    ):
        """Issues a command instructing the ngrok agent to restart. The agent restarts itself by calling exec() on platforms that support it. This operation is notably not supported on Windows. When an agent restarts, it reconnects with a new tunnel session ID.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-tunnel-sessions-restart
        """
        path = "/tunnel_sessions/{id}/restart"
        path = path.format(
            id=id,
        )
        self._client.http_client.post(path, dict())

    def stop(
        self,
        id: str,
    ):
        """Issues a command instructing the ngrok agent that started this tunnel session to exit.

        :param id: a resource identifier

        https://ngrok.com/docs/api#api-tunnel-sessions-stop
        """
        path = "/tunnel_sessions/{id}/stop"
        path = path.format(
            id=id,
        )
        self._client.http_client.post(path, dict())

    def update(
        self,
        id: str,
    ):
        """Issues a command instructing the ngrok agent to update itself to the latest version. After this call completes successfully, the ngrok agent will be in the update process. A caller should wait some amount of time to allow the update to complete (at least 10 seconds) before making a call to the Restart endpoint to request that the agent restart itself to start using the new code. This call will never update an ngrok agent to a new major version which could cause breaking compatibility issues. If you wish to update to a new major version, that must be done manually. Still, please be aware that updating your ngrok agent could break your integration. This call will fail in any of the following circumstances: there is no update available the ngrok agent's configuration disabled update checks the agent is currently in process of updating the agent has already successfully updated but has not yet been restarted

        :param id:

        https://ngrok.com/docs/api#api-tunnel-sessions-update
        """
        path = "/tunnel_sessions/{id}/update"
        path = path.format(
            id=id,
        )
        self._client.http_client.post(path, dict())


class TunnelsClient(object):
    """Tunnels provide endpoints to access services exposed by a running ngrok
    agent tunnel session or an SSH reverse tunnel session."""

    def __init__(self, client):
        self._client = client

    def list(
        self,
        before_id: str = None,
        limit: str = None,
    ) -> TunnelList:
        """List all online tunnels currently running on the account.

        :param before_id:
        :param limit:

        https://ngrok.com/docs/api#api-tunnels-list
        """
        path = "/tunnels"
        result = self._client.http_client.get(
            path,
            dict(
                before_id=before_id,
                limit=limit,
            ),
        )
        return TunnelList(self._client, result)
