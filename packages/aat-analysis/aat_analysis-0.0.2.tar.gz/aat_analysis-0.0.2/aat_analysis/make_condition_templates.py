# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/05_make_condition_templates.ipynb (unless otherwise specified).

__all__ = ['sorted_nicely', 'getProperty', 'makeConditionTable', 'make_condition_templates_from_files',
           'make_condition_templates', 'BASE_COLUMNS', 'AAT_COLUMNS']

# Cell
from .utils import loadJson
from .constants import Constants as C
import json
import os
import numpy as np
import pandas as pd
import re

BASE_COLUMNS = [C.PARTICIPANT_COLUMN, C.DEVICE_COLUMN, C.EXPERIMENT_COLUMN, C.CONDITION_COLUMN, C.SIGNED_UP_COLUMN, C.SESSION_COLUMN]
AAT_COLUMNS = [C.SENSOR_TYPE_COLUMN, C.BLOCK_COLUMN, C.TRIAL_NUMBER_COLUMN, C.TRIAL_NUMBER_CUM_COLUMN, C.IS_PRACTICE_COLUMN, C.STIMULUS_SET_COLUMN, C.STIMULUS_COLUMN, C.CORRECT_RESPONSE_COLUMN, C.TIME_COLUMN, C.ACCELERATION_COLUMN,C.ACCELERATION_X_COLUMN,C.ACCELERATION_Y_COLUMN, C.GYRO_TIME_COLUMN, C.GYRO_X_COLUMN,C.GYRO_Y_COLUMN,C.GYRO_Z_COLUMN,C.INTERPOLATED_COLUMN, C.INTERPOLATED_GYRO_COLUMN, C.DRAWN_AT_UNIX_COLUMN, C.DRAWN_AT_COLUMN]

def sorted_nicely(l):
    """Return list of sorted strings containing numbers (e.g. PI8, PI9, PI10, ...)"""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)

# Creates columns and lines based on condition
def getProperty(object, property, object_dict, default = np.nan):
    object = object_dict[object]
    if property in object.keys() and object[property]!=None:
        return object[property]
    elif "parent" in object.keys():
        return getProperty(object['parent'], property, object_dict, default=default)
    # Added functionality for "parents"
    elif "parents" in object.keys():
        for parent in object['parents']:
            parent_property = getProperty(parent, property, object_dict, default=default)
            if parent_property != default:
                return parent_property
    else:
        return default

def makeConditionTable(condition_name,conditions_file, sessions_file, tasks_file, stimulus_sets_file, blocks_file):
    columns = BASE_COLUMNS
    question_columns, numeric_question_columns, categorical_question_columns, block_numbers, trial_numbers, trial_numbers_cum, session_list, session_number_list, is_practice_list = [], [], [], [], [], [], [], [], []
    conditions = loadJson(conditions_file)
    condition = conditions[condition_name]
    sessions = loadJson(sessions_file)
    tasks = loadJson(tasks_file)
    stimulus_sets = loadJson(stimulus_sets_file)
    blocks = loadJson(blocks_file, default = None)
    for session_number, session in enumerate(condition['sessions']):
        has_aat = False
        task_names = getProperty(session, "tasks", sessions)
        for task in task_names:
            type = getProperty(task, "type", tasks)
            # For questionnaires and picture ratings add colums to the data table
            if type == 'questionnaire':
                questions = getProperty(task, "questions", tasks)
                for index, question in enumerate(questions):
                    if isinstance(question, str):
                        question = {"text":question}
                    if "type" in question.keys():
                        question_format = question['type']['format']
                    else:
                        question_format = getProperty(task, 'default_type', tasks)['format']
                    if question_format != "instruction":
                        if "id" in question.keys():
                            question_id = question['id']
                        else:
                            question_id = "%s_%02d"%(task,index+1)
                        question_columns.append(question_id)
                        question_columns.append(question_id+"_time")
                        categorical_question_columns.append(question_id+"_time")
                        if question_format in C.NUMERICAL_QUESTION_TYPES:
                            numeric_question_columns.append(question_id)
                        if question_format in C.CATEGORICAL_QUESTION_TYPES:
                            categorical_question_columns.append(question_id)
            # For AATs check how many trials there are in each block (based on stimulus sets and repetitions; TODO: This should also include repeat stimuli option)
            elif type == "aat":
                has_aat = True
                aat = tasks[task]
                if "blocks" in aat:
                    cum_trial = 1
                    for block_number, block_name in enumerate(aat["blocks"]):
                        block = blocks[block_name]
                        is_practice = False
                        if "give_feedback" in block:
                            is_practice = block["give_feedback"]
                        amount_of_trials = 0
                        for response in ["push","pull"]:
                            response_definition = block[response]
                            for chooser in response_definition["stimuli"]:
                                stim_set = chooser["from"]
                                repeat = 1
                                if "repeat" in chooser:
                                    repeat = chooser["repeat"]
                                amount_of_trials += chooser["pick"] * repeat
                        for trial_number in range(0, int(amount_of_trials)):
                            session_list.append(session)
                            session_number_list.append(session_number+1)
                            block_numbers.append(block_number+1)
                            trial_numbers.append(trial_number+1)
                            trial_numbers_cum.append(cum_trial)
                            is_practice_list.append(is_practice)
                            cum_trial += 1
                                #print(stim_set)

                else:
                    # Counting practice trials
                    practice_size = 0
                    for stim_set in getProperty(task, "practice_targets", tasks, default = []):
                        practice_size += len(stimulus_sets[stim_set])
                    for stim_set in getProperty(task, "practice_controls", tasks, default = []):
                        practice_size += len(stimulus_sets[stim_set])
                    stim_size = 0
                    # Counting experimental trials
                    for stim_set in getProperty(task, "targets", tasks, default = []):
                        stim_size += len(stimulus_sets[stim_set]) * getProperty(task, 'target_rep', tasks, default= 1)
                    for stim_set in getProperty(task, "controls", tasks, default = []):
                        stim_size += len(stimulus_sets[stim_set]) * getProperty(task, 'control_rep', tasks, default= 1)
                    amount_of_blocks = getProperty(task, "amount_of_blocks", tasks)
                    cum_trial = 1
                    for block_number in range(amount_of_blocks):
                        # If it's a practice block
                        if (block_number == 0 or block_number == amount_of_blocks/2):
                            amount_of_trials = practice_size/2
                            is_practice = True
                        else:
                            amount_of_trials = stim_size/(amount_of_blocks-2)
                            is_practice = False
                        for trial_number in range(0, int(amount_of_trials)):
                            session_list.append(session)
                            session_number_list.append(session_number+1)
                            block_numbers.append(block_number+1)
                            trial_numbers.append(trial_number+1)
                            trial_numbers_cum.append(cum_trial)
                            is_practice_list.append(is_practice)
                            cum_trial += 1
        if not has_aat:
            session_list.append(session)
            session_number_list.append(session_number+1)
            block_numbers.append(1)
            trial_numbers.append(1)
            trial_numbers_cum.append(1)
            is_practice_list.append(False)
    columns = columns + sorted_nicely(set(question_columns)) + AAT_COLUMNS
    numeric_question_columns = list(set(numeric_question_columns))
    categorical_question_columns = list(set(categorical_question_columns))

    df = pd.DataFrame(columns=columns, index = list(range(len(trial_numbers))))

    df[C.ACCELERATION_COLUMN] = df[C.ACCELERATION_COLUMN].apply(lambda x: [])
    df[C.ACCELERATION_X_COLUMN] = df[C.ACCELERATION_X_COLUMN].apply(lambda x: [])
    df[C.ACCELERATION_Y_COLUMN] = df[C.ACCELERATION_Y_COLUMN].apply(lambda x: [])
    df[C.GYRO_X_COLUMN] = df[C.GYRO_X_COLUMN].apply(lambda x: [])
    df[C.GYRO_Y_COLUMN] = df[C.GYRO_Y_COLUMN].apply(lambda x: [])
    df[C.GYRO_Z_COLUMN] = df[C.GYRO_Z_COLUMN].apply(lambda x: [])
    df[C.TIME_COLUMN] = df[C.TIME_COLUMN].apply(lambda x: [])
    df[C.GYRO_TIME_COLUMN] = df[C.GYRO_TIME_COLUMN].apply(lambda x: [])
    df[C.CONDITION_COLUMN] = condition_name
    df[C.SESSION_COLUMN] = session_list
    df[C.SESSION_NUMBER_COLUMN] = session_number_list
    df[C.BLOCK_COLUMN] = block_numbers
    df[C.IS_PRACTICE_COLUMN] = is_practice_list
    df[C.IS_PRACTICE_COLUMN] = df[C.IS_PRACTICE_COLUMN].astype(bool)
    df[C.TRIAL_NUMBER_COLUMN] = pd.Series(trial_numbers)
    df[C.TRIAL_NUMBER_CUM_COLUMN] = pd.Series(trial_numbers_cum)
    df[C.INTERPOLATED_COLUMN] = df[C.INTERPOLATED_COLUMN].astype('str')
    df[C.INTERPOLATED_GYRO_COLUMN] = df[C.INTERPOLATED_GYRO_COLUMN].astype('str')
    df[numeric_question_columns] = df[numeric_question_columns].astype(float)
    # Changing nan to None in String colums to facilitate conversion to pandas
    df[categorical_question_columns] = df[categorical_question_columns].where(pd.notnull(df[categorical_question_columns]),None)
    df = df.set_index([C.SESSION_COLUMN, C.BLOCK_COLUMN, C.TRIAL_NUMBER_COLUMN]).sort_index()
    return df


def make_condition_templates_from_files(conditions_file, sessions_file, tasks_file, stimulus_sets_file, blocks_file):

    # Getting condition
    condition_dict = {}
    conditions = loadJson(conditions_file)
    for condition in conditions.keys():
        condition_table = makeConditionTable(condition,conditions_file, sessions_file, tasks_file, stimulus_sets_file, blocks_file)
        condition_dict[condition] = condition_table
    return condition_dict

def make_condition_templates(external_folder):
    return make_condition_templates_from_files(os.path.join(external_folder, "conditions.json"),
                                      os.path.join(external_folder, "sessions.json"),
                                      os.path.join(external_folder, "tasks.json"),
                                      os.path.join(external_folder, "stimulus_sets.json"),
                                      os.path.join(external_folder, "blocks.json"));