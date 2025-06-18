import pytest
from unittest.mock import MagicMock
from typing import List
from datetime import datetime

from esquemas.producto import CrearProducto, RespuestaProducto
from servicios.documento import ServicioProducto

@pytest.fixture
def mock_repositorio():
    return MagicMock()

@pytest.fixture
def servicio_producto(mock_repositorio):
    return ServicioProducto(mock_repositorio)

def test_crear_producto(servicio_producto, mock_repositorio):
    producto_entrada = CrearProducto(
        nombre="Producto Test",
        precio=100,
        descripcion="Descripción de prueba",
        stock=10,
        usuario_id=1
    )
    producto_salida = RespuestaProducto(
        id=1,
        nombre="Producto Test",
        descripcion="Descripción de prueba",
        precio=100,
        stock=10,
        usuario_id=1,
        fecha_creacion=datetime.now()
    )

    mock_repositorio.insertar_producto.return_value = producto_salida

    resultado = servicio_producto.crear_producto(producto_entrada)

    assert resultado == producto_salida
    mock_repositorio.insertar_producto.assert_called_once_with(producto_entrada)

def test_obtener_producto(servicio_producto, mock_repositorio):
    id_producto = 1
    producto_salida = RespuestaProducto(
        id=1,
        nombre="Producto Test",
        descripcion="Descripción de prueba",
        precio=100,
        stock=10,
        usuario_id=1,
        fecha_creacion=datetime.now()
    )

    mock_repositorio.obtener_producto.return_value = producto_salida

    resultado = servicio_producto.obtener_producto(id_producto)

    assert resultado == producto_salida
    mock_repositorio.obtener_producto.assert_called_once_with(id_producto)

def test_obtener_productos_usuario(servicio_producto, mock_repositorio):
    id_usuario = 10
    productos_salida: List[RespuestaProducto] = [
        RespuestaProducto(
            id=1,
            nombre="Producto 1",
            descripcion="Descripción 1",
            precio=50,
            stock=5,
            usuario_id=id_usuario,
            fecha_creacion=datetime.now()
        ),
        RespuestaProducto(
            id=2,
            nombre="Producto 2",
            descripcion="Descripción 2",
            precio=75,
            stock=8,
            usuario_id=id_usuario,
            fecha_creacion=datetime.now()
        ),
    ]

    mock_repositorio.obtener_productos_de_usuario.return_value = productos_salida

    resultado = servicio_producto.obtener_productos_usuario(id_usuario)

    assert resultado == productos_salida
    mock_repositorio.obtener_productos_de_usuario.assert_called_once_with(id_usuario)
