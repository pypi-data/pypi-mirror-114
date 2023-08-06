from zou.app.models.project import Project
import requests
from zou.app.config import GENESIS_HOST, GENESIS_PORT, SVN_SERVER_PARENT_URL, FILE_MAP
from zou.app.models.entity import Entity
from zou.app.services import (
                                file_tree_service,
                                persons_service,
                                projects_service,
                                assets_service,
                                tasks_service,
                                shots_service,
                                entities_service
                            )
import os

def create_project(data):
    project_name = data['name']
    requests.post(url=f"{GENESIS_HOST}:{GENESIS_PORT}/project/{project_name}")
    svn_url = os.path.join(SVN_SERVER_PARENT_URL, project_name.replace(' ', '_').lower())
    if data['production_type'] == 'tvshow':
        data.update({'file_tree': file_tree_service.get_tree_from_file('eaxum_tv_show'), 'data': {'local_svn_url': svn_url, 'remote_svn_url': svn_url}})
    else:
        data.update({'file_tree': file_tree_service.get_tree_from_file('eaxum'), 'data': {'file_map': FILE_MAP, 'svn_url': svn_url}})


def project_rename(data, instance_dict):
    try:
        if instance_dict['name'] != data['name']:
            payload = {
                'old_project_name':instance_dict['name'],
                'new_project_name':data['name']
                }
            project_name = data['name']
            requests.put(url=f"{GENESIS_HOST}:{GENESIS_PORT}/project/{project_name}", json=payload)
    except KeyError:
        pass

def archive_project(project_name):
    requests.delete(url=f"{GENESIS_HOST}:{GENESIS_PORT}/project/{project_name}")

def get_svn_base_directory(project:dict, base_file_directory):
    '''
        get svn repository acl directory
    '''
    root = os.path.join(project['file_tree']['working']['mountpoint'], project['file_tree']['working']['root'],project['name'].replace(' ', '_'),'')
    base_svn_directory = os.path.join(f"{project['name']}:",base_file_directory.split(root.lower(),1)[1])
    return base_svn_directory.lower()

def get_base_file_directory(project, working_file_path, task_type_name, file_extension):
    project_id = project['id']
    project_file_map = project['data'].get('file_map')
    if project_file_map == None:
        update_project_data(project_id, {'file_map': FILE_MAP})
        project_file_map = FILE_MAP
    task_type_map = project_file_map.get(task_type_name)
    if task_type_map == 'base':
        base_file_directory = f'{working_file_path}.{file_extension}'
    elif task_type_map == 'none':
        base_file_directory = None
    elif task_type_map == None:
        update_file_map(project_id, {task_type_name:task_type_name})
        base_file_directory = f'{working_file_path}_{task_type_name}.{file_extension}'
    else:
        base_file_directory = f'{working_file_path}_{task_type_map}.{file_extension}'
    return base_file_directory

def update_file_map(project_id, data: dict):
    project = projects_service.get_project(project_id)
    project_data = project['data']
    project_data['file_map'].update(data)
    new_project_data = {'data': project_data}
    projects_service.update_project(project_id, new_project_data)

def update_project_data(project_id, data: dict):
    project = projects_service.get_project(project_id)
    project_data = project['data']
    project_data.update(data)
    new_project_data = {'data': project_data}
    projects_service.update_project(project_id, new_project_data)

def create_task_file(task, task_type, project_id):
    'sends detail of file to be created in gensys'
    file_extension = 'blend'
    task_type_name = task_type['name'].lower()
    working_file_path = file_tree_service.get_working_file_path(task.serialize())
    project = projects_service.get_project(project_id)
    all_persons = persons_service.get_persons()
    project_name = project['name'].replace(' ', '_').lower()
    base_file_directory = get_base_file_directory(project, working_file_path, task_type_name, file_extension)
    if base_file_directory:
        base_svn_directory = get_svn_base_directory(project, base_file_directory)
        payload = {
                "project":project,
                "base_file_directory":base_file_directory,
                "base_svn_directory":base_svn_directory,
                "all_persons":all_persons,
                "task_type":task_type_name
        }
        requests.post(url=f"{GENESIS_HOST}:{GENESIS_PORT}/task/{project_name}", json=payload)

def rename_task_file(data, task, entity, project, payload, entity_type):
    tasks_service.clear_task_cache(task['id'])
    task_type = tasks_service.get_task_type(task['task_type_id'])
    task_type_name = task_type['name'].lower()
    file_extension = 'blend'
    # FIXME working file path different from new entity name when task is renamed
    # added a hack for now
    if entity_type == 'asset':
        # set working file path to previous name
        working_file_path = file_tree_service.get_working_file_path(task) \
            .rsplit('/', 1)
        working_file_path = os.path.join(working_file_path[0], entity.serialize()['name'].replace(' ', '_').lower())
        new_file_name = data['name'].replace(' ', '_').lower()
        new_working_file_path = os.path.join(os.path.dirname(working_file_path), new_file_name)
    elif entity_type == 'shot':
        working_file_path = file_tree_service.get_working_file_path(task) \
            .rsplit('/', 2)
        entity_name = entity.serialize()['name'].replace(' ', '_').lower()
        shot_file_name = f"{working_file_path[2].rsplit('_', 1)[0]}_{entity_name}"
        new_file_name = f"{working_file_path[2].rsplit('_', 1)[0]}_{data['name'].replace(' ', '_').lower()}"
        working_file_path = os.path.join(working_file_path[0],entity_name,shot_file_name)
        shot_folder = os.path.join(os.path.dirname(os.path.dirname(working_file_path)), \
            new_file_name.rsplit('_', 1)[1])
        new_working_file_path = os.path.join(shot_folder, new_file_name)
    base_file_directory = get_base_file_directory(project, working_file_path, task_type_name, file_extension)
    new_base_file_directory = get_base_file_directory(project, new_working_file_path, task_type_name, file_extension)
    if base_file_directory:
        base_svn_directory = get_svn_base_directory(project, base_file_directory)
        new_base_svn_directory = get_svn_base_directory(project, new_base_file_directory)
        task_payload = {
            'entity_type':entity_type,
            'project':project,
            'base_svn_directory':base_svn_directory,
            'new_base_svn_directory':new_base_svn_directory,
            'base_file_directory':base_file_directory,
            'new_base_file_directory':new_base_file_directory,
            'task_type':task_type_name,
        }
        payload.append(task_payload)

def rename_asset_task_file(data, entity):
    if data['name'] != entity.serialize()['name']:
        project = projects_service.get_project(entity.serialize()["project_id"])
        if assets_service.is_asset(entity):
            assets_service.clear_asset_cache(str(entity.id))
            full_asset = assets_service.get_full_asset(entity.serialize()['id'])
            asset_tasks = full_asset['tasks']
            if asset_tasks:
                payload = []
                for task in asset_tasks:
                    rename_task_file(
                        data=data,
                        task=task,
                        entity=entity,
                        project=project,
                        payload=payload,
                        entity_type='asset'
                    )
                requests.put(url=f"{GENESIS_HOST}:{GENESIS_PORT}/asset/{project['name']}", json=payload)
        elif shots_service.is_shot(entity.serialize()):
            shots_service.clear_shot_cache(str(entity.id))
            full_shot = shots_service.get_full_shot(entity.serialize()['id'])
            shot_tasks = full_shot['tasks']
            if shot_tasks:
                payload = []
                for task in shot_tasks:
                    rename_task_file(
                        data=data,
                        task=task,
                        entity=entity,
                        project=project,
                        payload=payload,
                        entity_type='shot'
                    )
                requests.put(url=f"{GENESIS_HOST}:{GENESIS_PORT}/asset/{project['name']}", json=payload)

def delete_task_file(task, entity_type):
    file_extension = 'blend'
    tasks_service.clear_task_cache(task['id'])
    task_type = tasks_service.get_task_type(task['task_type_id'])
    project = projects_service.get_project(task["project_id"])
    task_type_name = task_type['name'].lower()
    if entity_type == 'asset':
        working_file_path = file_tree_service.get_working_file_path(task)
    elif entity_type == 'shot':
        working_file_path = file_tree_service.get_working_file_path(task)
    base_file_directory = get_base_file_directory(project, working_file_path, task_type_name, file_extension)
    base_svn_directory = get_svn_base_directory(project, base_file_directory)
    task_payload = {
        'entity_type':entity_type,
        'project':project,
        'base_svn_directory':base_svn_directory,
        "base_file_directory":base_file_directory,
        'task_type':task_type_name,
    }
    requests.delete(url=f"{GENESIS_HOST}:{GENESIS_PORT}/task/{project['name']}", json=task_payload)

def grant_file_access(task, person, project_id, permission='rw'):
    entity = entities_service.get_entity_raw(task.entity_id)
    file_extension = 'blend'
    task_type = tasks_service.get_task_type(str(task.task_type_id))
    task_type_name = task_type['name'].lower()
    dependencies = Entity.serialize_list(entity.entities_out, obj_type="Asset")
    project = projects_service.get_project(project_id)
    project_name = project['name'].replace(' ', '_').lower()
    working_file_path = file_tree_service.get_working_file_path(task.serialize())
    # working_file_path = os.path.join(working_file_path[0], entity.serialize()['name'].replace(' ', '_').lower())
    base_file_directory = get_base_file_directory(project, working_file_path, task_type_name, file_extension)
    if base_file_directory:
        base_svn_directory = get_svn_base_directory(project, base_file_directory)
        dependencies_payload = list()
        for dependency in dependencies:
            task_id = tasks_service.get_tasks_for_asset(dependency['id'])[0]
            dependency_working_file_path = file_tree_service.get_working_file_path(task_id)
            dependency_base_file_directory = get_base_file_directory(project, dependency_working_file_path, 'modeling', file_extension)
            dependency_base_svn_directory = get_svn_base_directory(project, dependency_base_file_directory)
            dependencies_payload.append(dependency_base_svn_directory)
        payload = {
            'base_svn_directory':base_svn_directory,
            "task_type":task_type['name'].lower(),
            'person':person.serialize(),
            'permission': permission,
            'dependencies': dependencies_payload,
        }
        requests.put(url=f"{GENESIS_HOST}:{GENESIS_PORT}/task_acl/{project_name}", json=payload)
