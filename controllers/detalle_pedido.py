import json
import logging

from fastapi import HTTPException

from models.Detalle_pedido import DetallePedido
from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

