def obtener_secciones_formulario_trabajador():
    secciones = [
        {"nombre": "DATOS_EMPLEADOR", "campos": ["R1", "R2", "R3", "R4", "R5"], "tipo": "dict"},
        {"nombre": "DATOS_TRABAJADOR", "campos": [f"R{i}" for i in range(6, 41)], "tipo": "dict"},
        {"nombre": "DATOS_OTROS_EMPLEADORES", "campos": [f"R{i}" for i in range(41, 47)], "tipo": "list"},
        {"nombre": "DATOS_CONYUGE", "campos": [f"R{i}" for i in range(47, 69)], "tipo": "dict"},
        {"nombre": "DATOS_BENEFICIARIOS", "campos": [f"R{i}" for i in range(69, 80)], "tipo": "list"},
        {"nombre": "OBSERVACIONES", "campos": ["R80"], "tipo": "dict"},
        {"nombre": "FIRMAS", "campos": [f"R{i}" for i in range(81, 85)], "tipo": "dict"}
    ]

    return secciones
