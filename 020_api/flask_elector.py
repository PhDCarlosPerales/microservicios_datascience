import asyncio
import json
import time
import aiohttp

from flask import Flask, request, Response

import logging


FORMAT = '[%(asctime)-15s][%(levelname)-8s]%(message)s'
logging.basicConfig(format=FORMAT,level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting Example")

DURACION_POR_LLAMADA = 5
DURACION_TOTAL = 10


app = Flask(__name__)


async def do_request(url, data, timeout_peticion, session):
    logger.info('[do_request][{}] Calling web'.format(url))
    try:
        async with session.post(url,timeout=timeout_peticion, json= data) as resp:
            respuesta = await resp.text()
            logger.info('[do_request][{}] Returns result:{}'.format(url,respuesta))
            return [ respuesta, url] # esta respuesta se devulve cuando ya ha terminado la petición
    except asyncio.TimeoutError as ex:
        logger.warning("[do_request][{}]Timeout captured:{}".format(url, ex))
        return None
    except Exception as ex:
        logger.error("[do_request][{}]Excepction:{}".format(url, ex))
        return None




async def esperar_respuestas(modelos):
    resultados = []
    tiempo_inicial = time.time()
    for completado in asyncio.as_completed(modelos):
        respuesta = await completado
        print(respuesta)
        resultados.append(respuesta)
        duracion = time.time() - tiempo_inicial
        if duracion > DURACION_TOTAL:
            logger.error("Se ha sobrepasado el tiempo de espera de respuestas")
            break
    return resultados


async def llamar_a_modelos(session,data):
    modelos_llamados = []
    modelos_llamados.append(do_request("http://canary:5001/predict", data, DURACION_POR_LLAMADA, session))
    modelos_llamados.append(do_request("http://model:5000/predict", data, DURACION_POR_LLAMADA, session))
    return modelos_llamados


def trata_resultados(resultados):
    """Elije qué llamada responde"""
    respuesta = "Sin resultado de modelos"
    for resultado in resultados:
        print(resultado)
        if resultado is not None:
            if resultado[1] == "http://model:5000/predict":
                respuesta= resultado[0]
    return respuesta



async def get_datos(data):
    resultados_tratados = []
    async with aiohttp.ClientSession() as session:
        logger.info("Llamando a los modelos")
        modelos_llamados = await llamar_a_modelos(session,data)

        logger.info("Esperando a los modelos")
        resultados = await esperar_respuestas(modelos_llamados)

        logger.info("Trata resultados")
        resultados_tratados = trata_resultados(resultados)

    return resultados_tratados


loop = asyncio.get_event_loop()

@app.route("/predict",methods=['POST'])
def predict():
    try:
        logger.debug(request)
        data= request.get_json()
        respuesta = loop.run_until_complete(get_datos(data))


        return Response(status=200, response=json.dumps(respuesta))
    except Exception as ex:
        return Response(status=400, response=ex)


if __name__ == "__main__":
    logger.info("Elector")
    app.run(host='0.0.0.0', port=5002)
    loop.close()

# curl -H "Content-Type: application/json" --request POST --data "{\"s_l\":5.9,\"s_w\":3,\"p_l\":5.1,\"p_w\":1.8}" http://127.0.0.1:5002/predict
