from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app import scraper
from app import database
from app import models

router = APIRouter()

@router.post("/scrape/", status_code=201)
def scrape_and_save(query: str = Query(..., min_length=3)):
    scraped_data = scraper.scrape_kabum(query)
    
    if not scraped_data:
        raise HTTPException(status_code=404, detail="Nenhum produto encontrado para a busca informada.")
    
    database.add_scrape_results(scraped_data)
    
    return {"message": f"Raspagem concluída! {len(scraped_data)} produtos encontrados e histórico de preços atualizado."}


@router.get("/products/", response_model=List[dict])
def get_products():
    """
    Endpoint para listar todos os produtos cadastrados com o seu último preço.
    """
    products = database.get_all_products_with_latest_price()
    if not products:
        raise HTTPException(status_code=404, detail="Nenhum produto cadastrado no banco de dados.")
    return products


@router.get("/products/history/{product_id}")
def get_product_with_history(product_id: int):
    """
    Endpoint para buscar um produto específico e todo o seu histórico de preços.
    """
    product_details = database.get_product_history(product_id)
    if not product_details:
        raise HTTPException(status_code=404, detail=f"Produto com ID {product_id} não encontrado.")
    return product_details

