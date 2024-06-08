def record_undo(func):
    def wrapper(self, *args, **kwargs):
        if self.current_df_name is not None:
            self.undo_stack.append(self.dataframes[self.current_df_name].copy())
            self.redo_stack.clear()
        return func(self, *args, **kwargs)
    return wrapper
