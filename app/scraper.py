import time
import random
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc

def scrape_kabum(query: str, max_items: int = 10) -> list[dict]:
    print(f"--- INICIANDO SCRAPER PARA: '{query}' ---")
    
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    
    print("[LOG] Inicializando Undetected Chromedriver em modo visível.")
    driver = uc.Chrome(options=options, use_subprocess=True)

    products_data = []
    
    try:
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.kabum.com.br/busca/{encoded_query}"
        
        print(f"[LOG] Acessando URL de busca direta: {search_url}")
        driver.get(search_url)

        wait = WebDriverWait(driver, 20)
        
        print("[LOG] Aguardando a página de resultados carregar...")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))
        print("[LOG] Página de resultados carregada.")

        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Não encontramos o que você buscou')]"))
            )
            print("[LOG] Página de 'Nenhum resultado' encontrada.")

        except TimeoutException:
            print("[LOG] A busca retornou resultados.")
            
            wait_time = random.uniform(3, 5)
            print(f"[LOG] Aguardando {wait_time:.2f} segundos para os produtos renderizarem...")
            time.sleep(wait_time)

            print("[LOG] Procurando pelos links dos produtos (//a[.//span[contains(@class, 'nameCard')]])...")
            product_links = driver.find_elements(By.XPATH, "//a[.//span[contains(@class, 'nameCard')]]")
            
            if not product_links:
                print("[AVISO] Nenhum link de produto foi encontrado com o seletor XPath.")
            else:
                print(f"[LOG] SUCESSO! {len(product_links)} links de produto encontrados. Extraindo dados...")
                for i, link_element in enumerate(product_links[:max_items]):
                    print(f"\n--- Processando Link de Produto {i + 1} ---")
                    try:
                        # 2. Extrai os dados de dentro de cada link
                        title = link_element.find_element(By.CSS_SELECTOR, "span.nameCard").text
                        price_raw = link_element.find_element(By.CSS_SELECTOR, "span.priceCard").text.strip()
                        link = link_element.get_attribute("href")

                        if not price_raw:
                            print(f"[AVISO] Produto '{title[:30]}...' sem preço. Pulando.")
                            continue

                        price_clean = price_raw.replace("R$", "").replace(".", "").replace(",", ".").strip()
                        price = float(price_clean)

                        products_data.append({
                            "title": title,
                            "price": price,
                            "link": link
                        })
                        print(f"[SUCESSO NO LINK] Extraído: {title[:30]}... | Preço: {price}")

                    except NoSuchElementException as e:
                        print(f"[ERRO NO LINK] Não foi possível encontrar um elemento dentro do link. Erro: {e.msg}")
                        continue
    
    except Exception as e:
        print(f"[ERRO GERAL] Ocorreu um erro inesperado: {e}")
        driver.save_screenshot('kabum_results.png')

    finally:
        print("[LOG] Finalizando. Aguardando 3 segundos antes de fechar.")
        time.sleep(3)
        driver.quit()

    print(f"--- SCRAPER FINALIZADO: {len(products_data)} produtos extraídos ---")
    return products_data

if __name__ == '__main__':
    termo_busca = "placa de video rtx 4070"
    produtos = scrape_kabum(termo_busca, max_items=5)
    
    print("\n--- RESULTADO FINAL DO TESTE ---")
    if produtos:
        for p in produtos:
            print(p)
    else:
        print(f"Nenhum produto encontrado para '{termo_busca}'.")

