from utils.globel_variables import variables

def record_undo(func):
    def wrapper(self, *args, **kwargs):
        if variables.current_df_name is not None:
            print('tsest')
            variables.undo_stack.append(variables.dataframes[variables.current_df_name].copy())
            variables.redo_stack.clear()
        return func(self, *args, **kwargs)
    return wrapper


