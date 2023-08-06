# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/2/24
import os
from yqn_project_pro.utils import (
    conf_loader,
    host_ip,
    host_name,
)
from yqn_project_pro.utils.sha512_aes_256 import parse_apollo_secret_jvm


class ProjectConfig:
    id = "${app_id}"
    name = "${project_name}"

    version = '1.0.0'
    version_int = 1 * 10000 + 0 * 100 + 0 * 1

    heartbeat_url = '/actuator/info/'
    heartbeat_urls = [heartbeat_url, '/actuator/prometheus/', '/info/']

    project_base_dir = os.path.dirname(os.path.dirname(__file__))
    project_father_dir = os.path.dirname(project_base_dir)

    resources = os.path.join(project_base_dir, 'resources')  # resource_path
    outputs = os.path.join(project_base_dir, 'outputs')  # output_path

    hot_update = False  # whether service hot-update or not

    timer_logger_over_secs = False  # disabled if False; must logger if None or 0; logger when greater than positive nums
    timer_logger_skip_endpoints = {'doc', 'specs', 'restx_doc.static', 'static'}  # set-typed
    timer_logger_type = 'bizlog'


class LoggerConfig:
    app_id = ProjectConfig.id
    app_name = ProjectConfig.name
    log_path = "/opt/web/ws-{}/logs/".format(ProjectConfig.id)

    os.makedirs(log_path, exist_ok=True)


local_conf_loader = conf_loader(
    os.path.join(ProjectConfig.project_father_dir, '.{}_config.py'.format(ProjectConfig.name)))


class ApolloClientConfig:
    apollo_cache_file_path = os.path.join(ProjectConfig.project_base_dir, 'config')  # apollo cached config-file path
    apollo_cluster = local_conf_loader('YQN_APOLLO_CLUSTER', "qa")
    apollo_meta_server_url = local_conf_loader('YQN_APOLLO_METADATA', 'http://192.168.10.227:8080')
    apollo_env = local_conf_loader('YQN_APOLLO_ENV', "FAT")
    apollo_namespace = local_conf_loader('APOLLO_NAMESPACE', "application")

    apollo_encrypt_jvm = local_conf_loader('APOLLO_ENCRYPT_JVM', "")
    apollo_secret = parse_apollo_secret_jvm(apollo_encrypt_jvm).get("password", "9i2x7DBpdWSe3XaJ")

    apollo_app_name = local_conf_loader('APP_NAME', ProjectConfig.name)
    apollo_app_id = local_conf_loader('APP_ID', ProjectConfig.id)

    os_node_ip = local_conf_loader('YQN_NODE_IP', host_ip())
    os_pod_ip = local_conf_loader('YQN_POD_IP', host_ip())
    os_pod_name = local_conf_loader('YQN_POD_NAME', host_name())

    # !important set in apollo platform, like key 'eureka.client.serviceUrl.defaultZone'
    apollo_eureka_server_url = local_conf_loader("YQN_EUREKA_SERVER", "")
    apollo_eureka_server_key = 'eureka_url'
    apollo_eureka_status_page_url = ProjectConfig.heartbeat_url
    apollo_eureka_health_check_url = ProjectConfig.heartbeat_url
    # apollo_eureka_instance_ip = os_pod_ip
    apollo_eureka_instance_ip = os_pod_name
    apollo_eureka_instance_port = int(apollo_app_id)


class ODPSConfig:
    odps_access_id = local_conf_loader('ODPS_ACCESS_ID', '')
    odps_secret_access_key = local_conf_loader('ODPS_SECRET_ACCESS_KEY', '')
    odps_project = local_conf_loader('ODPS_PROJECT', '')
    odps_endpoint = local_conf_loader('ODPS_ENDPOINT', '')


class MySQLConfig:
    mysql_engine = local_conf_loader('MYSQL_ENGINE', '')
    mysql_username = local_conf_loader('MYSQL_USERNAME', '')
    mysql_password = local_conf_loader('MYSQL_PASSWORD', '')
    mysql_host = local_conf_loader('MYSQL_HOST', '')
    mysql_port = local_conf_loader('MYSQL_PORT', '')
    mysql_charset = local_conf_loader('MYSQL_CHARSET', '')
    mysql_database = local_conf_loader('MYSQL_DATABASE', '')


class ESConfig:
    es_host = local_conf_loader('ES_HOST', 'es.host')
    es_port = local_conf_loader('ES_PORT', 'es.port')
    es_username = local_conf_loader('ES_USERNAME', 'es.account')
    es_password = local_conf_loader('ES_PASSWORD', 'es.password')
    es_index = local_conf_loader('ES_PASSWORD', 'es.index.test')
    es_doc = local_conf_loader('ES_PASSWORD', 'es.doc')


class RedisConfig:
    redis_host = local_conf_loader('REDIS_HOST', '')
    redis_port = local_conf_loader('REDIS_PORT', '')
    redis_db = local_conf_loader('REDIS_DB', '')
    redis_password = local_conf_loader('REDIS_PASSWORD', '')
