from states.print_game_agent_state import PrintGameState
from langchain_core.messages import ChatMessage, HumanMessage, SystemMessage
from langchain.output_parsers.json import SimpleJsonOutputParser

from tools import print_game
import time

import base64
import keyboard

from langgraph.graph import StateGraph, START
from llms.google import get_react_agent


def get_way_to_run(state: PrintGameState):

    prompt = '''
        Você é um agente especialista em red dead 2, onde seu papel é receber imagens e navegar pelas estradas do game, onde voce deve sempre andar pelas estradas analisando as correções de virar para a direita ou esquerda e ir para frente.

        #LINGUA
        - responda somente em pt br

        #SEU OBJETIVO
        - identificar a estrada onde você deve andar, tomar cuidado com curvas e ponte, voce deve sempre continuar na estrada sem sair dela
        - tendo o ponto identificado, você deve passar ordens que estão limitadas em, "andar para frente", "andar para esquerda", "andar para direita" e "andar para tras"
        - tendo isso em mente, você deve especificar em ordem o comando, de exemplo, para alcançar o objetivo, ande para frente por 5 segundos, depois ande para exquerda por 9 segundos
        - preste atenção no trajeto, na estrada, caso tenha um ponte adicione a correção para esquerda ou para a direta 
        #RETORNO
        - O retorno deve ser uma lista com as ordens de chegada de objetivos
        - O retorno deve trazer somente o json final a lista, não deve vir mais nada alem disso
        ## EXEMPLO DE RETORNO
        [{andar_direita: "5 segundos"}, {andar_tras: "9 segundos"}]
        #    
    '''
    print_game.screenshot_tool()
    screenshot =  "C:\\Users\\luizr\\Documents\\projetos\\play-game-agents\\capture.png"
    image_base64 = ""
    with open(screenshot, "rb") as image_file:
        # Lê os bytes da imagem
        image_data = image_file.read()
        
        # Codifica para base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')


    messages = [
        SystemMessage(content=prompt),
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source_type": "base64",
                    "data": image_base64,
                    "mime_type": "image/jpeg",
                },
            ],
        },
    ]

    agent = get_react_agent()
    response =agent.invoke({"messages": messages})


    message_out = response["messages"][-1]

    json_parsed = SimpleJsonOutputParser().parse(message_out.content)

    return {"messages": response["messages"],  "way_to_run": json_parsed}

def run_to_way(state: PrintGameState):
    way_to_run = state["way_to_run"]
    messages = state["messages"]

    for action in way_to_run:
        andar_frente = action.get("andar_frente")
        andar_tras = action.get("andar_tras")
        andar_direita = action.get("andar_direita")
        andar_esquerda = action.get("andar_esquerda")

        if andar_frente is not None:
            print("Andando para frente")
            keyboard.press("w")
            time.sleep(int(andar_frente.split(" ")[0]))
            keyboard.release("w")
        
        if andar_direita is not None:
            print("Andando para direita")
            keyboard.press("D")
            time.sleep(int(andar_direita.split(" ")[0]))
            keyboard.release("D")
        
        if andar_tras is not None:
            print("Andando para tras")
            keyboard.press("S")
            time.sleep(int(andar_tras.split(" ")[0]))
            keyboard.release("S")
        
        if andar_esquerda is not None:
            print("Andando para esquerda")
            keyboard.press("A")
            time.sleep(int(andar_esquerda.split(" ")[0]))
            keyboard.release("A")




graph_builder = StateGraph(PrintGameState)
graph_builder.add_node("start", get_way_to_run)
graph_builder.add_node("run_to_way", run_to_way)


graph_builder.add_edge(START, "start")
graph_builder.add_edge("start", "run_to_way")

graph = graph_builder.compile()