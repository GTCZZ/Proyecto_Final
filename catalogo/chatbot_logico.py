from pyDatalog import pyDatalog
from .models import Producto

# 1. DECLARAMOS LOS TÉRMINOS (A nivel global)
pyDatalog.create_terms('ProductoObj, PrecioVar, FrutaVar')
pyDatalog.create_terms('precio_rel, dulzura_rel, fruta_rel')
pyDatalog.create_terms('economico, premium, muy_dulce, frutal')

def consultar_chatbot(mensaje):
    pyDatalog.clear()
    
    # CARGAMOS LOS HECHOS 
    productos = Producto.objects.all()
    for p in productos:
        + precio_rel(p, float(p.precio_unidad))
        if p.nivel_dulzura:
            + dulzura_rel(p, p.nivel_dulzura)
        if p.fruta and p.fruta.lower() != 'ninguna':
            + fruta_rel(p, p.fruta)

    # REGLAS LÓGICAS 
    economico(ProductoObj) <= precio_rel(ProductoObj, PrecioVar) & (PrecioVar < 20.00)
    premium(ProductoObj) <= precio_rel(ProductoObj, PrecioVar) & (PrecioVar >= 100.00)
    muy_dulce(ProductoObj) <= dulzura_rel(ProductoObj, 'Alto')
    frutal(ProductoObj) <= fruta_rel(ProductoObj, FrutaVar)

    # MOTOR DE INFERENCIA
    mensaje = mensaje.lower()
    resultados_objetos = []
    
    if 'barato' in mensaje or 'economico' in mensaje or 'económico' in mensaje:
        respuestas = economico(ProductoObj) 
        if respuestas: resultados_objetos = [r[0] for r in respuestas]
            
    elif 'dulce' in mensaje:
        respuestas = muy_dulce(ProductoObj)
        if respuestas: resultados_objetos = [r[0] for r in respuestas]
            
    elif 'fruta' in mensaje or 'fresa' in mensaje:
        respuestas = frutal(ProductoObj)
        if respuestas: resultados_objetos = [r[0] for r in respuestas]
            
    elif 'caro' in mensaje or 'premium' in mensaje or 'elegante' in mensaje:
        respuestas = premium(ProductoObj)
        if respuestas: resultados_objetos = [r[0] for r in respuestas]

    # FORMATEAR RESPUESTA CON HTML
    if resultados_objetos:
        lista_html = []
        for prod in resultados_objetos:
            # Creamos un enlace dinámico usando el ID del producto
            enlace = f"<a href='/producto/{prod.id}/' style='color: #e91e63; font-weight: bold; text-decoration: none;'>{prod.nombre_producto}</a>"
            precio = f"<span style='color: #28a745;'> (S/ {prod.precio_unidad})</span>"
            lista_html.append(f"<li>{enlace}{precio}</li>")
        
        # Juntamos todo en una lista desordenada de HTML
        respuesta_final = "Aquí tienes las opciones que deduje para ti:<br><ul style='margin: 5px 0; padding-left: 20px;'>" + "".join(lista_html) + "</ul>"
        return respuesta_final
        
    elif any(palabra in mensaje for palabra in ['barato', 'dulce', 'fruta', 'caro', 'premium', 'economico']):
        return "No encontré productos que cumplan con esa regla."
    else:
        return "Dime si buscas algo 'económico', 'muy dulce', 'con fruta' o 'premium'."