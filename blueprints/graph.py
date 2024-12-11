# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from exts import mail, db
from flask_mail import Message
from flask import request
import string
import random
from models import EmailCaptchaModel
from .forms import RegisterForm, LoginForm
from models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash

from chatbot_graph import ChatBotGraph
from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt

# /auth
bp = Blueprint("graph", __name__, url_prefix="/graph")

uri = "bolt://localhost:7687"  # 替换为你的 Neo4j URI
username = "neo4j"             # 替换为你的用户名
password = "12345678"          # 替换为你的密码
driver = GraphDatabase.driver(uri, auth=(username, password))

@bp.route("/query_command")
def query_command():
    return render_template('graph_command.html')


@bp.route("/query_command_main", methods=['POST'])
def query_command_main():
    data = request.json
    query =data.get('cypher_query')

    if not query:
        return jsonify({'error': 'No query provided'}), 400
    else:
        with driver.session() as session:
            result = session.run(query)
            # 处理查询结果
            nodes = []
            edges = []
            nodes_set = set()
            # 遍历查询结果
            for record in result:
                for item in record.values():
                    #print(item)
                    if hasattr(item, 'start_node'):  # 处理关系
                        # 添加起始节点
                        print("edge")
                        start_node = item.start_node
                        #print(start_node)  //pycahrm终端编码有问题，输出会出现解码问题bug

                        if start_node.id not in nodes_set:
                            nodes.append({
                                'id': start_node.id,
                                'label': list(start_node.labels)[0],
                                'properties': dict(start_node.items())
                            })
                            nodes_set.add(start_node.id)

                        # 添加结束节点
                        end_node = item.end_node
                        #print(end_node)
                        if end_node.id not in nodes_set:
                            nodes.append({
                                'id': end_node.id,
                                'label': list(end_node.labels)[0],
                                'properties': dict(end_node.items())
                            })
                            nodes_set.add(end_node.id)

                        # 添加边
                        edges.append({
                            'from': item.start_node.id,
                            'to': item.end_node.id,
                            'label': item.type
                        })

                    elif hasattr(item, 'labels'):  # 处理节点
                        print("node")
                        #print(item)
                        if item.id not in nodes_set:
                            nodes.append({
                                'id': item.id,
                                'label': list(item.labels)[0],
                                'properties': dict(item.items())
                            })
                            nodes_set.add(item.id)

            return jsonify({'nodes': nodes, 'edges': edges})


@bp.route("/query_Language")
def query_Language():
    return render_template('graph_Language.html')

@bp.route("/query_Language_main", methods=['POST'])
def query_Language_main():
    data = request.json
    query =data.get('cypher_query')

    handler = ChatBotGraph()
    answer='图谱中没有搜寻到'
    res_classify=handler.classifier.classify(query)
    if not res_classify:
        return answer
    # print(res_classify)
    # print(res_classify['args'])
    # print(res_classify['args'].items())
    entities=res_classify['args']
    queries=generate_cypher_query(entities)


    if not query:
        return jsonify({'error': 'No query provided'}), 400
    else:
        with driver.session() as session:

            result=[]
            for query in queries:
                res =session.run(query)
                result += res
            print(queries)
            print(result)
            #处理查询结果

            nodes = []
            edges = []
            nodes_set = set()
            # 遍历查询结果
            for record in result:
                for item in record.values():
                    #print(item)
                    if hasattr(item, 'start_node'):  # 处理关系
                        # 添加起始节点
                        #print("edge")
                        start_node = item.start_node
                        #print(start_node)  //pycahrm终端编码有问题，输出会出现解码问题bug

                        if start_node.id not in nodes_set:
                            nodes.append({
                                'id': start_node.id,
                                'label': list(start_node.labels)[0],
                                'properties': dict(start_node.items())
                            })
                            nodes_set.add(start_node.id)

                        # 添加结束节点
                        end_node = item.end_node
                        #print(end_node)
                        if end_node.id not in nodes_set:
                            nodes.append({
                                'id': end_node.id,
                                'label': list(end_node.labels)[0],
                                'properties': dict(end_node.items())
                            })
                            nodes_set.add(end_node.id)

                        # 添加边
                        edges.append({
                            'from': item.start_node.id,
                            'to': item.end_node.id,
                            'label': item.type
                        })

                    elif hasattr(item, 'labels'):  # 处理节点
                        # print("node")
                        #print(item)
                        if item.id not in nodes_set:
                            nodes.append({
                                'id': item.id,
                                'label': list(item.labels)[0],
                                'properties': dict(item.items())
                            })
                            nodes_set.add(item.id)

            return jsonify({'nodes': nodes, 'edges': edges})


def generate_cypher_query(entities):
    queries = []

    for name, types in entities.items():
        entity_type = types[0]  # Assuming each entity has exactly one type
        print(entity_type)
        if entity_type == 'person':
            query = f"""
                MATCH (p:Person {{name: '{name}'}})-[r]->(related)
                OPTIONAL MATCH (related)-[rr]->(moreRelated)
                RETURN p,r,related,rr,moreRelated
                LIMIT 100
            """
            queries.append(query)

        elif entity_type == 'gener':  # 注意：'gener' 应该是 'Genre'
            query = f"""
                MATCH (g:Genre {{name: '{name}'}})<-[r]-(related)
                OPTIONAL MATCH (related)-[rr]->(moreRelated)
                RETURN g,r,related,rr,moreRelated
                LIMIT 100
            """
            queries.append(query)

        elif entity_type == 'movie':
            query = f"""
                MATCH (m:Movie {{title: '{name}'}})-[r]->(related)
                OPTIONAL MATCH (related)-[rr]->(moreRelated)
                RETURN m,r,related,rr,moreRelated
                LIMIT 100
            """
            queries.append(query)

    return queries