from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Item:
    nombre: str
    precio: float
    cantidad: int = 1

    def subtotal(self) -> float:
        return self.precio * self.cantidad


class Pedido(ABC):
    """
    Clase base de Pedido (LSP: las subclases deben comportarse como Pedido).
    """

    def __init__(self, id_pedido: int, cliente: str, items: List[Item]):
        self.id_pedido = id_pedido
        self.cliente = cliente
        self.items = items

    def calcular_total(self) -> float:
        return sum(i.subtotal() for i in self.items)

    @abstractmethod
    def descripcion_canal(self) -> str:
        pass


# ISP: interfaces pequeñas y específicas

class Notificable(ABC):
    @abstractmethod
    def enviar_notificacion(self) -> None:
        pass


class Facturable(ABC):
    @abstractmethod
    def generar_factura(self) -> str:
        pass


class PedidoOnline(Pedido, Notificable, Facturable):
    def __init__(self, id_pedido: int, cliente: str, items: List[Item], email: str):
        super().__init__(id_pedido, cliente, items)
        self.email = email

    def descripcion_canal(self) -> str:
        return "Pedido Online"

    def enviar_notificacion(self) -> None:
        print(f"[NOTIFICACIÓN EMAIL] Enviando email a {self.email} por pedido #{self.id_pedido}")

    def generar_factura(self) -> str:
        lineas = [f"Factura Pedido Online #{self.id_pedido}",
                  f"Cliente: {self.cliente}",
                  f"Email: {self.email}",
                  "Items:"]
        for item in self.items:
            lineas.append(f"- {item.nombre} x{item.cantidad} = {item.subtotal():.2f}")
        lineas.append(f"Total: {self.calcular_total():.2f}")
        return "\n".join(lineas)


class PedidoTelefonico(Pedido, Facturable):
    def __init__(self, id_pedido: int, cliente: str, items: List[Item], telefono: str):
        super().__init__(id_pedido, cliente, items)
        self.telefono = telefono

    def descripcion_canal(self) -> str:
        return "Pedido Telefónico"

    def generar_factura(self) -> str:
        lineas = [f"Factura Pedido Telefónico #{self.id_pedido}",
                  f"Cliente: {self.cliente}",
                  f"Teléfono: {self.telefono}",
                  "Items:"]
        for item in self.items:
            lineas.append(f"- {item.nombre} x{item.cantidad} = {item.subtotal():.2f}")
        lineas.append(f"Total: {self.calcular_total():.2f}")
        return "\n".join(lineas)
