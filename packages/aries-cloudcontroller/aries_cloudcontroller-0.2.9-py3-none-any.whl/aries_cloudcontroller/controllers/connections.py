from .base import BaseController
from ..models.connection import Connection

from aiohttp import (
    ClientSession,
)
import logging
import asyncio


logger = logging.getLogger("aries_controller.connections")


class ConnectionsController(BaseController):
    def __init__(self, admin_url: str, client_session: ClientSession):
        super().__init__(admin_url, client_session)
        self.connections = []

    # @staticmethod
    # def default_handler():

    # TODO Add Logging here!
    def default_handler(self, payload):
        connection_id = payload["connection_id"]
        state = payload["state"]
        logger.debug(f"connections hook for {connection_id} with state: {state}")
        for connection in self.connections:
            if connection.id == connection_id:
                connection.update_state(state)
                logger.debug(f"{connection_id} state updated")

    # Combines receive and accept connection api calls
    async def accept_connection(self, invitation):
        response = await self.receive_invitation(invitation)

        accepted = await self.accept_invitation(response["connection_id"])
        return accepted

    ### TODO refactor to extract out generic base - /connections

    async def get_connections(
        self,
        alias: str = None,
        initiator: str = None,
        invitation_key: str = None,
        my_did: str = None,
        state: str = None,
        their_did: str = None,
        their_role: str = None,
    ):
        params = {}
        if alias:
            params["alias"] = alias
        if initiator:
            params["initiator"] = initiator
        if invitation_key:
            params["invitation_key"] = invitation_key
        if my_did:
            params["my_did"] = my_did
        if state:
            params["state"] = state
        if their_did:
            params["their_did"] = their_did
        if their_role:
            params["their_role"] = their_role

        connections = await self.admin_GET("/connections", params=params)
        return connections

    async def get_connection(self, connection_id: str):
        connection = await self.admin_GET(f"/connections/{connection_id}")
        return connection

    async def create_invitation(
        self,
        alias: str = None,
        auto_accept: bool = None,
        public: str = None,
        multi_use: str = None,
        invite_options: {} = None,
    ):
        params = {}
        if alias:
            params["alias"] = alias
        if auto_accept:
            params["auto_accept"] = auto_accept
        if public:
            params["public"] = public
        if multi_use:
            params["multi_use"] = multi_use
        if invite_options:
            """A dictionary of the form:
            {
                "mediation_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "metadata": {},
                "recipient_keys": [
                    "H3C2AVvLMv6gmMNam3uVAjZpfkcJCwDwnZn6z3wXmqPV"
                ],
                "routing_keys": [
                    "H3C2AVvLMv6gmMNam3uVAjZpfkcJCwDwnZn6z3wXmqPV"
                ],
                "service_endpoint": "http://192.168.56.102:8020"
            }
            """
            invite_details = await self.admin_POST(
                "/connections/create-invitation",
                params=params,
                json_data=invite_options,
            )
        else:
            invite_details = await self.admin_POST(
                "/connections/create-invitation", params=params
            )
        connection = Connection(invite_details["connection_id"], "invitation")
        self.connections.append(connection)
        return invite_details

    async def receive_invitation(
        self, connection_details: str, alias: str = None, auto_accept: bool = None
    ):
        params = {}
        if alias:
            params["alias"] = alias
        if auto_accept:
            params["auto_accept"] = auto_accept

        response = await self.admin_POST(
            "/connections/receive-invitation", connection_details, params=params
        )
        connection = Connection(response["connection_id"], response["state"])
        self.connections.append(connection)
        logger.debug("Connection Received - " + connection.id)
        return response

    async def accept_invitation(
        self, connection_id: str, my_label: str = None, my_endpoint: str = None
    ):
        params = {}
        if my_label:
            params["my_label"] = my_label
        if my_endpoint:
            params["my_endpoint"] = my_endpoint
        response = await self.admin_POST(
            f"/connections/{connection_id}/accept-invitation", params=params
        )
        return response

    async def accept_request(self, connection_id: str, my_endpoint: str = None):
        # TODO get if connection_id is in request state, else throw error
        params = {}
        if my_endpoint:
            params["my_endpoint"] = my_endpoint
        connection_ready = await self.check_connection_ready(connection_id, "request")
        if connection_ready:
            response = await self.admin_POST(
                f"/connections/{connection_id}/accept-request", params=params
            )
            return response
        else:
            # TODO create proper error classes
            raise Exception("The connection is not in the request state")

    async def get_remote_endpoints(self, connection_id: str):
        response = await self.admin_GET(f"/connections/{connection_id}/endpoints")
        return response

    async def establish_inbound(self, connection_id: str, router_conn_id: str):
        response = await self.admin_POST(
            f"/connections/{connection_id}/establish-inbound/{router_conn_id}"
        )
        return response

    async def remove_connection(self, connection_id):
        response = await self.admin_DELETE(f"/connections/{connection_id}")
        return response

    async def create_static(
        self,
        their_seed,
        their_label,
        their_verkey,
        their_role,
        my_seed,
        my_did,
        their_endpoint,
        alias,
        their_did,
    ):
        params = {}
        if their_seed:
            params["their_seed"] = their_seed
        if their_label:
            params["their_label"] = their_label
        if their_verkey:
            params["their_verkey"] = their_verkey
        if their_role:
            params["their_role"] = their_role
        if my_seed:
            params["my_seed"] = my_seed
        if my_did:
            params["my_did"] = my_did
        if their_endpoint:
            params["their_endpoint"] = their_endpoint
        if alias:
            params["alias"] = alias
        if their_did:
            params["their_did"] = their_did

        response = await self.admin_POST(f"/connections/create-static", data=params)
        return response

    async def check_connection_ready(self, connection_id, state):
        stored = False
        for connection in self.connections:
            if connection.id == connection_id:
                try:
                    await asyncio.wait_for(connection.detect_state_ready(state), 5)
                    return True
                except asyncio.TimeoutError:
                    response = await self.get_connection(connection_id)
                    return state == response["state"]
        if not stored:
            try:
                response = await self.get_connection(connection_id)
                connection = Connection(response["connection_id"], response["state"])
                self.connections.append(connection)
                await asyncio.wait_for(connection.detect_state_ready(state), 5)
                return True
            except asyncio.TimeoutError:
                return False

    async def is_active(self, connection_id):
        is_active = await self.check_connection_ready(connection_id, "active")
        if not is_active:
            logger.error(f"Connection {connection_id} not active")
            raise Exception("Connection must be active to send a credential")
        return

    async def get_connection_metadata(self, connection_id: str, key: str = None):
        if key:
            response = await self.admin_GET(
                f"/connections/{connection_id}/metadata?key={key}"
            )
        else:
            response = await self.admin_GET(f"/connections/{connection_id}/metadata")
        return response

    async def set_connection_metadata(self, connection_id: str, metadata: dict = None):
        if metadata:
            metadata = {"metadata": metadata}
            response = await self.admin_POST(
                f"/connections/{connection_id}/metadata", data=metadata
            )
        else:
            response = await self.admin_POST(f"/connections/{connection_id}/metadata")
        return response

    async def start_introduction(
        self, connection_id: str, target_connection_id: str, message: str = None
    ):
        route = f"/connections/{connection_id}/start-introduction?target_connection_id={target_connection_id}"
        if message:
            route += f"&message={message}"
        response = self.admin_POST(route)
        return response
