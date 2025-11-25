from abc import ABC, abstractmethod


class MetodoPago(ABC):
    @abstractmethod
    def pagar(self, monto: float) -> bool:
        pass


class PagoTarjeta(MetodoPago):
    def pagar(self, monto: float) -> bool:
        print(f"[PAGO TARJETA] Cobro de {monto:.2f}")
        return True


class PagoPayPal(MetodoPago):
    def pagar(self, monto: float) -> bool:
        print(f"[PAGO PAYPAL] Cobro de {monto:.2f}")
        return True


# Ejemplo OCP: nuevo método sin tocar el resto del sistema
class PagoCrypto(MetodoPago):
    def pagar(self, monto: float) -> bool:
        print(f"[PAGO CRYPTO] Cobro de {monto:.2f} en USDT")
        return True
