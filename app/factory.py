# path: app/factory.py

from __future__ import annotations
from typing import List

from .models import Pedido, PedidoOnline, PedidoTelefonico, Item


class PedidoFactory:
    """
    Factory Method: la lógica de qué tipo de Pedido crear está centralizada aquí.
    Permite crear distintos tipos de pedidos (online, telefónico).
    """

    @staticmethod
    def crear_pedido(
        tipo: str,
        id_pedido: int,
        cliente: str,
        items: List[Item],
        contacto: str
    ) -> Pedido:
        if tipo == "online":
            return PedidoOnline(id_pedido, cliente, items, email=contacto)
        elif tipo == "telefono":
            return PedidoTelefonico(id_pedido, cliente, items, telefono=contacto)
        else:
            raise ValueError(f"Tipo de pedido no soportado: {tipo}")
