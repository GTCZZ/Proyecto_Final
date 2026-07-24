import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection

def update_db():
    with connection.cursor() as cursor:
        cursor.execute("ALTER TABLE pedidos_pedido ADD COLUMN IF NOT EXISTS metodo_entrega VARCHAR(20) DEFAULT 'DELIVERY';")
        cursor.execute("ALTER TABLE pedidos_pedido ADD COLUMN IF NOT EXISTS metodo_pago VARCHAR(20) DEFAULT 'TARJETA';")
        cursor.execute("ALTER TABLE pedidos_pedido ADD COLUMN IF NOT EXISTS tiempo_estimado VARCHAR(50) DEFAULT '35 - 45 minutos';")
    print("Columnas de Pedido actualizadas correctamente en PostgreSQL!")

if __name__ == '__main__':
    update_db()
