from __future__ import annotations

from .models import Item
from .factory import PedidoFactory
from .services import PedidoService


class PedidoCLI:
    """
    Capa de presentación muy simple (podría ser una API, GUI, etc.).
    SRP: solo se preocupa de orquestar interacción con el usuario/terminal.
    """

    def __init__(self, service: PedidoService):
        self.service = service

    def ejecutar_demo(self) -> None:
        # Pedido Online
        items_online = [
            Item("Teclado mecánico", 50000, 1),
            Item("Mouse gamer", 25000, 2),
        ]
        pedido_online = PedidoFactory.crear_pedido(
            tipo="online",
            id_pedido=1,
            cliente="Acme Corp",
            items=items_online,
            contacto="compras@acme.com",
        )
        self.service.procesar_pedido(pedido_online)

        # Pedido Telefónico
        items_tel = [
            Item("Monitor 27\"", 180000, 1),
        ]
        pedido_tel = PedidoFactory.crear_pedido(
            tipo="telefono",
            id_pedido=2,
            cliente="Inversiones XYZ",
            items=items_tel,
            contacto="+56 9 1234 5678",
        )
        self.service.procesar_pedido(pedido_tel)
